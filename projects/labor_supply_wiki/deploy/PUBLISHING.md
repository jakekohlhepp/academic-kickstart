# Publish This Wiki Under a Password

This wiki builds to plain static files in `site/`, and all internal links are relative. That means you can host it under a subdirectory on a personal website without rewriting links.

## Recommended setup

1. Run `python build.py`.
2. Upload the contents of `site/` into a private subdirectory on your website, for example `https://yourdomain.com/labor-supply-wiki/`.
3. Protect that subdirectory with server-side basic auth.

Server-side protection is the right choice here because it actually blocks access to the files. A client-side password prompt in JavaScript would only hide the content casually and would not really secure the wiki.

## Apache

- Use [apache/.htaccess.example](apache/.htaccess.example) in the deployed wiki directory.
- Create a password file outside the web root, for example:

```bash
htpasswd -c /absolute/path/outside-web-root/.htpasswd-labor-supply yourusername
```

- Update the `AuthUserFile` path in the example.

## Nginx

- Use [nginx/wiki-password-location.conf.example](nginx/wiki-password-location.conf.example) as the location block for the subdirectory where you upload the built site.
- Create a password file such as `/etc/nginx/.htpasswd-labor-supply`.
- Reload Nginx after adding the config.

## Caddy

- Use [caddy/Caddyfile.example](caddy/Caddyfile.example) as a starting point.
- Generate the password hash with:

```bash
caddy hash-password
```

- Replace the placeholder hash in the example.

## Notes

- The static build can live under a subpath like `/labor-supply-wiki/` because the generated pages use relative paths.
- If you later want a custom subpath name, you usually only need to change the upload folder and the web-server location block.
- If you tell me what stack your personal website uses, I can turn one of these examples into a ready-to-paste config.
