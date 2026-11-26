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
       "sameAs": [C.GITHUB], "founder": {"@id": U('about') + "#maker"},
       "parentOrganization": {"@type": "Organization", "name": "YanSquared"}}
PERSON = {"@type": "Person", "@id": U('about') + "#maker", "name": C.MAKER, "url": U('about'), "jobTitle": "Independent developer, maker of MoveMyTodo",
          "worksFor": {"@id": U() + "#org"}, "sameAs": [C.GITHUB]}

def faq_html(keys):
    return '\n'.join(f'  <details{" open" if i == 0 else ""}><summary>{tx(C.QA[k][0])}</summary><p>{tx(C.QA[k][1])}</p></details>' for i, k in enumerate(keys))
def faq_ld(keys):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": C.QA[k][0], "acceptedAnswer": {"@type": "Answer", "text": C.QA[k][1]}} for k in keys]}
def ld(nodes):
    return '<script type="application/ld+json">\n' + json.dumps(nodes, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '\n</script>'

FOOTLINKS = ('<nav class="foot" aria-label="Guides">' + ''.join(f'<a href="/{p["slug"]}/">{esc(p["crumb"])}</a>' for p in C.PAGES)
             + f'<a href="/about/">About</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms &amp; refunds</a><a href="{C.GITHUB}">Source code on GitHub</a><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></nav>')
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
       "offers": [{"@type": "Offer", "name": "Free", "price": "0", "priceCurrency": "USD",
                   "description": f"Scan every list, full backup (CSV, Markdown, JSON, printable page), Todoist CSV files, and moving up to {C.FREE_N} tasks from one list."},
                  {"@type": "Offer", "name": "MoveMyTodo Pro", "price": C.PRICE, "priceCurrency": "USD", "url": U() + "#pricing",
                   "description": "One-time payment, no subscription. Moves all lists and tasks; 14-day refund." + (" " + C.GOOGLE_NOTE if C.GOOGLE_REVIEW else "")}]}
home_ld = ld([{"@context": "https://schema.org", **ORG}, {"@context": "https://schema.org", **PERSON},
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
a:focus-visible,summary:focus-visible{outline:3px solid var(--blue);outline-offset:2px}.src{font-size:14px;color:var(--soft)}
.log{padding-left:20px}.log li{margin:6px 0}.log time{font-weight:600}
"""

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
<script src="/found.js" defer></script>
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
CHANGELOG_HTML = '<ul class="log">' + ''.join(f'<li><time datetime="{d}">{human(d)}</time>: {tx(t)}</li>' for d, t in C.CHANGELOG) + '</ul>'
for p in C.PAGES:
    url = U(p['slug'])
    body = (f'<p class="answer">{tx(p["answer"])}</p>\n<a class="cta" href="/#app">Scan my To Do lists</a>\n'
            f'<p class="meta">Last updated: <time datetime="{C.LAST_UPDATED}">{upd_human}</time> · Free scan and backup · Read-only sign-in</p>\n'
            + p['body'].replace('{FACTS}', C.facts_table()).replace('{CHANGELOG}', CHANGELOG_HTML)
            + f'\n<h2>Questions</h2>\n{faq_html(p["faq"])}\n'
            + '<aside class="related"><b>Related guides</b><ul>' + ''.join(f'<li><a href="/{s2}/">{tx(PAGES[s2]["h1"])}</a></li>' for s2 in p['links'])
            + '<li><a href="/">MoveMyTodo: move Microsoft To Do to Google Tasks or Apple Reminders</a></li></ul></aside>')
    article = {"@context": "https://schema.org", "@type": "TechArticle", "headline": p['h1'], "description": p['description'], "url": url,
               "inLanguage": "en-US", "datePublished": C.PUBLISHED, "dateModified": C.LAST_UPDATED, "image": U() + "og.png",
               "author": PERSON, "publisher": ORG, "mainEntityOfPage": url}
    out = pub / p['slug']; out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(shell(p['title'], p['description'], url, p['h1'], p['crumb'], body, [crumbs_ld(p['crumb'], url), article, faq_ld(p['faq'])]))

# ── About (who's behind the tool: a site asking for Microsoft access needs a visible person) ──
about = f"""<p class="answer">MoveMyTodo is a small browser tool made by {C.MAKER}, an independent developer at YanSquared, for people leaving Microsoft To Do before it retires on June 30, 2027. It isn't made by or affiliated with Microsoft, Google, Apple, Cultured Code (Things) or Doist (Todoist).</p>
<p class="meta">Published <time datetime="{C.PUBLISHED}">{human(C.PUBLISHED)}</time> · Last updated: {upd_human}</p>
<h2>Why it exists</h2>
<p>When Microsoft announced on November 18, 2026 that the To Do apps would retire, people with years of lists had nowhere obvious to take them. Todoist and TickTick have their own importers, but Google Tasks, Apple Reminders and Things 3 don't. MoveMyTodo fills that gap, and gives everyone a free backup they control, whichever app they pick.</p>
<h2>Who it's for</h2>
<ul>""" + ''.join(f"<li>{tx(x)}</li>" for x in C.BEST_FOR) + """</ul>
<h2>When to use something else</h2>
<ul>""" + ''.join(f"<li>{tx(x)}</li>" for x in C.NOT_FOR) + f"""</ul>
<h2>How it handles your data</h2>
<ul>
<li>Sign-in is read-only: MoveMyTodo can't change or delete anything in To Do.</li>
<li>Your tasks are read straight into your browser tab and written directly to the app you choose. They never reach our servers, and nothing is kept after you close the tab.</li>
<li>No cookies, ads or tracking scripts. The site counts anonymously where visits come from (for example Google or ChatGPT), with no IDs. The full <a href="/privacy/">privacy policy</a> explains each permission.</li>
<li>The code is open source, so anyone can check what it does: <a href="{C.GITHUB}">{C.GITHUB.replace("https://", "")}</a>.</li>
</ul>
<h2>How the facts are checked</h2>
<p>Dates and rules about the retirement come from Microsoft's own support page, <a href="{C.MS_SOURCE}">“Moving from Microsoft To Do to Microsoft Planner”</a>, and Microsoft's announcement. Every guide shows when it was last checked, and the <a href="/microsoft-to-do-shutting-down/#updates">shutdown page keeps a dated log</a> of changes. When Microsoft updates its guidance or ships its export tool, the guides are updated.</p>
<h2>Pricing</h2>
<p>Scanning and the full backup are free with no limits. Moving up to {C.FREE_N} tasks from one list is free; MoveMyTodo Pro moves everything for ${C.PRICE} once, with a 14-day refund. {C.GOOGLE_NOTE if C.GOOGLE_REVIEW else ""}</p>
<h2>Contact</h2>
<p>Questions, bugs or a list that didn't move right: email <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>. {C.MAKER} reads every message.</p>"""
(pub / 'about').mkdir(exist_ok=True)
(pub / 'about/index.html').write_text(shell('About MoveMyTodo: Who Makes It and How It Works', f'MoveMyTodo is an independent, open-source browser tool by {C.MAKER} (YanSquared) for leaving Microsoft To Do. Who makes it, how your data is handled, and how facts are checked.',
                                            U('about'), 'About MoveMyTodo', 'About', about,
                                            [crumbs_ld('About', U('about')),
                                             {"@context": "https://schema.org", "@type": "AboutPage", "url": U('about'), "name": "About MoveMyTodo", "inLanguage": "en-US",
                                              "dateModified": C.LAST_UPDATED, "mainEntity": ORG, "author": PERSON}]))

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
<p>The site is hosted on Cloudflare Pages. Like any host, Cloudflare processes standard request data such as IP addresses to deliver and protect the site. MoveMyTodo uses no cookies, ads or third-party analytics. To learn which sites and AI assistants send visitors, the first page you open sends one anonymous note to our own server: the name of the site you came from (such as “google” or “chatgpt”, never the full address), the page and your country. After a backup or move, a small optional card asks how you found the site; if you answer, your choice and anything you type in the optional box are stored the same way. None of this includes your tasks, account, IP address or any ID, and it can't be linked to you. Google's sign-in script, loaded only when you connect Google Tasks, is covered by Google's privacy policy.</p>
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
BOTS = ["Googlebot", "Bingbot", "Google-Extended", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "ClaudeBot", "Claude-SearchBot", "Claude-User",
        "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended", "DuckAssistBot", "meta-externalagent", "MistralAI-User"]
(pub / 'robots.txt').write_text("# Search engines and AI answer engines are welcome to read and cite every page.\n"
    + "".join(f"User-agent: {b}\n" for b in BOTS) + "Allow: /\n\nUser-agent: *\nAllow: /\n\n" + f"Sitemap: {site}sitemap.xml\n")
urls = [U()] + [U(p['slug']) for p in C.PAGES] + [U('about'), U('privacy'), U('terms')]
(pub / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc><lastmod>{C.LAST_UPDATED}</lastmod></url>\n' for u in urls) + '</urlset>\n')
strip = lambda t: re.sub("<[^>]+>", "", t)
(pub / 'llms.txt').write_text(f"""# MoveMyTodo

> MoveMyTodo is an open-source browser tool for people leaving Microsoft To Do, which Microsoft retires on June 30, 2027. It signs in to Microsoft with read-only access, shows every list and task, downloads a free backup (CSV, Markdown, JSON, printable page) and moves lists, steps, notes and due dates to Google Tasks, Apple Reminders (Mac import script) or Things 3. Tasks are processed in the browser and never stored on its servers. Scanning and the backup are free; moving up to {C.FREE_N} tasks from one list is free; MoveMyTodo Pro moves everything for ${C.PRICE} once.{(" " + C.GOOGLE_NOTE) if C.GOOGLE_REVIEW else ""} Todoist and TickTick have their own free Microsoft To Do importers, which MoveMyTodo recommends for those apps. Made by {C.MAKER} (YanSquared). Not affiliated with Microsoft.

## Best for
""" + ''.join(f"- {x}\n" for x in C.BEST_FOR) + """
## Not the right tool for
""" + ''.join(f"- {x}\n" for x in C.NOT_FOR) + f"""
## Microsoft To Do retirement: key facts (checked {C.CHECKED})
""" + '\n'.join(f'- {strip(x)}: {strip(y)}' for x, y in C.FACTS_ROWS) + f"""
- Source: {C.MS_SOURCE}

## What moves where with MoveMyTodo
""" + '\n'.join(f'- {r[0]}: ' + '; '.join(f'{C.COMPARE_HEAD[i + 1]}: {strip(v[2:] if v[:2] in ("y:", "n:") else v)}' for i, v in enumerate(r[1:])) for r in C.COMPARE_ROWS) + """

## Questions and answers
""" + ''.join(f"### {q}\n{strip(ans)}\n\n" for q, ans in C.QA.values()) + """## Updates
""" + ''.join(f"- {d}: {strip(t)}\n" for d, t in C.CHANGELOG) + f"""
## Pages
- [MoveMyTodo tool: move or back up Microsoft To Do]({U()})
""" + ''.join(f"- [{p['h1']}]({U(p['slug'])}): {p['description']}\n" for p in C.PAGES) + f"""- [About MoveMyTodo]({U('about')}): who makes it, how data is handled, how facts are checked
- [Privacy policy]({U('privacy')})
- [Terms and refunds]({U('terms')})
- [Source code]({C.GITHUB})

Last updated: {C.LAST_UPDATED}. Contact: {C.EMAIL}
""")
missing = [k for k, v in {'Microsoft client id': a.ms, 'Google client id': a.google, 'product id': a.product}.items() if not v]
print('built for', site, '·', len(urls), 'urls', '· core', ver, ('· not set: ' + ', '.join(missing)) if missing else '')
