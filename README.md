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

- ClaudeCLIBridge requires a RootHide jailbreak (arm64e).
- ActionButtonFix needs an iPhone with an Action Button; the button does not
  exist on other models. Per-version testing details are on its package page.
- shiv requires Node.js 18 or later. RootHide users get it automatically from
  this repo; rootless users should add https://imcynic.github.io/nodejs-ios/
- The Node.js package is imcynic's work, converted for RootHide with RootHide
  Patcher and republished here unmodified.
- Installing through Sileo routes the package via RootHide Patcher first. The
  convert screen is expected — a "dependency not satisfied" message before
  converting is a misleading symptom, not a real dependency error.
- ClaudeCLIBridge depends on `com.anthropic.claude-code`, which lives in a
  different repository: https://imcynic.github.io/claude-code-ios/

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
