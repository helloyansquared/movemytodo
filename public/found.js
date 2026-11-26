/* found.js: privacy-friendly "where do visitors come from" counter. No cookies, no IDs, no third parties.
   - Found.land(): once per tab session, sends {t:"land", src, path} to /api/hit, where src is the site that
     sent the visit (chatgpt, perplexity, google, reddit, a hostname, or "direct"). Raw URLs are never sent.
   - Found.ask(): after something worked, shows a skippable one-question card ("How did you find us?"),
     at most once per browser. The answer and the optional "what did you search or ask?" go to /api/hit too. */
(function () {
  var SITE = location.hostname.replace(/^www\./, "");
  var AI = [["chatgpt", /(^|\.)(chatgpt\.com|chat\.openai\.com|openai\.com)$/], ["perplexity", /(^|\.)perplexity\.ai$/],
    ["claude", /(^|\.)claude\.ai$/], ["gemini", /^gemini\.google\.com$/], ["copilot", /(^|\.)copilot\.(microsoft|cloud\.microsoft)\.com$|^copilot\.microsoft\.com$/],
    ["meta-ai", /(^|\.)meta\.ai$/], ["deepseek", /(^|\.)deepseek\.com$/], ["grok", /(^|\.)grok\.com$/], ["you", /(^|\.)you\.com$/],
    ["google", /(^|\.)google\.[a-z.]+$/], ["bing", /(^|\.)bing\.com$/], ["duckduckgo", /(^|\.)duckduckgo\.com$/],
    ["reddit", /(^|\.)reddit\.com$/], ["tumblr", /(^|\.)tumblr\.com$/], ["x", /(^|\.)(x\.com|t\.co|twitter\.com)$/]];
  function ss(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }
  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function send(d) {
    d.site = SITE; var body = JSON.stringify(d);
    try { if (navigator.sendBeacon && navigator.sendBeacon("/api/hit", new Blob([body], { type: "application/json" }))) return; } catch (e) {}
    try { fetch("/api/hit", { method: "POST", body: body, headers: { "content-type": "application/json" }, keepalive: true }); } catch (e) {}
  }
  function source() {
    var u = new URLSearchParams(location.search).get("utm_source");
    if (u) { u = u.toLowerCase().slice(0, 60); for (var i = 0; i < AI.length; i++) if (AI[i][1].test(u)) return AI[i][0]; return "utm:" + u; }
    var h = ""; try { h = document.referrer ? new URL(document.referrer).hostname.replace(/^www\./, "") : ""; } catch (e) {}
    if (!h) return "direct";
    if (h === SITE || h.endsWith("." + SITE)) return null; // moving between our own pages
    for (var j = 0; j < AI.length; j++) if (AI[j][1].test(h)) return AI[j][0];
    return h.slice(0, 60);
  }
  function land() {
    if (ss("found-landed")) return;
    var s = source(); if (s === null) return;
    ss("found-landed", "1"); ss("found-src", s);
    send({ t: "land", src: s, path: location.pathname.slice(0, 80) });
  }
  var shown = false;
  function ask() {
    if (shown || ls("found-asked")) return; shown = true;
    var box = document.createElement("div");
    box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Quick question");
    box.style.cssText = "position:fixed;right:16px;bottom:16px;z-index:9999;max-width:320px;background:#fff;color:#1d2433;border:2px solid #1d2433;border-radius:12px;padding:14px 16px;box-shadow:0 8px 24px rgba(0,0,0,.18);font:15px/1.4 system-ui,-apple-system,Segoe UI,sans-serif";
    var opts = ["ChatGPT", "Google", "Another AI", "Reddit", "Tumblr", "A friend", "Other"];
    box.innerHTML = '<button type="button" aria-label="Close" data-x style="position:absolute;top:6px;right:8px;border:0;background:none;font-size:20px;cursor:pointer;color:inherit">×</button>'
      + '<b style="display:block;margin:0 22px 8px 0">Glad it worked! How did you find this site?</b>'
      + '<div style="display:flex;flex-wrap:wrap;gap:6px">' + opts.map(function (o) {
        return '<button type="button" data-a="' + o + '" style="border:1.5px solid #1d2433;background:#f4f4f1;border-radius:99px;padding:5px 11px;cursor:pointer;font:inherit;color:inherit">' + o + '</button>'; }).join("") + '</div>'
      + '<form data-q hidden style="margin-top:10px"><label style="display:block;font-size:14px;margin-bottom:4px">What did you ask or search for? <span style="opacity:.7">(optional)</span></label>'
      + '<input maxlength="200" style="width:100%;box-sizing:border-box;padding:7px 9px;border:1.5px solid #1d2433;border-radius:8px;font:inherit">'
      + '<button style="margin-top:8px;border:0;background:#1d2433;color:#fff;border-radius:8px;padding:7px 14px;cursor:pointer;font:inherit">Send</button></form>'
      + '<p style="margin:8px 0 0;font-size:12.5px;opacity:.75">Anonymous, no cookies. Helps a one-person project know where people come from.</p>';
    var ans = "";
    function done(msg) { ls("found-asked", "1"); box.innerHTML = "<b>" + msg + "</b>"; setTimeout(function () { box.remove(); }, 1800); }
    box.addEventListener("click", function (e) {
      var t = e.target;
      if (t.hasAttribute && t.hasAttribute("data-x")) { ls("found-asked", "1"); send({ t: "ask", src: ss("found-src") || "", ans: "dismissed" }); box.remove(); return; }
      if (t.getAttribute && t.getAttribute("data-a")) {
        var first = !ans; ans = t.getAttribute("data-a");
        if (first) { ls("found-asked", "1"); send({ t: "ask", src: ss("found-src") || "", ans: ans }); }
        box.querySelectorAll("[data-a]").forEach(function (b) { b.style.background = b === t ? "#1d2433" : "#f4f4f1"; b.style.color = b === t ? "#fff" : "inherit"; });
        var f = box.querySelector("[data-q]"); f.hidden = false; f.querySelector("input").focus();
      }
    });
    box.querySelector("[data-q]").addEventListener("submit", function (e) {
      e.preventDefault();
      var q = box.querySelector("input").value.trim().slice(0, 200);
      if (q) send({ t: "askq", src: ss("found-src") || "", ans: ans, q: q });
      done("Thank you!");
    });
    setTimeout(function () { document.body.appendChild(box); }, 900);
  }
  window.Found = { land: land, ask: ask };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", land); else land();
})();
