# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/admin/console.py
# Compiled at: 2007-01-10 11:07:05
import sys, os, simpleweb.utils

def main():
    command = 'run'
    name = os.path.basename(sys.argv[0])
    del sys.argv[0]
    try:
        command = sys.argv[0]
        command = command.replace('-', '_')
        del sys.argv[0]
    except IndexError:
        pass

    args = sys.argv
    try:
        module = __import__('simpleweb.admin.plugins.' + command, {}, {}, command)
        func = vars(module)[command]
        name = '%s %s' % (name, command)
    except ImportError, e:
        simpleweb.utils.msg_err('Error loading the plugin : %s' % e)
        return
    except KeyError, e:
        simpleweb.utils.msg_err('Function %s is not defined in plugin module %s' % (command, command))
        return

    func(name, args)