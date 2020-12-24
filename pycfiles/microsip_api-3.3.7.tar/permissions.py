# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\core\permissions.py
# Compiled at: 2020-02-26 12:32:17
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from microsip_api.comun.sic_db import first_or_none
from django.contrib.auth.models import User

def setup_app_permissions(**kwargs):
    app_label = kwargs.get('app_label', None)
    permissions = kwargs.get('permissions', None)
    content_type_name = ('{} permissions').format(app_label)
    content_type, created = ContentType.objects.get_or_create(name=content_type_name, defaults={'app_label': app_label, 
       'model': 'unused'})
    for permission in permissions:
        permissionobj, created = Permission.objects.get_or_create(content_type=content_type, codename=permission['codename'], defaults={'name': permission['name']})
        if not created:
            permissionobj.name = permission['name']
            permissionobj.save(update_fields=['name'])

    return


class Permissions(object):
    """
    Clase para sacar los permisos de todas las aplicaciones installadas.
    """

    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username', None)
        self.dj_user = kwargs.get('dj_user', None)
        self.jstree_data = []
        self.permissions = {}
        for app in settings.EXTRA_MODULES:
            self.app_label = app
            self.currentparent = self.app_label.lower()
            app_name = self.app_label.replace('djmicrosip_', '').replace('django_microsip_', '').replace('django_msp_', '').upper()
            self.jstree_data.append({'id': self.app_label.lower(), 'parent': '#', 'text': app_name})
            from django.utils import importlib
            app_config = importlib.import_module(('{}.config').format(self.app_label, self.app_label))
            try:
                self.read_permisions(app_config.PERMISSIONS)
            except Exception:
                pass

        return

    def read_permisions(self, node):
        for node, childs in node.iteritems():
            if self.currentparent == self.app_label.lower():
                new_parentid = ('{}.{}').format(self.app_label, node.lower())
            else:
                new_parentid = ('{}.{}').format(self.currentparent, node.lower())
            if node == 'permissions':
                permissions = childs
                for permission in permissions:
                    if self.app_label in self.permissions:
                        self.permissions[self.app_label].append(permission)
                    else:
                        self.permissions[self.app_label] = [
                         permission]
                    permission_id = permission['codename']
                    permission_object = first_or_none(Permission.objects.filter(content_type__name=self.app_label, codename=permission['codename']))
                    if permission_object:
                        permission_id = permission_object.id
                    selected = False
                    if self.username and permission['codename'] != permission_id:
                        django_user = first_or_none(User.objects.filter(username__exact=self.username))
                        dj_user = first_or_none(User.objects.filter(username__exact=self.dj_user))
                        permiso_str = ('{}.{}').format(self.app_label, permission['codename'])
                        selected = dj_user.has_perm(permiso_str)
                        print permission_id
                        print permiso_str
                        print selected
                    self.jstree_data.append({'id': permission_id, 
                       'parent': self.currentparent, 
                       'text': permission['name'], 
                       'state': {'selected': selected}})

                self.currentparent = self.app_label.lower()
            else:
                self.jstree_data.append({'id': new_parentid, 'parent': self.currentparent, 'text': node})
                self.currentparent = new_parentid
                self.read_permisions(childs)

    def setup_app_permissions(self):
        for app, permissions in self.permissions.iteritems():
            app_label = app
            content_type_name = ('{} permissions').format(app_label)
            content_type, created = ContentType.objects.get_or_create(name=content_type_name, defaults={'app_label': app_label, 
               'model': 'unused'})
            permissions_list = []
            for permission in permissions:
                permissionobj, created = Permission.objects.get_or_create(content_type=content_type, codename=permission['codename'], defaults={'name': permission['name']})
                if not created:
                    permissionobj.name = permission['name']
                    permissionobj.save(update_fields=['name'])
                permissions_list.append(permission['codename'])

            Permission.objects.filter(content_type=content_type).exclude(codename__in=permissions_list).delete()

    def get_permissions(self):
        return self.jstree_data