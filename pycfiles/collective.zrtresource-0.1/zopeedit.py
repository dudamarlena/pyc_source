# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/zopeedit/zopeedit.py
# Compiled at: 2011-03-04 07:55:43
__doc__ = 'Zope External Editor Helper Application\nhttp://plone.org/products/zope-externaleditor-client'
APP_NAME = 'zopeedit'
import sys, os
try:
    system_path = os.path.split(__file__)[0]
except NameError:
    system_path = os.path.realpath(os.path.dirname(sys.argv[0]))

try:
    f = open(os.path.join(system_path, 'docs/VERSION.txt'), 'r')
except IOError:
    f = open(os.path.join(system_path, '../../docs/VERSION.txt'), 'r')

__version__ = f.readline()[:-1]
f.close()
from sys import platform, version_info
py3 = version_info[0] == 3
win32 = sys.platform == 'win32'
osx = sys.platform == 'darwin'
linux = sys.platform == 'linux2'
if win32:
    from os import startfile
    import pythoncom, pywintypes, warnings
    warnings.filterwarnings('ignore')
if osx:
    from LaunchServices import LSOpenFSRef
import re
from subprocess import Popen, call
import time, rfc822, traceback, logging, urllib, shutil, glob
from time import sleep
from tempfile import mktemp
from ConfigParser import ConfigParser
from httplib import HTTPConnection, HTTPSConnection, FakeSocket
import socket, base64
from urlparse import urlparse
from hashlib import md5, sha1
from urllib2 import parse_http_list, parse_keqv_list, getproxies
import ssl, locale, gettext
local_path = os.path.join(system_path, 'locales')
LOG_LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 
   'warning': logging.WARNING, 
   'error': logging.ERROR, 
   'critical': logging.CRITICAL}
logger = logging.getLogger('zopeedit')
log_file = None
(lc, encoding) = locale.getdefaultlocale()
gettext.bindtextdomain(APP_NAME, local_path)
gettext.textdomain(APP_NAME)
lang = gettext.translation(APP_NAME, local_path, languages=[
 lc], fallback=True)
_ = lang.lgettext

class Configuration():

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            f = open(path, 'w')
            f.write(default_configuration)
            f.close()
        self.config = ConfigParser()
        self.config.readfp(open(path))
        logger.info('init at: %s' % time.asctime(time.localtime()))
        logger.info('local_path: %r' % local_path)

    def save(self):
        """Save config options to disk"""
        self.config.write(open(self.path, 'w'))
        logger.info('save at: %s' % time.asctime(time.localtime()))

    def set(self, section, option, value):
        self.config.set(section, option, value)

    def __getattr__(self, name):
        return getattr(self.config, name)

    def getAllOptions(self, meta_type, content_type, title, extension, host_domain):
        """Return a dict of all applicable options for the
           given meta_type, content_type and host_domain
        """
        opt = {}
        sep = content_type.find('/')
        general_type = '%s/*' % content_type[:sep]
        host_domain = host_domain.split('.')
        domains = []
        for i in range(len(host_domain)):
            domains.append('domain:%s' % ('.').join(host_domain[i:]))

        domains.reverse()
        sections = [
         'general']
        sections.extend(domains)
        sections.append('meta-type:%s' % meta_type)
        sections.append('general-type:%s' % general_type)
        sections.append('content-type:%s' % content_type)
        sections.append('title:%s' % title)
        for section in sections:
            if self.config.has_section(section):
                for option in self.config.options(section):
                    opt[option] = self.config.get(section, option)
                    logger.debug('option %s: %s' % (option, opt[option]))

        if opt.get('extension') is None and extension is not None:
            opt['extension'] = extension
        return opt


class NullResponse():
    """ Fake Response in case of http error
    """

    def getheader(self, n, d=None):
        return d

    def read(self):
        return '(No Response From Server)'


class ExternalEditor():
    """ ExternalEditor is the main class of zopeedit.
        It is in charge of making the link between the client editor
        and the server file object.
        There are 2 main actions :
        - launch('filename') : starts the edition process
        - editConfig() : allows the end user to edit a local options file
    """

    def __init__(self, input_file=''):
        """ arguments :
                - 'input_file' is the main file received from the server.
        """
        global log_file
        self.networkerror = False
        self.input_file = input_file
        log_file = mktemp(suffix='-zopeedit-log.txt')
        log_filehandler = logging.FileHandler(log_file)
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_filehandler.setFormatter(log_formatter)
        logger.addHandler(log_filehandler)
        logger.setLevel(logging.DEBUG)
        logger.info(_('\n|-----------------------------------------------------------|\n|                                                           |\n| ZopeEdit version %s                                       |\n|                                                           |\n| This file is a log file.                                  |\n|                                                           |\n| Please save it and send it to your administrator.         |\n|                                                           |\n|-----------------------------------------------------------|\n| This version is maintained by atReal contact@atreal.net   |\n|-----------------------------------------------------------|\n\n\n\n\n') % __version__)
        logger.info('Opening %r.', self.input_file)
        if self.input_file == '':
            self.metadata = {}
            self.host = ''
            self.loadConfig()
            return
        else:
            try:
                in_f = open(self.input_file, 'rb')
                m = rfc822.Message(in_f)
                self.metadata = m.dict.copy()
                logger.debug('metadata: %s' % repr(self.metadata))
                (scheme, self.host, self.path) = urlparse(self.metadata['url'])[:3]
                self.url = self.metadata['url']
                self.ssl = scheme == 'https'
                self.loadConfig()
                last_modified = None
                if self.metadata.has_key('last-modified'):
                    last_modified = self.metadata['last-modified']
                    self.last_modified = http_date_to_datetime(last_modified)
                    logger.debug('last_modified: %s' % str(self.last_modified))
                self.title = self.metadata['title'].decode(self.server_charset).encode(self.client_charset, 'ignore')
                if self.long_file_name:
                    sep = self.options.get('file_name_separator', ',')
                    content_file = urllib.unquote('-%s%s' % (self.host,
                     self.path))
                    content_file = content_file.replace('/', sep).replace(':', sep).replace(' ', '_')
                else:
                    content_file = '-' + urllib.unquote(self.path.split('/')[(-1)]).replace(' ', '_')
                extension = self.options.get('extension')
                if extension and not content_file.endswith(extension):
                    content_file = content_file + extension
                if self.options.has_key('temp_dir'):
                    while 1:
                        temp = os.path.expanduser(self.options['temp_dir'])
                        temp = os.tempnam(temp)
                        content_file = '%s%s' % (temp, content_file)
                        if not os.path.exists(content_file):
                            break

                else:
                    content_file = mktemp(content_file, 'rw')
                logger.debug('Destination filename will be: %r.', content_file)
                body_f = open(content_file, 'wb')
                shutil.copyfileobj(in_f, body_f)
                self.content_file = content_file
                self.saved = False
                body_f.close()
                in_f.close()
                if self.clean_up:
                    try:
                        logger.debug('Cleaning up %r.', self.input_file)
                        os.chmod(self.input_file, 511)
                        os.remove(self.input_file)
                    except OSError:
                        logger.exception('Failed to clean up %r.', self.input_file)

                if self.ssl:
                    try:
                        from socket import ssl
                    except ImportError:
                        fatalError('SSL support is not available on this                                 system.\nMake sure openssl is installed and reinstall Python.')

                self.lock_token = None
                self.did_lock = False
            except:
                if getattr(self, 'clean_up', 1):
                    try:
                        (exc, exc_data) = sys.exc_info()[:2]
                        os.remove(self.input_file)
                    except OSError:
                        raise exc, exc_data

                raise

            return

    def __del__(self):
        logger.info('ZopeEdit ends at: %s' % time.asctime(time.localtime()))

    def loadConfig(self):
        """ Read the configuration file and set default values """
        config_path = self.getConfigPath()
        self.config = Configuration(config_path)
        self.options = self.config.getAllOptions(self.metadata.get('meta_type', ''), self.metadata.get('content_type', ''), self.metadata.get('title', ''), self.metadata.get('extension'), self.host)
        logger.info('loadConfig: all options : %r' % self.options)
        logger.setLevel(LOG_LEVELS[self.options.get('log_level', 'info')])
        self.autolauncher = self.options.get('autolauncher', 'gnome-open;kde-open;xdg-open')
        logger.debug('loadConfig: autolauncher: %r' % self.autolauncher)
        if win32:
            self.defaulteditors = self.options.get('defaulteditors', 'notepad')
        else:
            self.defaulteditors = self.options.get('defaulteditors', 'gedit;kedit;gvim;emacs;vim;nano')
        logger.debug('loadConfig: defaulteditors: %s' % self.defaulteditors)
        self.autoproxy = self.options.get('autoproxy', '')
        logger.debug('loadConfig: autoproxy: %r' % self.autoproxy)
        self.proxy = self.options.get('proxy', '')
        proxies = getproxies()
        logger.debug('loadConfig: system proxies : %r' % proxies)
        if self.proxy == '' and self.autoproxy:
            if proxies.has_key('http'):
                self.proxy = proxies['http']
        if self.proxy.startswith('http://'):
            self.proxy = self.proxy[7:]
        if self.proxy.find('/') > -1:
            self.proxy = self.proxy[:self.proxy.find('/')]
        logger.debug('loadConfig: Proxy set to : %s' % self.proxy)
        self.lock_file_schemes = self.options.get('lock_file_schemes', '.~lock.%s#;~%s.lock;.%s.swp').split(';')
        logger.debug('loadConfig: lock_files_schemes: %s' % self.lock_file_schemes)
        self.proxy_user = self.options.get('proxy_user', '')
        logger.debug('loadConfig: proxy_user: %s' % self.proxy_user)
        self.proxy_pass = self.options.get('proxy_pass', '')
        logger.debug('loadConfig: proxy_pass: %s' % self.proxy_pass)
        self.version_control = int(self.options.get('version_control', 0))
        logger.debug('loadConfig: version_control: %s' % self.version_control)
        self.version_command = self.options.get('version_command', '/saveasnewversion')
        self.version_command += '?versioncomment=ZopeEdit%%20%s' % __version__
        logger.debug('loadConfig: version_command: %s' % self.version_command)
        self.keep_log = int(self.options.get('keep_log', 1))
        logger.debug('loadConfig: keep_log: %s' % self.keep_log)
        self.use_locks = int(self.options.get('use_locks', 1))
        logger.debug('loadConfig: use_locks: %s' % self.use_locks)
        self.always_borrow_locks = int(self.options.get('always_borrow_locks', 0))
        logger.debug('loadConfig: always_borrow_locks: %s' % self.always_borrow_locks)
        self.manage_locks = int(self.options.get('manage_locks', 1))
        logger.debug('loadConfig: manage_locks: %s' % self.manage_locks)
        self.lock_timeout = self.options.get('lock_timeout', '86400')
        logger.debug('loadConfig: lock_timeout: %s' % self.lock_timeout)
        self.clean_up = int(self.options.get('cleanup_files', 1))
        logger.debug('loadConfig: cleanup_files: %s' % self.clean_up)
        self.save_interval = float(self.options.get('save_interval', 2))
        logger.debug('loadConfig: save_interval: %s' % self.save_interval)
        self.max_is_alive_counter = int(self.options.get('max_isalive_counter', 5))
        logger.debug('loadConfig: max_isalive_counter: %s' % self.max_is_alive_counter)
        self.server_charset = self.options.get('server_charset', 'utf-8')
        logger.debug('loadConfig: server_charset: %s' % self.server_charset)
        self.client_charset = encoding
        logger.debug('loadConfig: client_charset: %s' % self.client_charset)
        self.long_file_name = int(self.options.get('long_file_name', 0))
        logger.debug('loadConfig: long_filename: %s' % self.long_file_name)
        self.editor = self.options.get('editor')
        if self.editor is not None:
            self.editor = self.findAvailableEditor(self.editor)
        logger.debug('loadConfig: editor: %s' % self.editor)
        return

    def findAvailableEditor(self, editors_list):
        """ Find an available editor (Linux only)
        """
        if not linux:
            return editors_list
        else:
            editors = editors_list.split(';')
            for editor in editors:
                for path in os.environ['PATH'].split(':'):
                    if editor in os.listdir(path):
                        return editor

            return

    def getConfigPath(self, force_local_config=False):
        """ Retrieve the configuration path
            It may be local if there is a user configuration file
            or global for all users
        """
        if win32:
            app_data = os.environ['APPDATA']
            if not os.path.isdir(os.path.expanduser(os.path.join(app_data, 'collective.zopeedit'))):
                os.makedirs(os.path.expanduser(os.path.join(app_data, 'collective.zopeedit')))
            config_path = os.path.expanduser(os.path.join(app_data, 'collective.zopeedit', 'ZopeEdit.ini'))
            app_dir = sys.path[0]
            if app_dir.lower().endswith('library.zip'):
                app_dir = os.path.dirname(app_dir)
            global_config = os.path.join(app_dir or '', 'ZopeEdit.ini')
            if not force_local_config and not os.path.exists(config_path):
                logger.info('getConfigPath: Config file %r does not exist. Using global configuration file: %r.', config_path, global_config)
                config_path = global_config
        elif osx:
            config_path = os.path.expanduser('~/ZopeEdit.ini')
        else:
            if not os.path.isdir(os.path.expanduser('~/.config/collective.zopeedit')):
                os.makedirs(os.path.expanduser('~/.config/collective.zopeedit'))
            config_path = os.path.expanduser('~/.config/collective.zopeedit/ZopeEdit.ini')
        logger.info('getConfigPath: Using user configuration file: %r.', config_path)
        return config_path

    def cleanContentFile(self, tried_cleanup=False):
        if self.clean_up and hasattr(self, 'content_file'):
            try:
                os.remove(self.content_file)
                logger.info('Content File cleaned up %r at %s' % (
                 self.content_file,
                 time.asctime(time.localtime())))
                return True
            except OSError:
                if tried_cleanup:
                    logger.exception('Failed to clean up %r at %s' % (
                     self.content_file,
                     time.asctime(time.localtime())))
                    return False
                else:
                    logger.debug('Failed to clean up %r at %s ;                                  retry in 10 sec' % (
                     self.content_file,
                     time.asctime(time.localtime())))
                    time.sleep(10)
                    return self.cleanContentFile(tried_cleanup=True)

    def getEditorCommand(self):
        """ Return the editor command
        """
        editor = self.editor
        if win32 and editor is None:
            from _winreg import HKEY_CLASSES_ROOT, OpenKeyEx, QueryValueEx, EnumKey
            from win32api import FindExecutable, ExpandEnvironmentStrings
            content_type = self.metadata.get('content_type')
            extension = self.options.get('extension')
            logger.debug('Have content type: %r, extension: %r', content_type, extension)
            if content_type:
                try:
                    key = 'MIME\\Database\\Content Type\\%s' % content_type
                    key = OpenKeyEx(HKEY_CLASSES_ROOT, key)
                    (extension, nil) = QueryValueEx(key, 'Extension')
                    logger.debug('Registry has extension %r for content type %r', extension, content_type)
                except EnvironmentError:
                    pass

            if extension is None and self.metadata.has_key('url'):
                url = self.metadata['url']
                dot = url.rfind('.')
                if dot != -1 and dot > url.rfind('/'):
                    extension = url[dot:]
                    logger.debug('Extracted extension from url: %r', extension)
            classname = editor = None
            if extension is not None:
                try:
                    key = OpenKeyEx(HKEY_CLASSES_ROOT, extension)
                    (classname, nil) = QueryValueEx(key, None)
                    logger.debug('ClassName for extension %r is: %r', extension, classname)
                except EnvironmentError:
                    classname = None

            if classname is not None:
                try:
                    key = OpenKeyEx(HKEY_CLASSES_ROOT, classname + '\\Shell\\Edit\\Command')
                    (editor, nil) = QueryValueEx(key, None)
                    logger.debug('Edit action for %r is: %r', classname, editor)
                except EnvironmentError:
                    pass

            if classname is not None and editor is None:
                logger.debug('Could not find Edit action for %r. Brute-force enumeration.', classname)
                try:
                    key = OpenKeyEx(HKEY_CLASSES_ROOT, classname + '\\Shell')
                    index = 0
                    while 1:
                        try:
                            subkey = EnumKey(key, index)
                            index += 1
                            if str(subkey).lower().startswith('edit'):
                                subkey = OpenKeyEx(key, subkey + '\\Command')
                                (editor, nil) = QueryValueEx(subkey, None)
                            if editor is None:
                                continue
                            logger.debug('Found action %r for %r. Command will be: %r', subkey, classname, editor)
                        except EnvironmentError:
                            break

                except EnvironmentError:
                    pass

            if classname is not None and editor is None:
                try:
                    key = OpenKeyEx(HKEY_CLASSES_ROOT, classname + '\\Shell\\Open\\Command')
                    (editor, nil) = QueryValueEx(key, None)
                    logger.debug('Open action for %r has command: %r. ', classname, editor)
                except EnvironmentError:
                    pass

            if editor is None:
                try:
                    (nil, editor) = FindExecutable(self.content_file, '')
                    logger.debug('Executable for %r is: %r. ', self.content_file, editor)
                except pywintypes.error:
                    pass

            if editor is not None and editor.find('\\iexplore.exe') != -1:
                logger.debug('Found iexplore.exe. Skipping.')
                editor = None
            if editor is not None:
                return ExpandEnvironmentStrings(editor)
        elif editor is None and osx:
            pass
        elif editor is None:
            logger.debug('getEditorCommand: editor is None and linux')
            logger.debug('getEditorCommand: self.autolauncher = %s' % self.autolauncher)
            editor = self.findAvailableEditor(self.autolauncher)
            logger.debug('getEditorCommand: editor is : %s' % editor)
        return editor

    def launch(self):
        """ Launch external editor
        """
        if self.input_file == '':
            fatalError(_('No input file. \nZopeEdit will close.'), exit=0)
        self.last_mtime = os.path.getmtime(self.content_file)
        self.initial_mtime = self.last_mtime
        self.last_saved_mtime = self.last_mtime
        self.dirty_file = False
        command = self.getEditorCommand()
        if not self.lock():
            self.networkerror = True
            msg = _('%s\nUnable to lock the file on the server.\nThis may be a network or proxy issue.\nYour log file will be opened\nPlease save it and send it to your administrator.') % self.title
            errorDialog(msg)
            logger.error('launch: lock failed. Exit.')
            self.editFile(log_file, detach=True, default=True)
            sys.exit()
        if win32:
            if command.find('\\') != -1:
                bin = re.search('\\\\([^\\.\\\\]+)\\.exe', command.lower())
                if bin is not None:
                    bin = bin.group(1)
            else:
                bin = command.lower().strip()
        else:
            bin = command
        logger.info('launch: Command %r, will use %r', command, bin)
        if bin is not None:
            try:
                logger.debug('launch: bin is not None - try to load a plugin : %s' % bin)
                module = 'Plugins.%s' % bin
                Plugin = __import__(module, globals(), locals(), ('EditorProcess', ))
                self.editor = Plugin.EditorProcess(self.content_file)
                logger.info('launch: Launching Plugin %r with: %r', Plugin, self.content_file)
            except (ImportError, AttributeError):
                logger.debug('launch: Error while to load the plugin ; set bin to None')
                bin = None

        if bin is None:
            logger.info('launch: No plugin found ; using standard editor process')
            if win32:
                file_insert = '%1'
            else:
                file_insert = '$1'
            if command.find(file_insert) > -1:
                command = command.replace(file_insert, self.content_file)
            else:
                command = '%s %s' % (command, self.content_file)
            logger.info('launch: Launching EditorProcess with: %r', command)
            self.editor = EditorProcess(command, self.content_file, self.max_is_alive_counter, self.lock_file_schemes)
            logger.info('launch: Editor launched successfully')
        launch_success = self.editor.isAlive()
        if not launch_success:
            fatalError(_('Unable to edit your file.\n\n%s') % command)
        file_monitor_exit_state = self.monitorFile()
        unlock_success = self.unlock()
        if not unlock_success:
            logger.error('launch: not unlock_success. Flag networkerror')
            self.networkerror = True
        if self.dirty_file:
            logger.exception("launch: Some modifications are NOT saved we'll re-open file and logs")
            self.clean_up = False
            self.keep_log = True
        elif not unlock_success and self.clean_up:
            logger.exception('launch: Unlock failed and we have to clean up files')
            self.clean_up = False
            self.keep_log = True
        if self.networkerror or self.dirty_file:
            if self.dirty_file:
                errorDialog(_('Network error :\nYour working copy will be re-opened,\n\nSAVE YOUR WORK ON YOUR DESKTOP.\n\nA log file will be opened\nPlease save it and send it to your administrator.'))
                self.editor.startEditor()
            else:
                errorDialog(_('Network error : your file is still locked.\n\nA log file will be opened\nPlease save it and send it to your administrator.'))
            self.editFile(log_file, detach=True, default=True)
            sys.exit(0)
        if file_monitor_exit_state == 'closed modified' or file_monitor_exit_state == 'manual close modified':
            msg = _('%(title)s\n\nFile : %(content_file)s\n\nSaved at : %(time)s\n\nEdition completed') % {'title': self.title, 
               'content_file': self.content_file, 
               'time': time.ctime(self.last_saved_mtime)}
            messageDialog(msg)
        elif file_monitor_exit_state == 'closed not modified' or file_monitor_exit_state == 'manual close not modified':
            msg = _('%(title)s\n\nEdition completed') % {'title': self.title}
            messageDialog(msg)
        self.cleanContentFile()
        return

    def monitorFile(self):
        """ Check if the file is edited and if it is modified.
        If it's modified save it back.
        If it is not any more edited exit with an information on what happened.
         -> was saved back
         -> was automatically detected
         -> was manually controled by the user
        """
        final_loop = False
        isAlive_detected = False
        returnChain = ''
        while 1:
            if not final_loop:
                self.editor.wait(self.save_interval)
            mtime = os.path.getmtime(self.content_file)
            if mtime != self.last_mtime:
                logger.debug('monitorFile: File is dirty : changes detected !')
                self.dirty_file = True
                launch_success = True
                if self.versionControl():
                    logger.info('monitorFile: New version created successfully')
                else:
                    logger.debug('monitorFile: No new version created')
                self.saved = self.putChanges()
                self.last_mtime = mtime
                if self.saved:
                    self.last_saved_mtime = mtime
                    self.dirty_file = False
            if not self.editor.isAlive():
                if final_loop:
                    logger.info('monitorFile: Final loop done; break')
                    return returnChain
                    if mtime != self.last_saved_mtime:
                        self.dirty_file = True
                        launch_success = True
                        self.saved = self.putChanges()
                        self.last_mtime = mtime
                        if self.saved:
                            self.last_saved_mtime = mtime
                            self.dirty_file = False
                    if isAlive_detected:
                        if self.last_saved_mtime != self.initial_mtime:
                            logger.debug('monitorFile: closed modified')
                            returnChain = 'closed modified'
                        else:
                            logger.debug('monitorFile: closed not modified')
                            returnChain = 'closed not modified'
                    if self.last_saved_mtime != self.initial_mtime:
                        msg = _('%(title)s\n\nFile : %(content_file)s\nSaved at : %(time)s\n\nDid you close your file ?') % {'title': self.title, 
                           'content_file': self.content_file, 
                           'time': time.ctime(self.last_saved_mtime)}
                        askYesNo(msg) or logger.debug('monitorFile: manual continue modified')
                        continue
                    else:
                        logger.debug('monitorFile: manual closed modified')
                        returnChain = 'manual close modified'
                else:
                    msg = _('%(title)s :\n\nDid you close your file ?') % {'title': self.title}
                    if not askYesNo(msg):
                        logger.debug('monitorFile: manual continue not modified')
                        continue
                    else:
                        logger.debug('monitorFile: manual close not monified')
                        returnChain = 'manual close not modified'
                final_loop = True
                logger.info('monitorFile: Final loop')
            else:
                isAlive_detected = True

    def putChanges(self):
        """Save changes to the file back to Zope"""
        logger.info('putChanges at: %s' % time.asctime(time.localtime()))
        f = open(self.content_file, 'rb')
        body = f.read()
        logger.info('Document is %s bytes long' % len(body))
        f.close()
        headers = {'Content-Type': self.metadata.get('content_type', 'text/plain')}
        if self.lock_token is not None:
            headers['If'] = '<%s> (<%s>)' % (self.path, self.lock_token)
        response = self.zopeRequest('PUT', headers, body)
        del body
        if response.status / 100 != 2:
            if self.manage_locks and askRetryAfterError(response, _('Network error\n\nCould not save the file to server.\n\nError detail :\n')):
                return self.putChanges()
            else:
                logger.error('Could not save to Zope\nError during HTTP PUT')
                return False
        logger.info('File successfully saved back to the intranet')
        return True

    def lock(self):
        """Apply a webdav lock to the object in Zope
        usecases :
        - use_locks "1" and manage_locks "1"
            1 - no existing lock
                lock the file
                if error : ask user if retry or not
                if no retry and error : return False
            2 - existing lock
                if always_borrow_locks "yes"
                    borrow the lock and return True
                else ask user wether retrieve it or not
                    if not : exit with error
                    if yes : borrow the lock
        - use_locks "yes" and manage_locks "no"
            1 - no existing lock
                lock the file
                if error : exit with error
            2 - existing lock
                exit with error
        - use_locks "no"
            don't do anything and exit with no error
        """
        logger.debug('lock: lock at: %s' % time.asctime(time.localtime()))
        if not self.use_locks:
            logger.debug("lock: don't use locks")
            return True
        else:
            if self.metadata.get('lock-token'):
                if not self.manage_locks:
                    logger.critical("lock: object already locked : lock tocken not empty\n user doesn't manage locks, so... exit")
                    msg = _('%s\nThis object is already locked.') % self.title
                    errorDialog(msg)
                    sys.exit()
                if self.always_borrow_locks or self.metadata.get('borrow_lock'):
                    self.lock_token = 'opaquelocktoken:%s' % self.metadata['lock-token']
                else:
                    msg = _('%s\nThis object is already locked by you in another session.\nDo you want to borrow this lock and continue ?') % self.title
                    if askYesNo(msg):
                        self.lock_token = 'opaquelocktoken:%s' % self.metadata['lock-token']
                    else:
                        logger.critical("lock: File locked and user doesn't want to borrow the lock. Exit.")
                        sys.exit()
            if self.lock_token is not None:
                logger.warning('lock: Existing lock borrowed.')
                return True
            dav_lock_response = self.DAVLock()
            if dav_lock_response / 100 == 2:
                logger.info('lock: OK')
                self.did_lock = True
                return True
            while self.manage_locks and not self.did_lock:
                dav_lock_response = self.DAVLock()
                if dav_lock_response / 100 == 2:
                    logger.info('lock: OK')
                    self.did_lock = True
                    return True
                if dav_lock_response == 423:
                    logger.warning('lock: object locked by someone else... EXIT !')
                    msg = _('%s\nObject already locked') % self.title
                    errorDialog(msg)
                    exit()
                else:
                    logger.error('lock: failed to lock object: response status %s' % dav_lock_response)
                    msg = _('%(title)s\nUnable to get a lock on the server(return value %(dav_lock_response)s)') % {'title': self.title, 'dav_lock_response': dav_lock_response}
                msg += '\n'
                msg += _('Do you want to retry ?')
                if askRetryCancel(msg):
                    logger.info('lock: Retry lock')
                    continue
                else:
                    logger.critical('lock: Unable to lock the file ; return False')
                    logger.error('lock failed. Return False.')
                    return False

            return

    def DAVLock(self):
        """Do effectively lock the object"""
        logger.debug('DAVLock at: %s' % time.asctime(time.localtime()))
        headers = {'Content-Type': 'text/xml; charset="utf-8"', 'Timeout': self.lock_timeout, 
           'Depth': '0'}
        body = '<?xml version="1.0" encoding="utf-8"?>\n<d:lockinfo xmlns:d="DAV:">\n  <d:lockscope><d:exclusive/></d:lockscope>\n  <d:locktype><d:write/></d:locktype>\n  <d:depth>infinity</d:depth>\n  <d:owner>\n  <d:href>Zope External Editor</d:href>\n  </d:owner>\n</d:lockinfo>'
        response = self.zopeRequest('LOCK', headers, body)
        logger.debug('DAVLock response:%r' % response.status)
        dav_lock_response = response.status
        if dav_lock_response / 100 == 2:
            logger.info('Lock success.')
            reply = response.read()
            token_start = reply.find('>opaquelocktoken:')
            token_end = reply.find('<', token_start)
            if token_start > 0 and token_end > 0:
                self.lock_token = reply[token_start + 1:token_end]
        return dav_lock_response

    def versionControl(self):
        """ If version_control is enabled, ZopeEdit will try to 
            automatically create a new version of the file.
            The version is created only if the file is modified,
            just before the first save.
        """
        if not self.version_control:
            logger.debug('versionControl: version_control is False : %s' % self.version_control)
            return False
        else:
            if self.saved:
                logger.debug("versionControl: don't create a version if already saved")
                return False
            response = self.zopeRequest('GET', command='%s' % self.version_command)
            logger.debug('versionControl : return code of new version is %s' % response.status)
            if response.status == 302:
                return True
            logger.warning('Creation of version failed : response status %s' % response.status)
            return False

    def unlock(self, interactive=True):
        """Remove webdav lock from edited zope object"""
        if not self.use_locks:
            logger.debug('unlock: use_locks is False return True.')
            return True
        else:
            if not self.did_lock and self.lock_token is None:
                return True
            response = self.DAVunlock()
            status = int(response.status)
            logger.debug('response : %s status : %s status/100: %s' % (
             response, status, status / 100))
            while status / 100 != 2:
                logger.error('Unlock failed at: %s did_lock=%s status=%s' % (
                 time.asctime(time.localtime()),
                 self.did_lock, status))
                if askRetryAfterError(response, _('Network error\n\nUnable to unlock the file on server.\n')):
                    status = self.DAVunlock().status
                    continue
                else:
                    return False

            logger.info('Unlock successfully. did_lock = %s' % self.did_lock)
            self.did_lock = False
            return True

    def DAVunlock(self):
        logger.debug('DAVunlock at: %s' % time.asctime(time.localtime()))
        headers = {'Lock-Token': self.lock_token}
        response = self.zopeRequest('UNLOCK', headers)
        logger.debug('DAVunlock response:%r' % response)
        return response

    def _get_authorization(self, host, method, selector, cookie, ssl, old_response):
        if ssl is True:
            h = HTTPSConnection(host)
        else:
            h = HTTPConnection(host)
        if cookie is not None:
            headers = {'Cookie': cookie}
        else:
            headers = {}
        h.request('HEAD', selector, headers=headers)
        r = h.getresponse()
        if r.status != 401:
            return
        else:
            auth_header = r.getheader('www-authenticate').strip()
            if auth_header is None or not auth_header.lower().startswith('digest'):
                return
            chal = parse_keqv_list(parse_http_list(auth_header[7:]))
            if self.identity is not None:
                (username, password) = self.identity
            else:
                username = parse_keqv_list(parse_http_list(old_response[7:]))['username']
                password = askPassword(chal['realm'], username)
                self.identity = (username, password)
            algorithm = chal.get('algorithm', 'MD5')
            if algorithm == 'MD5':
                H = lambda x: md5(x).hexdigest()
            elif algorithm == 'SHA':
                H = lambda x: sha1(x).hexdigest()
            KD = lambda s, d: H('%s:%s' % (s, d))
            nonce = chal['nonce']
            res = 'Digest username="%s", realm="%s", nonce="%s", algorithm="%s", uri="%s"' % (
             username,
             chal['realm'],
             nonce,
             chal['algorithm'],
             selector)
            if 'opaque' in chal:
                res += ', opaque="%s"' % chal['opaque']
            A1 = '%s:%s:%s' % (username, chal['realm'], password)
            A2 = '%s:%s' % (method, selector)
            if 'qop' in chal:
                qop = chal['qop']
                nc = '00000001'
                cnonce = '12345678'
                res += ', qop="%s", nc="%s", cnonce="%s"' % (qop, nc, cnonce)
                response = KD(H(A1), '%s:%s:%s:%s:%s' % (nonce,
                 nc,
                 cnonce,
                 qop,
                 H(A2)))
            else:
                response = KD(H(A1), '%s:%s' % (nonce, H(A2)))
            res += ', response="%s"' % response
            return res

    def zopeRequest(self, method, headers={}, body='', command=''):
        """Send a request back to Zope"""
        logger.debug('zopeRequest: method: %r, headers: %r, command: %r' % (method, headers, command))
        if self.proxy == '':
            logger.debug('zopeRequest: no proxy definition in config file : self.proxy is empty')
            host = self.host
            url = self.path
            logger.debug('zopeRequest: host:%s and url path:%r retrieved from system' % (
             host, url))
        else:
            host = self.proxy
            url = self.url
            logger.debug('zopeRequest: proxy defined in config file : host:%s url:%s' % (
             host, url))
        url += command
        logger.debug('zopeRequest: url = %s' % url)
        logger.debug('zopeRequest: method = %s' % method)
        logger.debug('zopeRequest: command = %s' % command)
        try:
            if self.ssl and self.proxy:
                logger.debug('zopeRequest: ssl and proxy')
                (proxy_host, proxy_port) = self.proxy.split(':')
                proxy_port = int(proxy_port)
                logger.debug('zopeRequest: proxy_host; %r, proxy_port: %r' % (proxy_host, proxy_port))
                taburl = url.split('/')
                if len(taburl[2].split(':')) == 2:
                    port = int(taburl[2].split(':')[1])
                    host = taburl[2].split(':')[0]
                else:
                    if taburl[0] == 'https:':
                        port = 443
                    else:
                        port = 80
                    host = taburl[2]
                proxy_authorization = ''
                if self.proxy_user and self.proxy_passwd:
                    logger.debug('zopeRequest: proxy_user: %r, proxy_passwd: XXX' % self.proxy_user)
                    user_pass = base64.encodestring(self.proxy_user + ':' + self.proxy_passwd)
                    proxy_authorization = 'Proxy-authorization: Basic ' + user_pass + '\r\n'
                proxy_connect = 'CONNECT %s:%s HTTP/1.0\r\n' % (host, port)
                logger.debug('zopeRequest: proxy_connect: %r' % proxy_connect)
                user_agent = 'User-Agent: Zope External Editor %s\r\n' % __version__
                proxy_pieces = proxy_connect + proxy_authorization + user_agent + '\r\n'
                logger.debug('zopeRequest: initialyze proxy socket')
                proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logger.debug('zopeRequest: connect to proxy')
                proxy.connect((proxy_host, proxy_port))
                logger.debug('zopeRequest: send auth pieces to proxy (%r)' % proxy_pieces)
                proxy.sendall(proxy_pieces)
                logger.debug('zopeRequest: receive response fron proxy')
                response = proxy.recv(8192)
                status = response.split()[1]
                if status != str(200):
                    raise 'Error status=', str(status)
                logger.debug('zopeRequest: wrap proxy to ssl')
                sock = ssl.wrap_socket(proxy)
                logger.debug('zopeRequest: initialyze HTTP connection')
                hc = HTTPConnection(proxy_host, proxy_port)
                hc.set_debuglevel(9)
                hc.sock = sock
                logger.debug('zopeRequest: putrequest method: %r, url: %r' % (method, url))
                hc.putrequest(method, url)
                hc.putheader('User-Agent', 'Zope External Editor/%s' % __version__)
                for (header, value) in headers.items():
                    hc.putheader(header, value)

                hc.putheader('Content-Length', str(len(body)))
                if self.metadata.get('auth', '').lower().startswith('basic'):
                    hc.putheader('Authorization', self.metadata['auth'])
                if self.metadata.get('cookie'):
                    hc.putheader('Cookie', self.metadata['cookie'])
                hc.endheaders()
                hc.send(body)
                response = hc.getresponse()
                logger.debug('zopeRequest: response: %r' % response)
                return response
            else:
                if self.ssl and not self.proxy:
                    logger.debug('zopeRequest: ssl and no proxy')
                    h = HTTPSConnection(host)
                else:
                    logger.debug('zopeRequest: no ssl and no proxy')
                    h = HTTPConnection(host)
                h.putrequest(method, url)
                h.putheader('User-Agent', 'Zope External Editor/%s' % __version__)
                for (header, value) in headers.items():
                    h.putheader(header, value)

                h.putheader('Content-Length', str(len(body)))
                auth_header = self.metadata.get('auth', '')
                if auth_header.lower().startswith('basic'):
                    h.putheader('Authorization', self.metadata['auth'])
                if auth_header.lower().startswith('digest'):
                    authorization = self._get_authorization(host, method, url, self.metadata.get('cookie'), False, auth_header)
                    if authorization is not None:
                        h.putheader('Authorization', authorization)
                if self.metadata.get('cookie'):
                    h.putheader('Cookie', self.metadata['cookie'])
                h.endheaders()
                h.send(body)
                response = h.getresponse()
                logger.debug('zopeRequest: response: %r' % response.status)
                return response
        except:
            logger.error('zopeRequest: we got an exception !')
            response = NullResponse()
            response.reason = sys.exc_info()[1]
            try:
                (response.status, response.reason) = response.reason
            except ValueError:
                response.status = 0

            if response.reason == 'EOF occurred in violation of protocol':
                response.status = 200
            return response

        return

    def editConfig(self):
        logger.info('Edit local configuration')
        user_config = self.getConfigPath(force_local_config=True)
        if win32:
            app_dir = sys.path[0]
            if app_dir.lower().endswith('library.zip'):
                app_dir = os.path.dirname(app_dir)
            global_config = os.path.join(app_dir or '', 'ZopeEdit.ini')
            create_config_file = False
            if not os.path.exists(user_config):
                logger.info('Local configuration file %r does not exist. Global configuration file is : %r.', user_config, global_config)
                create_config_file = True
            elif askYesNo(_('Reset configuration file ?')):
                create_config_file = True
                logger.info('Replace the configuration file with the default one.')
            if create_config_file:
                input_config_file = open(global_config, 'r')
                output_config_file = open(user_config, 'w')
                for l in input_config_file.readlines():
                    output_config_file.write(l)

                input_config_file.close()
                output_config_file.close()
        elif askYesNo(_('Do you want to replace your configuration file \nwith the default one ?')):
            logger.info('Replace the configuration file with the default one.')
            output_config = open(user_config, 'w')
            output_config.write(default_configuration)
            output_config.close()
        self.editFile(user_config, default=True)

    def editFile(self, file, detach=False, default=False):
        if default:
            editor = self.findAvailableEditor(self.defaulteditors)
        else:
            editor = self.getEditorCommand()
        if not editor:
            if osx:
                LSOpenFSRef(file, None)
            else:
                logger.critical('editFile: No editor found. File edition failed.')
        logger.info('editFile: Edit file %s with editor %s' % (
         file, editor))
        p = Popen('%s %s' % (editor, file), shell=True)
        if linux:
            if detach:
                p.poll()
            else:
                sts = os.waitpid(p.pid, 0)[1]
                logger.debug('sts : %s' % sts)
            if p.pid == 0:
                logger.debug('editFile: error with the detected editor ; try with a default one as last option')
                editor = self.findAvailableEditor(self.defaulteditors)
                logger.info('editFile: Edit file %s with editor %s' % (
                 file, editor))
                logger.debug('editFile: launching editor in a shell environment : %s %s' % (
                 editor, file))
                p = Popen('%s %s' % (editor, file), shell=True)
                if linux:
                    if detach:
                        p.poll()
                    else:
                        sts = os.waitpid(p.pid, 0)[1]
                        logger.debug('sts : %s' % sts)
        return


title = 'Zope External Editor'

def askRetryAfterError(response, operation, message=''):
    """Dumps response data"""
    if not message and response.getheader('Bobo-Exception-Type') is not None:
        message = '%s: %s' % (response.getheader('Bobo-Exception-Type'),
         response.getheader('Bobo-Exception-Value'))
    return askRetryCancel('%s\n"%d %s - %s"' % (operation, response.status,
     response.reason, message))


class EditorProcess():

    def __init__(self, command, contentfile, max_is_alive_counter, lock_file_schemes):
        """Launch editor process"""
        self.command = command
        self.contentfile = contentfile
        self.max_is_alive_counter = max_is_alive_counter
        self.lock_file_schemes = lock_file_schemes
        self.arg_re = '\\s*([^\'"]\\S+)\\s+|\\s*"([^"]+)"\\s*|\\s*\'([^\']+)\'\\s*'
        self.is_alive_by_file = None
        self.is_alive_counter = 0
        self.starting = True
        if win32:
            self.methods = {1: self.isFileLockedByLockFile, 2: self.isFileOpenWin32, 
               3: self.isPidUpWin32}
            self.nb_methods = 3
        elif osx:
            self.methods = {1: self.isFileLockedByLockFile, 2: self.isFileOpen}
            self.nb_methods = 2
        else:
            self.methods = {1: self.isFileLockedByLockFile, 
               2: self.isFileOpen, 
               3: self.isPidUp}
            self.nb_methods = 3
        self.lock_detected = False
        self.selected_method = False
        if win32:
            self.startEditorWin32()
        elif osx:
            self.startEditorOsx()
        else:
            self.startEditor()
        return

    def startEditorWin32(self):
        try:
            logger.debug('CreateProcess: %r', self.command)
            (self.handle, nil, nil, nil) = CreateProcess(None, self.command, None, None, 1, 0, None, None, STARTUPINFO())
        except pywintypes.error, e:
            fatalError('Error launching editor process\n(%s):\n%s' % (
             self.command, e[2]))

        return

    def startEditorOsx(self):
        res = LSOpenFSRef(self.contentfile, None)
        return

    def startEditor(self):
        args = re.split(self.arg_re, self.command.strip())
        args = filter(None, args)
        logger.debug('starting editor %r' % args)
        self.pid = Popen(args).pid
        logger.debug('Pid is %s' % self.pid)
        return

    def wait(self, timeout):
        """Wait for editor to exit or until timeout"""
        sleep(timeout)

    def isFileOpenWin32(self):
        try:
            fileOpen = file(self.contentfile, 'a')
        except IOError, e:
            if e.args[0] == 13:
                logger.debug('Document is writeLocked by command')
                self.cmdLocksWrite = True
                return True
            logger.error('%s %s ' % (e.__class__.__name__, str(e)))

        fileOpen.close()
        logger.info('File is not open : Editor is closed')
        return False

    def isPidUpWin32(self):
        if GetExitCodeProcess(self.handle) == 259:
            logger.info('Pid is up : Editor is still running')
            return True
        logger.info('Pid is not up : Editor exited')
        return False

    def isFileOpen(self):
        """Test if File is locked (filesystem)"""
        logger.debug('test if the file edited is locked by filesystem')
        isFileOpenNum = call(['/bin/fuser',
         re.split(self.arg_re, self.command.strip())[(-1)]])
        return isFileOpenNum == 0

    def isPidUp(self):
        """Test PID"""
        logger.debug('test if PID is up')
        try:
            (exit_pid, exit_status) = os.waitpid(self.pid, os.WNOHANG)
        except OSError:
            return False

        return exit_pid != self.pid

    def isFileLockedByLockFile(self):
        """Test Lock File (extra file)"""
        if win32:
            file_separator = '\\'
        else:
            file_separator = '/'
        original_filepath = self.contentfile.split(file_separator)
        logger.debug('log file schemes : %s' % self.lock_file_schemes)
        for i in self.lock_file_schemes:
            filepath = original_filepath[:]
            if i == '':
                continue
            filepath[-1] = i % filepath[(-1)]
            filename = file_separator.join(filepath)
            logger.debug('Test: lock file : %s' % filename)
            if glob.glob(filename):
                self.lock_file_schemes = [
                 i]
                return True

        return False

    def isAlive(self):
        """Returns true if the editor process is still alive
           is_alive_by_file stores whether we check file or pid
           file check has priority"""
        if self.starting:
            logger.info('isAlive : still starting. Counter : %s' % self.is_alive_counter)
            if self.is_alive_counter < self.max_is_alive_counter:
                self.is_alive_counter += 1
            else:
                self.starting = False
        for i in range(1, self.nb_methods + 1):
            if self.methods[i]():
                logger.debug('isAlive: True( %s : %s)' % (
                 i, self.methods[i].__doc__))
                if i != self.selected_method:
                    logger.info('DETECTION METHOD CHANGE : Level %s - %s' % (
                     i,
                     self.methods[i].__doc__))
                self.selected_method = i
                self.nb_methods = i
                self.lock_detected = True
                return True

        logger.info('isAlive : no edition detected.')
        if self.starting and not self.lock_detected:
            logger.debug('isAlive : still in the startup process :continue.')
            return True
        return False


if win32:
    import Plugins
    from win32ui import MessageBox
    from win32process import CreateProcess, GetExitCodeProcess, STARTUPINFO
    from win32event import WaitForSingleObject
    from win32con import MB_OK, MB_OKCANCEL, MB_YESNO, MB_RETRYCANCEL, MB_SYSTEMMODAL, MB_ICONERROR, MB_ICONQUESTION, MB_ICONEXCLAMATION

    def errorDialog(message):
        MessageBox(message, title, MB_OK + MB_ICONERROR + MB_SYSTEMMODAL)


    def messageDialog(message):
        MessageBox(message, title, MB_OK + MB_ICONEXCLAMATION + MB_SYSTEMMODAL)


    def askRetryCancel(message):
        return MessageBox(message, title, MB_OK + MB_RETRYCANCEL + MB_ICONEXCLAMATION + MB_SYSTEMMODAL) == 4


    def askYesNo(message):
        return MessageBox(message, title, MB_OK + MB_YESNO + MB_ICONQUESTION + MB_SYSTEMMODAL) == 6


    def askPassword(realm, username):
        import pywin.dialogs.login
        title = _('Please enter your password')
        (userid, password) = pywin.dialogs.login.GetLogin(title, username)
        return password


else:
    from time import sleep
    import re

    def has_tk():
        """Sets up a suitable tk root window if one has not
           already been setup. Returns true if tk is happy,
           false if tk throws an error (like its not available)"""
        global tk_root
        if not locals().has_key('tk_root'):
            try:
                from Tkinter import Tk
                tk_root = Tk()
                tk_root.withdraw()
                return True
            except:
                return False

        return True


    def tk_flush():
        tk_root.update()


    def errorDialog(message):
        """Error dialog box"""
        if has_tk():
            from tkMessageBox import showerror
            showerror(title, message)
            tk_flush()
        else:
            print message


    def messageDialog(message):
        """Error dialog box"""
        if has_tk():
            from tkMessageBox import showinfo
            showinfo(title, message)
            tk_flush()
        else:
            print message


    def askRetryCancel(message):
        if has_tk():
            from tkMessageBox import askretrycancel
            r = askretrycancel(title, message)
            tk_flush()
            return r


    def askYesNo(message):
        if has_tk():
            from tkMessageBox import askyesno
            r = askyesno(title, message)
            tk_flush()
            return r


    def askPassword(realm, username):
        if has_tk():
            from tkSimpleDialog import askstring
            r = askstring(title, "Please enter the password for '%s' in '%s'" % (
             username, realm), show='*')
            tk_flush()
            return r


def fatalError(message, exit=1):
    """Show error message and exit"""
    global log_file
    msg = _('FATAL ERROR: %s\n            ZopeEdit will close.') % message
    errorDialog(msg)
    if log_file is None:
        log_file = mktemp(suffix='-zopeedit-traceback.txt')
    debug_f = open(log_file, 'a+b')
    try:
        traceback.print_exc(file=debug_f)
    finally:
        debug_f.close()

    if exit:
        sys.exit(0)
    return


def messageScrolledText(text):
    if has_tk():
        from ScrolledText import ScrolledText
        myText = ScrolledText(tk_root, width=80, wrap='word')
        myText.pack()
        myText.insert('end', ('').join(text))
        tk_root.wm_deiconify()
        tk_flush()
        tk_root.protocol('WM_DELETE_WINDOW', sys.exit)
        tk_root.mainloop()
    else:
        print text


default_configuration = "\n#######################################################################\n#                                                                     #\n#       Zope External Editor helper application configuration         #\n#                                                                     #\n#             maintained by atReal contact@atreal.fr                  #\n#######################################################################\n#                                                                     #\n# Remove '#' to make an option active                                 #\n#                                                                     #\n#######################################################################\n\n[general]\n# General configuration options\nversion = %s\n" % __version__
default_configuration += '\n# Create a new version when the file is closed ?\n#version_control = 0\n\n# Temporary file cleanup. Set to false for debugging or\n# to waste disk space. Note: setting this to false is a\n# security risk to the zope server\n#cleanup_files = 1\n#keep_log = 1\n\n# Use WebDAV locking to prevent concurrent editing by\n# different users. Disable for single user use or for\n# better performance\n# set use_locks = 0 if you use a proxy that does not allow wabdav LOCKs\n#use_locks = 1\n\n# If you wish to inform the user about locks issues\n# set manage_locks = 1\n# This will allow the user to borrow a lock or edit a locked file\n# without informing the administrator\n#manage_locks = 1\n\n# To suppress warnings about borrowing locks on objects\n# locked by you before you began editing you can\n# set this flag. This is useful for applications that\n# use server-side locking, like CMFStaging\n#always_borrow_locks = 0\n\n# Duration of file Lock : 1 day = 86400 seconds\n# If this option is removed, fall back on \'infinite\' zope default\n# Default \'infinite\' value is about 12 minutes\n#lock_timeout = 86400\n\n# Proxy address\n#proxy = http://www.myproxy.com:8080\n\n# Proxy user and password ( optional )\n#proxy_user = \'username\'\n#proxy_pass = \'password\'\n\n# Automatic proxy configuration from system\n# does nothing if proxy is configured\n# Default value is "disabled" : 0\n#autoproxy = 1\n\n# Max isAlive counter\n# This is used in order to wait the editor to effectively lock the file\n# This is the number of \'probing\' cycles\n# default value is 5 cycles of save_interval\n#max_isalive_counter = 5\n\n# Automatic save interval, in seconds. Set to zero for\n# no auto save (save to Zope only on exit).\n#save_interval = 5\n\n# log level : default is \'info\'.\n# It can be set to debug, info, warning, error or critical.\n#log_level = debug\n\n# If your server is not using utf-8\n#server_charset = utf-8\n\n# If your client charset is not iso-8859-1\n# client_charset = iso-8859-1\n\n# Lock File Scheme\n# These are schemes that are used in order to detect "lock" files\n# %s is the edited file\'s name (add a \';\' between each scheme):\n#lock_file_schemes = .~lock.%s#;~%s.lock;.%s.swp\n\n'
if linux:
    default_configuration += "\n# Uncomment and specify an editor value to override the editor\n# specified in the environment. You can add several editors separated by ';'\n\n# Default editor\n#editor = gedit;kwrite;gvim;emacs;nano;vi\n\n# Environment auto-launcher\n# based on the association between mime type and applications\n#autolaunchers = gnome-open;kde-open;xdg-open\n\n# Specific settings by content-type or meta-type. Specific\n# settings override general options above. Content-type settings\n# override meta-type settings for the same option.\n\n[meta-type:DTML Document]\nextension=.dtml\n\n[meta-type:DTML Method]\nextension=.dtml\n\n[meta-type:Script (Python)]\nextension=.py\n\n[meta-type:Page Template]\nextension=.pt\n\n[meta-type:Z SQL Method]\nextension=.sql\n\n[content-type:text/plain]\nextension=.txt\n\n[content-type:text/html]\nextension=.html\n\n[content-type:text/xml]\nextension=.xml\n\n[content-type:text/css]\nextension=.css\n\n[content-type:text/javascript]\nextension=.js\n\n[general-type:image/*]\neditor=gimp -n\n\n[content-type:application/x-xcf]\neditor=gimp -n\n\n[content-type:application/vnd.oasis.opendocument.text]\nextension=.odt\neditor=\n\n[content-type:application/vnd.sun.xml.writer]\nextension=.sxw\neditor=\n\n[content-type:application/vnd.sun.xml.calc]\nextension=.sxc\neditor=\n\n[content-type:application/vnd.oasis.opendocument.spreadsheet]\nextension=.ods\neditor=\n\n[content-type:application/vnd.oasis.opendocument.presentation]\nextension=.odp\neditor=\n\n[content-type:application/msword]\nextension=.doc\neditor=\n\n[content-type:application/vnd.ms-excel]\nextension=.xls\neditor=\n\n[content-type:application/vnd.ms-powerpoint]\nextension=.ppt\neditor=\n\n[content-type:application/x-freemind]\nextension=.mm\neditor=freemind\n\n[content-type:text/xml]\nextension=.planner\neditor=planner\n"

def main():
    """ call zopeedit as a lib
    """
    args = sys.argv
    input_file = ''
    if '--version' in args or '-v' in args:
        credits = 'Zope External Editor %s\nBy atReal\nhttp://www.atreal.net' % __version__
        messageDialog(credits)
        sys.exit(0)
    if '--help' in args or '-h' in args:
        try:
            f = open(os.path.join(system_path, 'docs', 'README.txt'), 'r')
        except IOError:
            f = open(os.path.join(system_path, '..', '..', 'README.txt'), 'r')
        else:
            README = f.readlines()
            f.close()
            messageScrolledText(README)
            sys.exit(0)
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        try:
            ExternalEditor(input_file).launch()
        except (KeyboardInterrupt, SystemExit):
            pass
        except:
            fatalError(sys.exc_info()[1])

    else:
        ExternalEditor().editConfig()


if __name__ == '__main__':
    main()