# muratkurt's Repo

APT repository for jailbroken iOS devices.

**Repo page:** https://muratkurt.github.io/

## Add this source

```
https://muratkurt.github.io/
```

The [repo page](https://muratkurt.github.io/) has one-tap buttons for Sileo, Zebra, Cydia, Installer and Saily. Those links only work on the device.

## Packages

| Package | Version | Description |
| --- | --- | --- |
| [ClaudeCLIBridge](https://muratkurt.github.io/depictions/com.muratkurt.claude-cli-bridge.html) | 0.4.3 | Makes Claude Code CLI work on RootHide, with provider profiles and separate session pools |

## Notes

- ClaudeCLIBridge requires a RootHide jailbreak (arm64e).
- Installing through Sileo routes the package via RootHide Patcher first. The convert screen is expected — a "dependency not satisfied" message before converting is a misleading symptom, not a real dependency error.
- ClaudeCLIBridge depends on `com.anthropic.claude-code`, which lives in a different repository: https://imcynic.github.io/claude-code-ios/

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

Claude Code is proprietary software by Anthropic. Packages here are for personal use on jailbroken devices.
