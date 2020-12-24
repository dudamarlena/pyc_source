# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sysadmin/src/malt/malt/ext/malt_breadcrumbs.py
# Compiled at: 2017-05-12 18:30:07
# Size of source mod 2**32: 2093 bytes
import malt, os

@malt.hooks.register('init_record')
def assemble_record_trail(record):
    typedata = malt.site.typedata(record['type'])
    record['crumbs'] = breadcrumb_trail(record['srcdir'], typedata)


@malt.hooks.register('render_page')
def assemble_page_trail(page):
    if page['record']:
        page['crumbs'] = page['record']['crumbs']
    elif page['srcdir']:
        page['crumbs'] = breadcrumb_trail(page['srcdir'], page['type'])


def breadcrumb_trail(srcdir, typedata):
    names, links = [], []
    names.append(typedata['title'])
    if typedata['indexed']:
        url = malt.site.index_url(typedata['name'])
        link = '<a href="%s">%s</a>' % (url, typedata['title'])
        links.append(link)
    else:
        links.append(typedata['title'])
    relpath = os.path.relpath(srcdir, malt.site.src())
    dirnames = relpath.replace('\\', '/').split('/')
    dirnames = dirnames[1:]
    dirslugs = malt.site.slugs(typedata['name'])
    for dirname in dirnames:
        names.append(dirname)
        dirslugs.append(malt.utils.slugify(dirname))
        url = malt.site.url(dirslugs + ['index'])
        link = '<a href="%s">%s</a>' % (url, dirname)
        links.append(link)

    return {'names':names,  'links':links}