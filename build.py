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

FONT_FACES = ''.join(f'@font-face{{font-family:"Instrument Sans";src:url(/fonts/instrument-sans-latin-{w}-normal.woff2) format("woff2");font-weight:{w};font-display:swap}}\n' for w in (400, 500, 600))
PRELOAD = '<link rel="preload" href="/fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/fonts/instrument-sans-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>'
LOGO_SVG = '<svg width="26" height="26" viewBox="0 0 28 28" aria-hidden="true"><rect width="28" height="28" rx="7" fill="#16775a"/><path d="M7 14.5l4.2 4.2L21 9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M16.2 8.6H21v4.8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
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
             + f'<a href="/privacy/">Privacy</a><a href="/terms/">Terms &amp; refunds</a><a href="{C.GITHUB}">Source code on GitHub</a><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></nav>')
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
PAGE_CSS = FONT_FACES + """:root{--line:#e4e7ec;--line2:#d3d8df;--ink:#1a2230;--soft:#5b6472;--green:#16775a;--green-d:#0f5f47;--green-t:#e9f4ef;--surface:#f6f7f9}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:17px/1.65 "Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--green);text-underline-offset:2px}a:hover{color:var(--green-d)}
h1,h2,h3{font-weight:600;letter-spacing:-.02em;line-height:1.15;text-wrap:balance}
.top{border-bottom:1px solid var(--line)}.bar{display:flex;align-items:center;justify-content:space-between;height:64px}
.wrap{max-width:760px;margin:0 auto;padding:0 max(5vw,20px)}.top .wrap{max-width:1120px}
.logo{display:inline-flex;align-items:center;gap:10px;font-weight:600;font-size:18px;color:var(--ink);text-decoration:none;letter-spacing:-.01em}
.navcta{font-size:15px;color:var(--ink);text-decoration:none;border:1px solid var(--line2);border-radius:9px;padding:7px 14px}.navcta:hover{border-color:var(--ink);color:var(--ink)}
.head{padding:56px 0 8px}.crumbs{font-size:14.5px;color:var(--soft);margin:0 0 14px}.crumbs a{color:var(--soft)}
.head h1{font-size:clamp(32px,4.6vw,48px);letter-spacing:-.035em;line-height:1.08;margin:0}
main{padding:20px 0 64px}.answer{font-size:20px;line-height:1.55;margin:18px 0 26px;color:var(--ink)}
.cta{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;border-radius:10px;background:var(--green);color:#fff;font-weight:500;text-decoration:none}.cta:hover{background:var(--green-d);color:#fff}
.meta{font-size:14.5px;color:var(--soft);margin:16px 0 36px}
h2{font-size:clamp(24px,3vw,30px);letter-spacing:-.03em;margin:52px 0 12px}h3{font-size:19px;margin:28px 0 8px}li{margin:8px 0}
code{font:.9em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--surface);border:1px solid var(--line);padding:1px 5px;border-radius:5px}
pre{background:var(--ink);color:#e9edf3;border-radius:8px;padding:14px 16px;overflow:auto}pre code{background:none;border:0;color:inherit;padding:0}
.facts,.cmp{border-collapse:collapse;width:100%;margin:16px 0;font-size:15.5px}.facts caption{text-align:left;color:var(--soft);font-size:14px;padding-bottom:8px}
.facts th,.facts td,.cmp th,.cmp td{padding:12px 12px 12px 0;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.facts th,.cmp tbody th{font-weight:500}.facts th{width:30%}.cmp thead th{font-weight:600;font-size:14.5px;color:var(--soft);border-bottom:1px solid var(--ink)}
.note{background:var(--green-t);border-radius:10px;padding:4px 18px;margin:18px 0}
details{border-bottom:1px solid var(--line)}details:first-of-type{border-top:1px solid var(--line)}
summary{cursor:pointer;font-weight:500;min-height:56px;display:flex;align-items:center;justify-content:space-between;gap:16px;list-style:none}summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:22px;color:var(--soft);transition:transform .2s}details[open] summary::after{transform:rotate(45deg)}details p{margin:0 0 18px;color:var(--soft)}
.related{border-top:1px solid var(--ink);padding-top:18px;margin-top:52px}.related ul{margin:8px 0 0;padding-left:20px}
footer{border-top:1px solid var(--line);background:var(--surface);color:var(--soft);font-size:14.5px;padding:32px 0 40px}footer .wrap{max-width:1120px}footer a{color:var(--ink)}.foot{display:flex;flex-wrap:wrap;gap:8px 22px;margin-bottom:12px}
a:focus-visible,summary:focus-visible{outline:2px solid var(--green);outline-offset:3px}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}"""

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
<header class="top"><div class="wrap bar"><a class="logo" href="/">{LOGO_SVG}MoveMyTodo</a><a class="navcta" href="/#app">Scan my lists</a></div></header>
<div class="head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">MoveMyTodo</a> › {tx(crumb)}</nav>
  <h1>{tx(h1)}</h1>
</div></div>
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
<tr><th scope="row">Google</th><td><b>Google Tasks</b> (<code>https://www.googleapis.com/auth/tasks</code>), asked for only when you click “Connect Google Tasks &amp; move”. It's the narrowest Google permission that can create tasks; the read-only one can't. MoveMyTodo asks for no other Google data: not Gmail, Drive, Calendar or Contacts.</td></tr>
</table>
<h2>Where your data goes</h2>
<p>Sign-in happens on Microsoft's and Google's own pages. The access they grant is kept only in the memory of your browser tab, never saved to disk or sent to us, and ends when you close the tab (Microsoft and Google tokens also expire within about an hour). Your tasks travel directly between your browser and Microsoft's and Google's servers. Files you download (backups, the Apple Reminders script, Todoist files) are made in your browser.</p>
<h2 id="google">Google user data</h2>
<p><b>What we access.</b> With the Google Tasks permission, MoveMyTodo reads the <i>names</i> of your existing task lists (so a new list never overwrites one with the same name) and creates new task lists and tasks: title, notes, due date, completed status and subtasks, copied from the Microsoft To Do lists you chose. It doesn't read the contents of your existing Google tasks, and it doesn't change or delete anything in Google Tasks.</p>
<p><b>How we use it.</b> Only to carry out the move you start by clicking the button, and only while this browser tab is open. Nothing runs in the background or later.</p>
<p><b>Storage and retention.</b> None. Google's access token and your task data stay in your browser tab's memory and are discarded when you close or reload it. MoveMyTodo has no database, and no Google user data ever reaches our servers or logs.</p>
<p><b>Sharing.</b> We don't share, transfer, sell or disclose Google user data to anyone. Your tasks travel directly between your browser and Google over an encrypted (HTTPS) connection.</p>
<p><b>Limited Use.</b> MoveMyTodo's use and transfer to any other app of information received from Google APIs will adhere to the <a href="https://developers.google.com/terms/api-services-user-data-policy">Google API Services User Data Policy</a>, including the Limited Use requirements. We don't use Google user data for advertising, and we don't use it to develop, improve or train AI or machine-learning models. No human at YanSquared can read it.</p>
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
