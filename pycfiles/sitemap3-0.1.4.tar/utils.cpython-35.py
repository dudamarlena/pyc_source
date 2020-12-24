# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/PYTHON/sitemap/sitemap/utils.py
# Compiled at: 2017-01-24 02:20:08
# Size of source mod 2**32: 1119 bytes


def clean_link(link, domain):
    """ Returns a cleaned url if it is worthwhile.
    Otherwise returns None.
    """
    avoid = [
     '.exe', '.pdf', '.png', '.jpg', '.iso', '.bat', '.gz']
    avoid_in_url = ['javascript:', 'mailto:', 'Javascript:']
    if link is not None:
        for a in avoid:
            if link.lower().endswith(a):
                return

        for a in avoid_in_url:
            if a in link:
                return

        if link.count('http') > 1:
            return
        if not link.startswith('//'):
            pass
        if link.startswith('/') or link.startswith(domain) or not link.startswith('http'):
            if not (link.startswith('http') or link.startswith('/')):
                link = '/{}'.format(link)
            if link.startswith('/'):
                link = '{}{}'.format(domain, link)
            if '?' in link and 'asp?' not in link:
                link = link.split('?')[0]
            return link


def write_text_sitemap(results, output='sitemap.txt'):
    with open(output, 'w') as (f):
        f.write(str('\n'.join(results)))