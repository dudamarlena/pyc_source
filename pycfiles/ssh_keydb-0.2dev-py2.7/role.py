# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ssh_keydb/plugins/role.py
# Compiled at: 2012-09-26 05:09:33
import sys
from model import *
from skeletool.controller import Controller
__all__ = [
 'RoleController']

class RoleController(Controller):

    def list(self, *kargs, **kwargs):
        if len(kargs) > 0:
            raise SyntaxError()
        lst = self.filter(*kargs, **kwargs)
        for item in lst:
            print item

    def filter(self, *args, **opts):
        if len(args) > 0:
            return
        else:
            rolelist = Role.query.filter(None)
            if 'role' in opts:
                rolelist = rolelist.filter_by(role=opts['role'])
            return rolelist.all()

    def set(self, *args, **opts):
        if len(args) != 1:
            raise SyntaxError()
        rolename = args[0]
        role = Role.get_by(role=rolename)
        if role is None:
            role = Role(role=rolename)
        session.flush()
        session.commit()
        return True

    def remove(self, *kargs, **kwargs):
        rolelist = self.filter(*kargs, **kwargs)
        n = len(rolelist)
        if n > 2:
            print 'Warning: remove all %i roles?' % n
            sys.exit(1)
        for role in rolelist:
            role.delete()

        session.flush()
        session.commit()
        return True

    set.usage = {'shortdesc': 'Manage role', 
       'usage': [
               '%(exec)s role set <role>'], 
       'options': {'help': 'displays the current help', 
                   'dbpath=': 'database path (~/.ssh-keydb.db by default)'}, 
       'shortopts': {'help': 'h', 'dbpath': 'd:'}}
    remove.usage = {'shortdesc': 'Manage role', 
       'usage': [
               '%(exec)s role remove [--role=<role>]'], 
       'options': {'help': 'displays the current help', 
                   'dbpath=': 'database path (~/.ssh-keydb.db by default)', 
                   'role=': 'filter by role name'}, 
       'shortopts': {'help': 'h', 'dbpath': 'd:'}}
    list.usage = {'shortdesc': 'Manage role', 
       'usage': [
               '%(exec)s role list [--role=<role>]'], 
       'options': {'help': 'displays the current help', 
                   'dbpath=': 'database path (~/.ssh-keydb.db by default)', 
                   'role=': 'filter by role name'}, 
       'shortopts': {'help': 'h', 'dbpath': 'd:'}}
    usage = {'command': [
                 'role'], 
       'shortdesc': 'Manage role'}


RoleController()
if __name__ == '__main__':
    c = RoleController()
    c.list()