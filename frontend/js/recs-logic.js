// Restaurant rec chat logic, moved out of script.js for HW 9 so it can be tested on its own.
// Each function takes what it needs as arguments and returns a value; none of them
// touch the page, the network or global variables. Behavior matches the original
// inline code in script.js exactly.

// Which backend to talk to, given the page's hostname (location.hostname).
export function apiBase(hostname) {
  var local = hostname === "localhost" || hostname === "127.0.0.1";
  return local ? "http://localhost:8000" : "https://emma-restaurant-recs.onrender.com";
}

// Given res.ok and the parsed JSON body of a /api/recs response, returns the body,
// or throws an Error carrying the message to show if the request failed.
export function checkReply(ok, data) {
  if (!ok) throw new Error(data.detail || "Something went wrong. Try again?");
  return data;
}

// The chat message to show when a request fails.
// A network error (not an error reply) almost always means the server is still waking up.
export function errorText(err) {
  return err instanceof TypeError
    ? "Sorry, I'm still waking up! Give me a few seconds and send that again."
    : err.message;
}
