// Cloudflare Pages Function: POST /api/license
// Activates or validates a MoveMyTodo Pro license key with Dodo Payments' public licence endpoints
// (no API key involved). Only keys issued for our product are accepted, and the customer's
// details in Dodo's answer are not passed on to the browser.
const PRODUCT_ID = "__PRODUCT_ID__";
const DODO = "https://live.dodopayments.com/licenses/";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export async function onRequestPost({ request }) {
  let input;
  try { input = await request.json(); } catch { return json({ ok: false, error: "bad_request" }, 400); }
  const action = input && input.action;
  const key = typeof input.license_key === "string" ? input.license_key.trim() : "";
  if (!["activate", "validate"].includes(action) || !key || key.length > 200) return json({ ok: false, error: "bad_request" }, 400);

  const body = action === "activate"
    ? { license_key: key, name: String(input.name || "browser").slice(0, 60) }
    : { license_key: key, ...(typeof input.instance_id === "string" && input.instance_id ? { license_key_instance_id: input.instance_id } : {}) };

  let r, data = {};
  try {
    r = await fetch(DODO + action, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
    data = await r.json().catch(() => ({}));
  } catch { return json({ ok: false, error: "unreachable" }, 502); }

  if (action === "activate") {
    if (r.status === 404) return json({ ok: false, error: "not_found" }, 404);
    if (r.status === 403) return json({ ok: false, error: "inactive" }, 403);
    if (r.status === 422) return json({ ok: false, error: "limit" }, 422);
    if (!r.ok) return json({ ok: false, error: "failed" }, 502);
    const product = data.product && data.product.product_id;
    if (product !== PRODUCT_ID) return json({ ok: false, error: "wrong_product" }, 403);
    return json({ ok: true, id: data.id });
  }
  // validate
  if (r.status === 404) return json({ ok: false, error: "not_found" }, 404);
  if (!r.ok) return json({ ok: false, error: "failed" }, 502);
  return json({ ok: data.valid === true });
}

export async function onRequest() {
  return json({ ok: false, error: "method_not_allowed" }, 405);
}
