# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/webserver.py
# Compiled at: 2007-01-10 11:07:05
import os, pwd, grp
from wsgiref.simple_server import make_server
import simpleweb.utils

def wsgiserve(wsgiapp, host='127.0.0.1', port=8080, reload=True, user='nobody', group='nobody', infomsg=None, warnmsg=None):
    if reload:
        reload_status = 'On'
    else:
        reload_status = 'Off'
    server = make_server(host, port, wsgiapp)
    if os.geteuid() == 0:
        try:
            gid = grp.getgrnam(group)[2]
            uid = pwd.getpwnam(user)[3]
        except KeyError:
            simpleweb.utils.msg_err("Could not find the specified user/group on the system, ignoring and running as '%s'" % pwd.getpwuid(os.geteuid())[0])
        else:
            if os.name == 'posix':
                os.setgid(gid)
                os.setuid(uid)
    simpleweb.utils.msg_info('simpleweb.webserver - v0.2')
    simpleweb.utils.msg_info('Based on wsgiref.simple_server')
    if infomsg:
        simpleweb.utils.msg_info(infomsg)
    if warnmsg:
        simpleweb.utils.msg_warn(warnmsg)
    simpleweb.utils.msg_info('Now Serving on %s port %s [reloading = %s]...' % (host, port, reload_status))
    server.serve_forever()