# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/formalworkflow/setuphandlers.py
# Compiled at: 2013-06-23 12:02:23


def setupVarious(context):
    """ Install plone.app.iterate if its not installed already """
    if context.readDataFile('ilrt.formalworkflow_various.txt') is None:
        return
    else:
        from Products.CMFCore.utils import getToolByName
        portal = context.getSite()
        qi_tool = getToolByName(portal, 'portal_quickinstaller')
        if not qi_tool.isProductInstalled('plone.app.iterate'):
            qi_tool.installProduct('plone.app.iterate', swallowExceptions=1)
            from Products.Five import zcml
            import ilrt.formalworkflow
            zcml.load_config('configure.zcml', ilrt.formalworkflow)
            gsetup = getToolByName(portal, 'portal_setup')
            gsetup.manage_importSelectedSteps(context_id='profile-ilrt.formalworkflow:formalworkflow', ids=[
             'actions', 'workflow'], run_dependencies=True)
        return