# Google OAuth verification — MoveMyTodo

Project: `movemytodo` · OAuth client `26189746666-r713cmmndeb2o79sm3ia2s89e1tivmm5.apps.googleusercontent.com`
App name: **MoveMyTodo** · Home: https://movemytodo.com/ · Privacy: https://movemytodo.com/privacy/ · Terms: https://movemytodo.com/terms/
Authorized domain: movemytodo.com (verified in Search Console as a Domain property by the project owner)
Support / developer contact: yanyan.wang@yansquared.com
Scope requested: `https://www.googleapis.com/auth/tasks` (sensitive). No other Google scopes.

## Scope justification (paste into "How will the scopes be used?"; ~950 characters)

MoveMyTodo copies the task lists a user selects from Microsoft To Do into Google Tasks. Google Tasks has no import feature, so the lists can only be created through the Google Tasks API.

When the user clicks "Connect Google Tasks & move", MoveMyTodo requests https://www.googleapis.com/auth/tasks and then:
1. tasklists.list: reads the names of existing task lists so a new list never duplicates a name;
2. tasklists.insert: creates one new list per selected To Do list;
3. tasks.insert: creates each task (title, notes, due date, completed status) in order, with To Do steps as subtasks.

tasks.readonly cannot create lists or tasks, and there is no narrower write scope. MoveMyTodo never reads existing tasks' contents and never updates or deletes anything.

Everything runs in the user's browser. The token and data stay in the tab's memory and are discarded when it closes. No server of ours receives Google user data; no storage, sharing, ads or AI training.

## Additional information for reviewers (paste into the notes field)

Demo video: recorded on the live domain as a sequence of unedited full-screen screenshots, on the test route https://movemytodo.com/?review-demo. That route uses the same OAuth client ID and the same single scope (https://www.googleapis.com/auth/tasks) as production; the only differences are sample To Do data instead of a Microsoft sign-in, and a same-tab Google sign-in (redirect URI https://movemytodo.com/) instead of the Google Identity Services pop-up, so the full client ID is visible in the address bar. The Google account in the video belongs to the project owner's Google Workspace organization, so Google did not show the unverified-app screen for it.

How to test without a Microsoft account or payment:
1. Open https://movemytodo.com/?review-demo (or https://movemytodo.com/ for the production pop-up flow) and click "Try with sample data".
2. Scroll to "Move everything with Pro", paste the reviewer license key REVIEW_KEY_HERE into "Already bought? Paste your license key" and click Activate. (Google Tasks is a paid destination, $6.99 one-time; this key unlocks it for review.)
3. Open the Google Tasks tab, click "Connect Google Tasks & move", sign in and allow access.
4. Check https://tasks.google.com/ for the new lists.
The only server request MoveMyTodo makes is the license-key check with our payment provider (Dodo Payments); it contains no Google user data.

## Demo video script (English UI, 1–2 minutes, upload to YouTube as Unlisted)

Record the browser window (Chrome, English language) including the address bar. Speak or add captions; captions are enough.

1. **0:00** Open https://movemytodo.com/ . Caption: "MoveMyTodo moves Microsoft To Do lists into Google Tasks." Scroll briefly past the hero, show the Privacy link in the footer.
2. **0:10** Click "Sign in with Microsoft", sign in, show the lists and counts that appear (use a test account with 2–3 tasks, one with a step and a due date).
3. **0:25** On camera: scroll to "Move everything with Pro", paste the reviewer key into "Already bought? Paste your license key", click Activate, show "Pro is unlocked". Then open the Google Tasks tab. Caption: "The user chooses to move their lists into Google Tasks." (Use a fresh browser profile or clear the site's data first so Pro isn't already unlocked.)
4. **0:30** Click "Connect Google Tasks & move". In the Google popup:
   - choose the Google account;
   - **click into the popup's address bar and pause so the URL with `client_id=26189746666-r713cmmndeb2o79sm3ia2s89e1tivmm5.apps.googleusercontent.com` is readable.** The popup's address bar usually cuts the URL off: click into it, press End / arrow keys until `client_id=…` is visible, or copy the URL and paste it into a text editor at large font for 3 seconds;
   - set the consent screen language to English (language menu at the bottom-left) if it isn't already;
   - show the consent screen listing the app name MoveMyTodo and the Google Tasks permission ("Create, edit, organize, and delete all your tasks"); (the unverified-app page will appear before it: click Advanced → Go to movemytodo.com; that's expected);
   - click Continue/Allow.
5. **0:55** Back on MoveMyTodo: show the progress and "Done! … are in Google Tasks." Caption: "MoveMyTodo reads list names to avoid duplicates, then creates a new list and its tasks."
6. **1:05** Click "Open Google Tasks →" and show the new list: tasks in order, a subtask, notes, due date, a completed task. Caption: "Nothing is stored on our servers; the token is discarded when the tab closes."
7. **1:20** Open https://movemytodo.com/privacy/#google for 3 seconds. End.

Add English captions (or voice-over) at each step saying what the Tasks permission is used for. A Microsoft test account isn't required in the video: you can use "Try with sample data" instead of signing in with Microsoft.

After recording: delete the test list in Google Tasks and the test tasks in To Do.

## Logo
https://movemytodo.com/logo-120.png (120×120 PNG, original artwork, no Google or Microsoft marks).

## After approval
- Set `GOOGLE_REVIEW = false` in `src/index.html` and `src/content.py`, then `./deploy.sh`, commit, push. That removes the warning copy and gives the free tier Google Tasks again (decide then whether to keep Google as Pro-only).
- Don't change the app name, logo, scopes, domains or client ID while in review or after, without expecting another review.

## While unverified
- 100-user lifetime cap (counts every Google account that has granted access, including our own tests: 1 used on 2026-11-26). Check Google Auth Platform → Audience. At ~80, hide the Google button and tell buyers to use Reminders/Things or wait.
