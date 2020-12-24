# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\app.py
# Compiled at: 2011-03-08 21:41:16
"""
This is a helper module for the framework start-up process.  It takes care of:

  * Initialising logging.
  * Instantiating the application's main loop subclass.
  * Starting the basic framework services.
"""
import logging, sys
from . import loginit
logging.root.setLevel(logging.DEBUG)
app = None

def InitializeApp(appClass, appname, redirectOutput=True, redirectLoggerToStdOut=False, **kw):
    global app
    loginit.Init(redirectOutput=redirectOutput, redirectLoggerToStdOut=redirectLoggerToStdOut)
    logging.root.info('Application %s starting up', appname)
    app = appClass(appname, **kw)
    app.InitConfigFiles()
    app.PostInitConfigFiles()
    from . import session
    from . import process
    from . import login
    services = [
     session.SessionManager,
     process.TaskletPool,
     login.LoginService]
    services.extend(app.GetAppServiceClasses())
    app.InitServices(services)
    return app