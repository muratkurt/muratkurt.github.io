#!/usr/bin/zsh
# muratkurt repo - Packages uretimi ve dogrulama
# Kullanim: depo klasorunde  ./update.sh

set -e
cd "$(dirname "$0")"

echo "=== 0. ON KONTROL ==="

# dpkg-scanpackages dpkg-dev paketindedir ve genelde kurulu DEGILDIR.
# Yoksa make_packages.py devreye girer; o yalniz dpkg-deb + python ister.
SCAN=""
if command -v dpkg-scanpackages >/dev/null 2>&1; then
  SCAN="dpkg-scanpackages"
  echo "  yontem: dpkg-scanpackages"
else
  if command -v python3.9 >/dev/null 2>&1; then
    PY=python3.9
  elif command -v python3 >/dev/null 2>&1; then
    PY=python3
  else
    echo "DUR: ne dpkg-scanpackages ne python3 var."
    echo "  Cozum: sudo apt install dpkg-dev   (ya da python3)"
    exit 1
  fi
  if [[ ! -f make_packages.py ]]; then
    echo "DUR: dpkg-scanpackages yok ve make_packages.py da bulunamadi"
    exit 1
  fi
  echo "  yontem: make_packages.py ($PY) - dpkg-scanpackages kurulu degil"
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
