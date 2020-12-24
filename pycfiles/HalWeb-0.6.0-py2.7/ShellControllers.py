# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/controllers/ShellControllers.py
# Compiled at: 2012-01-05 21:48:33
import os, sys, logging, new, traceback, types
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from models.ShellModels import Session
from google.appengine.api import users
from google.appengine.ext import db
from lib.halicea.decorators import *
UNPICKLABLE_TYPES = (
 types.ModuleType,
 types.TypeType,
 types.ClassType,
 types.FunctionType)
INITIAL_UNPICKLABLES = [
 'from google.appengine.ext import db',
 'from google.appengine.api import users',
 'import logging',
 'import os',
 'import sys',
 'class Foo(db.Expando):\n  pass']

class StatementController(hrh):
    """Evaluates a python statement in a given session and returns the result.
    """

    @AdminOnly()
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        if not self.params.statement:
            return
        statement = self.params.statement.replace('\r\n', '\n')
        statement += '\n\n'
        try:
            logging.info('Compiling and evaluating:\n%s' % statement)
            compiled = compile(statement, '<string>', 'single')
        except:
            self.response.out.write(traceback.format_exc())
            return

        statement_module = new.module('__main__')
        import __builtin__
        statement_module.__builtins__ = __builtin__
        session = Session.get(self.request.get('session'))
        old_main = sys.modules.get('__main__')
        try:
            sys.modules['__main__'] = statement_module
            statement_module.__name__ = '__main__'
            for code in session.unpicklables:
                exec code in statement_module.__dict__

            for name, val in session.globals_dict().items():
                try:
                    statement_module.__dict__[name] = val
                except:
                    msg = 'Dropping %s since it could not be unpickled.\n' % name
                    self.response.out.write(msg)
                    logging.warning(msg + traceback.format_exc())
                    session.remove_global(name)

            old_globals = dict(statement_module.__dict__)
            try:
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                try:
                    sys.stdout = self.response.out
                    sys.stderr = self.response.out
                    exec compiled in statement_module.__dict__
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

            except:
                self.response.out.write(traceback.format_exc())
                return

            new_globals = {}
            for name, val in statement_module.__dict__.items():
                if name not in old_globals or val != old_globals[name]:
                    new_globals[name] = val

            if True in [ isinstance(val, UNPICKLABLE_TYPES) for val in new_globals.values()
                       ]:
                session.add_unpicklable(statement, new_globals.keys())
                logging.debug('Storing this statement as an unpicklable.')
            else:
                for name, val in new_globals.items():
                    if not name.startswith('__'):
                        session.set_global(name, val)

        finally:
            sys.modules['__main__'] = old_main

        session.put()


class FrontPageController(hrh):
    """Creates a new session and renders the shell.html template.
    """

    @AdminOnly()
    def get(self):
        session_key = self.request.get('session')
        if session_key:
            session = Session.get(session_key)
        else:
            session = Session()
            session.unpicklables = [ db.Text(line) for line in INITIAL_UNPICKLABLES ]
            session_key = session.put()
        session_url = '/?session=%s' % session_key
        vars = {'server_software': os.environ['SERVER_SOFTWARE'], 'python_version': sys.version, 
           'session': str(session_key), 
           'user': users.get_current_user(), 
           'login_url': users.create_login_url(session_url), 
           'logout_url': users.create_logout_url(session_url)}
        self.respond(vars)