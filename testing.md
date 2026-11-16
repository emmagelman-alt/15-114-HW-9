The three piees of logic I picked are:

1. match answers and loosening the search(lines 214-231)
    - what is supposed to happen: when the exacty user query returns nothing, the system loosens the search constraints to see if it can cme up wth any matches. if the user reqests a combos earch and nothing is found for the first parameter, grok falls back to searching for what fits in the other parameter. However the problem is that this might not be what the user wanted and can end up pulling a list of irrelevant restaurants.
    -  
