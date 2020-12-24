# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/images.py
# Compiled at: 2013-08-06 07:04:47
"""
_dryxTBS_images
=============================
:Summary:
    Partial for the dryxTwitterBootstrap module

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

def image(src='http://placehold.it/200x200', href=False, display='False', pull='left', htmlClass=False, thumbnail=False, width=False, onPhone=True, onTablet=True, onDesktop=True):
    """Create an HTML image (with ot without link).
    Based on the Twitter bootstrap setup.

    **Key Arguments:**
        - ``src`` -- image url
        - ``href`` -- image link url
        - ``display`` -- how the image is to be displayed [ rounded | circle | polaroid ]
        - ``pull`` -- how to align the image if within a <div> [ "left" | "right" | "center" ]
        - ``htmlClass`` -- the class of the row
        - ``width`` -- the width of the image
        - ``onPhone`` -- does this container get displayed on a phone sized screen
        - ``onTablet`` -- does this container get displayed on a tablet sized screen
        - ``onDesktop`` -- does this container get displayed on a desktop sized screen

    **Return:**
        - ``image`` - the formatted image
    """
    falseList = [
     thumbnail, pull]
    for i in range(len(falseList)):
        if not falseList[i]:
            falseList[i] = ''

    thumbnail, pull = falseList
    if thumbnail is True:
        thumbnail = 'thumbnail'
    if pull:
        pull = 'pull-%s' % (pull,)
    if not display:
        display = ''
    else:
        display = 'img-%s' % (display,)
    if not htmlClass:
        htmlClass = ''
    if width:
        width = 'width=%s' % (width,)
    else:
        width = ''
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
    image = '<img src="%s" class="%s %s %s %s %s" %s>' % (src, display, htmlClass, onPhone, onTablet, onDesktop, width)
    if href:
        image = '<a href="%s" class="%s %s %s %s %s">%s</a>' % (href, thumbnail, onPhone, onTablet, onDesktop, pull, image)
    return image


def thumbnail(htmlContent=''):
    """Generate a thumbnail - TBS style

    **Key Arguments:**
        - ``htmlContent`` -- the html content of the thumbnail

    **Return:**
        - ``thumbnail`` -- the thumbnail with HTML content
    """
    thumbnail = '\n        <div class="thumbnail" id="  ">\n            %s\n        </div>' % (htmlContent,)
    return thumbnail