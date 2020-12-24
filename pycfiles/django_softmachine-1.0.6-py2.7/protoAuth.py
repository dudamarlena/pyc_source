# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoAuth.py
# Compiled at: 2014-06-19 11:12:01
from models import UserProfile, TeamHierarchy

def getUserProfile(pUser, action, actionInfo):
    """
    Obtiene el profile de usuario, permitira retornar valores como el
    idioma y otros eltos del entorno,

    Permitira tambien el manejo de logs,

    action :
    - login
    - saveData
    - loadData
    - saveConfig

    actionInfo :
    - Entidad, ids, fecha etc

    Se puede crear una sesion propia para manejar el log de autorizaciones
    permitira cerrar una sesion cambiando el estado tal como se maneja en sm

    """
    if pUser is None:
        return
    else:
        uProfile = UserProfile.objects.get_or_create(user=pUser)[0]
        if uProfile.userTeam is None:
            uProfile.userTeam = TeamHierarchy.objects.get_or_create(code='proto')[0]
            uProfile.save()
        if action == 'login':
            uOrgTree = uProfile.userTeam.treeHierarchy
            for item in pUser.usershare_set.all():
                uOrgTree += ',' + item.userTeam.treeHierarchy

            uProfile.userTree = (',').join(set(uOrgTree.split(',')))
            uProfile.save()
            usrLanguage = uProfile.language
            if usrLanguage not in ('es', 'en', 'fr'):
                usrLanguage = 'fr'
            usrLanguage = 'protoLib.localisation.' + usrLanguage
            myModule = __import__(usrLanguage, globals(), locals(), ['__language'], -1)
            return myModule.__language
        return uProfile


def getUserNodes(pUser, viewEntity):
    userProfile = getUserProfile(pUser, 'list', viewEntity)
    userNodes = None
    if userProfile and userProfile.userTree:
        userNodes = userProfile.userTree.split(',')
    return userNodes


def getModelPermissions(pUser, model, perm=None):
    appName = model._meta.app_label
    modName = model._meta.module_name
    permissions = {}

    def getIndPermission(perm):
        permissions[perm] = pUser.is_superuser or pUser.has_perm(appName + '.' + perm + '_' + modName)

    if perm is not None:
        getIndPermission(perm)
        return permissions[perm]
    else:
        getIndPermission('menu')
        getIndPermission('list')
        getIndPermission('add')
        getIndPermission('change')
        getIndPermission('delete')
        getIndPermission('config')
        getIndPermission('custom')
        getIndPermission('refallow')
        return permissions


def activityLog(action, user, option, info):
    pass