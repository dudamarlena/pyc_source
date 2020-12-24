# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/addons.py
# Compiled at: 2013-09-20 06:18:52
""" _dryxTBS_addons
===============================
:Summary:
    addon partial for the dryxTwitterBootstrap module

:Author:
    David Young

:Date Created:
    20130508

:dryx syntax:
    - ``xxx`` = come back here and do some more work
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this code please email me: d.r.young@qub.ac.uk """

def mediaObject(displayType='div', img='', headlineText='', nestedMediaObjects=False):
    """ Generate an abstract object style for building various types of components (like blog comments, Tweets, etc) that feature a left- or right-aligned image alongside textual content.

    **Key Arguments:**
        - ``displayType`` -- the display style of the media object [ "div" | "li" ]
        - ``img`` -- the image to include
        - ``headlineText`` -- the headline text for the object
        - ``nestedMediaObjects`` -- nested media objects to be appended

    **Return:**
        - ``media`` -- the media object """
    falseList = [
     nestedMediaObjects]
    for i in range(len(falseList)):
        if not falseList[i]:
            falseList[i] = ''

    nestedMediaObjects, = falseList
    mediaObject = '\n        <%s class="media" id="  ">\n            %s\n            <div class="media-body">\n                <h4 class="media-heading">%s</h4>\n                ...\n\n                <!-- Nested media object -->\n                %s\n            </div>\n        </%s>' % (
     displayType,
     img,
     headlineText,
     nestedMediaObjects,
     displayType)
    return mediaObject


def well(wellText='', wellSize='default'):
    """Get well. Use the well as a simple effect on an element to give it an inset effect.

    **Key Arguments:**
        - ``wellText`` -- the text to be displayed in the well
        - ``wellSize`` -- the size of the well [ "default" | "large" | "small" ]

    **Return:**
        - ``well`` -- the well """
    if wellSize == 'default':
        wellSize = ''
    else:
        wellSize = 'well-%s' % (wellSize,)
    well = '\n        <div class="well" id="  ">\n            %s\n        </div>' % (wellText,)
    return well


def closeIcon():
    """Get close icon. The generic close icon for dismissing content like modals and alerts.

    **Key Arguments:**

    **Return:**
        - ``closeIcon`` -- the closeIcon """
    closeIcon = '<button class="close">&times;</button>'
    return closeIcon