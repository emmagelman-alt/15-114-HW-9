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
