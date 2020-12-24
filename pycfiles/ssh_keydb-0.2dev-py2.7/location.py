# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ssh_keydb/plugins/location.py
# Compiled at: 2012-09-26 05:09:33
import sys
from model import *
from skeletool.controller import Controller
__all__ = [
 'LocationController']

class LocationController(Controller):

    def set(self, *kargs, **kwargs):
        if len(kargs) != 1:
            raise SyntaxError()
        locname = kargs[0]
        location = Location.get_by(location=locname)
        if location is not None:
            print 'Error: already exists.'
            raise AlreadyExists()
        location = Location(location=locname)
        session.flush()
        session.commit()
        return True

    def remove(self, *kargs, **kwargs):
        loclst = self.filter(*kargs, **kwargs)
        n = len(loclst)
        if n > 2:
            ch = raw_input('Warning: remove all %i locations (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)
        for loc in loclst:
            print 'Deleting %s...' % loc.location
            loc.delete()

    def filter(self, *kargs, **kwargs):
        if len(kargs) > 1:
            raise SyntaxError()
        if len(kargs) > 0:
            locname = kargs[0]
            loclst = Location.query.filter_by(location=locname)
        else:
            loclst = Location.query.filter(None)
        return loclst.all()

    def list(self, *kargs, **kwargs):
        if len(kargs) > 0:
            raise SyntaxError()
        print self.filter(*kargs, **kwargs)

    set.usage = {'shortdesc': 'Manage location', 
       'usage': [
               '%(exec)s location set <location>'], 
       'options': {'help': 'displays the current help', 
                   'dbpath=': 'database path (~/.ssh-keydb.db by default)'}, 
       'shortopts': {'help': 'h', 'dbpath': 'd:'}}
    remove.usage = {'shortdesc': 'Manage location', 
       'usage': [
               '%(exec)s location remove <location>'], 
       'options': {'help': 'displays the current help', 
                   'dbpath=': 'database path (~/.ssh-keydb.db by default)'}, 
       'shortopts': {'help': 'h', 'dbpath': 'd:'}}
    list.usage = {'shortdesc': 'Manage location', 
       'usage': [
               '%(exec)s location list [<location>]'], 
       'options': {'help': 'displays the current help', 
                   'dbpath=': 'database path (~/.ssh-keydb.db by default)'}, 
       'shortopts': {'help': 'h', 'dbpath': 'd:'}}
    usage = {'command': [
                 'location', 'loc'], 
       'shortdesc': 'Manage location'}


LocationController()
if __name__ == '__main__':
    c = LocationController()
    c.list()