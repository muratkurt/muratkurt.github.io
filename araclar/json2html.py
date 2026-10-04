# Sileo JSON depiction -> web HTML. <head> (stil) AYNEN korunur, yalniz
# <body> JSON'dan uretilir: iki sayfa ayrismasin, tek kaynak JSON olsun.
import json, re, sys, html
J, H = sys.argv[1], sys.argv[2]
d = json.load(open(J))
bas = open(H).read().split('<body>')[0]

def satir_ici(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s.replace(' — ', ' &mdash; ').replace(' → ', ' &rarr; ').replace(' · ', ' &middot; ')

def md(t):
    out, liste = [], False
    for blok in re.split(r'\n\n+', t.strip()):
        if blok.startswith('```'):
            kod = blok.strip('`').lstrip('\n').rstrip('\n')
            out.append('<pre><code>' + html.escape(kod, quote=False) + '</code></pre>')
        elif blok.startswith('# '):
            out.append('<h1>' + satir_ici(blok[2:]) + '</h1>')
        elif blok.startswith('## '):
            out.append('<h2>' + satir_ici(blok[3:]) + '</h2>')
        elif blok.startswith('### '):
            out.append('<h4>' + satir_ici(blok[4:]) + '</h4>')
        elif all(l.startswith('- ') for l in blok.split('\n')):
            out.append('<ul>\n' + '\n'.join('  <li>' + satir_ici(l[2:]) + '</li>'
                                               for l in blok.split('\n')) + '\n</ul>')
        else:
            out.append('<p>' + satir_ici(blok).replace('\n', '<br>') + '</p>')
    return '\n'.join(out)

govde = []
for i, tab in enumerate(d['tabs']):
    if i: govde.append('<hr>\n\n<h2>' + tab['tabname'] + '</h2>')
    tablo = []
    for v in tab['views']:
        c = v['class']
        if c != 'DepictionTableTextView' and tablo:
            govde.append('<table>\n' + '\n'.join(tablo) + '\n</table>'); tablo = []
        if c == 'DepictionMarkdownView': govde.append(md(v['markdown']))
        elif c == 'DepictionHeaderView':
            govde.append(('<h2>' if i == 0 else '<h3>') + satir_ici(v['title'])
                         + ('</h2>' if i == 0 else '</h3>'))
        elif c == 'DepictionScreenshotsView':
            # Sileo'daki kaydirilan resim seridi; web'de yatay kayan satir.
            govde.append('<div style="display:flex;gap:10px;overflow-x:auto;padding:4px 0">\n'
                + '\n'.join('  <a href="%s"><img src="%s" alt="%s" loading="lazy" '
                             'style="height:420px;border-radius:10px;flex:none"></a>'
                             % (x['url'], x['url'], html.escape(x.get('accessibilityText', '')))
                             for x in v['screenshots']) + '\n</div>')
        elif c == 'DepictionTableButtonView':
            govde.append('<p><a href="%s">%s &rarr;</a></p>' % (v['action'], satir_ici(v['title'])))
        elif c == 'DepictionTableTextView':
            tablo.append('  <tr><td>' + satir_ici(v['title']) + '</td><td>'
                         + satir_ici(v['text']) + '</td></tr>')
    if tablo: govde.append('<table>\n' + '\n'.join(tablo) + '\n</table>')

son = ('<p class="foot">muratkurt &middot; <a href="https://muratkurt.github.io/">'
       'muratkurt.github.io</a> &middot; <a href="https://github.com/muratkurt/shivtools">'
       'GitHub</a></p>')
open(H, 'w').write(bas + '<body>\n\n' + '\n\n'.join(govde) + '\n\n' + son + '\n\n</body>\n</html>\n')
print('tamam', len(govde), 'blok')
