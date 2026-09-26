#!/usr/bin/env zsh
# muratkurt repo - Packages uretimi ve dogrulama
# Kullanim: depo klasorunde  ./update.sh

set -e
cd "$(dirname "$0")"

echo "=== 0. ON KONTROL ==="

# ONCE make_packages.py — OLCULDU (26 Eyl 2026):
# 'dpkg-scanpackages' BILINMEYEN ALANLARI ATIYOR. 'SileoDepiction' onun
# icin bilinmeyen bir alan; o yolla uretilen Packages'ta 17 paketin
# HICBIRINDE kalmadi ve Sileo hepsinde yerel depiction yerine HTML'e
# dustu. Sebebi hicbir yerde yazmiyor, paket normal gorunuyor.
# make_packages.py control'u oldugu gibi kopyaliyor; tercih odur.
# dpkg-scanpackages yalniz python3 yoksa yedek olarak kullanilir.
SCAN=""
if command -v python3.9 >/dev/null 2>&1; then
  PY=python3.9
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
fi
if [[ -n "$PY" && -f make_packages.py ]]; then
  echo "  yontem: make_packages.py ($PY) - tum alanlar korunur"
elif command -v dpkg-scanpackages >/dev/null 2>&1; then
  SCAN="dpkg-scanpackages"
  echo "  yontem: dpkg-scanpackages (YEDEK)"
  echo "  UYARI: bu yol SileoDepiction gibi alanlari ATAR."
else
  echo "DUR: ne python3+make_packages.py ne dpkg-scanpackages var."
  exit 1
fi

if [[ ! -d debs ]];    then echo "DUR: debs/ klasoru yok"; exit 1; fi
if [[ ! -f Release ]]; then echo "DUR: Release dosyasi yok"; exit 1; fi

DEB_SAYI=$(ls -1 debs/*.deb 2>/dev/null | wc -l | tr -d ' ')
if [[ "$DEB_SAYI" == "0" ]]; then echo "DUR: debs/ altinda .deb yok"; exit 1; fi
echo "  debs/ icinde $DEB_SAYI paket"

# GNU sed mi BSD sed mi (BSD'de -i bir sonraki argumani uzanti sanar)
if sed --version >/dev/null 2>&1; then
  SED_INPLACE=(sed -i)
  echo "  sed: GNU"
else
  SED_INPLACE=(sed -i '')
  echo "  sed: BSD"
fi

echo
echo "=== 1. PACKAGES URET ==="
if [[ -n $SCAN ]]; then
  dpkg-scanpackages -m ./debs > Packages
  "${SED_INPLACE[@]}" 's|^Filename: \./|Filename: |' Packages
else
  $PY make_packages.py > Packages
fi

if [[ ! -s Packages ]]; then
  echo "DUR: Packages BOS uretildi"
  exit 1
fi

# ALAN DENETIMI — 26 Eyl 2026'da bir kez kaybedildi, bir daha sessizce
# kaybolmasin. deb'lerde kac SileoDepiction varsa Packages'ta da o kadar
# olmali.
DEB_SD=0
for f in debs/*.deb; do
  dpkg-deb -f "$f" SileoDepiction 2>/dev/null | grep -q . && DEB_SD=$((DEB_SD + 1))
done
PKG_SD=$(grep -c '^SileoDepiction:' Packages || true)
echo "  SileoDepiction: deb'lerde $DEB_SD · Packages'ta $PKG_SD"
if [[ "$DEB_SD" -gt 0 && "$PKG_SD" -lt "$DEB_SD" ]]; then
  echo "DUR: alan kaybi. Packages'ta $PKG_SD, olmasi gereken $DEB_SD."
  echo "  Sebep: uretici bilinmeyen alanlari atiyor (dpkg-scanpackages)."
  exit 1
fi

rm -f Packages.gz Packages.bz2

if command -v gzip >/dev/null 2>&1; then
  gzip -kf Packages
  echo "  Packages.gz uretildi"
else
  echo "  UYARI: gzip yok, Packages.gz uretilemedi"
fi

# .bz2 yalniz eski Cydia icindir. Sileo duz Packages ve .gz okur.
# bzip2 kurulu degilse ATLANIR, bu bir hata degildir.
if command -v bzip2 >/dev/null 2>&1; then
  bzip2 -kf Packages
  echo "  Packages.bz2 uretildi"
else
  echo "  Packages.bz2 ATLANDI (bzip2 kurulu degil - Sileo icin gerekmez)"
fi

echo
echo "=== 2. DOGRULAMA ==="
grep -E '^(Package|Version|Architecture|Depends|Filename):' Packages || true

echo
echo "--- Release ---"
grep -E '^(Origin|Architectures|Suite):' Release || true

echo
echo "*** MIMARI KONTROLU ***"
echo "Asagidaki satirlar UYUMLU olmali; degilse Sileo paketi"
echo "GOSTERMEZ ve sebebini hicbir yerde yazmaz."
grep '^Architecture:'  Packages || true
grep '^Architectures:' Release  || true

echo
echo "=== 3. SIZINTI TARAMASI (bos donmeli) ==="
find . \( -name '*.key' -o -name '*.working' -o -name '*.bak*' \
       -o -name 'dirmodes' -o -name 'active' -o -name '*.tmp.*' \) \
       -not -path './.git/*' -print > /tmp/repo-leak.txt 2>/dev/null || true
if [[ -s /tmp/repo-leak.txt ]]; then
  echo "DUR: sizinti bulundu:"
  cat /tmp/repo-leak.txt
  exit 1
fi
echo "  temiz"

echo
echo "=== 4. DOSYALAR ==="
ls -la Release Packages Packages.gz 2>/dev/null || true
[[ -f Packages.bz2 ]] && ls -la Packages.bz2
ls -la debs/

echo
echo "==================================================="
echo "TAMAM."
echo "  Yuklenecek dosyalar: debs/*.deb + Packages + varsa Packages.gz/.bz2"
echo "  HEPSINI yukleyin; biri eski kalirsa Sileo eski surumu gosterir."
echo
echo "SONRA: Sileo'da depoyu yenileyip paketi GOZUNLE gorun."
echo "Depoyu yayinlamak, paketi test etmek degildir."
echo "==================================================="
