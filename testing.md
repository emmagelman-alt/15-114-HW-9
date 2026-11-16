The three piees of logic I picked are:

1. match answers and loosening the search(lines 214-231)
    - what is supposed to happen: when the exacty user query returns nothing, the system loosens the search constraints to see if it can cme up wth any matches. if the user reqests a combos earch and nothing is found for the first parameter, grok falls back to searching for what fits in the other parameter. However the problem is that this might not be what the user wanted and can end up pulling a list of irrelevant restaurants.
    -  there is a check to prevent this but can occasionally be wrong. the check only runs for cuisines witih no place type. If someone asks for “Thai restaurant in Pittsburgh,” Groq could fill in both cuisine = Thai and type = restaurant. If you have no Thai spots there, the last fallback is “type = restaurant, any cuisine,” and the check never runs on that path.

2. load_places() merging places with multiple entries ( lines 62-70)
   - what is supposed to happen: treat entries with the same name and ciy as one place. the issue here is when multiple places are a result of different branches but the bot does not know which is which so it merges into the highest and the user only sees one entry but doesnt know which branch earned it.

3. extract_filters Remove all tags that arent in my lisrt to make sure it can only pull what is in the DB.
   - what is it supposed to do: throw out any city, country, cuisine or place type that isn’t really in my list, so the bot can never search for something I haven’t been to. It compares the exact text, while the rest of the file ignores capitals and accents. if grok responds with the non accented versions of any city name, then the real city is thrown out and the bot drepsonds with the convention when a city has no visits. this is a problem because it can overlook places I have been. 

## Break-it-on-purpose table

I made five one-line changes to the source on my Mac, one at a time. After each one I ran the tests, recorded which test caught it, and undid it (`git checkout -- <file>`) before making the next. After every undo the tests were back to normal: `apibasereturnhost` passed, and pytest showed 1 passed, 2 failed (the two known bugs above).

| # | Change I made | Test that caught it | Failure message |
|---|---|---|---|
| 1 | `frontend/js/recs-logic.js` line 9: `"http://localhost:8000"` → `"http://localhost:8010"` | `apibasereturnhost` (`tests/recs-logic.test.js`) | `AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:` actual `'http://localhost:8010'`, expected `'http://localhost:8000'` |
| 2 | `frontend/js/recs-logic.js` line 8: `hostname === "localhost"` → `hostname !== "localhost"` | `apibasereturnhost` (`tests/recs-logic.test.js`) | `AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:` actual `'https://emma-restaurant-recs.onrender.com'`, expected `'http://localhost:8000'` |
| 3 | `app.py` line 23: `MIN_SCORE` default `'8.0'` → `'9.0'` | `test_match_meets_every_search_criterion` (`tests/test_match.py`) | `assert 0 > 0` (where `0 = len([])`) |
| 4 | `app.py` line 208: `(not cuisine or ...)` → `(True or ...)` | `test_match_meets_every_search_criterion` (`tests/test_match.py`) | `AssertionError: LV. Coffee Project isn't tagged Thai: ['Coffee', 'Coffee Shop']` |
| 5 | `app.py` line 220: `attempts = [(f.cuisine, f.category)]` → `attempts = [(None, f.category)]` | `test_match_meets_every_search_criterion` (`tests/test_match.py`) | `assert 0 > 0` (where `0 = len([])`) |

## Getting to 8 passing tests (done with Claude Code)

**Starting point:** 4 tests. 2 passed, and 2 failed because of the real bugs in `app.py` described above.

### 4 new tests

| # | Test | File | What it checks |
|---|---|---|---|
| 5 | `checkReply throws the server's message when the request fails` | `tests/reply-handling.test.js` | A failed request with a text `detail` throws an error carrying that text |
| 6 | `errorText says the server is waking up when the network request fails` | `tests/reply-handling.test.js` | A network `TypeError` shows the "Sorry, I'm still waking up!" message |
| 7 | `test_load_places_merges_repeat_entries_into_one` | `tests/test_load_places.py` | Raku in New York City is on the Beli list 3 times (9.6, 8.6, 8.4) and becomes one place that keeps 9.6 |
| 8 | `test_extract_filters_throws_out_a_city_not_in_the_list` | `tests/test_extract_filters.py` | A city that isn't in the list ("Atlantis") is still thrown out, so the accent fix below can't let made-up cities through |

All four passed on their first run, before any code was changed. That made 8 tests: 6 passing, 2 failing.

### 2 bug fixes in `app.py`

| Bug | Test that showed it | Fix |
|---|---|---|
| `match()`: "Korean restaurant in Pittsburgh" returned all 23 Pittsburgh restaurants, because the "don't broaden to any restaurant" check only ran when no place type was given | `test_match_does_not_swap_a_cuisine_for_any_restaurant` | When a cuisine and a place type are both asked for, only fall back to "any place of that type" if the type isn't `restaurant`. "Japanese dessert" can still fall back to any dessert spot. Now the bot says it hasn't found a Korean spot there. |
| `extract_filters()`: "San Sebastian" (no accent) was thrown out, because the check compared exact text | `test_extract_filters_keeps_a_real_city_typed_without_its_accent` | New helper `in_list()` compares the way the rest of the file does (`norm()`, ignoring capitals and accents) and keeps the list's own spelling: "San Sebastian" → "San Sebastián". Anything not in the list still becomes `None`. |

No test's checks were changed to make it pass. The only edits to existing tests were the comments on the two that used to fail ("fails on purpose" → "failed until fixed").

### Checking the fixes didn't break anything else

- Ran the old and new `match()` on all 49,216 possible searches (every city or country × every cuisine × every place type). The only searches that changed were "cuisine + restaurant" where there's no spot of that cuisine: before, every restaurant came back; now, none do.
- Every real value in the list passes the `extract_filters()` check exactly as before, except "Ice cream", which now maps to "Ice Cream". The list has both spellings, and the search finds the same 7 places either way.
- Still not handled: letters that are their own letter rather than an accent, like the ø in Sørvågen. "Sorvagen" is still thrown out.
- The line numbers earlier in this file refer to `app.py` before these fixes. `match()` now starts at line 226.

### Results

| Command | Result |
|---|---|
| `node --test` | 3 passed, 0 failed |
| `.venv/bin/python -m pytest -v` | 5 passed, 0 failed |

**8 of 8 tests pass.** The GitHub Actions workflow (`.github/workflows/tests.yml`) still only runs the 3 JavaScript tests.

Claude changed the test to catch the accent bug for citie slike san sebastiàn. a neew helper filter ignores accents and capitals to make sure that even mispelled requests still recevie the intended result. It also fixed the bug where the system would send every list in a location if it couldnt find an exact cuisine match, now it doesnt default to every other place if it cant find a match. 

AI USAGE SUMMERY. I used ai for all the ai relevant steps in the nstructins such as the remaining tests, dettingup a suite, etc. I also used AI to help me understand the asignment. I think i had the mo ttehcnical difficulty with this assignment so I used ai to help me figure out what to do and outline and guide me. I explicitly told me not to give me the direct answers but to make sure I could get to them on my own. An example of this is "yes set it up but dont run the test or make it, help me write the tets by hand dont write it for me". 

