# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/misc/wingdbstub.py
# Compiled at: 2012-01-30 04:13:19
""" wingdbstub.py    -- Debug stub for debuggifying Python programs

Copyright (c) 1999-2001, Archaeopteryx Software, Inc.  All rights reserved.

Written by Stephan R.A. Deibel and John P. Ehresman

Usage:
-----

This is the file that Wing DB users copy into their python project 
directory if they want to be able to debug programs that are launched
outside of the IDE (e.g., CGI scripts, in response to a browser page
load).

To use this, edit the configuration values below to match your 
Wing IDE installation and requirements of your project.

Then, add the following line to your code:

  import wingdbstub

Debugging will start immediately after this import statements.

Next make sure that your IDE is running and that it's configured
to do passive listening and accept passive connections from the
host the debug program will be running on.

Now, invoking your python file should run the code within the debugger.
Note, however, that Wing will not stop in the code unless a breakpoint
set set.

If the debug process is started before the IDE, or is not listening
at the time this module is imported then the program will run with
debugging until an attach request is seen.  Attaching only works 
if the .wingdebugpw file is present; see the manual for details.

One win32, you either need to edit WINGHOME in this script or
pass in an environment variable called WINGHOME that points to
the Wing IDE installation directory.

"""
import sys, os, imp
kWingDebugDisabled = 0
kWingHostPort = 'localhost:50005'
kAttachPort = '50015'
kLogFile = None
kLogVeryVerbose = 0
kEmbedded = 0
kPWFilePath = [
 os.path.dirname(__file__), '$<winguserprofile>']
kPWFileName = 'wingdebugpw'
kExitOnFailure = 0
WINGHOME = '/usr/lib/wingide4.0'
if sys.hexversion >= 50331648:

    def has_key(o, key):
        return key in o


else:

    def has_key(o, key):
        return o.has_key(key)


if WINGHOME == None:
    if has_key(os.environ, 'WINGHOME'):
        WINGHOME = os.environ['WINGHOME']
    else:
        sys.stdout.write('*******************************************************************\n')
        sys.stdout.write('Error: Could not find Wing installation!  You must set WINGHOME or edit\n')
        sys.stdout.write('wingdbstub.py where indicated to point it to the location where\n')
        sys.stdout.write('Wing IDE is installed.\n')
        sys.exit(1)
kUserSettingsDir = None
if kUserSettingsDir is None:
    kUserSettingsDir = os.environ.get('WINGDB_USERSETTINGS')

def _ImportWingdb(winghome, user_settings=None):
    """ Find & import wingdb module. """
    try:
        exec_dict = {}
        execfile(os.path.join(winghome, 'bin', '_patchsupport.py'), exec_dict)
        find_matching = exec_dict['FindMatching']
        dir_list = find_matching('bin', winghome, user_settings)
    except Exception:
        dir_list = []

    dir_list.extend([os.path.join(WINGHOME, 'bin'), os.path.join(WINGHOME, 'src')])
    for path in dir_list:
        try:
            (f, p, d) = imp.find_module('wingdb', [path])
            try:
                return imp.load_module('wingdb', f, p, d)
            finally:
                if f is not None:
                    f.close()

            break
        except ImportError:
            pass

    return


if not has_key(os.environ, 'WINGDB_ACTIVE'):
    debugger = None
if not kWingDebugDisabled and not has_key(os.environ, 'WINGDB_DISABLED') and not has_key(os.environ, 'WINGDB_ACTIVE'):
    exit_on_fail = 0
    try:
        exit_on_fail = os.environ.get('WINGDB_EXITONFAILURE', kExitOnFailure)
        logfile = os.environ.get('WINGDB_LOGFILE', kLogFile)
        if logfile == '-' or logfile == None or len(logfile.strip()) == 0:
            logfile = None
        very_verbose_log = os.environ.get('WINGDB_LOGVERYVERBOSE', kLogVeryVerbose)
        if type(very_verbose_log) == type('') and very_verbose_log.strip() == '':
            very_verbose_log = 0
        hostport = os.environ.get('WINGDB_HOSTPORT', kWingHostPort)
        colonpos = hostport.find(':')
        host = hostport[:colonpos]
        port = int(hostport[colonpos + 1:])
        attachport = int(os.environ.get('WINGDB_ATTACHPORT', kAttachPort))
        embedded = int(os.environ.get('WINGDB_EMBEDDED', kEmbedded))
        if has_key(os.environ, 'WINGDB_PWFILEPATH'):
            pwfile_path = os.environ['WINGDB_PWFILEPATH'].split(os.pathsep)
        else:
            pwfile_path = kPWFilePath
        if has_key(os.environ, 'WINGDB_PWFILENAME'):
            pwfile_name = os.environ['WINGDB_PWFILENAME']
        else:
            pwfile_name = kPWFileName
        wingdb = _ImportWingdb(WINGHOME, kUserSettingsDir)
        if wingdb == None:
            sys.stdout.write('*******************************************************************\n')
            sys.stdout.write('Error: Cannot find wingdb.py in $(WINGHOME)/bin or $(WINGHOME)/src\n')
            sys.stdout.write('Error: Please check the WINGHOME definition in wingdbstub.py\n')
            sys.exit(2)
        netserver = wingdb.FindNetServerModule(WINGHOME, kUserSettingsDir)
        err = wingdb.CreateErrStream(netserver, logfile, very_verbose_log)
        debugger = netserver.CNetworkServer(host, port, attachport, err, pwfile_path=pwfile_path, pwfile_name=pwfile_name, autoquit=not embedded)
        debugger.StartDebug(stophere=0)
        os.environ['WINGDB_ACTIVE'] = '1'
        if debugger.ChannelClosed():
            raise ValueError('Not connected')
    except:
        if exit_on_fail:
            raise

def Ensure(require_connection=1, require_debugger=1):
    """ Ensure the debugger is started and attempt to connect to the IDE if
  not already connected.  Will raise a ValueError if:
  
  * the require_connection arg is true and the debugger is unable to connect
  * the require_debugger arg is true and the debugger cannot be loaded
  """
    if debugger is None:
        if require_debugger:
            raise ValueError('No debugger')
        return
    else:
        if not debugger.DebugActive():
            debugger.StartDebug()
        elif debugger.ChannelClosed():
            debugger.ConnectToClient()
        if require_connection and debugger.ChannelClosed():
            raise ValueError('Not connected')
        return