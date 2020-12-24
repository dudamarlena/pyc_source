# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/code.py
# Compiled at: 2013-08-06 07:04:58
"""
_dryxTBS_code
=============================
:Summary:
    Code partial for dryxTwitterBootstrap

:Author:
    David Young

:Date Created:
    April 16, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk
"""

def code(content='', inline=True, scroll=False):
    """Generate a code section

    **Key Arguments:**
        - ``content`` -- the content of the code block
        - ``inline`` -- inline or block?
        - ``scroll`` -- give the block a scroll bar on y-axis?

    **Return:**
        - ``code`` -- the code section
    """
    if scroll:
        scroll = 'pre-scrollable'
    else:
        scroll = ''
    if inline:
        code = '<code>%s</code>' % (content,)
    else:
        code = '\n            <pre class="%s">\n                %s\n            </pre>' % (scroll, content)
    return code