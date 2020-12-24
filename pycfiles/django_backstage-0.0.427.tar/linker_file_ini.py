# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/utils/uwsgi/linker_file_ini.py
# Compiled at: 2014-07-07 12:51:00
import os

def start(inst):
    """
    Start a backstage instance by *linking* it's INI file
    @param inst: Backstage Instance, such as an Act
    @return:
    """
    if not os.path.exists(inst.uwsgi_file):
        with open(inst.uwsgi_file, 'w') as (f):
            f.write(inst.uwsgi_ini)
    if os.path.exists(inst.uwsgi_vassal):
        try:
            a = inst.name
        except NameError:
            a = ''

        print 'Vassal file already exists. Hint: try %s.restart() instead' % a
        return
    os.symlink(inst.uwsgi_file, inst.uwsgi_vassal)
    print 'start request submitted for %s' % inst.name


def stop(inst):
    """
    Stop a backstage instance by *unlinking* it's INI file
    @param inst: Backstage Instance, such as an Act
    @return:
    """
    if not os.path.exists(inst.uwsgi_vassal):
        print 'vassal %s not running' % inst.name
        return
    else:
        try:
            os.unlink(inst.uwsgi_vassal)
            print 'stop request submitted for %s' % inst.name
        except:
            print 'error unlinking vassal'
            return

        inst.uwsgi_port = None
        return


def restart(inst):
    """
    Re-start a backstage instance by *touching* it's INI file
    @param inst: Backstage Instance, such as an Act
    @return:
    """
    try:
        with file(inst.uwsgi_file, 'a'):
            os.utime(inst.uwsgi_file, None)
    except IOError:
        print 'Could not update, permission denied.'
        return

    print 're-start request submitted for %s' % inst.name
    return