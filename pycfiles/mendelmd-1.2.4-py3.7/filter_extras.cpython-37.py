# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/filter_analysis/templatetags/filter_extras.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 992 bytes
from django import template
register = template.Library()

def cut(variant):
    links = variant.cln_omim.split('|')
    new_links = []
    for link in links:
        if link == 'http://www.ncbi.nlm.nih.gov/sites/varvu?gene':
            link = '%s=%s&rs=%s' % (link, variant.gene_name, variant.variant_id)
        new_links.append(link)

    return new_links


def cleanstr(value):
    """Removes all values of arg from the given string"""
    return value.replace('_', ' ')


@register.filter
def adjust_for_pagination(page, current):
    if current - page in (-1, -2, 1, 2):
        return True
    return False


register.filter('adjust_for_pagination', adjust_for_pagination)
register.filter('cut', cut)
register.filter('cleanstr', cleanstr)