# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/demoSetup.py
# Compiled at: 2010-10-22 19:01:08
import transaction
from zope.app.folder import Folder
from zope.app import zapi
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.securitypolicy.interfaces import IPrincipalPermissionManager
from zope.securitypolicy.interfaces import IPrincipalRoleManager

class Participation:
    __module__ = __name__
    interaction = None


class CreateStructure(object):
    __module__ = __name__

    def __init__(self, event):
        """ This method gets called on IDatabaseOpenedEvent when running the
            Demo we add some seemingly random security permissions to the
            folder tree created below so users of the demo can see what
            security tool can display
        """
        (db, connection, root, root_folder) = getInformationFromEvent(event)
        root = zapi.getRoot(root_folder)
        if 'Folder1' not in root:
            root['Folder1'] = Folder()
        if 'Folder2' not in root['Folder1']:
            root['Folder1']['Folder2'] = Folder()
        if 'Folder3' not in root['Folder1']['Folder2']:
            root['Folder1']['Folder2']['Folder3'] = Folder()
        sysPrincipals = zapi.principals()
        principals = [ x.id for x in sysPrincipals.getPrincipals('') if x.id not in ['zope.group1', 'zope.group2', 'zope.randy'] ]
        roleManager = IPrincipalRoleManager(root)
        permManager = IPrincipalPermissionManager(root)
        roleManager.assignRoleToPrincipal('zope.Editor', 'zope.group1')
        group1 = sysPrincipals.getPrincipal('zope.group1')
        group2 = sysPrincipals.getPrincipal('zope.group2')
        daniel = sysPrincipals.getPrincipal('zope.daniel')
        randy = sysPrincipals.getPrincipal('zope.randy')
        randy.groups.append('zope.group1')
        randy.groups.append('zope.group2')
        daniel.groups.append('zope.randy')
        roleManager.assignRoleToPrincipal('zope.Writer', 'zope.daniel')
        roleManager.assignRoleToPrincipal('zope.Writer', 'zope.stephan')
        for principal in principals:
            permManager.grantPermissionToPrincipal('concord.ReadIssue', principal)
            permManager.denyPermissionToPrincipal('concord.DeleteArticle', principal)
            permManager.denyPermissionToPrincipal('concord.CreateArticle', principal)

        for perm in ['concord.DeleteIssue', 'concord.CreateIssue', 'concord.ReadIssue', 'concord.CreateArticle', 'concord.DeleteArticle', 'concord.PublishIssue']:
            permManager.denyPermissionToPrincipal(perm, group1.id)
            permManager.grantPermissionToPrincipal(perm, group2.id)

        roleManager = IPrincipalRoleManager(root['Folder1'])
        permManager = IPrincipalPermissionManager(root['Folder1'])
        roleManager.assignRoleToPrincipal('zope.Janitor', 'zope.markus')
        roleManager.assignRoleToPrincipal('zope.Writer', 'zope.daniel')
        for principal in principals:
            permManager.denyPermissionToPrincipal('concord.ReadIssue', principal)
            permManager.grantPermissionToPrincipal('concord.DeleteIssue', principal)
            permManager.grantPermissionToPrincipal('concord.CreateArticle', principal)

        roleManager = IPrincipalRoleManager(root['Folder1']['Folder2'])
        permManager = IPrincipalPermissionManager(root['Folder1']['Folder2'])
        roleManager.assignRoleToPrincipal('zope.Janitor', 'zope.markus')
        roleManager.assignRoleToPrincipal('zope.Writer', 'zope.daniel')
        permManager.denyPermissionToPrincipal('concord.CreateArticle', 'zope.daniel')
        permManager.denyPermissionToPrincipal('concord.CreateIssue', 'zope.daniel')
        permManager.denyPermissionToPrincipal('concord.CreateIssue', 'zope.stephan')
        permManager.denyPermissionToPrincipal('concord.CreateIssue', 'zope.markus')
        permManager.denyPermissionToPrincipal('concord.CreateIssue', 'zope.anybody')
        roleManager = IPrincipalRoleManager(root['Folder1']['Folder2']['Folder3'])
        permManager = IPrincipalPermissionManager(root['Folder1']['Folder2']['Folder3'])
        roleManager.removeRoleFromPrincipal('zope.Writer', 'zope.daniel')
        roleManager.removeRoleFromPrincipal('zope.Janitor', 'zope.markus')
        transaction.commit()