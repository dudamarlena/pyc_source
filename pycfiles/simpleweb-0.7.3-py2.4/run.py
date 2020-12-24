# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/admin/plugins/run.py
# Compiled at: 2007-01-10 11:07:04
import sys, simpleweb

def run(name, args):
    """Usage: simpleweb-admin run 

Start the simpleweb application in the current directory, 
in the internal development web server
        """
    if len(args) > 0:
        simpleweb.utils.msg_err("'%s' takes no arguments" % name)
        sys.exit(0)
    simpleweb.run()