# muratkurt's Repo

APT repository for jailbroken iOS devices.

**Repo page:** https://muratkurt.github.io/

## Add this source

```
https://muratkurt.github.io/
```

The [repo page](https://muratkurt.github.io/) lists every package with its
current version, and has one-tap buttons for Sileo, Zebra, Cydia, Installer and
Saily. Those buttons open an app, so they only work on the device.

Versions are deliberately not repeated here. The repo page reads them from the
`Packages` index, so it is current by construction — this file cannot go stale.

## Notes

- ActionButtonFix needs an iPhone with an Action Button; the button does not
  exist on other models. Per-version testing details are on its package page.
- shivtools is the on-device tweak development toolkit. Node.js, frida and
  iOS MCP are **not** required to install it: it recommends them and its
  Settings page installs the ones you want.
- The Node.js package is Node.js 24 built for iOS from
  [realAndi/nodejs-for-ios](https://github.com/realAndi/nodejs-for-ios),
  packaged here for both rootless and RootHide. It replaces the older
  `io.github.imcynic.nodejs` (18.x) if you have it installed.
- The frida package repackages the official release so it runs on RootHide,
  and provides `re.frida.server`. iOS MCP is
  [witchan/ios-mcp](https://github.com/witchan/ios-mcp) with the server bound
  to loopback and auto-respring off by default.
- Installing through Sileo routes the package via RootHide Patcher first. The
  convert screen is expected — a "dependency not satisfied" message before
  converting is a misleading symptom, not a real dependency error.

## Repository layout

```
Release  Packages  Packages.gz     APT metadata
index.html                         repo page
CydiaIcon.png                      repo icon
update.sh  make_packages.py        regenerate Packages
debs/                              .deb files
depictions/                        one .json + .html per package
assets/<package>/                  icon.png, banner.png
```

## Publishing a new version

```
cp <new>.deb debs/
./update.sh                        regenerates Packages / .gz / .bz2
git add -A && git commit && git push
```

Only the package's own depiction (`depictions/<id>.json` and `.html`) carries a
version number by hand. `index.html` and this README do not — leave them alone.

Claude Code is proprietary software by Anthropic. Packages here are for personal
use on jailbroken devices.
