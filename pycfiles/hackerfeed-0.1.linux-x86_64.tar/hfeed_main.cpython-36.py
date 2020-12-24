# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratyush/Projects/HackerFeed/venv/lib/python3.6/site-packages/hfeedlib/hfeed_main.py
# Compiled at: 2017-07-01 05:48:34
# Size of source mod 2**32: 1641 bytes
from .fetchlib import getTopArticles, getBestArticles, getNewArticles, getSavedArticles
from .utils import printArticles, openItem, clearSavedArticles, removeSavedArticles
from .parsing.cli import getParser

def main(args=[]):
    hfeedParser = getParser()
    p = hfeedParser.parse_args(args)
    open_item = True if ('open' in dir(p) and p.open is not None) else False
    remove_item = True if ('remove' in dir(p) and p.remove is not None) else False
    if p.type == 'top':
        if open_item:
            openItem(getTopArticles((p.open), single=True, save_flag=(p.save)))
        else:
            printArticles(getTopArticles((p.number), save_flag=(p.save)))
    else:
        if p.type == 'best':
            if open_item:
                openItem(getBestArticles((p.open), single=True, save_flag=(p.save)))
            else:
                printArticles(getBestArticles((p.number), save_flag=(p.save)))
        else:
            if p.type == 'new':
                if open_item:
                    openItem(getNewArticles((p.open), single=True, save_flag=(p.save)))
                else:
                    printArticles(getNewArticles((p.number), save_flag=(p.save)))
            else:
                if p.type == 'saved':
                    if open_item:
                        openItem(getSavedArticles(p.open)[(p.open - 1)])
                    else:
                        if remove_item:
                            removeSavedArticles(p.remove)
                        else:
                            if p.clear:
                                clearSavedArticles()
                            else:
                                printArticles(getSavedArticles((p.number), display_all=(p.all)))
                elif p.type is None:
                    printArticles([getTopArticles(1, single=True, save_flag=(p.save))], show_numbering=False)