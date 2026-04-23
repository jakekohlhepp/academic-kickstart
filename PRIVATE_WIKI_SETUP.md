# Private Labor Supply Wiki

The labor supply wiki is published from this website repo at:

- `/private/labor-supply-wiki-qv7m4t2x/`

It is intentionally not linked from the public site navigation.

## Protection

This path is protected by the Netlify Edge Function in [netlify/edge-functions/private-wiki-auth.js](netlify/edge-functions/private-wiki-auth.js), which serves a standard HTTP basic-auth challenge before any wiki files are returned.

Set these environment variables in Netlify with scope including `Functions`:

- `PRIVATE_WIKI_USERNAME`
- `PRIVATE_WIKI_PASSWORD`

Important:

- Do not store these credentials in `netlify.toml`. Netlify does not expose `netlify.toml` environment variables to edge functions at runtime.
- After changing either variable, trigger a fresh deploy.

## Source location

The wiki source project lives in:

- `projects/labor_supply_wiki/`

The published static copy lives in:

- `static/private/labor-supply-wiki-qv7m4t2x/`

## Update workflow

To rebuild and republish the wiki into the website:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync_labor_supply_wiki.ps1
```

That script rebuilds the wiki from `projects/labor_supply_wiki/` and refreshes the published files under the private website path.
