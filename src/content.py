# All MoveMyTodo page copy. FAQ text feeds both the visible FAQ and the FAQPage JSON-LD.
# Facts about the Microsoft To Do retirement checked against Microsoft's transition notice as reported on
# 18–25 November 2026 (Planner blog post of 18 Nov; coverage by 9to5Mac, MakeUseOf, Office Watch, LazyAdmin).
PUBLISHED = "2026-11-26"
LAST_UPDATED = "2026-11-26"
CHECKED = "26 November 2026"
EMAIL = "hello@yansquared.com"
GITHUB = "https://github.com/helloyansquared/movemytodo"
PRICE = "6.99"
FREE_N = 25
# True until Google approves the Tasks scope: Google shows an "unverified app" page and Google Tasks is Pro-only.
# Flip together with GOOGLE_REVIEW in src/index.html.
GOOGLE_REVIEW = True
# Same sentence everywhere it's needed (page, FAQ, llms.txt), so AI answers quote one version.
GOOGLE_NOTE = "Google Tasks is part of MoveMyTodo Pro while Google reviews the app, because Google limits unverified apps to 100 users."
MAKER = "Yan"
MS_SOURCE = "https://support.microsoft.com/en-us/planner/to-do-to-planner"
TODOIST_IMPORTER = "https://www.todoist.com/importer/microsoft-todo"
# Dated log of what changed in Microsoft's guidance or on this site (newest first). Shown on the shutdown page.
CHANGELOG = [
    ("2026-11-26", "Checked Microsoft's support page again: Microsoft's export tool is still not available. Added guides for Planner and Todoist."),
    ("2026-11-21", "Todoist launched a free Microsoft To Do importer that works on every Todoist plan."),
    ("2026-11-18", "Microsoft announced that the To Do apps retire on June 30, 2027."),
]

DEFINITION = ("Microsoft is retiring the Microsoft To Do apps on June 30, 2027, on the web, Windows, Mac, iPhone and Android. "
              "Your lists don't move anywhere by themselves: personal accounts get no replacement app, and work or school accounts "
              "are pointed to Planner, but existing To Do tasks are not copied into it.")

FACTS_ROWS = [
    ("Announced", "November 18, 2026, in a Microsoft Planner blog post and the To Do transition guide."),
    ("Shutdown date", "June 30, 2027. The To Do apps stop working on web, Windows, Mac, iOS and Android."),
    ("Personal accounts", "Outlook.com, Hotmail, Live and Microsoft 365 Personal or Family get no replacement. Microsoft says to choose another task app."),
    ("Work or school accounts", "Moved to Planner (“My tasks” is being redesigned from December 2026). Existing To Do tasks and lists are <b>not</b> migrated into it; they stay visible in Planner until June 30, 2027."),
    ("Microsoft's export", f"Promised before the shutdown, but not available as of {CHECKED}. Microsoft hasn't said what format it will use, and says an export doesn't mean another app can import it."),
    ("Your data", "Retiring the apps doesn't by itself schedule your task data for deletion, but there will be no app to see it in."),
    ("What reads To Do today", "Microsoft Graph, the official API that apps like MoveMyTodo use with your permission. Microsoft says the To Do service, APIs and sync retire later, on dates it hasn't announced."),
]

def facts_table():
    rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in FACTS_ROWS)
    return (f'<table class="facts"><caption>Microsoft To Do retirement: key facts (checked {CHECKED})</caption>{rows}</table>'
            f'<p class="src">Source: <a href="{MS_SOURCE}">Microsoft Support, “Moving from Microsoft To Do to Microsoft Planner”</a>, and Microsoft\'s Planner blog post of November 18, 2026.</p>')

# What each destination keeps. y = kept, n = not kept, text = how it's handled.
COMPARE_HEAD = ["", "Google Tasks", "Apple Reminders (Mac)", "Things 3", "Free CSV / Markdown"]
COMPARE_ROWS = [
    ("Lists", "y:New list each", "y:New list each", "y:Project each", "y:Column / heading"),
    ("Steps", "y:Subtasks", "Checklist in notes", "y:Checklist items", "y:Kept"),
    ("Notes and links", "y:Kept", "y:Kept", "y:Kept", "y:Kept"),
    ("Due dates", "y:Kept (date only)", "y:Kept", "y:Deadline", "y:Kept"),
    ("Reminder times", "Written into notes", "y:Kept", "y:“When” + time", "y:Kept"),
    ("Repeating tasks", "Written into notes", "Written into notes", "Written into notes", "y:Kept as text + rule"),
    ("Important / flagged", "Noted with ★", "y:Flag + priority", "y:“Important” tag", "y:Kept"),
    ("Completed tasks", "y:Marked done", "y:Marked done", "y:Logged", "y:Kept with date"),
    ("File attachments", "n:Not moved", "n:Not moved", "n:Not moved", "n:Listed only"),
]

def compare_table():
    def cell(v):
        if v.startswith("y:"): return f'<td class="y">✓ {v[2:]}</td>'
        if v.startswith("n:"): return f'<td class="n">{v[2:]}</td>'
        return f"<td>{v}</td>"
    head = "".join(f'<th scope="col">{h}</th>' for h in COMPARE_HEAD)
    body = "".join(f'<tr><th scope="row">{r[0]}</th>{"".join(cell(v) for v in r[1:])}</tr>' for r in COMPARE_ROWS)
    return f'<div style="overflow-x:auto"><table class="cmp"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div><p style="font-size:14.5px;color:#5b6478">Google Tasks, Apple Reminders and Things can’t take a repeat rule through an import, so MoveMyTodo writes it into the task’s notes (for example “Repeats: Every 2 weeks on Mon”) and you set it again in two taps. Checked {CHECKED}.</p>'

QA = {
    "when": ("When is Microsoft To Do shutting down?",
             "Microsoft To Do stops working on June 30, 2027, on the web, Windows, Mac, iPhone and Android. Microsoft announced it on November 18, 2026. Personal accounts get no replacement; work and school accounts are pointed to Planner."),
    "migrate": ("Will my To Do tasks move to Planner or another app automatically?",
                "No. Microsoft says existing To Do tasks and lists will not migrate to Planner, and personal accounts can't use Planner at all. You have to export or move them yourself before June 30, 2027."),
    "export": ("How do I export Microsoft To Do?",
               f"Sign in to MoveMyTodo with your Microsoft account and download a free backup as CSV (opens in Excel and Google Sheets), Markdown, JSON or a printable page. Microsoft's own export isn't available yet as of {CHECKED}."),
    "excel": ("Can you export a Microsoft To Do list to Excel?",
              "Yes. MoveMyTodo downloads every Microsoft To Do list as a free CSV file that opens in Excel or Google Sheets, with one row per task and columns for list, title, status, due date, reminder, repeats, steps and notes."),
    "account": ("Can I move Microsoft To Do lists to another Microsoft account?",
                "It wouldn't help for long: Microsoft To Do retires on June 30, 2027 for every account, so a second Microsoft account loses it on the same day. Download a free CSV backup of your lists and take them to the app you'll use next."),
    "google": ("Can I move Microsoft To Do to Google Tasks?",
               "Yes. MoveMyTodo signs in to Google Tasks with your permission and creates a list for each To Do list, with steps as subtasks, notes, due dates and completed tasks. Google Tasks has no import button of its own." + (" Until Google finishes reviewing MoveMyTodo, Google shows an extra “Google hasn't verified this app” screen first; choose Advanced there to continue." if GOOGLE_REVIEW else "")),
    "apple": ("Can I move Microsoft To Do to Apple Reminders?",
              "Yes, on a Mac: MoveMyTodo makes an import file that adds a Reminders list for each To Do list, with notes, due dates, reminder times and flags, and iCloud syncs it to your iPhone. Without a Mac, see the free iPhone method in our Apple Reminders guide."),
    "safe": ("Is it safe to sign in? What can MoveMyTodo see?",
             "MoveMyTodo asks Microsoft for read-only access to your tasks, so it cannot change or delete anything in To Do. Your tasks are read straight into your browser tab and are never sent to or stored on our servers. Close the tab and they're gone."),
    "cost": ("Is MoveMyTodo free?",
             (f"Scanning, the full backup (CSV, Markdown, JSON, printable) and Todoist files are free with no limits. Moving to Apple Reminders or Things is free for up to {FREE_N} tasks from one list; MoveMyTodo Pro moves everything, including to Google Tasks, for ${PRICE} once. {GOOGLE_NOTE}" if GOOGLE_REVIEW else
              f"Scanning and the full backup (CSV, Markdown, JSON, printable) are free with no limits. Moving to Google Tasks, Apple Reminders or Things is free for up to {FREE_N} tasks from one list; MoveMyTodo Pro moves everything for ${PRICE} once.")),
    "work": ("Does it work with a work or school account?",
             "Often, but not always. Some organisations only let you sign in to apps an admin has approved; if you see an admin-approval message, ask your IT team or use the free backup another way. Personal Microsoft accounts work straight away."),
    "repeat": ("What happens to repeating tasks and reminders?",
               "Due dates move everywhere. Google Tasks, Apple Reminders and Things can't receive a repeat rule through an import, so MoveMyTodo writes it into the task's notes, for example “Repeats: Every month on day 1”, and you set it again in the new app."),
    "todoist": ("What about Todoist or TickTick?",
                "Both have their own free Microsoft To Do importers, so you don't need MoveMyTodo to get there. Todoist's importer (launched November 21, 2026, free on every plan) copies the lists you choose with due dates, reminders and steps; TickTick's is in its web app under Settings → Integrations & Import. MoveMyTodo is for the apps without an importer: Google Tasks, Apple Reminders and Things 3. Either way, download the free backup first so you keep a copy you control."),
    "things": ("Can I move Microsoft To Do to Things 3?",
               "Yes. Things 3 has no Microsoft To Do importer, but MoveMyTodo turns each To Do list into a Things project through Things' own link feature: steps become checklist items, due dates become deadlines and categories become tags. Open MoveMyTodo on the Mac, iPhone or iPad where Things is installed and tap the buttons it makes."),
    "best": ("What's the best Microsoft To Do alternative?",
             "It depends on what you need and how much moving you want to do. Todoist and TickTick have their own free importers; Superlist keeps a live sync with To Do; Google Tasks, Apple Reminders and Things 3 are simpler or Apple-only apps without an importer, which is where MoveMyTodo helps. Work and school accounts are pointed to Planner, but tasks aren't copied into it."),
    "deleted": ("Will moving delete anything from To Do?",
                "No. MoveMyTodo only reads To Do, and in the new app it only adds new lists, never changing or deleting the lists you already have there."),
    "planner": ("Can I import Microsoft To Do into Planner?",
                "No. Microsoft says existing To Do tasks and lists will not migrate to Planner, and it hasn't published an import. Work and school accounts can still see old To Do tasks in Planner until June 30, 2027. To keep them after that, download a backup (CSV, Markdown or JSON) and recreate the tasks you still need in Planner. MoveMyTodo can't write to Planner."),
    "planner_see": ("Can I still see my To Do tasks in Planner?",
                    "Yes, until June 30, 2027, for work and school accounts. Microsoft says you can view and manage existing To Do tasks in Planner until then, but not after. Personal Microsoft accounts can't use Planner at all."),
    "todoist_free": ("Does Todoist's Microsoft To Do importer work on the free plan?",
                     "Yes. Todoist says its importer works on every plan, including the free Beginner plan. Each To Do list becomes a Todoist project, and the Beginner plan allows 5 active personal projects, so pick up to 5 lists, merge small ones first, or upgrade. Every Todoist plan allows 300 active tasks per project."),
    "todoist_repeat": ("Do repeating tasks and reminders move to Todoist?",
                       "Mostly. Todoist's importer copies due dates, reminders and steps; a repeating task whose schedule Todoist can't match arrives as a one-time task, and reminders or files over your plan's limits are skipped. Todoist emails a summary of what changed."),
    "after": ("What if I wait until after June 30, 2027?",
              "The apps will be gone, and Microsoft hasn't promised how long the export or API will keep working after that. Back up now; it takes a minute and costs nothing."),
}
HOME_FAQ = ["when", "migrate", "export", "google", "apple", "safe", "cost", "work", "repeat", "todoist", "deleted", "after"]

PAGES = [
  {
    "slug": "microsoft-to-do-to-google-tasks",
    "crumb": "To Do → Google Tasks",
    "title": "Move Microsoft To Do to Google Tasks (Lists, Steps, Dates)",
    "description": "Google Tasks has no import button. Move every Microsoft To Do list to Google Tasks with steps as subtasks, notes and due dates, in about two minutes.",
    "h1": "How to move Microsoft To Do to Google Tasks",
    "answer": "Google Tasks has no import feature, so the only ways across are retyping or a tool that writes through Google's Tasks API. With MoveMyTodo you sign in to Microsoft (read-only), pick your lists, then connect Google Tasks: each To Do list becomes a Google Tasks list, steps become subtasks, and notes, due dates and completed tasks come along.",
    "faq": ["google", "repeat", "safe", "cost"],
    "links": ["microsoft-to-do-to-apple-reminders", "export-microsoft-to-do", "microsoft-to-do-shutting-down"],
    "body": """
<h2>Steps</h2>
<ol>
<li>On <a href="/#app">MoveMyTodo</a>, click <b>Sign in with Microsoft</b> and use the account you use for To Do. Microsoft asks you to allow <i>read</i> access to your tasks.</li>
<li>Check the numbers (lists, tasks, steps) and untick any lists you don't want. Download the free CSV backup while you're there.</li>
<li>In <b>Move to your new app</b>, choose <b>Google Tasks</b> and click <b>Connect Google Tasks &amp; move</b>.</li>
<li>Pick your Google account and allow access to Google Tasks. """ + ("""While Google's review of MoveMyTodo isn't finished, Google first shows an extra screen saying “Google hasn't verified this app”; choose <b>Advanced</b> there to continue. """ if GOOGLE_REVIEW else "") + """The lists appear in Google Tasks as they're written; a big account takes a few minutes.</li>
<li>Open <a href="https://tasks.google.com/">tasks.google.com</a>, Gmail's side panel or the Google Tasks app to check them.</li>
</ol>
<h2>What carries over</h2>
<table class="facts"><caption>Microsoft To Do → Google Tasks</caption>
<tr><th scope="row">Lists</th><td>A new Google Tasks list for each To Do list. If you already have a list with the same name, the new one is called “… (from To Do)”.</td></tr>
<tr><th scope="row">Steps</th><td>Become subtasks (Google Tasks allows one level), ticked if they were done.</td></tr>
<tr><th scope="row">Notes and links</th><td>Copied into the task's details. Google allows about 8,000 characters per note.</td></tr>
<tr><th scope="row">Due dates</th><td>Copied. Google Tasks stores a date, not a time.</td></tr>
<tr><th scope="row">Reminders and repeats</th><td>Written into the notes (“Reminder: 2026-12-03 09:00”, “Repeats: Every month on day 1”). Google's Tasks API can't set them, so add them again for the tasks that need them.</td></tr>
<tr><th scope="row">Completed tasks</th><td>Optional. Moved as completed, under “Completed” in each list.</td></tr>
<tr><th scope="row">Order</th><td>Kept: open tasks first, in To Do's order.</td></tr>
</table>
<h2>Without a tool</h2>
<p>For a few tasks, retyping is fine. For more, there's no file you can upload to Google Tasks: it has no import menu, and Google Calendar's import creates events, not tasks. Automation services such as Zapier only copy <i>new</i> tasks as they're created, not the ones you already have.</p>
"""
  },
  {
    "slug": "microsoft-to-do-to-apple-reminders",
    "crumb": "To Do → Apple Reminders",
    "title": "Move Microsoft To Do to Apple Reminders (Mac & iPhone)",
    "description": "Move Microsoft To Do lists into Apple Reminders with notes, due dates and reminder times. A one-command Mac import, plus a free method for iPhone.",
    "h1": "How to move Microsoft To Do to Apple Reminders",
    "answer": "Apple Reminders has no import button, but a Mac can add reminders from a script. MoveMyTodo reads your To Do lists (read-only) and gives you an import file; one Terminal command adds a Reminders list for each To Do list, with notes, due dates, reminder times and flags, and iCloud syncs them to your iPhone and iPad.",
    "faq": ["apple", "repeat", "deleted", "cost"],
    "links": ["microsoft-to-do-to-google-tasks", "export-microsoft-to-do", "microsoft-to-do-shutting-down"],
    "body": """
<h2>On a Mac</h2>
<ol>
<li>On <a href="/#app">MoveMyTodo</a>, sign in with Microsoft and pick your lists.</li>
<li>Open the <b>Apple Reminders</b> tab and click <b>Download the Reminders import file</b>. It saves <code>import-to-reminders.js</code> to Downloads.</li>
<li>Open Terminal (⌘ Space, type “Terminal”) and run:<pre><code>osascript -l JavaScript ~/Downloads/import-to-reminders.js</code></pre></li>
<li>Allow Terminal to control Reminders when macOS asks. When it prints “Done: added … reminders”, open Reminders.</li>
</ol>
<p>The script only adds new lists. If you already have a Reminders list with the same name, the new one is called “… (To Do)”. Make sure iCloud is turned on for Reminders (System Settings → your name → iCloud) so the lists reach your iPhone.</p>
<h2>What carries over</h2>
<table class="facts"><caption>Microsoft To Do → Apple Reminders</caption>
<tr><th scope="row">Lists</th><td>A new Reminders list for each To Do list.</td></tr>
<tr><th scope="row">Notes, links</th><td>Copied into the reminder's notes.</td></tr>
<tr><th scope="row">Due dates and reminders</th><td>Due dates become all-day due dates; reminder times become alerts.</td></tr>
<tr><th scope="row">Important</th><td>Flagged, with high priority.</td></tr>
<tr><th scope="row">Steps</th><td>Listed in the notes as a checklist (“◻︎ Passport”). Apple's scripting interface can't create subtasks.</td></tr>
<tr><th scope="row">Repeats</th><td>Written into the notes; set them again in Reminders.</td></tr>
<tr><th scope="row">Completed tasks</th><td>Optional; added and marked completed.</td></tr>
</table>
<h2 id="iphone">On an iPhone or iPad, without a Mac</h2>
<p>There's a free route that uses Apple's own Exchange support, while To Do still works:</p>
<ol>
<li>On the iPhone, open <b>Settings → Apps → Reminders → Reminders Accounts → Add Account</b> (on older iOS: Settings → Mail → Accounts → Add Account) and choose <b>Outlook.com</b>. Sign in with your To Do account and turn on <b>Reminders</b>.</li>
<li>Open Reminders. Your To Do lists appear under the Outlook account.</li>
<li>Open each list, tap <b>⋯ → Select Reminders</b>, select all, tap the folder icon and move them to an <b>iCloud</b> list.</li>
</ol>
<p>Limits: To Do's steps, file attachments and some repeat rules don't come through this way, and anything left in the Outlook account disappears when To Do's service is switched off. Download the <a href="/#backup">free backup</a> first so you keep a full copy.</p>
"""
  },
  {
    "slug": "export-microsoft-to-do",
    "crumb": "Export To Do",
    "title": "How to Export Microsoft To Do to Excel, CSV or PDF (Free)",
    "description": "Microsoft To Do has no export button and Microsoft's promised export isn't out yet. Download every list, step and due date as CSV, Markdown, JSON or a printable page.",
    "h1": "How to export Microsoft To Do (free)",
    "answer": f"Microsoft To Do has no export button, and the export Microsoft promised before the June 30, 2027 shutdown isn't available yet (checked {CHECKED}). MoveMyTodo reads your lists through Microsoft's official API, read-only, and downloads them for free as CSV for Excel or Google Sheets, Markdown, JSON or a printable page, including steps, notes, due dates, reminders and repeat rules.",
    "faq": ["export", "excel", "account", "safe", "after", "work"],
    "links": ["microsoft-to-do-shutting-down", "microsoft-to-do-to-google-tasks", "microsoft-to-do-to-apple-reminders"],
    "body": """
<h2>Steps</h2>
<ol>
<li>Go to <a href="/#app">MoveMyTodo</a> and click <b>Sign in with Microsoft</b>.</li>
<li>Allow read access to your tasks. Your lists load into the page.</li>
<li>Untick lists you don't need and choose whether to include completed tasks.</li>
<li>Click <b>CSV for Excel / Sheets</b>, <b>Markdown</b>, <b>JSON</b> or <b>Printable page</b>. For a PDF, open the printable page and print it to PDF.</li>
</ol>
<h2>What's in the export</h2>
<table class="facts"><caption>Columns in the CSV</caption>
<tr><th scope="row">List, Title, Status</th><td>One row per task, open or completed.</td></tr>
<tr><th scope="row">Due date, Reminder, Repeats</th><td>Due day, reminder time with your time zone, and the repeat rule in words (the JSON also has it as an iCalendar RRULE).</td></tr>
<tr><th scope="row">Steps</th><td>All steps in one cell, ticked or not, plus a “2/5 done” count.</td></tr>
<tr><th scope="row">Notes, Categories, Links</th><td>As in To Do. Formatting is turned into plain text.</td></tr>
<tr><th scope="row">Created, Completed</th><td>Dates for your own records.</td></tr>
</table>
<p>File attachments aren't downloaded; the export marks which tasks have them so you can save those files from To Do.</p>
<h2>Other ways to export</h2>
<table class="cmp"><thead><tr><th scope="col">Method</th><th scope="col">Gets</th><th scope="col">Good for</th></tr></thead><tbody>
<tr><th scope="row">MoveMyTodo (this site)</th><td>Every list, step, note, date and repeat rule</td><td>Anyone; runs in the browser</td></tr>
<tr><th scope="row">Classic Outlook for Windows → Export to .pst</th><td>Tasks folders inside a mailbox file</td><td>Windows users with classic Outlook; not a spreadsheet</td></tr>
<tr><th scope="row">Open-source command-line exporters</th><td>JSON or CSV</td><td>People comfortable registering an app and running scripts</td></tr>
<tr><th scope="row">Microsoft's own export</th><td>Not available yet</td><td>Waiting; format unknown</td></tr>
<tr><th scope="row">Copy or print each list</th><td>Titles only</td><td>A handful of tasks</td></tr>
</tbody></table>
<h2 id="official-export">When Microsoft's own export arrives</h2>
<p>Microsoft says it will offer a way to export To Do data before June 30, 2027, but it hasn't said when, what format it will use or what it includes (checked """ + CHECKED + """). It has also said an export doesn't mean another app can import it. When it ships, we'll test it and update this page with what it contains, and add a way to move that file to Google Tasks, Apple Reminders or Things 3. Until then, a backup you make today is the safe option.</p>
"""
  },
  {
    "slug": "microsoft-to-do-shutting-down",
    "crumb": "To Do shutdown",
    "title": "Microsoft To Do Shutting Down June 30, 2027: What to Do",
    "description": "Microsoft To Do retires June 30, 2027 and nothing migrates automatically. Key dates, what happens to your tasks, and how to back up and move them.",
    "h1": "Microsoft To Do is shutting down: what to do now",
    "answer": "Microsoft To Do retires on June 30, 2027, on every platform. Personal accounts get no replacement and work or school accounts are pointed to Planner, but existing To Do tasks aren't moved anywhere. Back up your lists now, pick a new app, and move them while To Do still works.",
    "faq": ["when", "migrate", "after", "todoist"],
    "links": ["export-microsoft-to-do", "microsoft-to-do-to-planner", "microsoft-to-do-to-google-tasks", "microsoft-to-do-to-apple-reminders"],
    "body": """
<h2>Key facts</h2>
{FACTS}
<h2>What to do, in order</h2>
<ol>
<li><b>Back up today.</b> A <a href="/export-microsoft-to-do/">free export</a> takes a minute and protects you whatever happens to Microsoft's own export.</li>
<li><b>Pick your new app.</b> Google Tasks if you live in Gmail or Android; Apple Reminders if you're on iPhone and Mac; Todoist or TickTick for more power. See <a href="/#compare">what moves to each</a>.</li>
<li><b>Move your lists.</b> <a href="/microsoft-to-do-to-google-tasks/">To Google Tasks</a>, <a href="/microsoft-to-do-to-apple-reminders/">to Apple Reminders</a> or <a href="/microsoft-to-do-to-things-3/">to Things 3</a> with MoveMyTodo. Todoist and TickTick have their own free importers; see <a href="/microsoft-to-do-alternatives/">where each app stands</a>.</li>
<li><b>Set repeats and shared lists again.</b> Repeating tasks keep their rule in the notes; shared lists need re-sharing in the new app.</li>
<li><b>Keep To Do until you're happy.</b> Nothing is deleted when you move; check the new app for a week, then stop using To Do.</li>
</ol>
<h2>Work and school accounts</h2>
<p>Planner's new “My tasks” page starts rolling out in December 2026 and will hold new private tasks. Your old To Do tasks stay visible in Planner until June 30, 2027 but are not copied into it, so export anything you want to keep. If your organisation requires admin approval for apps, ask IT before using any third-party tool. More detail: <a href="/microsoft-to-do-to-planner/">what moves from To Do to Planner</a>.</p>
<h2 id="updates">Updates</h2>
{CHANGELOG}
"""
  },
  {
    "slug": "microsoft-to-do-to-things-3",
    "crumb": "To Do → Things 3",
    "title": "How to Move Microsoft To Do to Things 3 (Lists, Steps, Due Dates)",
    "description": "Things 3 can't import Microsoft To Do. Move each To Do list into a Things project with steps as checklist items, due dates as deadlines and notes intact, on Mac, iPhone or iPad.",
    "h1": "How to move Microsoft To Do to Things 3",
    "answer": "Things 3 has no Microsoft To Do importer. MoveMyTodo reads your To Do lists (read-only) and hands them to Things through Things' own link feature, so each list becomes a Things project with its tasks, steps as checklist items, notes, due dates as deadlines, reminder times and categories as tags. It works on the Mac, iPhone or iPad where Things is installed.",
    "faq": ["things", "repeat", "safe", "cost"],
    "links": ["microsoft-to-do-alternatives", "microsoft-to-do-to-apple-reminders", "export-microsoft-to-do"],
    "body": """
<h2>Steps</h2>
<ol>
<li>On the device where Things is installed, open <a href="/#app">MoveMyTodo</a> and click <b>Sign in with Microsoft</b>. Allow read access to your tasks.</li>
<li>Untick any lists you don't want and download the free backup while you're there.</li>
<li>In <b>Move to your new app</b>, choose <b>Things 3</b> and click <b>Make my Things buttons</b>. You get one button per list (big lists are split into parts of 40 tasks).</li>
<li>Tap the first button. Things opens and asks whether to enable Things URLs; choose <b>Enable</b>. The list arrives as a new project.</li>
<li>Go back to the page and tap the next button. Wait for Things to finish each one before tapping the next.</li>
</ol>
<p>If nothing happens when you tap a button, check the setting in Things: on a Mac, <b>Things → Settings → General → Enable Things URLs</b>; on iPhone or iPad, <b>Settings → General → Things URLs</b>.</p>
<h2>What moves</h2>
<table class="facts"><caption>Microsoft To Do → Things 3</caption>
<tr><th scope="row">Lists</th><td>A new Things project for each list. Nothing already in Things is changed.</td></tr>
<tr><th scope="row">Steps</th><td>Checklist items inside the to-do, ticked or not.</td></tr>
<tr><th scope="row">Due dates and reminders</th><td>Due date becomes the deadline; a reminder becomes “When” with the same time.</td></tr>
<tr><th scope="row">Notes, links, categories</th><td>Notes and links are kept; categories become tags; Important becomes an “Important” tag.</td></tr>
<tr><th scope="row">Completed tasks</th><td>Added as completed, so they go to the Logbook.</td></tr>
<tr><th scope="row">Repeating tasks</th><td>The rule is written into the notes (for example “Repeats: Every week on Thu”); set it again in Things.</td></tr>
<tr><th scope="row">File attachments</th><td>Not moved. Save them from To Do first.</td></tr>
</table>
<h2>The other route: through Apple Reminders</h2>
<p>Things can import from Apple Reminders (on a Mac: <b>File → Import → Import From Reminders</b>), so another way is To Do → Reminders → Things. It works, but it's two hops, and Things doesn't import lists that sit inside Reminders groups, so drag those out first. Things' own help page explains the import. Moving straight from To Do keeps steps as checklists, which the Reminders route loses.</p>
<h2>Before you start</h2>
<ul>
<li>Things is a paid app for Mac, iPhone and iPad and syncs through its own Things Cloud. You need it installed on the device you use for the move.</li>
<li>You can try one list of up to 25 tasks for free. Moving all your lists is part of MoveMyTodo Pro.</li>
<li>To Do keeps your tasks until you stop using it, so you can compare both apps for a while.</li>
</ul>
"""
  },
  {
    "slug": "microsoft-to-do-alternatives",
    "crumb": "To Do alternatives",
    "title": "Microsoft To Do Alternatives: Where to Go and How Your Tasks Get There",
    "description": "Microsoft To Do retires June 30, 2027. Compare Todoist, TickTick, Superlist, Google Tasks, Apple Reminders, Things 3 and Planner by how your existing lists get there.",
    "h1": "Microsoft To Do alternatives, compared by how your tasks get there",
    "answer": "Every to-do app can replace Microsoft To Do; the hard part is bringing years of lists with you. Todoist and TickTick have free To Do importers and Superlist can sync with To Do, while Google Tasks, Apple Reminders and Things 3 have no importer, which is the gap MoveMyTodo fills. Work and school accounts are pointed to Planner, but existing tasks aren't copied into it.",
    "faq": ["best", "migrate", "todoist", "after"],
    "links": ["microsoft-to-do-shutting-down", "microsoft-to-do-to-todoist", "microsoft-to-do-to-planner", "microsoft-to-do-to-google-tasks", "microsoft-to-do-to-things-3"],
    "body": """
<h2>How your lists get to each app</h2>
<div style="overflow-x:auto"><table class="cmp"><thead><tr><th scope="col">App</th><th scope="col">How To Do lists get there</th><th scope="col">Good fit if you</th></tr></thead><tbody>
<tr><th scope="row">Todoist</th><td>Its own free importer (since November 21, 2026): pick lists, and due dates, reminders and steps come along. <a href="/microsoft-to-do-to-todoist/">Step by step</a>.</td><td>Want natural-language dates, filters and apps everywhere.</td></tr>
<tr><th scope="row">TickTick</th><td>Its own importer in the web app: Settings → Integrations &amp; Import → Microsoft To Do.</td><td>Want a calendar view, habits and a timer in one app.</td></tr>
<tr><th scope="row">Superlist</th><td>A live two-way sync with To Do for the lists you choose (titles, completion and due dates).</td><td>Liked Wunderlist; it's made by Wunderlist's original team.</td></tr>
<tr><th scope="row">Google Tasks</th><td>No importer. <a href="/microsoft-to-do-to-google-tasks/">MoveMyTodo</a> writes your lists through Google's Tasks API.</td><td>Live in Gmail, Google Calendar or Android and want it free and simple.</td></tr>
<tr><th scope="row">Apple Reminders</th><td>No importer. <a href="/microsoft-to-do-to-apple-reminders/">MoveMyTodo</a> makes a Mac import file; on iPhone there's a free route through an Outlook account.</td><td>Use iPhone, iPad and Mac and want it free and built in.</td></tr>
<tr><th scope="row">Things 3</th><td>No To Do importer. <a href="/microsoft-to-do-to-things-3/">MoveMyTodo</a> sends lists to Things as projects; or go through Reminders.</td><td>Are on Apple devices and want a carefully designed paid app.</td></tr>
<tr><th scope="row">Microsoft Planner</th><td>Work and school accounts only. Existing To Do tasks are not copied in; they stay visible in Planner until June 30, 2027. <a href="/microsoft-to-do-to-planner/">What moves</a>.</td><td>Have a work account and your organisation uses Planner.</td></tr>
<tr><th scope="row">Notion, Excel, Obsidian</th><td>Import the free CSV or Markdown <a href="/export-microsoft-to-do/">backup</a>.</td><td>Want tasks inside notes or a spreadsheet.</td></tr>
</tbody></table></div>
<p>Checked """ + CHECKED + """. Apps change their import options; check the app's own help pages before you rely on one.</p>
<h2>Three questions to decide</h2>
<ol>
<li><b>Which devices do you use?</b> Only Apple devices: Reminders or Things. Android or Windows too: Google Tasks, Todoist or TickTick.</li>
<li><b>Do you share lists?</b> Shared lists don't move as shared with any method; you re-share them in the new app. Check that it supports sharing the way your family or team needs before you move.</li>
<li><b>Free or paid?</b> Google Tasks and Reminders are free. Todoist and TickTick have free plans with limits. Things is a one-time purchase per device.</li>
</ol>
<h2>Whichever you choose</h2>
<p>Download a <a href="/export-microsoft-to-do/">free backup</a> first, so you keep a copy that doesn't depend on Microsoft or the new app. Then move, and keep To Do for a week or two until you're sure everything arrived.</p>
"""
  },
{
    "slug": "microsoft-to-do-to-planner",
    "crumb": "To Do → Planner",
    "title": "Microsoft To Do to Planner: What Moves and What Doesn't (2027)",
    "description": "Microsoft points work and school To Do users to Planner, but existing tasks don't migrate. What Planner shows until June 30, 2027, what's missing, and how to keep your lists.",
    "h1": "Microsoft To Do to Planner: what moves and what doesn't",
    "answer": "Microsoft To Do tasks do not migrate to Microsoft Planner. Microsoft says work and school accounts can view existing To Do tasks in Planner until June 30, 2027, and not after. To keep them, download a backup of your lists and recreate the tasks you still need in Planner. Personal Microsoft accounts can't use Planner.",
    "faq": ["planner", "planner_see", "work", "export"],
    "links": ["microsoft-to-do-shutting-down", "export-microsoft-to-do", "microsoft-to-do-alternatives"],
    "body": """
<h2>What Microsoft says happens</h2>
<table class="facts"><caption>Microsoft To Do → Planner, work and school accounts (checked """ + CHECKED + """)</caption>
<tr><th scope="row">Existing tasks and lists</th><td><b>Not migrated.</b> They stay visible and editable in Planner until June 30, 2027, then you can no longer view or manage them there.</td></tr>
<tr><th scope="row">New private tasks</th><td>Go into a redesigned Planner “My tasks” page (a list view with stars and a separate “Assigned to me” view), rolling out from December 2026.</td></tr>
<tr><th scope="row">Shared lists</th><td>Membership, assignments and permissions don't transfer.</td></tr>
<tr><th scope="row">Reminders</th><td>Planner sends due-date notifications, not To Do's per-task reminder times.</td></tr>
<tr><th scope="row">List groups</th><td>No direct Planner equivalent.</td></tr>
<tr><th scope="row">File attachments</th><td>Not supported on tasks in the new private Planner plan.</td></tr>
<tr><th scope="row">Desktop apps and offline</th><td>No native Planner app for Windows or Mac is planned; Planner runs on the web and in Teams, without equivalent offline use.</td></tr>
<tr><th scope="row">Access</th><td>Depends on your organisation's subscription, your license and admin settings. If Planner is turned off, your admin has to enable it.</td></tr>
<tr><th scope="row">Classic Outlook Tasks</th><td>A separate feature; Microsoft says it keeps working and syncing with Exchange.</td></tr>
</table>
<p class="src">Source: <a href="https://support.microsoft.com/en-us/planner/to-do-to-planner">Microsoft Support, “Moving from Microsoft To Do to Microsoft Planner”</a>. Microsoft hasn't said whether My tasks will have steps, repeating tasks or notes like To Do.</p>
<h2>How to keep your To Do lists</h2>
<ol>
<li><b>Back up everything now.</b> Sign in to <a href="/#app">MoveMyTodo</a> with your work account (read-only) and download the free CSV, Markdown or JSON backup. If you see an admin-approval message, your organisation blocks third-party apps; ask IT, and wait for Microsoft's own export.</li>
<li><b>Sort out what's still live.</b> Open the CSV in Excel and filter to open tasks. Most people carry over far fewer tasks than they have.</li>
<li><b>Recreate those tasks in Planner's My tasks.</b> Microsoft hasn't published a way to import To Do lists into Planner, and MoveMyTodo can't write to Planner.</li>
<li><b>Keep the backup.</b> Completed tasks, notes and old lists stay readable in the file after June 30, 2027.</li>
</ol>
<h2>Personal tasks in a work account?</h2>
<p>If you keep personal lists (groceries, travel) in your work account, consider moving those to a personal app instead, so they don't stay with your employer: <a href="/microsoft-to-do-to-google-tasks/">Google Tasks</a>, <a href="/microsoft-to-do-to-apple-reminders/">Apple Reminders</a>, <a href="/microsoft-to-do-to-things-3/">Things 3</a> or <a href="/microsoft-to-do-to-todoist/">Todoist</a>. If you use both a work and a personal Microsoft account, review each one separately.</p>
"""
  },
  {
    "slug": "microsoft-to-do-to-todoist",
    "crumb": "To Do → Todoist",
    "title": "How to Move Microsoft To Do to Todoist (Free Importer, 2026)",
    "description": "Todoist has a free Microsoft To Do importer on every plan. Step by step, what carries over, the 5-project limit on the free plan, and what to do if the importer doesn't fit.",
    "h1": "How to move Microsoft To Do to Todoist",
    "answer": "Todoist has its own free Microsoft To Do importer, launched November 21, 2026, and it works on every Todoist plan, including the free Beginner plan. You sign in to Microsoft with read-only access, choose lists, and each list becomes a Todoist project with its tasks, due dates, reminders and steps. On the free plan you can have 5 active personal projects.",
    "faq": ["todoist_free", "todoist_repeat", "todoist", "export"],
    "links": ["microsoft-to-do-alternatives", "export-microsoft-to-do", "microsoft-to-do-shutting-down"],
    "body": """
<h2>Steps</h2>
<ol>
<li><b>Back up first.</b> Download a free <a href="/export-microsoft-to-do/">backup of all your lists</a> (CSV, Markdown or JSON), so you keep a copy that doesn't depend on either app.</li>
<li>Open <a href="https://www.todoist.com/importer/microsoft-todo">Todoist's Microsoft To Do importer</a> and sign in to Todoist, or create a free account.</li>
<li>Sign in with Microsoft. Todoist gets read-only access to your To Do lists.</li>
<li>Choose one list to test, or several at once. Todoist shows how many new projects it needs before copying starts.</li>
<li>Start the import. It runs in the background, usually takes a few minutes, and Todoist emails you a summary when it's done.</li>
</ol>
<h2>What carries over</h2>
<table class="facts"><caption>Microsoft To Do → Todoist, according to Todoist (checked """ + CHECKED + """)</caption>
<tr><th scope="row">Lists</th><td>A new Todoist project for each list.</td></tr>
<tr><th scope="row">Tasks and steps</th><td>Copied as tasks, with steps.</td></tr>
<tr><th scope="row">Due dates and reminders</th><td>Copied. Reminders over your plan's limits are skipped.</td></tr>
<tr><th scope="row">Repeating tasks</th><td>Copied with their schedule when Todoist can match it; otherwise as a one-time task.</td></tr>
<tr><th scope="row">Files</th><td>Copied within your plan's file limits.</td></tr>
<tr><th scope="row">Shared lists</th><td>Copied, but nobody is invited to Todoist; share the project again.</td></tr>
<tr><th scope="row">Your To Do lists</th><td>Not changed. Todoist only reads them and disconnects when the import finishes.</td></tr>
</table>
<p class="src">Source: <a href="https://www.todoist.com/importer/microsoft-todo">Todoist's Microsoft To Do importer page</a> and Todoist's usage-limits help page. Importing the same list twice creates duplicate tasks.</p>
<h2>Free plan limits to plan around</h2>
<ul>
<li><b>5 active personal projects</b> on the free Beginner plan (300 on Pro). With more than 5 To Do lists, merge small lists in To Do first, import your 5 most important lists, archive old projects, or upgrade.</li>
<li><b>300 active tasks per project</b> on every plan. Completed tasks don't count toward it.</li>
</ul>
<h2>If the importer doesn't fit</h2>
<p>If your organisation blocks the Todoist app on your work account, or you'd rather not connect Todoist to your Microsoft account, <a href="/#app">MoveMyTodo</a> makes a Todoist CSV file for each list, free. In Todoist, open a project, choose <b>Import from CSV</b> from the project menu, and pick the file.</p>
"""
  },
]

# Who MoveMyTodo is for, and who should use something else. Plain statements, shown on /about/ and in llms.txt.
BEST_FOR = [
    "People with a personal Microsoft account (Outlook.com, Hotmail, Live, Microsoft 365 Personal or Family) who are moving to Google Tasks, Apple Reminders or Things 3, which have no Microsoft To Do importer of their own.",
    "Anyone who wants a complete, free backup of their To Do lists (CSV, Markdown, JSON or a printable page) before June 30, 2027, whichever app they pick next.",
    "People who want lists, steps, notes, due dates and completed tasks to arrive in the right lists, not retyped by hand.",
]
NOT_FOR = [
    "Moving to Todoist or TickTick: both have free built-in Microsoft To Do importers, so MoveMyTodo isn't needed.",
    "Most work or school accounts right now: many organizations block sign-in to apps from unverified publishers, including MoveMyTodo. Ask your IT admin, or use Planner, which Microsoft provides for those accounts.",
    "Keeping To Do and another app in live two-way sync: MoveMyTodo copies once. File attachments aren't moved either; save them from To Do first.",
]

