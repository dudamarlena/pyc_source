# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/main/utils.py
# Compiled at: 2019-09-28 15:53:13
# Size of source mod 2**32: 788 bytes
from flask import url_for
from ..models import ObjectMenuItem
from utils.menu import MenuItem, VisibilityOptions

def menu_items():
    q = ObjectMenuItem.query.filter_by(active=True).order_by(ObjectMenuItem.menu_order, ObjectMenuItem.title)
    return q


def menu_tools():
    return [
     MenuItem('zaloguj', url_for('auth.login'), VisibilityOptions(True, False)),
     MenuItem('profil', url_for('user.profile'), VisibilityOptions(False, True)),
     MenuItem('wyloguj', url_for('auth.logout'), VisibilityOptions(False, True))]


def admin_tools():
    return [
     MenuItem('administracja', url_for('admin.home'), VisibilityOptions(False, True))]