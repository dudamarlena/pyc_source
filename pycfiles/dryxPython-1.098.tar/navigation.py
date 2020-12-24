# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/navigation.py
# Compiled at: 2013-09-20 11:32:44
""" _dryxTBS_navigation
==================================
:Summary:
    Navigation component partial for dryxTwitterBootstrap module

:Author:
    David Young

:Date Created:
    March 15, 2013

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script please email me: d.r.young@qub.ac.uk """

def responsive_navigation_bar(shade='dark', brand=False, outsideNavList=False, insideNavList=False, htmlId=False, onPhone=True, onTablet=True, onDesktop=True):
    """ Create a twitter bootstrap responsive nav-bar component

    **Key Arguments:**
        - ``shade`` -- if dark then colors are inverted [ False | 'dark' ]
        - ``brand`` -- the website brand [ image | text ]
        - ``outsideNavList`` -- nav-list to be contained outside collapsible content
        - ``insideNavList`` -- nav-list to be contained inside collapsible content
        - ``htmlId`` --
        - ``onPhone`` -- does this container get displayed on a phone sized screen
        - ``onTablet`` -- does this container get displayed on a tablet sized screen
        - ``onDesktop`` -- does this container get displayed on a desktop sized screen

    **Return:**
        - ``navBar`` -- """
    if 'dark' in shade:
        shade = 'navbar-inverse'
    else:
        shade = ''
    if not brand:
        brand = ''
    else:
        brand = '<a class="brand" href="#">%s</a>' % (brand,)
    if not outsideNavList:
        outsideNavList = ''
    if insideNavList:
        insideNavList = '\n            <div class="nav-collapse collapse">\n                %s\n            </div>\n        ' % (
         insideNavList,)
    else:
        insideNavList = ''
    if htmlId:
        htmlId = 'id="%s" ' % (htmlId,)
    else:
        htmlId = ''
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
    navBar = '\n        <div class="navbar %s %s %s %s" %s>\n            <div class="navbar-inner">\n                <div class="container">\n                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n                        <span class="icon-bar"></span>\n                        <span class="icon-bar"></span>\n                        <span class="icon-bar"></span>\n                    </a>\n                    %s\n                    %s\n                    %s\n                </div>\n            </div>\n         </div>\n    ' % (
     shade,
     onPhone,
     onTablet,
     onDesktop,
     htmlId,
     brand,
     outsideNavList,
     insideNavList)
    return navBar


def nav_list(itemList=[], pull=False, onPhone=True, onTablet=True, onDesktop=True):
    """Create an html list of navigation items from the required python list

    **Key Arguments:**
        - ``itemList`` -- items to be included in the navigation list
        - ``pull`` -- float the nav-list [ False | 'right' | 'left' ]
        - ``onPhone`` -- does this container get displayed on a phone sized screen
        - ``onTablet`` -- does this container get displayed on a tablet sized screen
        - ``onDesktop`` -- does this container get displayed on a desktop sized screen

    **Return:**
        - navList """
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
    navList = '<ul class="nav %s %s %s %s">' % (
     pull,
     onPhone,
     onTablet,
     onDesktop)
    for item in itemList:
        navList += '\n            <li>\n                %s\n            </li>' % (item,)

    navList += '</ul>'
    return navList


def searchbox(size='medium', placeHolder=False, button=False, buttonSize='small', buttonColor='grey', navBar=False, pull=False):
    """Create a Search box

    **Key Arguments:**
        - ``size`` -- size = mini | small | medium | large | xlarge | xxlarge
        - ``placeholder`` -- placeholder text
        - ``button`` -- do you want a search button?
        - ``buttonSize``
        - ``buttonColor``

    **Return:**
        - ``markup`` -- markup for the searchbar """
    if button:
        button = '<button type="submit" class="btn-%s btn-%s">Search</button>' % (buttonSize, buttonColor)
    else:
        button = ''
    if placeHolder:
        placeHolder = 'placeholder="%s" ' % (placeHolder,)
    else:
        placeHolder = ''
    if navBar:
        navBar = 'navbar-search'
    else:
        navBar = ''
    if pull:
        pull = 'pull-%s' % (pull,)
    else:
        pull = ''
    markup = '\n    <form class="form-search pull-right">\n      <input type="text" class="input-%s search-query %s %s" %s>\n      %s\n    </form>\n    ' % (
     size,
     navBar,
     pull,
     placeHolder,
     button)
    return markup


def tabbableNavigation(log, contentDictionary={}, fadeIn=True, direction='top'):
    """ Generate a tabbable Navigation

    **Key Arguments:**
        - ``contentDictionary`` -- the content dictionary { name : content }
        - ``fadeIn`` -- make tabs fade in
        - ``direction`` -- the position of the tabs [ above | below | left | right ]

    **Return:**
        - ``tabbableNavigation`` -- the tabbableNavigation """
    if fadeIn is True:
        fadeIn = 'fade'
    else:
        fadeIn = ''
    titleList = ''
    contentList = ''
    count = 0
    if len(contentDictionary) == 0:
        log.error('contentDictionary has no content')
        return
    for k, v in contentDictionary.iteritems():
        if count == 0:
            titleList += '<li class="active"><a href="#tab%s" data-toggle="tab">%s</a></li>' % (count, k)
            contentList += '\n                <div class="tab-pane active %s" id="tab%s">\n                    <p>%s</p>\n                </div>' % (
             fadeIn, count, v)
        else:
            titleList += '<li><a href="#tab%s" data-toggle="tab">%s</a></li>' % (count, k)
            contentList += '\n                <div class="tab-pane %s" id="tab%s">\n                    <p>%s</p>\n                </div>' % (
             fadeIn, count, v)
        count += 1

    tabbableNavigation = '\n        <div class="tabbable" id="  ">\n            <ul class="nav nav-tabs">\n                %s\n            </ul>\n            <div class="tab-content">\n                %s\n            </div>\n        </div>' % (
     titleList, contentList)
    if direction != 'top':
        tabbableNavigation = '\n            <div class="tabbable tabs-%s" id="  ">\n                <div class="tab-content">\n                    %s\n                </div>\n                <ul class="nav nav-tabs">\n                    %s\n                </ul>\n            </div>' % (
         direction, contentList, titleList)
    return tabbableNavigation


def navBar(brand='', contentDictionary={}, dividers=False, fixedOrStatic=False, location='top', responsive=False, dark=False):
    """ Generate a navBar - TBS style

    **Key Arguments:**
        - ``brand`` -- the website brand [ image | text ]
        - ``contentDictionary`` -- the content dictionary { text : href }
        - ``fixedOrStatic`` -- Fix the navbar to the top or bottom of the viewport, or create a static full-width navbar that scrolls away with the page [ False | fixed | static ]
        - ``location`` -- location of the navigation bar if fixed or static
        - ``dark`` -- Modify the look of the navbar by making it dark

    **Return:**
        - ``navBar`` -- the navBar """
    brand = '<a class="brand" href="#">%s</a>' % (brand,)
    toggleButton = ''
    falseList = [dividers, fixedOrStatic, toggleButton, dark]
    for i in range(len(falseList)):
        if not falseList[i]:
            falseList[i] = ''

    dividers, fixedOrStatic, toggleButton, dark = falseList
    if dividers:
        dividers = '<li class="divider-vertical"></li>'
    titleList = ''
    contentList = ''
    count = 0
    for k, v in contentDictionary.iteritems():
        if count == 0:
            titleList += '<li class="active"><a href="%s">%s</a></li>%s' % (v, k, dividers)
        else:
            titleList += '<li><a href="%s">%s</a></li>%s' % (v, k, dividers)
        count += 1

    titleList = '\n    <ul class="nav" id="  ">\n        %s\n    </ul>\n    ' % (titleList,)
    if fixedOrStatic:
        fixedOrStatic = 'navbar-%s-%s' % (fixedOrStatic, location)
    if responsive:
        toggleButton = '\n            <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n                <span class="icon-bar"></span>\n                <span class="icon-bar"></span>\n                <span class="icon-bar"></span>\n              </a>\n        '
        titleList = '\n            <div class="nav-collapse collapse">\n                %s\n            </div>' % (
         titleList,)
    if dark is True:
        dark = 'navbar-inverse'
    else:
        dark = ''
    navBar = '\n        <div class="navbar %s %s">\n          <div class="navbar-inner">\n            %s\n            %s\n          </div>\n        </div>\n        ' % (
     fixedOrStatic, dark, brand, titleList)
    return navBar


def pagination(listItems='', size='default', align='left'):
    """Generate pagination - TBS style. Simple pagination inspired by Rdio, great for apps and search results.

    **Key Arguments:**
        - ``listItems`` -- the numbered items to be listed within the <ul> of the pagination block
        - ``size`` -- additional pagination block sizes [ "mini" | "small" | "default" | "large" ]
        - ``align`` -- change the alignment of pagination links [ "left" | "center" | "right" ]

    **Return:**
        - ``pagination`` -- the pagination
    """
    if size == 'default':
        size = ''
    else:
        size = 'pagination-%s' % (size,)
    if align == 'left':
        align = ''
    else:
        align = 'pagination-%s' % (align,)
    pagination = '\n        <div class="pagination" id="  ">\n            <ul>\n            %s\n            </ul>\n        </div>' % (listItems,)
    return pagination