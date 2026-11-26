// /api/hit: receives anonymous counts from /found.js (where a visit came from; the optional
// "how did you find us?" answer). No IPs, cookies or IDs are stored. Data goes to a Workers
// Analytics Engine dataset bound as HITS (Pages project → Settings → Bindings). Without the
// binding, hits are only printed to the Function's real-time log.
const clip = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u001f]/g, " ").slice(0, n);
const TYPES = new Set(["land", "ask", "askq"]);

export async function onRequestPost({ request, env }) {
  if (Number(request.headers.get("content-length") || 0) > 2000) return new Response(null, { status: 413 });
  let d;
  try { d = JSON.parse(await request.text()); } catch { return new Response(null, { status: 204 }); }
  if (!d || !TYPES.has(d.t)) return new Response(null, { status: 204 });
  const row = [clip(d.t, 8), clip(d.site, 60), clip(d.src, 60), clip(d.path, 80), clip(d.ans, 20), clip(d.q, 200),
               clip(request.cf && request.cf.country, 2)];
  try {
    if (env.HITS) env.HITS.writeDataPoint({ indexes: [row[1]], blobs: row, doubles: [1] });
    else console.log("hit", JSON.stringify(row));
  } catch (e) { console.log("hit error", String(e)); }
  return new Response(null, { status: 204 });
}

export const onRequestGet = () => new Response("POST only", { status: 405 });
