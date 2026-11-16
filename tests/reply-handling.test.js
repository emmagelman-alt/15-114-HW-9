import { test } from "node:test";
import assert from "node:assert/strict";
import { checkReply, errorText } from "../frontend/js/recs-logic.js";

test("checkReply throws the server's message when the request fails", () => {
  assert.throws(
    () => checkReply(false, { detail: "Type a city and a cuisine to get started!" }),
    { message: "Type a city and a cuisine to get started!" }
  );
});

test("errorText says the server is waking up when the network request fails", () => {
  assert.equal(
    errorText(new TypeError("Failed to fetch")),
    "Sorry, I'm still waking up! Give me a few seconds and send that again."
  );
});
