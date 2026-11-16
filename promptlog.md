# Prompt log: 15-114 HW 9

The important prompts I gave **Claude Code** (Claude desktop app, model **Claude Opus 5.5**) while doing HW 9, on 2026-11-15 and 2026-11-16. Each prompt is copied **verbatim**, typos included. Under each one is a short note on what happened.

I left out short replies like "Signed in" or "Commit and push". The older `prompt_log.md` in this repo is from building the original restaurant-recs backend, not this homework.

---

## 1. Finding the code and picking three pieces of logic

### Prompt 1
```text
dont start coding yet but pull up the coee base from hw projhect about the restaraunt chatbopt on my website
```
**What happened:** Claude found the chat's frontend in my portfolio repo (`index.html`, `js/script.js`, `css/style.css`) and cloned the backend repo (`backend-for-restaurant-bot-`) to my Mac. Then it explained how the two fit together. No code was changed.

### Prompt 2
```text
give me a link to find the actual code
```
**What happened:** Claude gave GitHub links to the backend's `app.py` and to the chat code in the portfolio.

### Prompt 3
```text
find 3 pices of real logic in the maincode. d o not changre anything
```
**What happened:** Claude picked three pieces in `app.py`: `match()` (loosening the search), `load_places()` (merging repeat entries) and the check in `extract_filters()` that throws out values not in my list.

### Prompt 4
```text
Write down, for each one, what it is supposed to do and one way it could plausibly be wrong.
```
**What happened:** Claude explained each piece and one way it could go wrong, checking two of them against my Beli data. I used this to write the first part of `testing.md`.

### Prompt 5
```text
create a new repo called "15-114 HW 9" that contains a branch version of the codebase from the restaraunt backend code and a blank file called "testing.md"
```
**What happened:** Claude copied the backend with its full git history into `15-114-HW-9` and added an empty `testing.md`. I created the empty repo on GitHub myself, and Claude pushed the code to it.

---

## 2. Moving the logic into a module

### Prompt 6
````text
what does this mean./ how do i do this? "

Move those three pieces into a module of their own, as functions that take arguments and return values. Add a `package.json` at the top of your repo containing exactly this, so Node treats your `.js` files as modules:

```
{ "type": "module" }

```

If any of your existing code uses `require()`, this will break it, because the setting applies to the whole repository. In that case skip the `package.json` and give your logic and test files the `.mjs` extension instead, which is always treated as a module.
Then update your page to import from the new module, switch the script tag to `type="module"`, and replace any inline `onclick` attributes with `addEventListener` calls.
````
**What happened:** Claude explained each instruction. It pointed out that the steps are for JavaScript but my three pieces were Python, and suggested using three pieces from the chat's JavaScript instead (`apiBase`, `checkReply`, `errorText`).

### Prompt 7
```text
Use the JavaScript
```

### Prompt 8
```text
keep going but DO NOT FIX ANY BUGS just get the modules
```
**What happened:** Claude copied the chat page into `frontend/`, moved the three pieces into `frontend/js/recs-logic.js`, added `package.json`, imported the module in `script.js`, and changed the script tag to `type="module"`. There were no inline `onclick` attributes to replace. It checked that the functions behave exactly like the old code, bugs included.

### Prompt 9
```text
Open your app and click every button before moving on. This is the step most likely to break something quietly.
This is a good place to use an agent, since it's a mechanical refactor
```
**What happened:** An agent clicked every button on the new page and on the original portfolio page, side by side. It found no differences, only bugs that were already in both.

---

## 3. Learning to write tests and writing one by hand

### Prompt 10
```text
whathat is a /tests directory in github?
```

### Prompt 11
```text
how would i set up a tet? can you help me make an outline
```

### Prompt 12
```text
im confused
```
**What happened:** Claude explained what a test is and where the homework stood, and gave an outline of test cases for each function.

### Prompt 13
```text
i need to wrtie at least one test manually, help me do that but dont write for me
```
**What happened:** Claude gave the steps and a fill-in-the-blank template, but not the answers.

### Prompt 14
```text
could i use apiBaser as the test first blank
```

### Prompt 15
```text
im ofnused which logic piece api base ties to
```

### Prompt 16
```text
i need a test that correspond to one of the three og logic pieces, how od i do this
```

### Prompt 17
```text
i need to test that logic pieces so leta do a test for match
```

### Prompt 18
```text
yes set it up but dont run the test or make it, help me write the tets by hand dont write it for me
```
**What happened:** Claude set up a Python environment for pytest in `.venv`, which git ignores. It didn't write or run my test.

### Prompt 19
```text
wait, lets actually contonue with api base first and then i csan have you make the remaining tests
```

### Prompt 20
```text
what does it mena by deicdes what server the chat sends questions to
```

### Prompt 21
```text
so what would the full name be for apibase, im confused
```

### Prompt 22
```text
i dont know whart my hostname and exepctd adres shsould be '
```
**What happened:** Claude walked through the three lines of `apiBase` so I could work out the input and the expected answer myself.

### Prompt 23: my hand-written test, first try
```text
does this work 
```
```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { apiBase } from "../frontend/js/recs-logic.js";
test("apibasereturnhost", () => {
  assert.equal(apiBase, 127.0.0.1);
});
```
**What happened:** Claude pointed out the problems without rewriting it: the function wasn't being called, the text needed quotes, and the second slot needed the expected address.

### Prompt 24: second try
```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { apiBase } from "../frontend/js/recs-logic.js";
test("apibasereturnhost", () => {
  assert.equal(true, "127.0.0.1");
});
```

### Prompt 25: third try
```js
import { apibasereturnhost } from "node:test";
import assert from "node:assert/strict";
import { apiBase } from "../frontend/js/recs-logic.js";
test("apibasereturnhost", (apiBase) => {
  assert.equal(true, "127.0.0.1");
});
```

### Prompt 26: fourth try
```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { apiBase } from "../frontend/js/recs-logic.js";
test("apibasereturnhost", () => {
  assert.equal(apiBase("localHost"), ("127.0.0.1");
});
```

### Prompt 27: final version (works)
```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { apiBase } from "../frontend/js/recs-logic.js";
test("apibasereturnhost", () => {
  assert.equal(apiBase("localhost"),"http://localhost:8000");
});
```
**What happened:** Claude confirmed it was correct. I committed it on GitHub as `tests/recs-logic.test.js`.

### Prompt 28
```text
i committed it how do i run
```

### Prompt 29
```text
i changed the github test so that the host was 8010 instead of 8000 why did it still pss
```
**What happened:** Claude explained that `node --test` runs the copy on my Mac, which still had 8000, and that I needed to `git pull` first.

---

## 4. The pytest tests

### Prompt 30
```text
now time for the next three tests written in pytest. The first test should check that all search criteria are met when a match is found. For instance if someone asks for Thai in Pittsburgh, then only entries with both Pittsburgh and Thai should come up, not just one or the other.
```
**What happened:** Claude wrote the Thai in Pittsburgh test (`tests/test_match.py`), which passes. It also checked the test would catch a wrong answer, and suggested what tests 2 and 3 could be.

### Prompt 31
```text
Use your suggestions
```
**What happened:** Claude wrote the Korean restaurant in Pittsburgh test and the San Sebastian test. Both failed on purpose, proving the `match()` and `extract_filters()` bugs from `testing.md`.

---

## 5. Breaking it on purpose

### Prompt 32
```text
* the next step is to Make five one-line changes to your source, one at a time, each confirmed by a failing test, each undone before the next. Keep the table as you go. 
* 
* The break-it-on-purpose table: five rows, each with the change you made, the test that caught it, and the failure message

where would be good to change
```
**What happened:** Claude tried candidate changes in a throwaway copy and suggested five that a passing test would catch. It also pointed out that only the passing tests can catch a change.

### Prompt 33
```text
what does it mean make the change on my  mac
```

### Prompt 34
```text
watch my screen, il make the changes can you r3cord in the table and upload the fiunal table to my testing read me when im done
```
**What happened:** I made the five changes in VS Code and undid each one with `git checkout`. Claude recorded every save and test result, then added the table to `testing.md` and pushed it.

---

## 6. GitHub Actions

### Prompt 35
```text
whatg is .github/workflows/tests.yml
```

### Prompt 36
```text
how owuld i mak the file
```
**What happened:** I created `.github/workflows/tests.yml` on GitHub myself, running `node --test`.

### Prompt 37
```text
what would i change if the instructions aksed me to push a commit with code i know is broken
```
**What happened:** I pushed a broken commit (port 8000 → 8010), GitHub showed a red ✗, and then I fixed it and the next run was green.

### Prompt 38
```text
do any of my teat genuinyl fail
```

### Prompt 39
```text
do i have a /test suite
```

---

## 7. Getting to 8 passing tests

### Prompt 40
```text
i need 8 tests total. take in my repo and make all the tests pass. record wht you do
```
**What happened:** Claude added four tests and fixed the two real bugs in `app.py`. It compared the old and new code on all 49,216 possible searches to make sure nothing else changed, and recorded it all in `testing.md`. All 8 tests pass.

### Prompt 41
```text
csan we add python test workflows
```
**What happened:** Claude added a `python` job to `tests.yml`. Both jobs (3 JavaScript tests, 5 Python tests) passed on GitHub.

### Prompt 42
```text
where did you ut your documented chabges that you did to make the tests pass
```

### Prompt 43
```text
whatis the diff before you did what yoi had to do to make the tests [ass and after
```

### Prompt 44
```text
make a promptlog.md file with relevant important prompts represented veerbatim
```
**What happened:** Claude wrote this file.
