import asyncio

import app


def test_extract_filters_keeps_a_real_city_typed_without_its_accent(monkeypatch):
    """If Groq answers "San Sebastian" (no accent), the city should be kept, because
    San Sebastián IS in the list.

    This is the bug from testing.md: the check compares the exact text, so the city
    gets thrown out. Fails on purpose."""

    # Pretend Groq answered without the accent, so no API key or internet is needed
    async def fake_groq(messages, schema=None, temperature=0.2):
        return '{"city": "San Sebastian", "country": "Spain"}'

    # monkeypatch swaps app.groq for the fake, only while this test runs
    monkeypatch.setattr(app, "groq", fake_groq)

    filters = asyncio.run(app.extract_filters(app.Ask(message="tapas in san sebastian")))

    assert filters.city is not None, "San Sebastian was thrown out, even though San Sebastián is in the list"
