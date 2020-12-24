# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twitabit/controllers/bits.py
# Compiled at: 2008-01-19 12:54:35
import logging
from operator import attrgetter
from twitabit.lib.base import *
log = logging.getLogger(__name__)

class BitsController(BaseController):

    def all(self):
        c.statuses = self.db.Status.by('-when')
        return render('/bits/all.mako')

    def user(self, name):
        c.user = self.db.User.findone(name=name)
        if c.user is None:
            c.name = name
            return render('/bits/user_404.mako')
        c.statuses = reversed(sorted(c.user.m.statuses(), key=attrgetter('when')))
        return render('/bits/user.mako')

    def post(self):
        if c.remote_user is None:
            h.redirect_to('signin')
        tx = c.remote_user.t.change_status()
        tx.text = request.params.get('text', '')
        status = self.db.execute(tx)
        abort(302, request.params.get('_url', ''))
        return