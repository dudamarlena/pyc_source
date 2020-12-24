# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/dropdowns.py
# Compiled at: 2013-09-20 11:44:58
"""
_dryxTBS_dropdowns
=================================
:Summary:
    Dropdown menus partial for the dryxTwitterBootstrap module

:Author:
    David Young

:Date Created:
    March 15, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk
"""

def dropdown(buttonSize='default', buttonColor='default', color='grey', menuTitle='#', splitButton=False, linkList=[], separatedLinkList=False, pull=False, direction='down', onPhone=True, onTablet=True, onDesktop=True):
    """get a toggleable, contextual menu for displaying lists of links. Made interactive with the dropdown JavaScript plugin. You need to wrap the dropdown's trigger and the dropdown menu within .dropdown, or another element that declares position: relative;

    - ``buttonSize`` -- size of button [ mini | small | default | large ]
    - ``buttonColor`` -- [ default | sucess | error | warning | info ]
    - ``menuTitle`` -- the title of the menu
    - ``splitButton`` -- split the button into a separate action button and a dropdown
    - ``linkList`` -- a list of (linked) items items that the menu should display
    - ``separatedLinkList`` -- a list of (linked) items items that the menu should display below divider
    - ``pull`` -- [ false | right | left ] (e.g Add ``right`` to a ``.dropdown-menu`` to right align the dropdown menu.)
    - ``direction`` -- drop [ down | up ]
    - ``onPhone`` -- does this container get displayed on a phone sized screen
    - ``onTablet`` -- does this container get displayed on a tablet sized screen
    - ``onDesktop`` -- does this container get displayed on a desktop sized screen

      **Return:**
        - ``dropdown`` -- the dropdown menu
    """
    thisLinkList = ''
    for link in linkList:
        thisLinkList += '%s' % (link,)

    thisSeparatedLinkList = ''
    if separatedLinkList:
        thisSeparatedLinkList = '<li class="divider"></li>'
        for link in separatedLinkList:
            thisSeparatedLinkList += '%s' % (link,)

    thisLinkList = thisLinkList + thisSeparatedLinkList
    if buttonSize == 'default':
        buttonSize = ''
    else:
        buttonSize = 'btn-%s' % (buttonSize,)
    if direction == 'up':
        direction = 'dropup'
    else:
        direction = ''
    if splitButton:
        dropdownButton = '\n            <button class="btn %s %s">%s</button>\n            <button class="btn %s %s dropdown-toggle" data-toggle="dropdown">\n                <span class="caret"></span>\n            </button>' % (buttonSize, buttonColor, menuTitle, buttonSize, buttonColor)
    else:
        dropdownButton = '\n            <a class="btn %s %s dropdown-toggle" data-toggle="dropdown" href="#">\n              %s\n              <span class="caret"></span>\n            </a>' % (buttonSize, buttonColor, menuTitle)
    if pull:
        pull = 'pull-%s' % (pull,)
    else:
        pull = ''
    if onPhone:
        onPhone = ''
    else:
        onPhone = 'hidden-phone'
    if onTablet:
        onTablet = ''
    else:
        onTablet = 'hidden-tablet'
    if onDesktop:
        onDesktop = ''
    else:
        onDesktop = 'hidden-desktop'
    dropdown = '\n        <div class="btn-group %s %s %s %s" id="" %s>\n            %s\n            <ul class="dropdown-menu">\n                <!-- dropdown menu links -->\n                %s\n          </ul>\n        </div>' % (pull, onPhone, onTablet, onDesktop, direction, dropdownButton, thisLinkList)
    return dropdown


if __name__ == '__main__':
    main()