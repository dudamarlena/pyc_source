# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/admin/plugins/help.py
# Compiled at: 2007-01-10 11:07:04
import sys, simpleweb

def help(name, args):
    if len(args) < 1:
        print 'Usage: simpleweb-admin [command]'
        print
        print 'Available Commands:'
        try:
            plugins = __import__('simpleweb.admin.plugins', {}, {}, 'plugins')
        except ImportError, e:
            simpleweb.utils.msg_err('Failed to import simpleweb.admin.plugins: %s' % e)
            sys.exit()
        else:
            for i in plugins.__all__:
                print '  %s' % i.replace('_', '-')

            print '  help'
            print '  help [command]'
    if len(args) == 1:
        command = args[0]
        try:
            module = __import__('simpleweb.admin.plugins.%s' % command, {}, {}, command)
        except ImportError:
            simpleweb.utils.msg_err("Command '%s' is not implemented" % command)
        else:
            sys.stdout.write('%s\n' % getattr(module, command).__doc__)