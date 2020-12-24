# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/misc/wingdbstub.py
# Compiled at: 2012-01-30 04:13:19
__doc__ = " wingdbstub.py    -- Debug stub for debuggifying Python programs\n\nCopyright (c) 1999-2001, Archaeopteryx Software, Inc.  All rights reserved.\n\nWritten by Stephan R.A. Deibel and John P. Ehresman\n\nUsage:\n-----\n\nThis is the file that Wing DB users copy into their python project \ndirectory if they want to be able to debug programs that are launched\noutside of the IDE (e.g., CGI scripts, in response to a browser page\nload).\n\nTo use this, edit the configuration values below to match your \nWing IDE installation and requirements of your project.\n\nThen, add the following line to your code:\n\n  import wingdbstub\n\nDebugging will start immediately after this import statements.\n\nNext make sure that your IDE is running and that it's configured\nto do passive listening and accept passive connections from the\nhost the debug program will be running on.\n\nNow, invoking your python file should run the code within the debugger.\nNote, however, that Wing will not stop in the code unless a breakpoint\nset set.\n\nIf the debug process is started before the IDE, or is not listening\nat the time this module is imported then the program will run with\ndebugging until an attach request is seen.  Attaching only works \nif the .wingdebugpw file is present; see the manual for details.\n\nOne win32, you either need to edit WINGHOME in this script or\npass in an environment variable called WINGHOME that points to\nthe Wing IDE installation directory.\n\n"
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