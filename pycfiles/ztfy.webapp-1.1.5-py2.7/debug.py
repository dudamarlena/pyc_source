# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/webapp/webapp_base/webapp_template/src/webapp/debug.py
# Compiled at: 2011-12-19 03:06:16
import os
from paste.script import command
from paste.deploy import appconfig
from zope.app.debug.debug import Debugger
import zope.app.wsgi

class Shell(command.Command):
    max_args = 1
    min_args = 1
    usage = 'CONFIG_FILE'
    summary = 'Python debug shell with BlueBream application loaded'
    group_name = 'bluebream'
    parser = command.Command.standard_parser(verbose=True)

    def command(self):
        cwd = os.getcwd()
        config_file = self.args[0]
        config_name = 'config:%s' % config_file
        conf = appconfig(config_name, relative_to=cwd)
        zope_conf = conf['zope_conf']
        db = zope.app.wsgi.config(zope_conf)
        debugger = Debugger.fromDatabase(db)
        banner = "Welcome to the interactive debug prompt.\nThe 'root' variable contains the ZODB root folder.\nThe 'app' variable contains the Debugger, 'app.publish(path)' simulates a request."
        __import__('code').interact(banner=banner, local={'debugger': debugger, 'app': debugger, 
           'root': debugger.root()})