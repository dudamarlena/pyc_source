# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twitabit/schema/twitabit_001.py
# Compiled at: 2008-01-19 12:54:35
"""twitabit schema version 1."""
from schevo.schema import *
schevo.schema.prep(locals())
import datetime, random, string

class Status(E.Entity):
    user = f.entity('User', on_delete=CASCADE)
    text = f.unicode(max_size=140)
    when = f.datetime(default=datetime.datetime.now)
    _index(when)
    _plural = 'Statuses'
    _hide('t_create', 't_delete', 't_update')

    class _Create(T.Create):

        def _after_execute(self, db, status):
            db.execute(self.user.t.update(current_status=status))

    _initial = [
     (
      ('admin', ), 'Created a new twitabit database!', DEFAULT)]
    _initial_priority = 2


class User(E.Entity):
    name = f.unicode()
    password = f.hashed_password()
    current_status = f.entity('Status', required=False)
    _key(name)
    _hide('t_create', 't_delete', 't_update')

    def t_change_password(self):
        tx = self.t.update()
        tx.f.name.hidden = True
        tx.f.current_status.hidden = True
        relabel(tx, 'Change Password')
        return tx

    def t_change_status(self):
        tx = db.Status.t.create()
        tx.user = self
        tx.f.user.hidden = True
        tx.f.when.hidden = True
        relabel(tx, 'Change Status')
        return tx

    @staticmethod
    def _initial(db):
        alphanum = string.lowercase + string.digits
        random_password = ('').join((random.choice(alphanum) for x in xrange(8)))
        print '  * admin password is %r' % random_password
        return [
         (
          'admin', random_password, UNASSIGNED)]

    _initial_priority = 1