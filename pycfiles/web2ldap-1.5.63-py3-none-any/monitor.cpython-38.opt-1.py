# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/monitor.py
# Compiled at: 2019-12-01 11:45:40
# Size of source mod 2**32: 7871 bytes
"""
web2ldap.app.monitor: Display (SSL) connection data

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import os, time, socket, threading, pwd, web2ldapcnf, web2ldap.__about__, web2ldap.app.gui, web2ldap.app.handler
from web2ldap.app.session import session_store, cleanUpThread
from web2ldap.utctime import strftimeiso8601
from ..ldapsession import LDAPSession
from ..log import logger, EXC_TYPE_COUNTER
from .core import STARTUP_TIME
from .metrics import METRICS_AVAIL
MONITOR_TEMPLATE = '\n<h1>Monitor</h1>\n\n<h2>System information</h2>\n\n{text_metricsurl}\n\n<table summary="System information">\n  <tr>\n    <td>web2ldap version:</td>\n    <td>{text_version}</td>\n  </tr>\n  <tr>\n    <td>Hostname:</td>\n    <td>{text_sysfqdn}</td>\n  </tr>\n  <tr>\n    <td>PID / PPID:</td>\n    <td>{int_pid:d} / {int_ppid:d}</td>\n  </tr>\n  <tr>\n    <td>UID:</td>\n    <td>{text_username} ({int_uid:d})</td>\n  </tr>\n</table>\n\n<h3>Time information</h3>\n<table summary="Time information">\n  <tr>\n    <td>Current time:</td>\n    <td>{text_currenttime}</td>\n  </tr>\n  <tr>\n    <td>Startup time:</td>\n    <td>{text_startuptime}</td>\n  </tr>\n  <tr>\n    <td>Uptime:</td>\n    <td>{text_uptime}</td>\n  </tr>\n</table>\n\n<h3>{int_numthreads:d} active threads:</h3>\n<ul>\n  {text_threadlist}\n</ul>\n\n<h2>Session counters</h2>\n<table summary="Session counters">\n  <tr>\n    <td>Web sessions initialized:</td>\n    <td>{int_sessioncounter:d}</td>\n  </tr>\n  <tr>\n    <td>Max. concurrent sessions:</td>\n    <td>{int_maxconcurrentsessions:d}</td>\n  </tr>\n  <tr>\n    <td>Sessions removed after timeout:</td>\n    <td>{int_removedsessions:d}</td>\n  </tr>\n  <tr>\n    <td>Web session limit:</td>\n    <td>{int_sessionlimit:d}</td>\n  </tr>\n  <tr>\n    <td>Web session limit per remote IP:</td>\n    <td>{int_sessionlimitperip:d}</td>\n  </tr>\n  <tr>\n    <td>Session removal time:</td>\n    <td>{int_sessionremoveperiod:d}</td>\n  </tr>\n  <tr>\n    <td>Currently active remote IPs:</td>\n    <td>{int_currentnumremoteipaddrs:d}</td>\n  </tr>\n</table>\n\n<h3>{int_numremoteipaddrs:d} remote IPs seen:</h3>\n<table>\n  <tr><th>Remote IP</th><th>Count</th></tr>\n  {text_remoteiphitlist}\n</table>\n\n<h3>Command URLs:</h3>\n<table>\n  <tr><th>URL</th><th>Count</th></tr>\n  {text_cmd_counters}\n</table>\n\n<h3>Unhandled exceptions:</h3>\n<table>\n  <tr><th>Exception</th><th>Count</th></tr>\n  {text_exc_counters}\n</table>\n\n<h2>Active sessions</h2>\n'
MONITOR_CONNECTIONS_TMPL = '\n<h3>%d active LDAP connections:</h3>\n<table summary="Active LDAP connections">\n  <tr>\n    <th>Remote IP</th>\n    <th>Last access time</th>\n    <th>Target URI</th>\n    <th>Bound as</th>\n  </tr>\n  %s\n</table>\n'
MONITOR_SESSIONS_JUST_CREATED_TMPL = '\n<h3>%d sessions just created:</h3>\n<table summary="Sessions not fully initialized">\n  <tr>\n    <th>Creation time</th>\n  </tr>\n  %s\n</table>\n'

def get_uptime() -> float:
    """
    returns seconds since start
    """
    return time.time() - STARTUP_TIME


def get_user_info() -> tuple:
    """
    returns tuple of numeric POSIX-ID and accompanying user name (if found)
    """
    uid = os.getuid()
    try:
        username = pwd.getpwuid(uid).pw_name
    except KeyError:
        username = None
    else:
        return (
         uid, username)


def w2l_monitor(app):
    """
    List several general gateway stats
    """
    uptime = get_uptime()
    posix_uid, posix_username = get_user_info()
    web2ldap.app.gui.top_section(app, 'Monitor', web2ldap.app.gui.simple_main_menu(app), [])
    monitor_tmpl_vars = dict(text_metricsurl=(METRICS_AVAIL * app.anchor('metrics', 'Metrics endpoint', [])),
      text_version=(web2ldap.__about__.__version__),
      text_sysfqdn=(socket.getfqdn()),
      int_pid=(os.getpid()),
      int_ppid=(os.getppid()),
      text_username=(app.form.utf2display(posix_username or '-/-')),
      int_uid=posix_uid,
      text_currenttime=(strftimeiso8601(time.gmtime(time.time()))),
      text_startuptime=(strftimeiso8601(time.gmtime(STARTUP_TIME))),
      text_uptime=('%02d:%02d' % (int(uptime // 3600), int(uptime // 60 % 60))),
      int_numthreads=(threading.activeCount()),
      text_threadlist=('\n'.join(['<li>%s</li>' % ''.join([
     app.form.utf2display(str(repr(t))),
     ', alive' * t.is_alive(),
     ', daemon' * t.isDaemon()]) for t in threading.enumerate()])),
      int_sessioncounter=(session_store.sessionCounter),
      int_maxconcurrentsessions=(session_store.max_concurrent_sessions),
      int_removedsessions=(cleanUpThread.removed_sessions),
      int_sessionlimit=(web2ldapcnf.session_limit),
      int_sessionlimitperip=(web2ldapcnf.session_per_ip_limit),
      int_sessionremoveperiod=(session_store.session_ttl),
      int_currentnumremoteipaddrs=(len(session_store.remote_ip_sessions)),
      int_numremoteipaddrs=(len(session_store.remote_ip_counter)),
      text_remoteiphitlist=('\n'.join(['<tr><td>%s</td><td>%d</td></tr>' % (
     app.form.utf2display(ip or '-'),
     count) for ip, count in session_store.remote_ip_counter.most_common()])),
      text_cmd_counters=('\n'.join(['<tr><td>%s</td><td>%d</td></tr>' % (
     app.form.utf2display(cmd),
     ctr) for cmd, ctr in sorted(web2ldap.app.handler.COMMAND_COUNT.items())])),
      text_exc_counters=('\n'.join(['<tr><td>%s</td><td>%d</td></tr>' % (
     app.form.utf2display(str(exc_type)),
     exc_ctr) for exc_type, exc_ctr in EXC_TYPE_COUNTER.items()])))
    app.outf.write((MONITOR_TEMPLATE.format)(**monitor_tmpl_vars))
    if session_store.sessiondict:
        real_ldap_sessions = []
        fresh_ldap_sessions = []
        for k, i in session_store.sessiondict.items():
            if not k.startswith('__'):
                if isinstance(i[1], LDAPSession):
                    if i[1].uri:
                        real_ldap_sessions.append((k, i))
                fresh_ldap_sessions.append((k, i))
            if real_ldap_sessions:
                app.outf.write(MONITOR_CONNECTIONS_TMPL % (
                 len(real_ldap_sessions),
                 '\n'.join(['<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(app.form.utf2display(i[1].onBehalf or '' or 'unknown'), strftimeiso8601(time.gmtime(i[0])), app.form.utf2display(i[1].uri or 'no connection'), app.form.utf2display(i[1].who or 'anonymous')) for k, i in real_ldap_sessions])))
            if fresh_ldap_sessions:
                app.outf.write(MONITOR_SESSIONS_JUST_CREATED_TMPL % (
                 len(fresh_ldap_sessions),
                 '\n'.join(['<tr><td>{}</td></tr>'.format(strftimeiso8601(time.gmtime(i[0]))) for k, i in fresh_ldap_sessions])))

    else:
        app.outf.write('No active sessions.\n')
    web2ldap.app.gui.footer(app)