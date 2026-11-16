from app import load_places


def test_load_places_merges_repeat_entries_into_one():
    """Raku in New York City is on the Beli list three times (9.6, 8.6 and 8.4).
    load_places should turn that into ONE place that keeps the highest score."""
    places = load_places()

    raku = [p for p in places if p["name"] == "Raku" and p["city"] == "New York City"]

    assert len(raku) == 1, f"expected Raku once, found it {len(raku)} times"
    assert raku[0]["score"] == 9.6
