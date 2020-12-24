# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fosswallproxy0/heartbeat.py
# Compiled at: 2008-02-20 19:25:13
import sys, commands
from base import *
from heartbeatconf import HeartBeatConf

class HeartBeat(Base):
    filename = BASE_DIR + '/ha.d/ha.cf'
    conf = HeartBeatConf(filename)

    def copy(self):
        cmd = 'sudo scp %s root@lbslave:/etc/ha.d/haresources > /dev/null 2>&1 &' % self.filename
        stat = os.system(cmd)
        stat = commands.get_output(cmd)

    @expose('fosswallproxy.templates.heartbeat')
    def edit_conf(self, action=None, **kw):
        if action is None:
            action = 'modify'
        else:
            options = ('serial', 'bcast', 'keepalive', 'deadtime', 'warntime', 'ping',
                       'auto_failback')
            for (k, v) in kw.iteritems():
                if k in options:
                    setattr(self.conf, k, v)

            if kw['ping'] == '':
                self.conf.ping = None
            print self.conf.logfile
            self.conf.write()
            flash('Successfully modified heartbeat configuration')
        return dict(action='modify', conf=self.conf, title='HeartBeat Configuration')

    @expose('fosswallproxy.templates.view')
    def view(self):
        return dict(title='Heartbeat Configuration', conf=str(self.conf))