# Google OAuth verification — MoveMyTodo

Project: `movemytodo` · OAuth client `26189746666-r713cmmndeb2o79sm3ia2s89e1tivmm5.apps.googleusercontent.com`
App name: **MoveMyTodo** · Home: https://movemytodo.com/ · Privacy: https://movemytodo.com/privacy/ · Terms: https://movemytodo.com/terms/
Authorized domain: movemytodo.com (verified in Search Console as a Domain property by the project owner)
Support / developer contact: yanyan.wang@yansquared.com
Scope requested: `https://www.googleapis.com/auth/tasks` (sensitive). No other Google scopes.

## Scope justification (paste into "How will the scopes be used?")

MoveMyTodo helps people move their task lists out of Microsoft To Do, which Microsoft is retiring on June 30, 2027, into Google Tasks. Google Tasks has no import feature, so the only way to copy existing lists in is to create them through the Google Tasks API.

When the user clicks "Connect Google Tasks & move", MoveMyTodo requests https://www.googleapis.com/auth/tasks and then, for each Microsoft To Do list the user selected:
1. calls tasklists.list to read the names of the user's existing task lists, so that a new list never takes the same name as an existing one;
2. calls tasklists.insert to create one new task list;
3. calls tasks.insert to create each task (title, notes, due date, completed status) in the original order, and each To Do "step" as a subtask.

Why a narrower scope is not enough: tasks.readonly cannot create task lists or tasks, and creating them is the whole purpose of the feature. Google Tasks has no narrower write scope. MoveMyTodo does not read the contents of existing tasks and never updates or deletes anything.

Data handling: the app runs entirely in the user's browser (Google Identity Services token client). The access token and task data stay in the tab's memory only and are discarded when the tab is closed. There is no backend that receives Google user data, no database, no logging of it, no sharing with third parties, and no use for advertising or AI/ML training. Our privacy policy (https://movemytodo.com/privacy/#google) discloses this and includes the Limited Use statement.

## Demo video script (English UI, 1–2 minutes, upload to YouTube as Unlisted)

Record the browser window (Chrome, English language) including the address bar. Speak or add captions; captions are enough.

1. **0:00** Open https://movemytodo.com/ . Caption: "MoveMyTodo moves Microsoft To Do lists into Google Tasks." Scroll briefly past the hero, show the Privacy link in the footer.
2. **0:10** Click "Sign in with Microsoft", sign in, show the lists and counts that appear (use a test account with 2–3 tasks, one with a step and a due date).
3. **0:25** Open the Google Tasks tab. Pro must be unlocked on this browser (paste the license key first, off camera is fine). Caption: "The user chooses to move their lists into Google Tasks."
4. **0:30** Click "Connect Google Tasks & move". In the Google popup:
   - choose the Google account;
   - **click into the popup's address bar and pause ~3 seconds so the URL with `client_id=26189746666-r713cmmndeb2o79sm3ia2s89e1tivmm5.apps.googleusercontent.com` is readable** (zoom in if needed);
   - show the consent screen listing the app name MoveMyTodo and the Google Tasks permission ("Create, edit, organize, and delete all your tasks"); (the unverified-app page will appear before it: click Advanced → Go to movemytodo.com; that's expected);
   - click Continue/Allow.
5. **0:55** Back on MoveMyTodo: show the progress and "Done! … are in Google Tasks." Caption: "MoveMyTodo reads list names to avoid duplicates, then creates a new list and its tasks."
6. **1:05** Click "Open Google Tasks →" and show the new list: tasks in order, a subtask, notes, due date, a completed task. Caption: "Nothing is stored on our servers; the token is discarded when the tab closes."
7. **1:20** Optional: open https://movemytodo.com/privacy/#google for 3 seconds. End.

After recording: delete the test list in Google Tasks and the test tasks in To Do.

## Logo
https://movemytodo.com/logo-120.png (120×120 PNG, original artwork, no Google or Microsoft marks).

## After approval
- Set `GOOGLE_REVIEW = false` in `src/index.html` and `src/content.py`, then `./deploy.sh`, commit, push. That removes the warning copy and gives the free tier Google Tasks again (decide then whether to keep Google as Pro-only).
- Don't change the app name, logo, scopes, domains or client ID while in review or after, without expecting another review.

## While unverified
- 100-user lifetime cap (counts every Google account that has granted access, including our own tests: 1 used on 2026-11-26). Check Google Auth Platform → Audience. At ~80, hide the Google button and tell buyers to use Reminders/Things or wait.
