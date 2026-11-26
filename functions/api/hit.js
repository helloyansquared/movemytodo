// /api/hit: receives anonymous counts from /found.js (which site sent a visit; the optional
// "how did you find us?" answer). No IPs, cookies or IDs are stored. Rows go to the D1 database
// bound as DB (table hits, kept 180 days) and to the Analytics Engine dataset bound as HITS.
const TYPES = new Set(["land", "ask", "askq"]);
const ANSWERS = new Set(["ChatGPT", "Google", "Another AI", "Reddit", "Tumblr", "A friend", "Other", "dismissed", ""]);
const KEEP_DAYS = 180;

const clean = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, n);
// Free text is anonymous by design: strip anything that looks like an email address or a long number.
const scrub = (s) => s.replace(/[^\s@]+@[^\s@]+\.[^\s@]+/g, "[email]").replace(/\d[\d\s().-]{6,}\d/g, "[number]");

export async function onRequestPost({ request, env, waitUntil }) {
  const none = new Response(null, { status: 204 });
  const url = new URL(request.url);
  const site = url.hostname.replace(/^www\./, "");
  const origin = request.headers.get("origin");
  if (origin) { try { if (new URL(origin).hostname !== url.hostname) return none; } catch { return none; } }
  if (Number(request.headers.get("content-length") || 0) > 2000) return new Response(null, { status: 413 });

  let d;
  try { d = JSON.parse(await request.text()); } catch { return none; }
  if (!d || !TYPES.has(d.t)) return none;
  const src = clean(d.src, 60).toLowerCase();
  if (src && !/^[a-z0-9.:_-]{1,60}$/.test(src)) return none;
  const path = clean(d.path, 80);
  if (path && !path.startsWith("/")) return none;
  const ans = clean(d.ans, 20);
  if (!ANSWERS.has(ans)) return none;
  const q = d.t === "askq" ? scrub(clean(d.q, 200)) : "";
  if (d.t === "askq" && !q) return none;
  const country = clean(request.cf && request.cf.country, 2);

  try { if (env.HITS) env.HITS.writeDataPoint({ indexes: [site], blobs: [d.t, site, src, path, ans, q, country], doubles: [1] }); }
  catch (e) { console.log("ae error", String(e)); }

  if (env.DB) {
    const work = (async () => {
      try {
        await env.DB.prepare("INSERT INTO hits (t, site, src, path, ans, q, country) VALUES (?, ?, ?, ?, ?, ?, ?)")
          .bind(d.t, site, src, path, ans, q, country).run();
        if (Math.random() < 0.01) await env.DB.prepare("DELETE FROM hits WHERE ts < unixepoch() - ?").bind(KEEP_DAYS * 86400).run();
      } catch (e) { console.log("d1 error", String(e)); }
    })();
    try { waitUntil(work); } catch { await work; }
  } else {
    console.log("hit", d.t, site, src, path, ans);
  }
  return none;
}

export const onRequestGet = () => new Response("POST only", { status: 405 });
