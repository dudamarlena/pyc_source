# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/tables.py
# Compiled at: 2013-08-06 07:04:34
"""
_dryxTBS_tables
=============================
:Summary:
    Tables partial for dryxTwitterBootstrap

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

def tr(cellContent='', color=False):
    """Generate a table row - TBS style

    **Key Arguments:**
        - ``cellContent`` -- the content - either <td>s or <th>s
        - ``color`` -- [ sucess | error | warning | info ]

    **Return:**
        - ``tr`` -- the table row
    """
    if color is False:
        color = ''
    tr = '\n        <tr class="%s">\n            %s\n        </tr>' % (color, cellContent)
    return tr


def th(content='', color=False):
    """Generate a table header cell - TBS style

    **Key Arguments:**
        - ``content`` -- the content
        - ``color`` -- [ sucess | error | warning | info ]

    **Return:**
        - ``th`` -- the table header cell
    """
    if color is False:
        color = ''
    th = '\n        <th class="%s">\n            %s\n        </th>' % (color, content)
    return th


def td(content='', color=False):
    """Generate a table data cell - TBS style

    **Key Arguments:**
        - ``content`` -- the content
        - ``color`` -- [ sucess | error | warning | info ]

    **Return:**
        - ``td`` -- the table data cell
    """
    if color is False:
        color = ''
    td = '\n        <td class="%s">\n            %s\n        </td>' % (color, content)
    return td


def tableCaption(content=''):
    """Generate a table caption - TBS style

    **Key Arguments:**
        - ``content`` -- the content

    **Return:**
        - ``tableCaption`` -- the table caption
    """
    tableCaption = '\n        <tableCaption class="">\n            %s\n        </tableCaption>' % (content,)
    return tableCaption


def thead(trContent=''):
    """Generate a table head - TBS style

    **Key Arguments:**
        - ``trContent`` -- the table row content

    **Return:**
        - ``thead`` -- the table head
    """
    thead = '\n        <thead class="">\n            %s\n        </thead>' % (trContent,)
    return thead


def tbody(trContent=''):
    """Generate a table body - TBS style

    **Key Arguments:**
        - ``trContent`` -- the table row content

    **Return:**
        - ``tbody`` -- the table body
    """
    tbody = '\n        <tbody class="">\n            %s\n        </tbody>' % (trContent,)
    return tbody


def table(caption='', thead='', tbody='', stripped=True, bordered=False, hover=True, condensed=False):
    """Generate a table - TBS style

    **Key Arguments:**
        - ``caption`` -- the table caption
        - ``thead`` -- the table head
        - ``tbody`` -- the table body
        - ``stripped`` -- Adds zebra-striping to any odd table row
        - ``bordered`` -- Add borders and rounded corners to the table.
        - ``hover`` -- Enable a hover state on table rows within a <tbody>
        - ``condensed`` -- Makes tables more compact by cutting cell padding in half.

    **Return:**
        - ``table`` -- the table
    """
    if stripped is True:
        stripped = 'table-stripped'
    else:
        stripped = ''
    if bordered is True:
        bordered = 'table-bordered'
    else:
        bordered = ''
    if hover is True:
        hover = 'table-hover'
    else:
        hover = ''
    if condensed is True:
        condensed = 'table-condensed'
    else:
        condensed = ''
    table = '\n        <table class="table %s %s %s %s">\n            %s\n            %s\n            %s\n        </table>' % (stripped, bordered, hover, condensed, caption, thead, tbody)
    return table