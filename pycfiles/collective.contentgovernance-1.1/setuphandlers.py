# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentgenerator/setuphandlers.py
# Compiled at: 2009-01-19 09:24:11
from collective.contentgenerator.ContentGenerator import ContentSetup
from collective.contentgenerator.UserGenerator import UserSetup

def runSetup(context, content, users):
    """ Runs the content and user generation methods """
    if context.readDataFile('collective.contentgenerator_various.txt') is None:
        return
    portal = context.getSite()
    cs = ContentSetup()
    cs.customize(portal, context, content)
    cu = UserSetup()
    cu.customize(portal, context, users)
    return


def setupVarious(context):
    """ Run this content / user creation after standard generic setup
        This default setting just adds minimal token content for testing
        Default settings for test content = 1 min ~ 1 Mb """
    content = {'sectioncount': 1, 'foldercount': 1, 'itemcount': 2, 'imagecount': 1, 'bigimagecount': 0, 'multiply': 1, 'profile': 'default'}
    users = {'groups': 2, 'memberships': 2, 'local': True, 'users': 10}
    runSetup(context, content, users)


def setupIntranet(context):
    """ Run this content / user creation after standard generic setup handling
        Default settings for intranet ~ 10 mins ~ 200 Mb """
    content = {'sectioncount': 3, 'foldercount': 5, 'itemcount': 10, 'imagecount': 5, 'bigimagecount': 5, 'multiply': 2, 'profile': 'intranet'}
    users = {'groups': 10, 'memberships': 10, 'local': False, 'users': 100}
    runSetup(context, content, users)


def setupPublic(context):
    """ Run this content / user creation after standard generic setup handling
        Default settings for public site ~ 20 mins ~ 200 Mb """
    content = {'sectioncount': 5, 'foldercount': 10, 'itemcount': 20, 'imagecount': 5, 'bigimagecount': 1, 'multiply': 2, 'profile': 'public'}
    users = {'groups': 500, 'memberships': 20, 'local': True, 'users': 2000}
    runSetup(context, content, users)