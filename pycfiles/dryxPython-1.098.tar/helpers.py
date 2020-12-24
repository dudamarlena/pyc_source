# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/helpers.py
# Compiled at: 2013-09-20 10:51:00
"""
helpers
======================================
:Summary:
    Partial for the htmlframework modules - contains helper functions for building webpages

:Author:
    David Young

:Date Created:
    May 28, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this code please email me: d.r.young@qub.ac.uk
"""

def main():
    pass


if __name__ == '__main__':
    main()

def unescape_html(html):
    """Unescape a string previously escaped with cgi.escape()

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``html`` -- the string to be unescaped

    **Return:**
        - ``html`` -- the unescaped string
    """
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&quot;', '"')
    html = html.replace('&amp;', '&')
    return html