# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/actions/zope/chpwduser.py
# Compiled at: 2007-12-01 11:00:28
"""Define ``ZopeUserPasswordModifier``, a plug-in which connects to
Zope instances via XML-RPC and tries to change the password of an
user.

$Id: chpwduser.py 42 2007-12-01 16:00:28Z damien.baty $
"""
import logging
from ximenez.actions.action import Action
from ximenez.shared import ConnectionException
from ximenez.shared.zope import ZopeInstance
from ximenez.shared.zope import UnauthorizedException
from ximenez.shared.zope import UserDoNoExistException

def getInstance():
    """Return an instance of ``ZopeUserPasswordModifier``."""
    return ZopeUserPasswordModifier()


class ZopeUserPasswordModifier(Action):
    """An action which changes the password of an user from a
    collection of Zope instances, via XML-RPC.
    """
    __module__ = __name__
    _input_info = ()

    def getInput(self, cl_input=None):
        """Get input from the user."""
        if cl_input:
            Action.getInput(self, cl_input)
            return
        ask = self.askForInput
        self._input = {}
        self._input.update(ask(({'name': 'user', 'prompt': 'User id to change: ', 'required': True}, {'name': 'user_pwd', 'prompt': 'New password: ', 'required': True, 'hidden': True})))
        self._input.update(ask(({'name': 'manager', 'prompt': 'Manager username: ', 'required': True}, {'name': 'manager_pwd', 'prompt': 'Manager password: ', 'required': True, 'hidden': True})))

    def execute(self, instances):
        """Change the password of an user on each item of
        ``instances``.

        ``instances`` is supposed to be a sequence of ``ZopeInstance``
        instances or ``<host>:<port>`` strings.
        """
        manager = self._input['manager']
        manager_pwd = self._input['manager_pwd']
        user = self._input['user']
        user_pwd = self._input['user_pwd']
        for instance in instances:
            try:
                instance.modifyUserPassword(user, user_pwd, manager, manager_pwd)
                logging.info('Changed password of "%s" on "%s".', user, instance)
            except ConnectionException:
                msg = 'Could not connect to "%s".'
                logging.error(msg, instance)
            except UnauthorizedException:
                msg = '"%s" is not authorized to change user\'s password on "%s".'
                logging.error(msg, manager, instance)
            except UserDoNoExistException:
                msg = '"%s" does not exist on "%s".'
                logging.error(msg, user, instance)
            except:
                logging.error('Could not change password of "%s" in "%s" because of an unexpected exception.', user, instance, exc_info=True)