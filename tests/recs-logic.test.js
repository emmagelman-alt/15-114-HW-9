import { test } from "node:test";
import assert from "node:assert/strict";
import { apiBase } from "../frontend/js/recs-logic.js";
test("apibasereturnhost", () => {
  assert.equal(apiBase("localhost"),"http://localhost:8010");
});
