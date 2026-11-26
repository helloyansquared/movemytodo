// Pure data helpers: turn Microsoft Graph To Do responses into one tidy model, and write it out
// as backup files (JSON, CSV, Markdown, printable HTML) and import files for other apps.
// No network and no DOM here, so it runs the same in the browser and in Node tests.
(function (root) {
"use strict";

// ── Dates ────────────────────────────────────────────────────────────────────
// Graph returns dateTimeTimeZone objects: {dateTime: "2026-11-27T00:00:00.0000000", timeZone: "UTC"}.
// We always ask for UTC. To Do keeps due dates as a calendar day; depending on the client that set it,
// it comes back as midnight UTC or as the user's local midnight expressed in UTC.
const pad = n => String(n).padStart(2, "0");
function utcDate(dt) {
  if (!dt || !dt.dateTime) return null;
  const s = dt.dateTime.replace(/(\.\d{3})\d*$/, "$1");
  const tz = (dt.timeZone || "UTC").toUpperCase();
  return new Date(tz === "UTC" || tz === "Z" ? s + (/[zZ]|[+-]\d\d:?\d\d$/.test(s) ? "" : "Z") : s);
}
function localDay(d) { return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; }
// A due *day* (YYYY-MM-DD).
function dueDay(dt) {
  if (!dt || !dt.dateTime) return null;
  const m = /^(\d{4}-\d\d-\d\d)T(\d\d):(\d\d)/.exec(dt.dateTime);
  if (!m) return null;
  if (m[2] === "00" && m[3] === "00") return m[1];          // stored as plain midnight: that is the day
  const d = utcDate(dt);                                       // local midnight stored in UTC: convert back
  return d && !isNaN(d) ? localDay(d) : m[1];
}
// A moment (ISO string with offset of the viewer's time zone), for reminders and completion times.
function moment(dt) {
  const d = utcDate(dt);
  if (!d || isNaN(d)) return null;
  const off = -d.getTimezoneOffset(), sign = off >= 0 ? "+" : "-", a = Math.abs(off);
  return `${localDay(d)}T${pad(d.getHours())}:${pad(d.getMinutes())}:00${sign}${pad(Math.floor(a / 60))}:${pad(a % 60)}`;
}
function isoOrNull(s) { return typeof s === "string" && s ? s.replace(/(\.\d{3})\d*Z$/, "$1Z") : null; }

// ── Text ─────────────────────────────────────────────────────────────────────
function htmlToText(h) {
  if (!h) return "";
  return String(h)
    .replace(/<\s*br\s*\/?>/gi, "\n").replace(/<\/(p|div|li|h\d|tr)>/gi, "\n").replace(/<li[^>]*>/gi, "• ")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&")
    .replace(/\r\n?/g, "\n").replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
}
function bodyText(body) {
  if (!body || !body.content) return "";
  return (body.contentType || "").toLowerCase() === "html" ? htmlToText(body.content) : String(body.content).replace(/\r\n?/g, "\n").trim();
}
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// ── Recurrence ───────────────────────────────────────────────────────────────
const DAY = { sunday: "SU", monday: "MO", tuesday: "TU", wednesday: "WE", thursday: "TH", friday: "FR", saturday: "SA" };
const DAYNAME = { sunday: "Sun", monday: "Mon", tuesday: "Tue", wednesday: "Wed", thursday: "Thu", friday: "Fri", saturday: "Sat" };
const IDX = { first: 1, second: 2, third: 3, fourth: 4, last: -1 };
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
function recurrence(r) {
  if (!r || !r.pattern || !r.pattern.type) return null;
  const p = r.pattern, n = Math.max(1, p.interval || 1), days = (p.daysOfWeek || []).map(d => String(d).toLowerCase());
  let rule, text, freq;
  switch (p.type) {
    case "daily": freq = "daily"; rule = "FREQ=DAILY"; text = n === 1 ? "Every day" : `Every ${n} days`; break;
    case "weekly":
      freq = "weekly"; rule = "FREQ=WEEKLY" + (days.length ? ";BYDAY=" + days.map(d => DAY[d]).join(",") : "");
      text = (n === 1 ? "Every week" : `Every ${n} weeks`) + (days.length ? " on " + days.map(d => DAYNAME[d]).join(", ") : "");
      if (days.length === 5 && !days.includes("saturday") && !days.includes("sunday") && n === 1) text = "Every weekday";
      break;
    case "absoluteMonthly": freq = "monthly"; rule = "FREQ=MONTHLY" + (p.dayOfMonth ? ";BYMONTHDAY=" + p.dayOfMonth : ""); text = (n === 1 ? "Every month" : `Every ${n} months`) + (p.dayOfMonth ? ` on day ${p.dayOfMonth}` : ""); break;
    case "relativeMonthly": freq = "monthly"; rule = "FREQ=MONTHLY" + (days.length ? ";BYDAY=" + days.map(d => (IDX[p.index] || 1) + DAY[d]).join(",") : ""); text = (n === 1 ? "Every month" : `Every ${n} months`) + (days.length ? ` on the ${p.index || "first"} ${days.map(d => DAYNAME[d]).join("/")}` : ""); break;
    case "absoluteYearly": freq = "yearly"; rule = "FREQ=YEARLY" + (p.month ? ";BYMONTH=" + p.month : "") + (p.dayOfMonth ? ";BYMONTHDAY=" + p.dayOfMonth : ""); text = (n === 1 ? "Every year" : `Every ${n} years`) + (p.month ? ` on ${MONTHS[p.month - 1]} ${p.dayOfMonth || ""}`.trimEnd() : ""); break;
    case "relativeYearly": freq = "yearly"; rule = "FREQ=YEARLY" + (p.month ? ";BYMONTH=" + p.month : "") + (days.length ? ";BYDAY=" + days.map(d => (IDX[p.index] || 1) + DAY[d]).join(",") : ""); text = (n === 1 ? "Every year" : `Every ${n} years`); break;
    default: return { freq: null, interval: n, rrule: null, text: "Repeats (" + p.type + ")", raw: r };
  }
  if (n > 1) rule += ";INTERVAL=" + n;
  const rg = r.range || {};
  if (rg.type === "endDate" && rg.endDate) { rule += ";UNTIL=" + rg.endDate.replace(/-/g, "") + "T235959Z"; text += ` until ${rg.endDate}`; }
  if (rg.type === "numbered" && rg.numberOfOccurrences) { rule += ";COUNT=" + rg.numberOfOccurrences; text += `, ${rg.numberOfOccurrences} times`; }
  return { freq, interval: n, days: days.map(d => DAY[d]), rrule: rule, text, raw: r };
}

// ── Normalise ────────────────────────────────────────────────────────────────
const WELLKNOWN = { defaultList: "Tasks", flaggedEmails: "Flagged email" };
function normTask(t) {
  const steps = (t.checklistItems || []).map(c => ({ title: (c.displayName || "").trim(), done: !!c.isChecked, created: isoOrNull(c.createdDateTime), checked: isoOrNull(c.checkedDateTime) }));
  return {
    id: t.id,
    title: (t.title || "").trim() || "(untitled)",
    notes: bodyText(t.body),
    status: t.status || "notStarted",
    completed: t.status === "completed",
    completedAt: moment(t.completedDateTime),
    created: isoOrNull(t.createdDateTime),
    modified: isoOrNull(t.lastModifiedDateTime),
    due: dueDay(t.dueDateTime),
    start: dueDay(t.startDateTime),
    reminder: t.isReminderOn ? moment(t.reminderDateTime) : null,
    importance: t.importance || "normal",
    important: t.importance === "high",
    recurrence: recurrence(t.recurrence),
    categories: Array.isArray(t.categories) ? t.categories.slice() : [],
    steps,
    links: (t.linkedResources || []).filter(l => l && (l.webUrl || l.displayName)).map(l => ({ url: l.webUrl || "", name: l.displayName || "", app: l.applicationName || "" })),
    hasAttachments: !!t.hasAttachments,
    attachments: (t.attachments || []).map(a => ({ name: a.name || "", size: a.size || 0, type: a.contentType || "" })),
  };
}
function normList(l, tasks) {
  const name = (l.displayName || "").trim() || WELLKNOWN[l.wellknownListName] || "Untitled list";
  return { id: l.id, name, wellknown: l.wellknownListName && l.wellknownListName !== "none" ? l.wellknownListName : null, shared: !!l.isShared, owner: l.isOwner !== false, tasks: (tasks || []).map(normTask) };
}
function sortTasks(tasks) {
  // Open tasks first (oldest first, like To Do's default), then completed tasks, newest completion first.
  return tasks.slice().sort((a, b) => (a.completed - b.completed) || (a.completed ? String(b.completedAt || "").localeCompare(String(a.completedAt || "")) : String(a.created || "").localeCompare(String(b.created || ""))));
}
function buildModel(lists, account) {
  const out = { app: "Microsoft To Do", exportedAt: new Date().toISOString(), account: account || null, lists: lists.map(x => { const l = normList(x.list, x.tasks); l.tasks = sortTasks(l.tasks); return l; }) };
  out.stats = stats(out);
  return out;
}
function stats(m) {
  let tasks = 0, open = 0, done = 0, steps = 0, notes = 0, due = 0, recurring = 0, reminders = 0, attachments = 0;
  for (const l of m.lists) for (const t of l.tasks) {
    tasks++; t.completed ? done++ : open++; steps += t.steps.length; if (t.notes) notes++; if (t.due) due++; if (t.recurrence) recurring++; if (t.reminder) reminders++; if (t.hasAttachments) attachments++;
  }
  return { lists: m.lists.length, tasks, open, done, steps, notes, due, recurring, reminders, attachments };
}
function filterModel(m, opt) {
  // opt: {lists: Set of list ids (or null = all), completed: bool}
  const lists = m.lists.filter(l => !opt.lists || opt.lists.has(l.id)).map(l => ({ ...l, tasks: l.tasks.filter(t => opt.completed || !t.completed) }));
  const r = { ...m, lists };
  r.stats = stats(r);
  return r;
}

// ── Free backups ─────────────────────────────────────────────────────────────
function toJSON(m) {
  return JSON.stringify({ ...m, format: "todomove-backup-1", note: "Exported from Microsoft To Do. Dates: due/start are calendar days; reminder and completedAt are local times with offsets." }, null, 2);
}
const csvCell = v => { const s = v == null ? "" : String(v); return /[",\n\r]/.test(s) || /^[=+\-@]/.test(s) ? '"' + (/^[=+\-@]/.test(s) ? "'" : "") + s.replace(/"/g, '""') + '"' : s; };
function toCSV(m) {
  const head = ["List", "Title", "Status", "Due date", "Reminder", "Repeats", "Important", "My Day / start", "Steps", "Steps done", "Notes", "Categories", "Links", "Has attachments", "Created", "Completed"];
  const rows = [head];
  for (const l of m.lists) for (const t of l.tasks) rows.push([
    l.name, t.title, t.completed ? "Completed" : "Open", t.due || "", t.reminder || "", t.recurrence ? t.recurrence.text : "", t.important ? "Yes" : "",
    t.start || "", t.steps.map(s => (s.done ? "[x] " : "[ ] ") + s.title).join("\n"), t.steps.filter(s => s.done).length + "/" + t.steps.length,
    t.notes, t.categories.join(", "), t.links.map(x => x.url || x.name).join("\n"), t.hasAttachments ? "Yes" : "", t.created || "", t.completedAt || ""]);
  return "﻿" + rows.map(r => r.map(csvCell).join(",")).join("\r\n") + "\r\n";
}
function mdEsc(s) { return String(s).replace(/([\\`*_[\]<>#|])/g, "\\$1"); }
function toMarkdown(m) {
  const out = [`# Microsoft To Do backup`, ``, `Exported ${m.exportedAt.slice(0, 10)} · ${m.stats.lists} lists · ${m.stats.tasks} tasks (${m.stats.open} open, ${m.stats.done} completed)`, ``];
  for (const l of m.lists) {
    out.push(`## ${mdEsc(l.name)}`, ``);
    if (!l.tasks.length) out.push(`_No tasks_`, ``);
    for (const t of l.tasks) {
      const meta = [t.due && `due ${t.due}`, t.reminder && `reminder ${t.reminder.slice(0, 16).replace("T", " ")}`, t.recurrence && t.recurrence.text.toLowerCase(), t.important && "important", t.categories.length && t.categories.join(", ")].filter(Boolean);
      out.push(`- [${t.completed ? "x" : " "}] ${mdEsc(t.title)}${meta.length ? ` — ${meta.join(" · ")}` : ""}`);
      for (const s of t.steps) out.push(`    - [${s.done ? "x" : " "}] ${mdEsc(s.title)}`);
      if (t.notes) out.push(...t.notes.split("\n").map(x => "    > " + x));
      for (const k of t.links) out.push(`    - 🔗 ${k.url ? `<${k.url}>` : mdEsc(k.name)}`);
    }
    out.push(``);
  }
  return out.join("\n");
}
function toHTML(m, title) {
  const sec = m.lists.map(l => `<section><h2>${esc(l.name)} <small>${l.tasks.length} task${l.tasks.length === 1 ? "" : "s"}</small></h2><ul>` + l.tasks.map(t => {
    const meta = [t.due && `Due ${esc(t.due)}`, t.reminder && `Reminder ${esc(t.reminder.slice(0, 16).replace("T", " "))}`, t.recurrence && esc(t.recurrence.text), t.important && "★ Important", t.categories.length && esc(t.categories.join(", ")), t.completed && t.completedAt && `Done ${esc(t.completedAt.slice(0, 10))}`].filter(Boolean).join(" · ");
    return `<li class="${t.completed ? "done" : ""}"><span class="box">${t.completed ? "☑" : "☐"}</span><div><b>${esc(t.title)}</b>${meta ? `<div class="m">${meta}</div>` : ""}${t.steps.length ? "<ul class=\"st\">" + t.steps.map(s => `<li class="${s.done ? "done" : ""}">${s.done ? "☑" : "☐"} ${esc(s.title)}</li>`).join("") + "</ul>" : ""}${t.notes ? `<p class="n">${esc(t.notes).replace(/\n/g, "<br>")}</p>` : ""}${t.links.map(k => `<div class="m">🔗 ${k.url ? `<a href="${esc(k.url)}">${esc(k.name || k.url)}</a>` : esc(k.name)}</div>`).join("")}</div></li>`;
  }).join("") + `</ul></section>`).join("");
  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title || "Microsoft To Do backup")}</title>
<style>body{font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;max-width:820px;margin:32px auto;padding:0 18px;color:#1d2433}h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:28px 0 8px;border-bottom:2px solid #e3e7ef;padding-bottom:4px}h2 small{color:#7a8396;font-weight:400;font-size:13px}ul{list-style:none;padding:0;margin:0}li{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #eef1f6;break-inside:avoid}.box{font-size:17px;line-height:1.3}.m{color:#66708a;font-size:13px}.n{white-space:normal;margin:4px 0 0;color:#3b4459;font-size:14px}.st li{border:0;padding:1px 0;font-size:14px}li.done>div>b,.st li.done{color:#8b93a6;text-decoration:line-through}.top{color:#66708a;font-size:13px;margin-bottom:18px}@media print{body{margin:0}a{color:inherit}}</style></head>
<body><h1>${esc(title || "Microsoft To Do backup")}</h1><div class="top">Exported ${esc(m.exportedAt.slice(0, 10))} · ${m.stats.lists} lists · ${m.stats.tasks} tasks (${m.stats.open} open, ${m.stats.done} completed)</div>${sec}</body></html>`;
}

// ── Import files for other apps ──────────────────────────────────────────────
// Things 3: things:///json?data=[...] — one project per list. Things caps an import at 250 items per 10 seconds,
// so callers split big lists with thingsChunks().
function thingsItems(l) {
  return l.tasks.map(t => {
    const a = { title: t.title.slice(0, 4000) };
    const notes = [t.notes, t.recurrence && `Repeats: ${t.recurrence.text} (set this again in Things)`, ...t.links.map(k => k.url || k.name)].filter(Boolean).join("\n\n");
    if (notes) a.notes = notes.slice(0, 9500);
    if (t.due) a.deadline = t.due;
    if (t.reminder && !t.completed) a.when = t.reminder.slice(0, 16).replace("T", "@").replace(/@(\d\d):(\d\d)$/, "@$1:$2");
    if (t.steps.length) a["checklist-items"] = t.steps.slice(0, 100).map(s => ({ type: "checklist-item", attributes: { title: s.title.slice(0, 1000), completed: s.done } }));
    const tags = [...t.categories, t.important ? "Important" : null].filter(Boolean);
    if (tags.length) a.tags = tags;
    if (t.completed) a.completed = true;
    return { type: "to-do", attributes: a };
  });
}
function thingsChunks(l, size) {
  size = size || 40;
  const items = thingsItems(l), out = [];
  for (let i = 0; i < Math.max(items.length, 1); i += size) {
    const part = items.slice(i, i + size);
    const proj = { type: "project", attributes: { title: l.name + (items.length > size ? ` (${i / size + 1})` : ""), items: part } };
    out.push("things:///json?data=" + encodeURIComponent(JSON.stringify([proj])) + "&reveal=" + (i === 0 ? "true" : "false"));
  }
  return out;
}

// Todoist: its CSV import template, one file per project (Todoist imports up to 300 tasks per file).
// PRIORITY 1 is Todoist's p1 (urgent), 4 is p4 (normal). INDENT 2 makes a sub-task of the task above.
function todoistCSV(l) {
  const head = ["TYPE", "CONTENT", "DESCRIPTION", "PRIORITY", "INDENT", "AUTHOR", "RESPONSIBLE", "DATE", "DATE_LANG", "TIMEZONE", "DURATION", "DURATION_UNIT", "DEADLINE", "DEADLINE_LANG"];
  const rows = [head];
  const clean = s => String(s).replace(/\r?\n/g, " ").replace(/^[*!#]+/, "").trim();
  for (const t of l.tasks.filter(x => !x.completed)) {
    const desc = [t.notes, t.recurrence && `Repeats: ${t.recurrence.text}`, t.reminder && `Reminder: ${t.reminder.slice(0, 16).replace("T", " ")}`, ...t.links.map(k => k.url || k.name)].filter(Boolean).join("\n");
    rows.push(["task", clean(t.title), desc, t.important ? 1 : 4, 1, "", "", t.due || "", t.due ? "en" : "", "", "", "", "", ""]);
    for (const s of t.steps.filter(x => !x.done)) rows.push(["task", clean(s.title) || "(step)", "", 4, 2, "", "", "", "", "", "", "", "", ""]);
  }
  return rows.map(r => r.map(v => { const s = v == null ? "" : String(v); return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }).join(",")).join("\r\n") + "\r\n";
}

// Apple Reminders on a Mac: a JavaScript for Automation script run with `osascript -l JavaScript`.
// It creates one Reminders list per To Do list (adding " (To Do)" if the name is taken) and adds the
// reminders with notes, due dates, priority and flags. Steps become the reminder's notes as a checklist,
// because the Reminders scripting interface has no subtasks.
function remindersScript(m) {
  const data = m.lists.map(l => ({
    name: l.name,
    items: l.tasks.map(t => {
      const lines = [];
      if (t.notes) lines.push(t.notes);
      if (t.steps.length) lines.push((t.notes ? "\n" : "") + "Steps:\n" + t.steps.map(s => (s.done ? "✓ " : "◻︎ ") + s.title).join("\n"));
      if (t.recurrence) lines.push(`\nRepeats: ${t.recurrence.text} (set this again in Reminders)`);
      for (const k of t.links) lines.push(k.url || k.name);
      return { t: t.title, n: lines.join("\n").trim(), d: t.due || null, r: t.reminder || null, p: t.important ? 1 : 0, c: t.completed, f: t.important };
    }),
  }));
  return `// Microsoft To Do → Apple Reminders import script, made by ${"__SITE_NAME__"}.
// Run it in Terminal with:  osascript -l JavaScript ~/Downloads/import-to-reminders.js
// It only ADDS lists and reminders. It never changes or deletes anything you already have.
ObjC.import("stdlib");
const DATA = ${JSON.stringify(data)};
const app = Application("Reminders");
app.includeStandardAdditions = true;
const existing = app.lists.name();
let made = 0, lists = 0;
function day(s) { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d, 9, 0, 0); }
for (const L of DATA) {
  let name = L.name;
  if (existing.indexOf(name) !== -1) name = name + " (To Do)";
  let n = 2; while (existing.indexOf(name) !== -1) name = L.name + " (To Do " + (n++) + ")";
  const list = app.List({ name: name });
  app.lists.push(list);
  existing.push(name);
  lists++;
  const target = app.lists.byName(name);
  for (const it of L.items) {
    const props = { name: it.t };
    if (it.n) props.body = it.n;
    if (it.p) props.priority = it.p;
    if (it.f) props.flagged = true;
    if (it.r && !it.c) { props.remindMeDate = new Date(it.r); }
    if (it.d) { props.alldayDueDate = day(it.d); }
    if (it.c) props.completed = true;
    try { target.reminders.push(app.Reminder(props)); }
    catch (e) { delete props.flagged; delete props.alldayDueDate; if (it.d) props.dueDate = day(it.d); target.reminders.push(app.Reminder(props)); }
    made++;
  }
}
"Done: added " + made + " reminders in " + lists + " new lists.";
`;
}

// Google Tasks: the plan the browser executes against the Tasks API.
// Google Tasks has a single level of subtasks, plain-text notes (max 8192 chars) and due *dates* only.
function googlePlan(m) {
  return m.lists.map(l => ({
    title: l.name.slice(0, 1024),
    tasks: l.tasks.map(t => {
      const extra = [t.reminder && !t.completed ? `Reminder: ${t.reminder.slice(0, 16).replace("T", " ")}` : null,
                     t.recurrence ? `Repeats: ${t.recurrence.text} (set this again in Google Tasks)` : null,
                     t.important ? "★ Important" : null, t.categories.length ? "Categories: " + t.categories.join(", ") : null,
                     ...t.links.map(k => k.url || k.name)].filter(Boolean);
      const notes = [t.notes, extra.join("\n")].filter(Boolean).join("\n\n").slice(0, 8000);
      const body = { title: t.title.slice(0, 1024), status: t.completed ? "completed" : "needsAction" };
      if (notes) body.notes = notes;
      if (t.due) body.due = t.due + "T00:00:00.000Z";
      if (t.completed && t.completedAt) body.completed = new Date(t.completedAt).toISOString();
      return { body, steps: t.steps.map(s => ({ title: s.title.slice(0, 1024) || "(step)", status: s.done ? "completed" : "needsAction" })) };
    }),
  }));
}

const CORE = { utcDate, dueDay, moment, htmlToText, bodyText, recurrence, normTask, normList, buildModel, filterModel, stats,
               toJSON, toCSV, toMarkdown, toHTML, todoistCSV, thingsItems, thingsChunks, remindersScript, googlePlan, esc };
if (typeof module !== "undefined" && module.exports) module.exports = CORE; else root.CORE = CORE;
})(typeof window !== "undefined" ? window : globalThis);
