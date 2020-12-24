# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\utils.py
# Compiled at: 2009-03-02 16:14:25
from copy import copy
IS_PLONE_21 = False
IS_PLONE_25 = False
IS_PLONE_30 = False
IS_PLONE_31 = False
try:
    from Products.CMFPlone.migrations import v2_1
    IS_PLONE_21 = True
except ImportError:
    pass

try:
    from Products.CMFPlone.migrations import v2_5
    IS_PLONE_21 = False
    IS_PLONE_25 = True
except ImportError:
    pass

try:
    from Products.CMFPlone.migrations import v3_0
    IS_PLONE_21 = False
    IS_PLONE_25 = False
    IS_PLONE_30 = True
except ImportError:
    pass

try:
    from Products.CMFPlone.migrations import v3_1
    IS_PLONE_21 = False
    IS_PLONE_25 = False
    IS_PLONE_30 = False
    IS_PLONE_31 = True
except ImportError:
    pass

def updateActions(klass, actions):
    """
    Merge the actions from a class with a list of actions.
    Copied from ATcontentTypes because it doesn't exists in Plone3
    """
    if hasattr(klass, 'actions'):
        kactions = copy(klass.actions)
        aids = [ action.get('id') for action in actions ]
        actions = list(actions)
        for kaction in kactions:
            kaid = kaction.get('id')
            if kaid not in aids:
                actions.append(kaction)

        return tuple(actions)
    else:
        return ()