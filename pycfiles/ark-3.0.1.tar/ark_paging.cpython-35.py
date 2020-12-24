# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_paging.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 4071 bytes
from ark import hooks, site

@hooks.register('render_page')
def add_paging_links(page):
    if page['is_paged']:
        page['paging'] = generate_paging_links(page['slugs'][:-1], page['page'], page['total'])


def generate_paging_links(slugs, page_number, total_pages):
    data = {'first': 'First', 
     'last': 'Last', 
     'prev': 'Prev', 
     'next': 'Next', 
     'delta': 2, 
     'multiples': 2, 
     'multiple': 10}
    data.update(site.config.get('paging', {}))
    start = page_number - data['delta']
    end = page_number + data['delta']
    if start < 1:
        start = 1
        end = 1 + 2 * data['delta']
    if end > total_pages:
        start = total_pages - 2 * data['delta']
        end = total_pages
    if start < 1:
        start = 1
    out = []
    if start > 1:
        out.append("<a class='first' href='%s'>%s</a>" % (
         site.paged_url(slugs, 1, total_pages),
         data['first']))
    if page_number > 1:
        out.append("<a class='prev' href='%s'>%s</a>" % (
         site.paged_url(slugs, page_number - 1, total_pages),
         data['prev']))
    if data['multiples']:
        multiples = list(range(data['multiple'], start, data['multiple']))
        for multiple in multiples[-data['multiples']:]:
            out.append("<a class='pagenum multiple' href='%s'>%s</a>" % (
             site.paged_url(slugs, multiple, total_pages), multiple))

    for i in range(start, end + 1):
        if i == page_number:
            out.append("<span class='pagenum current'>%s</span>" % i)
        else:
            out.append("<a class='pagenum' href='%s'>%s</a>" % (
             site.paged_url(slugs, i, total_pages), i))

    if data['multiples']:
        starting_multiple = (int(end / data['multiple']) + 1) * data['multiple']
        multiples = list(range(starting_multiple, total_pages, data['multiple']))
        for multiple in multiples[:data['multiples']]:
            out.append("<a class='pagenum multiple' href='%s'>%s</a>" % (
             site.paged_url(slugs, multiple, total_pages), multiple))

    if page_number < total_pages:
        out.append("<a class='next' href='%s'>%s</a>" % (
         site.paged_url(slugs, page_number + 1, total_pages),
         data['next']))
    if end < total_pages:
        out.append("<a class='last' href='%s'>%s</a>" % (
         site.paged_url(slugs, total_pages, total_pages),
         data['last']))
    return ''.join(out)