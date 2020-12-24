# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/menu.py
# Compiled at: 2016-02-20 19:17:49
# Size of source mod 2**32: 1044 bytes
from bottle import app
from bottle import request

def __convert_menu(route):
    entry = {'name':route['name'], 
     'url':route['rule']}
    entry.update(route['config'])
    return entry


def read_menu_entry(name):
    try:
        for route in app().routes:
            entry = route.__dict__
            if name == entry['name']:
                return __convert_menu(entry)

        return
    except:
        return


def read_menu(menutitle):
    entries = []
    for route in app().routes:
        entry = route.__dict__
        if not 'name' not in entry:
            if not entry['name']:
                pass
            else:
                if 'menu' not in entry['config'] or entry['config']['menu'] != menutitle:
                    pass
                else:
                    entries.append(__convert_menu(entry))

    return entries


def read_breadcrumb():
    current = read_current()
    if current['name'] == 'homepage':
        return []
    else:
        return [
         read_menu_entry(name='homepage')]


def read_current():
    return __convert_menu(request.route.__dict__)