# Yan paketlerin Sileo depiction'lari — shivtools duzeni (Details/Usage/Changelog).
import json, sys
OUT = sys.argv[1]
GH = 'https://github.com/muratkurt/shivtools'
def md(s): return {'class': 'DepictionMarkdownView', 'markdown': s}
def h(s): return {'class': 'DepictionHeaderView', 'title': s}
def sep(): return {'class': 'DepictionSeparatorView'}
def row(a, b): return {'class': 'DepictionTableTextView', 'title': a, 'text': b}
def sayfa(ad, renk, details, usage, changelog):
    return {'minVersion': '0.1',
            'headerImage': f'https://muratkurt.github.io/assets/{ad}/banner.png',
            'tintColor': renk, 'class': 'DepictionTabView', 'tabs': [
              {'class': 'DepictionStackView', 'tabname': 'Details', 'views': details},
              {'class': 'DepictionStackView', 'tabname': 'Usage', 'views': usage},
              {'class': 'DepictionStackView', 'tabname': 'Changelog', 'views': changelog}]}
TESTED = 'iOS 17.0.3 (RootHide) · iOS 16.1.1 (Dopamine)'

nodejs = sayfa('nodejs', '#D9653B', [
  md("# Node.js\n\nNode 24 with npm and npx, on the iPhone. Everything is in the package — nothing is "
     "downloaded or compiled when you install it. JIT works; it is not a `--jitless` build."),
  sep(), h('Information'),
  row('Developer', 'muratkurt'), row('Package', 'com.muratkurt.nodejs'), row('Version', '24.21.0-2'),
  row('Contains', 'Node 24.21.0 · npm 11.19.0 · npx · corepack'),
  row('Requires', 'iOS 15.0 or later · A12 or newer'), row('Compatibility', 'rootless · RootHide'),
  row('Tested on', TESTED), row('Replaces', 'io.github.imcynic.nodejs (Node 18)'),
], [
  h('Check it'),
  md("```\nnode -v && npm -v && npx --version\nnode -e 'require(\"child_process\").execSync(\"uname -m\")'\n```\n\n"
     "The second line is the one that matters: it proves `child_process` works, not just `node -v`."),
  sep(), h('Good to know'),
  md("- **Pure JavaScript packages install and run.** Native add-ons (`.node` files) do not load.\n"
     "- **A12 or newer.** Older chips stop with SIGILL.\n"
     "- **Run it from a login shell** — the terminal app does this. Over a one-shot `ssh host 'command'`, "
     "`/usr/local/bin` is not on `PATH`; use `ssh host \"zsh -lc 'node -v'\"`.\n"
     "- **Many workers at once** can run out of address space. `NODEIOS_V8_FLAGS=--jitless` is the escape hatch.\n"
     "- `shiv-sinif` from **shivtools** is the tool that needs it; the rest of shivtools does not."),
  sep(), h('Credits'),
  md("[Node.js](https://nodejs.org) — OpenJS Foundation (MIT) · iOS port "
     "[nodejs-for-ios](https://github.com/realAndi/nodejs-for-ios) — andi (MIT). "
     "Packaged by muratkurt. More in the [shivtools guide](" + GH + ")."),
], [
  h('24.21.0-2'), md("- Icon and depiction pages. The package contents are unchanged."), sep(),
  h('24.21.0-1'), md("- First release: Node 24.21.0, npm 11.19.0, npx.\n- Verified on RootHide and on rootless (A12), JIT included."),
])

mcp = sayfa('ios-mcp', '#3FB0A6', [
  md("# iOS MCP\n\nAn MCP server inside SpringBoard: an AI agent can take screenshots, read the "
     "accessibility tree and the live system log, tap, type, open apps and more — 46 tools.\n\n"
     "Based on [witchan/ios-mcp](https://github.com/witchan/ios-mcp) 1.2.8, packaged for **shivtools** "
     "with safer defaults: it listens on **127.0.0.1 only**, `mcp-root` comes **without setuid**, and "
     "installing a deb through it **does not respring** on its own."),
  sep(), h('Information'),
  row('Developer', 'witchan · packaged by muratkurt'), row('Package', 'com.muratkurt.ios-mcp'),
  row('Version', '1.2.8-2'), row('Requires', 'iOS 15.0 or later'), row('Compatibility', 'rootless · RootHide'),
  row('Tested on', TESTED), row('Replaces', 'com.witchan.ios-mcp'),
], [
  h('Connect an agent'),
  md("```\nshiv-mcp durum          # installed, running, which mode\nshiv-mcp baglan         # the claude mcp add line for this phone\n"
     "shiv-mcp baglan --mac   # SSH tunnel + claude mcp add for a Mac\n```\n\n"
     "`shiv-mcp` comes with **shivtools**. Restart the CLI after adding the server."),
  sep(), h('Security'),
  md("The server has **no authentication**. By default it only accepts connections from the phone itself.\n\n"
     "- `shiv-mcp mod ag` listens on the network — it asks first. Don't use it on public Wi-Fi.\n"
     "- From a Mac, prefer the SSH tunnel: login and encryption come for free.\n"
     "- `shiv-mcp root-ac` gives `mcp-root` its setuid bit. Only if you need root actions through the agent."),
  sep(), h('After installing'),
  md("Respring once so SpringBoard loads the server. **Settings → iOS MCP** starts and stops it."),
  sep(), h('Licence'),
  md("iOS MCP is MIT. The package also carries AppSync Unified and appinst (GPL-3.0) and ldid (AGPL-3.0), "
     "built unmodified from [witchan/ios-mcp v1.2.8](https://github.com/witchan/ios-mcp/tree/v1.2.8). "
     "Licence texts: `/usr/share/doc/`."),
], [
  h('1.2.8-2'), md("- Icon and depiction pages. The package contents are unchanged."), sep(),
  h('1.2.8-1'), md("- Listens on 127.0.0.1 by default; network mode is a setting.\n- `mcp-root` without setuid by default.\n"
                   "- Installing a deb no longer resprings by itself.\n- Turkish interface.\n- Everything included: server, OCR, IPA installer."),
])

frida = sayfa('frida', '#E05A4E', [
  md("# Frida\n\nThe official **frida-server 17.19.0** for rootless and RootHide.\n\n"
     "**Rootless:** the upstream build, unmodified. Only the package name and a real `postinst` are ours — "
     "upstream starts the daemon from `extrainst_`, which apt does not run.\n\n"
     "**RootHide:** `build.frida.re` has no RootHide build. This one adds a three-line wrapper and an "
     "architecture dpkg accepts.\n\n"
     "Already have `re.frida.server`? Keep it; shivtools uses whichever is installed."),
  sep(), h('Information'),
  row('Developer', 'Ole André Vadla Ravnås · packaged by muratkurt'), row('Package', 'com.muratkurt.frida'),
  row('Version', '17.19.0-3'), row('Requires', 'iOS 15.0 or later'), row('Compatibility', 'rootless · RootHide'),
  row('Tested on', 'iOS 17.0.3 (RootHide) · iOS 16.1.1 (Dopamine)'), row('Replaces', 're.frida.server'),
], [
  h('Check it'),
  md("```\nshiv-ortam --ajan-sina\n```\n\nFrom **shivtools**: checks client → server → attach → ObjC and prints the frida version it talks to."),
  sep(), h('Known issue on RootHide'),
  md("frida 17 can bring **SpringBoard** down on about the third attach in a row; the device drops into safe mode "
     "and comes back in one go. Apps are fine, and frida 16 or rootless are not affected. frida 17 wants a "
     "memory-hooking API from the jailbreak that RootHide does not offer yet. Batch your SpringBoard work."),
  sep(), h('Clients'),
  md("A frida client must match the **major** version: use frida-tools 17 on your computer. "
     "The client inside shivtools (`shivfrida`) is already built for 17."),
  sep(), h('Going back to 16'),
  md("Remove this package, then install `re.frida.server` 16.x — from `build.frida.re` on rootless, "
     "from the RootHide repo on RootHide."),
], [
  h('17.19.0-3'), md("- Rootless build: the upstream binary, unmodified (sha256 checked at packaging).\n"
                       "- Icon and depiction pages."), sep(),
  h('17.19.0-1 · -2'), md("- First releases: frida-server 17.19.0 for RootHide.\n"
                           "- The daemon starts from a real `postinst`, so a plain `dpkg -i` works too."),
])

for ad, d in (('com.muratkurt.nodejs', nodejs), ('com.muratkurt.ios-mcp', mcp), ('com.muratkurt.frida', frida)):
    json.dump(d, open(f'{OUT}/{ad}.json', 'w'), ensure_ascii=False, indent=2)
    print(ad, [len(t['views']) for t in d['tabs']])
