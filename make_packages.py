#!/usr/bin/env python3
"""
Packages uretici - dpkg-scanpackages YOKKEN kullanilir.

Yalniz dpkg-deb ve python3 gerektirir; ikisi de RootHide bootstrap'inde
zaten vardir. dpkg-scanpackages ise dpkg-dev paketindedir ve genelde
kurulu degildir.

Kullanim (depo klasorunde):
    python3.9 make_packages.py

Cikti: stdout -> Packages
"""

import hashlib
import os
import subprocess
import sys

DEBS_DIR = "debs"


def control_of(path):
    """dpkg-deb ile paketin control alanlarini oku."""
    out = subprocess.run(["dpkg-deb", "-f", path],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.stderr.write("HATA: dpkg-deb okuyamadi: %s\n%s\n"
                         % (path, out.stderr))
        sys.exit(1)
    return out.stdout.rstrip("\n")


def hashes(path):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            size += len(chunk)
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
    return size, md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()


def main():
    if not os.path.isdir(DEBS_DIR):
        sys.stderr.write("DUR: %s/ klasoru yok\n" % DEBS_DIR)
        sys.exit(1)

    debs = sorted(f for f in os.listdir(DEBS_DIR) if f.endswith(".deb"))
    if not debs:
        sys.stderr.write("DUR: %s/ altinda .deb yok\n" % DEBS_DIR)
        sys.exit(1)

    stanzas = []
    for name in debs:
        path = os.path.join(DEBS_DIR, name)
        ctrl = control_of(path)
        size, md5, sha1, sha256 = hashes(path)
        stanzas.append("\n".join([
            ctrl,
            "Filename: %s" % path,
            "Size: %d" % size,
            "MD5sum: %s" % md5,
            "SHA1: %s" % sha1,
            "SHA256: %s" % sha256,
        ]))
        sys.stderr.write("  islendi: %s (%d bayt)\n" % (name, size))

    sys.stdout.write("\n\n".join(stanzas) + "\n")


if __name__ == "__main__":
    main()
