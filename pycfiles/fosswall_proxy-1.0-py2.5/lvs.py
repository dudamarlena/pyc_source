# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fosswallproxy0/lvs.py
# Compiled at: 2008-02-20 19:10:43
import sys, commands
from base import *
from lvsconf import lvsconf

class LVS(Base):
    filename = BASE_DIR + '/lvs.cf'
    conf = lvsconf.LVSConf(filename)

    def copy(self):
        cp_command = 'sudo scp %s root@lbslave:/etc/ha.d/haresources > /dev/null 2>&1 &' % self.filename
        stat = os.system(cp_command)
        stat = commands.get_output(cp_command)

    @expose(template='fosswallproxy.templates.view')
    def view(self):
        return dict(title='LVS', conf=str(self.conf))