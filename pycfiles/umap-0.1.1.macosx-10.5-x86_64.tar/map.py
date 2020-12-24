# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/KyunghoonKim/anaconda/lib/python2.7/site-packages/umap/map.py
# Compiled at: 2016-01-19 21:37:03
from IPython.display import HTML
import folium

def inline_map(map):
    """
    Embeds the HTML source of the map directly into the IPython notebook.

    This method will not work if the map depends on any files (json data). Also this uses
    the HTML5 srcdoc attribute, which may not be supported in all browsers.
    """
    if isinstance(map, folium.Map):
        map._build_map()
        srcdoc = map.HTML.replace('"', '&quot;')
        embed = HTML(('<iframe srcdoc="{srcdoc}" style="width: 100%; height: 500px; border: none"></iframe>').format(srcdoc=srcdoc))
    else:
        raise ValueError('{!r} is not a folium Map instance.')
    return embed


def embed_map(map, path='map.html'):
    path = path
    map.create_map(path=path)
    return HTML(('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>').format(path=path))


def export_map(map, path='export_data.html', js='test.js'):
    path = path
    map.create_map(path=path)
    f = open(path, 'r')
    text = f.read()
    f.close()
    pos = text.find('var circle_1')
    if len(splited) > 1:
        circles = text[pos:]
    else:
        print 'Length is 1'
    circles = circles.replace('</script>', '').replace('</body>', '')
    cv = ''
    vs = []
    for i in circles.split('\n'):
        if 'map' not in i:
            cv += i.replace('  ', '') + '\n'
        if 'var ' in i:
            i = i.replace('  ', '')
            vs.append(i.split(' ')[1])

    head = 'var circle_group = L.layerGroup('
    vs = str(vs).replace("'", '')
    tail = ');'
    java_1 = cv
    java_2 = head + vs + tail
    f = open(js, 'w')
    filename = js.split('.')[0] + '_'
    f.write(java_1.replace('circle_', filename))
    f.write(java_2.replace('circle_', filename))
    f.close()
    return js