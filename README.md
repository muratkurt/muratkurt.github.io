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
| [ActionButtonFix](https://muratkurt.github.io/depictions/com.muratkurt.actionbuttonfix.html) | 2.2.0 | Single and double click actions for the Action Button on iPhone 15 Pro |
| [shiv](https://muratkurt.github.io/depictions/com.muratkurt.shiv.html) | 0.1.0 | AI assistant in your terminal, on the device |
| [Node.js 18](https://github.com/imcynic/nodejs-ios) | 18.20.4-1 | RootHide build of Node.js, packaged by imcynic |

## Notes

- ClaudeCLIBridge requires a RootHide jailbreak (arm64e).
- ActionButtonFix only works on iPhone 15 Pro and Pro Max; the Action Button does not exist on other models. Tested on iOS 17.0.3.
- shiv requires Node.js 18 or later. RootHide users get it automatically from this repo; rootless users should add https://imcynic.github.io/nodejs-ios/
- The Node.js package is imcynic's work, converted for RootHide with RootHide Patcher and republished here unmodified.
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
