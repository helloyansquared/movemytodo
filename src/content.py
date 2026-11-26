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
    ("What reads To Do today", "Microsoft Graph, the official API that apps like MoveMyTodo use with your permission. It will also be retired later; no date yet."),
]

def facts_table():
    rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in FACTS_ROWS)
    return f'<table class="facts"><caption>Microsoft To Do retirement: key facts (checked {CHECKED})</caption>{rows}</table>'

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
    "google": ("Can I move Microsoft To Do to Google Tasks?",
               "Yes. MoveMyTodo signs in to Google Tasks with your permission and creates a list for each To Do list, with steps as subtasks, notes, due dates and completed tasks. Google Tasks has no import button of its own."),
    "apple": ("Can I move Microsoft To Do to Apple Reminders?",
              "Yes, on a Mac: MoveMyTodo makes an import file that adds a Reminders list for each To Do list, with notes, due dates, reminder times and flags, and iCloud syncs it to your iPhone. Without a Mac, see the free iPhone method in our Apple Reminders guide."),
    "safe": ("Is it safe to sign in? What can MoveMyTodo see?",
             "MoveMyTodo asks Microsoft for read-only access to your tasks, so it cannot change or delete anything in To Do. Your tasks are read straight into your browser tab and are never sent to or stored on our servers. Close the tab and they're gone."),
    "cost": ("Is MoveMyTodo free?",
             f"Scanning and the full backup (CSV, Markdown, JSON, printable) are free with no limits. Moving to Google Tasks, Apple Reminders or Things is free for up to {FREE_N} tasks from one list; MoveMyTodo Pro moves everything for ${PRICE} once."),
    "work": ("Does it work with a work or school account?",
             "Often, but not always. Some organisations only let you sign in to apps an admin has approved; if you see an admin-approval message, ask your IT team or use the free backup another way. Personal Microsoft accounts work straight away."),
    "repeat": ("What happens to repeating tasks and reminders?",
               "Due dates move everywhere. Google Tasks, Apple Reminders and Things can't receive a repeat rule through an import, so MoveMyTodo writes it into the task's notes, for example “Repeats: Every month on day 1”, and you set it again in the new app."),
    "todoist": ("What about Todoist or TickTick?",
                "TickTick has its own Microsoft To Do importer in its web app (Settings → Integrations & Import). For Todoist, MoveMyTodo makes free Todoist CSV files, one per list, that you import into a project. Either way, download the free backup first so you keep a copy you control."),
    "deleted": ("Will moving delete anything from To Do?",
                "No. MoveMyTodo only reads To Do, and in the new app it only adds new lists, never changing or deleting the lists you already have there."),
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
<li>Pick your Google account and allow access to Google Tasks. The lists appear in Google Tasks as they're written; a big account takes a few minutes.</li>
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
    "faq": ["export", "safe", "after", "work"],
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
    "links": ["export-microsoft-to-do", "microsoft-to-do-to-google-tasks", "microsoft-to-do-to-apple-reminders"],
    "body": """
<h2>Key facts</h2>
{FACTS}
<h2>What to do, in order</h2>
<ol>
<li><b>Back up today.</b> A <a href="/export-microsoft-to-do/">free export</a> takes a minute and protects you whatever happens to Microsoft's own export.</li>
<li><b>Pick your new app.</b> Google Tasks if you live in Gmail or Android; Apple Reminders if you're on iPhone and Mac; Todoist or TickTick for more power. See <a href="/#compare">what moves to each</a>.</li>
<li><b>Move your lists.</b> <a href="/microsoft-to-do-to-google-tasks/">To Google Tasks</a>, <a href="/microsoft-to-do-to-apple-reminders/">to Apple Reminders</a> or Things with MoveMyTodo; free Todoist CSV files are on the same page, and TickTick has its own importer.</li>
<li><b>Set repeats and shared lists again.</b> Repeating tasks keep their rule in the notes; shared lists need re-sharing in the new app.</li>
<li><b>Keep To Do until you're happy.</b> Nothing is deleted when you move; check the new app for a week, then stop using To Do.</li>
</ol>
<h2>Work and school accounts</h2>
<p>Planner's new “My tasks” page starts rolling out in December 2026 and will hold new private tasks. Your old To Do tasks stay visible in Planner until June 30, 2027 but are not copied into it, so export anything you want to keep. If your organisation requires admin approval for apps, ask IT before using any third-party tool.</p>
"""
  },
]
