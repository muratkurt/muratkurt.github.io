# araclar — depo sayfalarini ureten betikler (28 Eyl 2026)

| Dosya | Ne yapar |
|---|---|
| `json2html.py <paket>.json <paket>.html` | Web sayfasini Sileo JSON'undan uretir; `<head>` (stil) korunur. Iki sayfa ayrismasin diye HTML elle yazilmaz. |
| `yan-depiction.py <depictions-dizini>` | nodejs / ios-mcp / frida JSON'larini uretir. Metin buradadir; degistir, yeniden calistir, sonra json2html. |
| `control-ekle.sh <deb> <revizyon> <paket> <assets-adi>` | Var olan deb'in `control`'une Icon/Depiction/SileoDepiction ekler, revizyonu artirir; ikililere dokunmaz, sonda icerik hash'ini karsilastirir. |

Ikon/banner cizici: `Tweaks-dev/shivtools/gorseller/araclar/gorsel.m`
(UIKit + SF Symbols; cihazda `clang` + `ldid -Sent.plist`; cikti yolu
GERCEK yol olmali — ikili jbroot'u bilmez).
