from app import Filters, match


def test_match_meets_every_search_criterion():
    """Asking for Thai in Pittsburgh should only return places that are BOTH
    in Pittsburgh AND tagged Thai, never just one or the other."""
    # match gives back two things: the places it found, and the search it used
    hits, used = match(Filters(city="Pittsburgh", cuisine="Thai"))

    # Make sure something came back; otherwise the loop below would check nothing
    assert len(hits) > 0

    for place in hits:
        assert place["city"] == "Pittsburgh", f"{place['name']} is in {place['city']}, not Pittsburgh"
        assert "Thai" in place["cuisines"], f"{place['name']} isn't tagged Thai: {place['cuisines']}"


def test_match_does_not_swap_a_cuisine_for_any_restaurant():
    """Asking for a Korean restaurant in Pittsburgh, where there are no Korean spots,
    should NOT hand back every restaurant in Pittsburgh.

    This is the bug from testing.md: the "don't broaden to any restaurant" check is
    skipped when both a cuisine and a place type are given. Fails on purpose."""
    hits, used = match(Filters(city="Pittsburgh", cuisine="Korean", category="restaurant"))

    # Collect every place that came back without the Korean tag
    wrong = []
    for place in hits:
        if "Korean" not in place["cuisines"]:
            wrong.append(place["name"])

    assert wrong == [], f"asked for Korean, but got {len(wrong)} non-Korean restaurants: {wrong}"
