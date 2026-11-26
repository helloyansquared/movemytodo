# MoveMyTodo

**Microsoft To Do shuts down on June 30, 2027, and nothing moves on its own.** MoveMyTodo signs in to Microsoft with read-only access, shows every list and task, downloads a free backup, and moves your lists, steps, notes and due dates to Google Tasks, Apple Reminders, Things 3 or Todoist.

Live: **https://movemytodo.com/**

## What it does

| | |
|---|---|
| Read | Microsoft Graph `Tasks.Read` (delegated, read-only), authorization code + PKCE from the browser. The token lives only in the tab's memory. |
| Free backup | CSV (Excel / Google Sheets), Markdown, JSON (with iCalendar RRULEs), printable HTML |
| Google Tasks | Writes through the Google Tasks API: one list per To Do list, steps → subtasks, notes, due dates, completed tasks |
| Apple Reminders | A JavaScript-for-Automation script for macOS (`osascript -l JavaScript …`): lists, notes, due dates, reminder times, flags |
| Things 3 | `things:///json` links: projects, checklist items, deadlines, tags |
| Todoist | Todoist CSV import files, one per list |

Your tasks are never sent to or stored on MoveMyTodo's servers. The only server code is `functions/api/license.js`, which checks Pro license keys with Dodo Payments.

## Develop

```sh
node test/core.test.js
python3 build.py https://movemytodo.com/ --ms <entra-client-id> --google <google-client-id> --product <dodo-product-id>
```

Page copy lives in `src/content.py`; the app is `src/index.html` + `public/core.js`. Output goes to `public/` (deployed by Cloudflare Pages).

Not affiliated with Microsoft, Google, Apple or Cultured Code. Microsoft To Do is a trademark of Microsoft Corporation. MIT licensed. Contact: hello@yansquared.com
