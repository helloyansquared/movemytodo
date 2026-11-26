#!/usr/bin/env python3
"""Build the public site.
Usage: python3 build.py https://movemytodo.com/ [--ms CLIENT_ID] [--google CLIENT_ID] [--product pdt_ID]
- public/index.html from src/index.html (+ FAQ, facts, comparison, JSON-LD from src/content.py)
- one page per guide in src/content.py, plus /privacy/ and /terms/
- robots.txt, sitemap.xml, llms.txt, 404.html
IDs that aren't given stay as placeholders, and the page then says that feature isn't set up."""
import sys, re, json, pathlib, html as H, argparse, hashlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent / 'src'))
import content as C

ap = argparse.ArgumentParser(); ap.add_argument('site'); ap.add_argument('--ms'); ap.add_argument('--google'); ap.add_argument('--product')
a = ap.parse_args()
site = a.site.rstrip('/') + '/'
root = pathlib.Path(__file__).parent
pub = root / 'public'
esc = lambda s: H.escape(s, quote=True)
tx = lambda s: H.escape(s, quote=False)
U = lambda slug='': site + (slug + '/' if slug else '')
human = lambda d: datetime.date.fromisoformat(d).strftime('%B %-d, %Y')
upd_human = human(C.LAST_UPDATED)
ver = hashlib.sha1((pub / 'core.js').read_bytes()).hexdigest()[:8]

FONT_FACES = ''.join(f'@font-face{{font-family:"{fam}";src:url(/fonts/{f}.woff2) format("woff2");font-weight:{w};font-display:swap}}\n'
  for fam, f, w in [("Big Shoulders Display", "big-shoulders-display-latin-800-normal", 800),
                    ("Big Shoulders Stencil Display", "big-shoulders-stencil-display-latin-800-normal", 800),
                    ("Public Sans", "public-sans-latin-400-normal", 400), ("Public Sans", "public-sans-latin-600-normal", 600), ("Public Sans", "public-sans-latin-700-normal", 700)])
PRELOAD = '<link rel="preload" href="/fonts/big-shoulders-display-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/fonts/public-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>'
ORG = {"@type": "Organization", "@id": U() + "#org", "name": "MoveMyTodo", "url": U(), "logo": U() + "logo.png", "email": C.EMAIL,
       "parentOrganization": {"@type": "Organization", "name": "YanSquared"}}

def faq_html(keys):
    return '\n'.join(f'  <details{" open" if i == 0 else ""}><summary>{tx(C.QA[k][0])}</summary><p>{tx(C.QA[k][1])}</p></details>' for i, k in enumerate(keys))
def faq_ld(keys):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": C.QA[k][0], "acceptedAnswer": {"@type": "Answer", "text": C.QA[k][1]}} for k in keys]}
def ld(nodes):
    return '<script type="application/ld+json">\n' + json.dumps(nodes, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '\n</script>'

FOOTLINKS = ('<nav class="foot" aria-label="Guides">' + ''.join(f'<a href="/{p["slug"]}/">{esc(p["crumb"])}</a>' for p in C.PAGES)
             + '<a href="/privacy/">Privacy</a><a href="/terms/">Terms &amp; refunds</a></nav>')
GUIDES = ''.join(f'<a href="/{p["slug"]}/">{esc(p["h1"])}<span>{esc(p["description"])}</span></a>' for p in C.PAGES)

def fill_ids(s):
    s = s.replace('__SITE__', site).replace('__V__', ver)
    if a.ms: s = s.replace('__MS_CLIENT_ID__', a.ms)
    if a.google: s = s.replace('__GOOGLE_CLIENT_ID__', a.google)
    if a.product:
        assert re.fullmatch(r'pdt_[A-Za-z0-9]+', a.product)
        s = s.replace('__PRODUCT_ID__', a.product)
    return s

# ── Home ──────────────────────────────────────────────────────────────────────
s = (root / 'src/index.html').read_text()
s = s.replace('<style>\n', '<style>\n' + FONT_FACES, 1)
head = (f'{PRELOAD}\n<link rel="canonical" href="{site}">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="/logo.png">\n'
        f'<meta property="og:url" content="{site}">\n<meta property="og:image" content="{site}og.png">\n'
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">'
        + (f'\n<meta name="msvalidate.01" content="{(root / "src/msvalidate.txt").read_text().strip()}">' if (root / 'src/msvalidate.txt').exists() else ''))
app = {"@type": "WebApplication", "@id": U() + "#app", "name": "MoveMyTodo", "url": U(),
       "description": "Browser-based tool that reads Microsoft To Do (read-only) and exports it as CSV, Markdown or JSON, or moves lists, steps, notes and due dates to Google Tasks, Apple Reminders, Things 3 or Todoist.",
       "applicationCategory": "UtilitiesApplication", "operatingSystem": "Windows, macOS, iOS, Android, ChromeOS, Linux",
       "browserRequirements": "Requires JavaScript. Current Chrome, Edge, Firefox or Safari.", "image": U() + "og.png", "inLanguage": "en-US",
       "datePublished": C.PUBLISHED, "dateModified": C.LAST_UPDATED, "publisher": {"@id": U() + "#org"}, "isAccessibleForFree": True,
       "featureList": ["Read-only Microsoft sign-in", "Free backup as CSV, Markdown, JSON and printable page", "Move to Google Tasks with steps as subtasks",
                       "Apple Reminders import for Mac", "Things 3 import", "Todoist CSV files"],
       "offers": [{"@type": "Offer", "name": "Backup and scan", "price": "0", "priceCurrency": "USD"},
                  {"@type": "Offer", "name": "MoveMyTodo Pro (move all lists)", "price": C.PRICE, "priceCurrency": "USD", "url": U() + "#pricing"}]}
home_ld = ld([{"@context": "https://schema.org", **ORG},
              {"@context": "https://schema.org", "@type": "WebSite", "@id": U() + "#site", "name": "MoveMyTodo", "url": U(), "inLanguage": "en-US", "publisher": {"@id": U() + "#org"}},
              {"@context": "https://schema.org", **app}, faq_ld(C.HOME_FAQ)])
for k, v in {'<!--SEO-HEAD-->': head, '<!--LDJSON-->': home_ld, '<!--HOME-FAQ-->': faq_html(C.HOME_FAQ), '<!--FACTS-->': C.facts_table(),
             '<!--DEFINITION-->': tx(C.DEFINITION), '<!--COMPARE-->': C.compare_table(), '<!--GUIDES-->': GUIDES,
             '<!--FOOTLINKS-->': FOOTLINKS, '<!--UPDATED-->': upd_human, '<!--PUBLISHED-->': human(C.PUBLISHED), '{EMAIL}': C.EMAIL}.items():
    assert k in s, k
    s = s.replace(k, v)
(pub / 'index.html').write_text(fill_ids(s))
fn = root / 'functions/api/license.js'
if a.product: fn.write_text(re.sub(r'const PRODUCT_ID = "[^"]*";', f'const PRODUCT_ID = "{a.product}";', fn.read_text()))

# ── Sub-pages ─────────────────────────────────────────────────────────────────
PAGE_CSS = FONT_FACES + """:root{--kraft:#e9d8b8;--paper:#fbf6ec;--ink:#1f2a44;--soft:#5b6478;--line:#d6c7a8;--tape:#f4c430;--tape2:#e0ad12;--blue:#2453c8;--green:#1e7a4f}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 "Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--blue)}h1,h2{font-family:"Big Shoulders Display",Impact,sans-serif;font-weight:800;line-height:1.04;text-wrap:balance;text-transform:uppercase}
.top{background:var(--ink);color:#fff;padding:16px 0 0}.top a{color:#fff;text-decoration:none}
.wrap{max-width:800px;margin:0 auto;padding:0 max(4vw,18px)}
.logo{font:800 24px/1 "Big Shoulders Stencil Display","Big Shoulders Display",Impact,sans-serif;letter-spacing:.02em;text-transform:uppercase}
.band{background:var(--kraft);border-bottom:3px solid var(--ink);margin-top:16px;padding:18px 0 30px}
.crumbs{font-size:14px;color:#4a536b;margin:0 0 6px}.crumbs a{color:var(--ink)}
.band h1{font-size:clamp(34px,5.4vw,54px);margin:4px 0 0}
main{padding:28px 0 44px}.answer{font-size:19px;line-height:1.6;border-left:5px solid var(--tape);padding:4px 0 4px 16px;margin:0 0 18px}
.cta{display:inline-flex;align-items:center;min-height:50px;padding:0 22px;border-radius:10px;border:2px solid var(--ink);background:var(--tape);color:var(--ink);font-weight:700;text-decoration:none;box-shadow:4px 4px 0 var(--ink)}
.meta{font-size:14px;color:var(--soft);margin:16px 0 26px}
h2{font-size:clamp(26px,3.4vw,34px);margin:36px 0 10px}li{margin:6px 0}
code{font:.9em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:#efe6d3;padding:1px 5px;border-radius:5px}
pre{background:var(--ink);color:#f6f0de;border-radius:10px;padding:14px;overflow:auto}pre code{background:none;color:inherit;padding:0}
.facts,.cmp{border-collapse:collapse;width:100%;margin:12px 0;border:2px solid var(--ink);font-size:15.5px;background:#fff}.facts caption{text-align:left;color:var(--soft);font-size:13px;padding-bottom:6px}
.facts th,.facts td,.cmp th,.cmp td{padding:9px 12px;border-top:1px solid var(--line);text-align:left;vertical-align:top}.facts th{width:30%}.cmp thead th{background:var(--ink);color:#fff}
details{border-bottom:1.5px solid var(--line);padding:4px 0}summary{cursor:pointer;font-weight:700;min-height:46px;display:flex;align-items:center}details p{margin:2px 0 14px;color:#3c4560}
.related{background:#fff;border:2px solid var(--ink);border-radius:12px;padding:16px 18px;margin-top:30px}.related ul{margin:6px 0 0;padding-left:20px}
footer{background:var(--ink);color:#c9d0e4;font-size:14px;padding:26px 0}footer a{color:#fff}.foot{display:flex;flex-wrap:wrap;gap:6px 16px;margin-bottom:10px}
a:focus-visible,summary:focus-visible{outline:3px solid var(--blue);outline-offset:2px}"""

def shell(title, desc, canon, h1, crumb, body_html, ldnodes, robots=None):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{tx(title)}</title>
<meta name="description" content="{esc(desc)}">
{f'<meta name="robots" content="{robots}">' if robots else f'<link rel="canonical" href="{canon}">'}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article"><meta property="og:site_name" content="MoveMyTodo"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{site}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
{PRELOAD}
{ld(ldnodes) if ldnodes else ''}
<style>{PAGE_CSS}</style>
</head>
<body>
<header class="top"><div class="wrap"><a class="logo" href="/">MoveMyTodo</a></div>
<div class="band"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">MoveMyTodo</a> › {tx(crumb)}</nav>
  <h1>{tx(h1)}</h1>
</div></div></header>
<main class="wrap">
{body_html}
</main>
<footer><div class="wrap">{FOOTLINKS}MoveMyTodo is an independent tool by YanSquared. It is not affiliated with, endorsed by or connected to Microsoft, Google, Apple or Cultured Code. Microsoft To Do is a trademark of Microsoft Corporation. Questions: <a href="mailto:{C.EMAIL}">{C.EMAIL}</a> · Last updated: {upd_human}</div></footer>
</body>
</html>
"""

def crumbs_ld(name, url):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "MoveMyTodo", "item": U()},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}

PAGES = {p['slug']: p for p in C.PAGES}
for p in C.PAGES:
    url = U(p['slug'])
    body = (f'<p class="answer">{tx(p["answer"])}</p>\n<a class="cta" href="/#app">Scan my To Do lists</a>\n'
            f'<p class="meta">Last updated: <time datetime="{C.LAST_UPDATED}">{upd_human}</time> · Free scan and backup · Read-only sign-in</p>\n'
            + p['body'].replace('{FACTS}', C.facts_table())
            + f'\n<h2>Questions</h2>\n{faq_html(p["faq"])}\n'
            + '<aside class="related"><b>Related guides</b><ul>' + ''.join(f'<li><a href="/{s2}/">{tx(PAGES[s2]["h1"])}</a></li>' for s2 in p['links'])
            + '<li><a href="/">MoveMyTodo: move Microsoft To Do to Google Tasks or Apple Reminders</a></li></ul></aside>')
    article = {"@context": "https://schema.org", "@type": "TechArticle", "headline": p['h1'], "description": p['description'], "url": url,
               "inLanguage": "en-US", "datePublished": C.PUBLISHED, "dateModified": C.LAST_UPDATED, "image": U() + "og.png",
               "author": {"@id": U() + "#org"}, "publisher": {"@context": "https://schema.org", **ORG}, "mainEntityOfPage": url}
    out = pub / p['slug']; out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(shell(p['title'], p['description'], url, p['h1'], p['crumb'], body, [crumbs_ld(p['crumb'], url), article, faq_ld(p['faq'])]))

# ── Privacy & terms (also what Google and Microsoft show on their consent screens) ──
priv = f"""<p class="answer">MoveMyTodo reads your Microsoft To Do tasks inside your own browser tab, and only when you ask it to. Your tasks are never sent to, stored on or seen by our servers.</p>
<p class="meta">Effective: <time datetime="{C.PUBLISHED}">{human(C.PUBLISHED)}</time> · Last updated: {upd_human}</p>
<h2>What you allow, and why</h2>
<table class="facts">
<tr><th scope="row">Microsoft</th><td><b>Tasks.Read</b> (read your tasks) plus basic sign-in (your name and email, to show which account you used). Read-only: MoveMyTodo can't change or delete anything in To Do.</td></tr>
<tr><th scope="row">Google</th><td><b>Google Tasks</b> access, asked for only when you click “Connect Google Tasks”. MoveMyTodo uses it only to list your task lists' names (so it doesn't overwrite one) and to create the new lists and tasks you asked to move. It doesn't read, change or delete your existing tasks.</td></tr>
</table>
<h2>Where your data goes</h2>
<p>Sign-in happens on Microsoft's and Google's own pages. The access they grant is kept only in the memory of your browser tab, never saved to disk or sent to us, and ends when you close the tab (Microsoft and Google tokens also expire within about an hour). Your tasks travel directly between your browser and Microsoft's and Google's servers. Files you download (backups, the Apple Reminders script, Todoist files) are made in your browser.</p>
<h2>Google user data</h2>
<p>MoveMyTodo's use and transfer of information received from Google APIs adheres to the <a href="https://developers.google.com/terms/api-services-user-data-policy">Google API Services User Data Policy</a>, including the Limited Use requirements. We don't store, sell or share Google user data, don't use it for advertising, and don't use it to train AI models. No human at YanSquared can read it.</p>
<h2>License keys and payments</h2>
<p>If you buy MoveMyTodo Pro, payment is handled by Dodo Payments (merchant of record), which processes your card, sales tax and receipt under its own privacy policy. When you activate Pro, your license key is sent to our small checking service (a Cloudflare Pages Function), which asks Dodo Payments whether it's valid. The key and an activation ID are saved in your browser's local storage so Pro stays unlocked. The checking service doesn't keep the key and never receives your tasks.</p>
<h2>Hosting, cookies and analytics</h2>
<p>The site is hosted on Cloudflare Pages. Like any host, Cloudflare processes standard request data such as IP addresses to deliver and protect the site. MoveMyTodo uses no cookies, analytics or ads. Google's sign-in script, loaded only when you connect Google Tasks, is covered by Google's privacy policy.</p>
<h2>Removing access</h2>
<p>You can remove MoveMyTodo's access at any time: Microsoft at <a href="https://account.live.com/consent/Manage">account.live.com/consent/Manage</a> (personal accounts) or <a href="https://myapps.microsoft.com">myapps.microsoft.com</a> (work or school), and Google at <a href="https://myaccount.google.com/permissions">myaccount.google.com/permissions</a>.</p>
<h2>Contact</h2>
<p>MoveMyTodo is made by YanSquared. Email <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p>"""
(pub / 'privacy').mkdir(exist_ok=True)
(pub / 'privacy/index.html').write_text(shell('Privacy Policy | MoveMyTodo', 'How MoveMyTodo handles your Microsoft To Do and Google Tasks data: read in your browser, never stored on our servers.',
                                              U('privacy'), 'Privacy policy', 'Privacy', priv, [crumbs_ld('Privacy', U('privacy'))]))
terms = f"""<p class="answer">MoveMyTodo is a small independent tool. Use it to back up and move your own tasks. Here are the few rules.</p>
<p class="meta">Effective: {human(C.PUBLISHED)}</p>
<h2>The service</h2><p>MoveMyTodo reads your Microsoft To Do tasks with your permission and writes copies to files or to the app you choose. It only adds; it never deletes your tasks in To Do or in the destination app. Check the result in your new app before you stop using To Do. MoveMyTodo depends on Microsoft's and Google's services, which they can change or switch off.</p>
<h2>Pro</h2><p>MoveMyTodo Pro is a one-time purchase (${C.PRICE}, tax included) that unlocks moving all lists and tasks. A license works on up to 3 browsers. There's no subscription.</p>
<h2>Refunds</h2><p>If MoveMyTodo doesn't work for your account, email <a href="mailto:{C.EMAIL}">{C.EMAIL}</a> within 14 days of buying and we'll refund you in full.</p>
<h2>Fair use</h2><p>Use MoveMyTodo only with accounts you're allowed to use. Don't try to break, overload or resell it.</p>
<h2>No warranty</h2><p>MoveMyTodo is provided as is. We're careful, but we can't promise every field moves perfectly, so keep the free backup. Our liability is limited to what you paid us.</p>
<h2>Contact</h2><p>YanSquared · <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>"""
(pub / 'terms').mkdir(exist_ok=True)
(pub / 'terms/index.html').write_text(shell('Terms & Refunds | MoveMyTodo', 'Terms of use and refund policy for MoveMyTodo and MoveMyTodo Pro.',
                                            U('terms'), 'Terms & refunds', 'Terms', terms, [crumbs_ld('Terms', U('terms'))]))
(pub / '404.html').write_text(shell('Page not found | MoveMyTodo', 'This page does not exist.', U(), 'Page not found', 'Not found',
                                    '<p class="answer">That page doesn\'t exist. <a href="/">Go to MoveMyTodo</a> to back up or move your Microsoft To Do lists.</p>', None, robots='noindex'))

# ── robots, sitemap, llms.txt ─────────────────────────────────────────────────
(pub / 'robots.txt').write_text(f"User-agent: *\nAllow: /\n\nSitemap: {site}sitemap.xml\n")
urls = [U()] + [U(p['slug']) for p in C.PAGES] + [U('privacy'), U('terms')]
(pub / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc><lastmod>{C.LAST_UPDATED}</lastmod></url>\n' for u in urls) + '</urlset>\n')
strip = lambda t: re.sub("<[^>]+>", "", t)
(pub / 'llms.txt').write_text(f"""# MoveMyTodo

> MoveMyTodo is a browser-based tool for people leaving Microsoft To Do, which Microsoft retires on June 30, 2027. It signs in to Microsoft with read-only access, shows every list and task, downloads a free backup (CSV, Markdown, JSON, printable page) and moves lists, steps, notes and due dates to Google Tasks, Apple Reminders (Mac import script), Things 3 or Todoist (CSV). Tasks are processed in the browser and never stored on its servers. Backup is free; moving more than {C.FREE_N} tasks costs ${C.PRICE} once. Not affiliated with Microsoft.

## Microsoft To Do retirement: key facts (checked {C.CHECKED})
""" + '\n'.join(f'- {strip(x)}: {strip(y)}' for x, y in C.FACTS_ROWS) + f"""

## What moves where
""" + '\n'.join(f'- {r[0]}: ' + '; '.join(f'{C.COMPARE_HEAD[i + 1]}: {strip(v[2:] if v[:2] in ("y:", "n:") else v)}' for i, v in enumerate(r[1:])) for r in C.COMPARE_ROWS) + f"""

## Pages
- [Tool: move Microsoft To Do to Google Tasks or Apple Reminders]({U()})
""" + ''.join(f"- [{p['h1']}]({U(p['slug'])}): {p['description']}\n" for p in C.PAGES) + f"""- [Privacy policy]({U('privacy')})
- [Terms and refunds]({U('terms')})

Last updated: {C.LAST_UPDATED}. Contact: {C.EMAIL}
""")
missing = [k for k, v in {'Microsoft client id': a.ms, 'Google client id': a.google, 'product id': a.product}.items() if not v]
print('built for', site, '·', len(urls), 'urls', '· core', ver, ('· not set: ' + ', '.join(missing)) if missing else '')
