#!/bin/sh
# control-ekle <eski.deb> <yeni-revizyon> <paket-kimligi> <assets-adi>
# Yalniz DEBIAN/control'e Icon/Depiction/SileoDepiction ekler ve revizyonu
# artirir. Ikililere DOKUNMAZ; sonunda dosya hash'lerini karsilastirir.
set -e
ESKI="$1"; REV="$2"; PKG="$3"; AS="$4"
T=$(mktemp -d)
printf 'root\n' | sudo -S -p '' dpkg-deb -R "$ESKI" "$T/x"
C="$T/x/DEBIAN/control"
printf 'root\n' | sudo -S -p '' chmod a+rX "$T/x" "$T/x/DEBIAN" "$C"   # frida: DEBIAN 700, control 600 (root)
grep -q '^Depiction:' "$C" && { echo "zaten var: $ESKI"; exit 1; }
SUR=$(sed -n 's/^Version: //p' "$C"); YENI_SUR="${SUR%-*}-$REV"
printf 'root\n' | sudo -S -p '' sed -i "s/^Version: .*/Version: $YENI_SUR/" "$C"
printf 'root\n' | sudo -S -p '' sed -i "/^Homepage:/a SileoDepiction: https://muratkurt.github.io/depictions/$PKG.json" "$C"
printf 'root\n' | sudo -S -p '' sed -i "/^Homepage:/a Depiction: https://muratkurt.github.io/depictions/$PKG.html" "$C"
printf 'root\n' | sudo -S -p '' sed -i "/^Homepage:/a Icon: https://muratkurt.github.io/assets/$AS/icon.png" "$C"
ARCH=$(sed -n 's/^Architecture: //p' "$C")
YENI="$(dirname "$ESKI")/${PKG}_${YENI_SUR}_${ARCH}.deb"
printf 'root\n' | sudo -S -p '' dpkg-deb -b "$T/x" "$YENI" >/dev/null
printf 'root\n' | sudo -S -p '' chown mobile "$YENI"
# Icerik ayni mi: iki paketin dosya hash listesi (control haric)
h() { D=$(mktemp -d); dpkg-deb -x "$1" "$D"; (cd "$D" && find . -type f -exec shasum {} + | sort -k2); rm -rf "$D"; }
if [ "$(h "$ESKI")" = "$(h "$YENI")" ]; then S="icerik AYNI"; else S="ICERIK FARKLI!"; fi
echo "$(basename "$YENI")  ·  $S  ·  $(dpkg-deb -f "$YENI" Icon | sed 's|.*/assets/||')"
printf 'root\n' | sudo -S -p '' rm -rf "$T"
