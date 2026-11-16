The three piees of logic I picked are:

1. match answers and loosening the search(lines 214-231)
    - what is supposed to happen: when the exacty user query returns nothing, the system loosens the search constraints to see if it can cme up wth any matches. if the user reqests a combos earch and nothing is found for the first parameter, grok falls back to searching for what fits in the other parameter. However the problem is that this might not be what the user wanted and can end up pulling a list of irrelevant restaurants.
    -  there is a check to prevent this but can occasionally be wrong. the check only runs for cuisines witih no place type. If someone asks for “Thai restaurant in Pittsburgh,” Groq could fill in both cuisine = Thai and type = restaurant. If you have no Thai spots there, the last fallback is “type = restaurant, any cuisine,” and the check never runs on that path.

2. load_places() merging places with multiple entries ( lines 62-70)
   - what is supposed to happen: treat entries with the same name and ciy as one place. the issue here is when multiple places are a result of different branches but the bot does not know which is which so it merges into the highest and the user only sees one entry but doesnt know which branch earned it.

3. extract_filters Remove all tags that arent in my lisrt to make sure it can only pull what is in the DB.
   - what is it supposed to do: throw out any city, country, cuisine or place type that isn’t really in my list, so the bot can never search for something I haven’t been to. It compares the exact text, while the rest of the file ignores capitals and accents. if grok responds with the non accented versions of any city name, then the real city is thrown out and the bot drepsonds with the convention when a city has no visits. this is a problem because it can overlook places I have been. 
