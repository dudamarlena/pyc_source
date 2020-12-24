# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\lib\mvc.py
# Compiled at: 2012-03-22 11:55:46
"""
:mod:`piano.libs.mvc`
---------------------

.. autoclass:: PageModel

"""

class PageModel(dict):
    """ PageModel to standardize the dict values used across pages.
    """

    def __init__(self, context, **kwargs):
        self['page_id'] = context.id
        self['page_slug'] = context.slug
        self['page_title'] = context.title
        self['page_template'] = getattr(context, 'template', None)
        self['page_data'] = getattr(context, 'data', None)
        site = context.__site__
        if site is not None:
            self['site_id'] = site.id
            self['site_slug'] = site.slug
            self['site_title'] = site.title
        for key in kwargs:
            self[key] = kwargs[key]

        return