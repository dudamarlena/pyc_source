# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/valtioneuvosto_scraper/util.py
# Compiled at: 2010-07-13 17:15:45
import logging
from datetime import date
from urllib import urlopen
logging.basicConfig()
logging.root.setLevel(logging.INFO)
from templates import *
concat = lambda x: ('\n').join(x)

def parse_date(datestr):
    """from finnish str rep to date obj"""
    datestr.strip()
    (d, m, y) = datestr.split('.')
    return date(int(y), int(m), int(d))


def output_xml(govts, cabs):
    govts_out = []
    for g in govts:
        cab = cabs[g[0]]
        psts_out = []
        for pos in cab:
            msts_out = []
            for mst in cab[pos]:
                msts_out.append(tmpl_minister.strip() % mst)

            txt = concat(msts_out)
            psts_out.append(tmpl_position % (pos, txt))

        txt = concat(psts_out)
        g_begin = g[(-5)].strftime('%d.%m.%Y')
        g_end = '' if not g[(-4)] else g[(-4)].strftime('%d.%m.%Y')
        govts_out.append(tmpl_government % (g[0], g[(-2)], g[(-3)], g[1], g_begin, g_end, txt))

    txt = concat(govts_out)
    return tmpl_main.strip() % txt