# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\filters.py
# Compiled at: 2019-07-14 05:38:45
# Size of source mod 2**32: 1314 bytes
"""
filters - filters which work with tables-assets/static/filters.css

Usage::

    filters = filtercontainerdiv()
    filters.append(filterdiv('filter1-id', 'Filter 1 Label'))
    filters.append(filterdiv('filter2-id', 'Filter 2 Label'))

        :

    example = CrudApi(
            :
        pretablehtml = filters,
            :
    )
"""
from dominate.tags import div, span

def filterdiv(id, label):
    """
    build div with spans for label, filter
    :param id:
    :param label:
    :return: dominate div
    """
    return div(span(label, _class='label'),
      span(id=id, _class='filter'),
      _class='filter-item')


def filtercontainerdiv():
    """
    build div for filter container
    :return: dominate div
    """
    return div(_class='external-filter filter-container')