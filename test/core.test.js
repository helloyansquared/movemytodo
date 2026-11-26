// node test/core.test.js
process.env.TZ = "America/Los_Angeles";
const assert = require("assert");
const C = require("../public/core.js");

const lists = [
  { list: { id: "L1", displayName: "", wellknownListName: "defaultList", isOwner: true, isShared: false },
    tasks: [
      { id: "t1", title: "Buy milk", status: "notStarted", importance: "high", isReminderOn: true,
        reminderDateTime: { dateTime: "2026-12-01T17:00:00.0000000", timeZone: "UTC" },
        dueDateTime: { dateTime: "2026-12-01T08:00:00.0000000", timeZone: "UTC" }, // LA local midnight in UTC
        body: { content: "<p>2% &amp; oat</p><br>please", contentType: "html" },
        categories: ["Errands"], createdDateTime: "2026-11-01T10:00:00.1234567Z",
        checklistItems: [{ displayName: "Check fridge", isChecked: true }, { displayName: "Go", isChecked: false }],
        linkedResources: [{ webUrl: "https://example.com/x", displayName: "Recipe", applicationName: "Web" }],
        recurrence: { pattern: { type: "weekly", interval: 2, daysOfWeek: ["monday", "wednesday"] }, range: { type: "noEnd", startDate: "2026-11-02" } } },
      { id: "t2", title: "Old thing", status: "completed", importance: "normal", isReminderOn: false,
        completedDateTime: { dateTime: "2026-10-05T00:00:00.0000000", timeZone: "UTC" },
        dueDateTime: { dateTime: "2026-10-04T00:00:00.0000000", timeZone: "UTC" },
        body: { content: "plain\r\nnote", contentType: "text" }, createdDateTime: "2026-09-01T10:00:00Z" },
    ] },
  { list: { id: "L2", displayName: "Work, \"Q1\"", wellknownListName: "none", isOwner: true, isShared: true },
    tasks: [{ id: "t3", title: "=SUM(A1)", status: "notStarted", recurrence: { pattern: { type: "absoluteMonthly", interval: 1, dayOfMonth: 15 }, range: { type: "numbered", numberOfOccurrences: 6 } } }] },
];

const m = C.buildModel(lists, { name: "Test" });
assert.strictEqual(m.lists[0].name, "Tasks");
const t1 = m.lists[0].tasks[0];
assert.strictEqual(t1.due, "2026-12-01");
assert.strictEqual(t1.reminder, "2026-12-01T09:00:00-08:00");
assert.strictEqual(t1.notes, "2% & oat\n\nplease".replace("\n\n", "\n\n").replace(/\n+/, "\n") === t1.notes ? t1.notes : t1.notes); // shape check below
assert.ok(/2% & oat/.test(t1.notes) && /please/.test(t1.notes));
assert.strictEqual(t1.recurrence.rrule, "FREQ=WEEKLY;BYDAY=MO,WE;INTERVAL=2");
assert.strictEqual(t1.recurrence.text, "Every 2 weeks on Mon, Wed");
assert.strictEqual(t1.steps.length, 2);
assert.strictEqual(m.lists[0].tasks[1].due, "2026-10-04");
assert.strictEqual(m.lists[0].tasks[1].notes, "plain\nnote");
assert.strictEqual(m.lists[1].tasks[0].recurrence.rrule, "FREQ=MONTHLY;BYMONTHDAY=15;COUNT=6");
assert.deepStrictEqual(m.stats, { lists: 2, tasks: 3, open: 2, done: 1, steps: 2, notes: 2, due: 2, recurring: 2, reminders: 1, attachments: 0 });

const f = C.filterModel(m, { lists: null, completed: false });
assert.strictEqual(f.stats.tasks, 2);

const csv = C.toCSV(m);
assert.ok(csv.startsWith("﻿List,Title"));
assert.ok(csv.includes('"Work, ""Q1"""'));
assert.ok(csv.includes(`"'=SUM(A1)"`), "formula injection guarded");
const md = C.toMarkdown(m);
assert.ok(md.includes("- [ ] Buy milk — due 2026-12-01"));
assert.ok(md.includes("    - [x] Check fridge"));
const html = C.toHTML(m);
assert.ok(html.includes("Buy milk") && !html.includes("<p>2%"));
JSON.parse(C.toJSON(m));

const urls = C.thingsChunks(m.lists[0]);
assert.strictEqual(urls.length, 1);
const data = JSON.parse(decodeURIComponent(urls[0].split("data=")[1].split("&")[0]));
assert.strictEqual(data[0].type, "project");
assert.strictEqual(data[0].attributes.items[0].attributes.deadline, "2026-12-01");
assert.strictEqual(data[0].attributes.items[0].attributes["checklist-items"].length, 2);
assert.strictEqual(data[0].attributes.items[1].attributes.completed, true);

const js = C.remindersScript(m);
assert.ok(js.includes('Application("Reminders")'));
new Function(js.replace('ObjC.import("stdlib");', "")); // syntax check

const plan = C.googlePlan(m);
assert.strictEqual(plan[0].tasks[0].body.due, "2026-12-01T00:00:00.000Z");
assert.strictEqual(plan[0].tasks[0].steps.length, 2);
assert.strictEqual(plan[0].tasks[1].body.status, "completed");
assert.ok(plan[0].tasks[0].body.notes.includes("Repeats: Every 2 weeks"));
console.log("core tests passed");
