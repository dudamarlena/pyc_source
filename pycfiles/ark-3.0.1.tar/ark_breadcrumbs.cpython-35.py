# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_breadcrumbs.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 2084 bytes
import ark, os

@ark.hooks.register('init_record')
def assemble_record_trail(record):
    typedata = ark.site.typedata(record['type'])
    record['crumbs'] = breadcrumb_trail(record['srcdir'], typedata)


@ark.hooks.register('render_page')
def assemble_page_trail(page):
    if page['record']:
        page['crumbs'] = page['record']['crumbs']
    elif page['srcdir']:
        page['crumbs'] = breadcrumb_trail(page['srcdir'], page['type'])


def breadcrumb_trail(srcdir, typedata):
    names, links = [], []
    names.append(typedata['title'])
    if typedata['indexed']:
        url = ark.site.index_url(typedata['name'])
        link = '<a href="%s">%s</a>' % (url, typedata['title'])
        links.append(link)
    else:
        links.append(typedata['title'])
    relpath = os.path.relpath(srcdir, ark.site.src())
    dirnames = relpath.replace('\\', '/').split('/')
    dirnames = dirnames[1:]
    dirslugs = ark.site.slugs(typedata['name'])
    for dirname in dirnames:
        names.append(dirname)
        dirslugs.append(ark.utils.slugify(dirname))
        url = ark.site.url(dirslugs + ['index'])
        link = '<a href="%s">%s</a>' % (url, dirname)
        links.append(link)

    return {'names': names, 'links': links}