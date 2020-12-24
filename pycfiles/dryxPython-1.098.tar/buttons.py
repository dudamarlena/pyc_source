# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/buttons.py
# Compiled at: 2013-08-06 07:03:49
"""
_dryxTBS_buttons
===============================
:Summary:
    Buttons partial for the dryxTwitterBootstrap module

:Author:
    David Young

:Date Created:
    April 25, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk
"""

def get_button(size='large', block=False, color='blue', text='button', htmlId=False, htmlClass=False, extraAttr=False, disabled=False):
    """The button method (bases on the twitter bootstrap buttons)

    **Key Arguments:**
        - ``size`` - button size - mini, small, default, large
        - ``block`` - block button?
        - ``color`` - color
        - ``text`` - button text
        - ``htmlId`` -- the name of the button
        - ``htmlClass`` -- the class of the button
        - ``disabled`` -- disable the button if true (flatten & unclickable)

    **Return:**
        - ``button``
    """
    size = 'btn-%s' % (size,)
    if block:
        block = 'btn-block'
    else:
        block = ''
    if htmlId:
        htmlId = 'id="%s" ' % (htmlId,)
    else:
        htmlId = ''
    if not htmlClass:
        htmlClass = ''
    if not extraAttr:
        extraAttr = ''
    if disabled:
        disabled = 'disabled'
    else:
        disabled = ''
    color = 'btn-%s' % (color,)
    button = '\n        <button class="btn %s %s %s %s %s" %s %s type="button">\n        %s\n        </button>' % (size, block, color, htmlClass, disabled, htmlId, extraAttr, text)
    return button


def button(buttonText='', buttonStyle='default', buttonSize='default', href=False, submit=False, block=False, disable=False):
    u"""Generate a button - TBS style

    **Key Arguments:**
        - ``buttonText`` -- the text to display on the button
        - ``buttonStyle`` -- the style of the button required [ default | primary | info | success | warning | danger | inverse | link ]
        - ``buttonSize`` -- the size of the button required [ large | small | mini ]
        - ``href`` -- link the button to another location?
        - ``submit`` -- set to true if a form button [ true | false ]
        - ``block`` -- create block level buttons—those that span the full width of a parent [ True | False ]
        - ``disable`` -- this class is only for aesthetic; you must use custom JavaScript to disable links here

    **Return:**
        - ``button`` -- the button
    """
    if buttonStyle == 'default':
        buttonStyle = ''
    else:
        buttonStyle = 'btn-%s' % (buttonStyle,)
    if buttonSize == 'default':
        buttonSize = ''
    else:
        buttonSize = 'btn-%s' % (buttonSize,)
    if block is True:
        block = 'btn-block'
    else:
        block = ''
    if disable is True:
        disable = 'disable'
    else:
        disable = ''
    if submit is True:
        submit = 'type="submit" '
    else:
        submit = ''
    if href:
        elementOpen = 'a href="%s" ' % (href,)
        elementClose = 'a'
    else:
        elementOpen = 'button type="button" '
        elementClose = 'button'
    button = '\n        <%s class="btn %s %s %s %s" id="  " %s >\n            %s\n        </%s>' % (elementOpen, buttonStyle, buttonSize, block, disable, submit, buttonText, elementClose)
    return button


def buttonGroup(buttonList='', format='default'):
    """Generate a buttonGroup - TBS style

    **Key Arguments:**
        - ``buttonList`` -- a list of buttons
        - ``format`` -- format of the button [ default | toolbar | vertical ]

    **Return:**
        - ``buttonGroup`` -- the buttonGroup
    """
    thisButtonList = ''
    for button in buttonList:
        thisButtonList += button

    if format is 'vertical':
        vertical = 'btn-group-vertical'
    else:
        vertical = ''
    buttonGroup = '\n        <div class="btn-group %s" id="  ">\n            %s\n        </div>' % (vertical, buttonList)
    if format == 'toolbar':
        buttonGroup = '\n        <div class="btn-toolbar">\n            %s\n        </div>' % (buttonGroup,)
    return buttonGroup