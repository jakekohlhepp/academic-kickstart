const REALM = "Private Labor Supply Wiki";

function authHeaders() {
  return {
    "WWW-Authenticate": `Basic realm="${REALM}"`,
    "Cache-Control": "no-store",
    "X-Robots-Tag": "noindex, nofollow, noarchive",
  };
}

function unauthorized() {
  return new Response("Authentication required.", {
    status: 401,
    headers: authHeaders(),
  });
}

function parseBasicAuth(headerValue) {
  if (!headerValue || !headerValue.startsWith("Basic ")) {
    return null;
  }

  try {
    const decoded = atob(headerValue.slice("Basic ".length));
    const separator = decoded.indexOf(":");
    if (separator < 0) {
      return null;
    }

    return {
      username: decoded.slice(0, separator),
      password: decoded.slice(separator + 1),
    };
  } catch (_error) {
    return null;
  }
}

export default async (request, context) => {
  const expectedUsername = Netlify.env.get("PRIVATE_WIKI_USERNAME");
  const expectedPassword = Netlify.env.get("PRIVATE_WIKI_PASSWORD");

  if (!expectedUsername || !expectedPassword) {
    return new Response("Private wiki credentials are not configured.", {
      status: 503,
      headers: {
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }

  const provided = parseBasicAuth(request.headers.get("authorization"));
  if (!provided) {
    return unauthorized();
  }

  if (
    provided.username !== expectedUsername ||
    provided.password !== expectedPassword
  ) {
    return unauthorized();
  }

  const response = await context.next();
  const headers = new Headers(response.headers);
  headers.set("Cache-Control", "private, no-store");
  headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
};
