# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\lib\helpers.py
# Compiled at: 2012-03-20 09:36:41
"""
:mod:`piano.libs.helpers`
-------------------------

.. autofunction:: now

"""
from webhelpers.text import urlify
import datetime as dt

def now():
    return dt.datetime.utcnow()


def available_pages(app='sample'):
    """Temporary helper function to return a list of available pages for use
    in a site.
    
    This should eventually read from a data-source
    """
    j = lambda a, s, t: (
     ('.').join([a, s]), t)
    return [
     j(app, 'home', 'Home'),
     j(app, 'contactus', 'Contact Us'),
     j(app, 'sitemap', 'Site Map')]