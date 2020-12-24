# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/utils.py
# Compiled at: 2013-02-13 13:37:18
"""Utils class."""
import os, re, time, atomac, fnmatch, logging, threading, traceback, logging.handlers
from constants import abbreviated_roles, ldtp_class_type
from server_exception import LdtpServerException
importPsUtil = False
try:
    import psutil
    importPsUtil = True
except ImportError:
    pass

class LdtpCustomLog(logging.Handler):
    """
    Custom LDTP log, inherit logging.Handler and implement
    required API
    """

    def __init__(self):
        logging.Handler.__init__(self)
        self.log_events = []

    def emit(self, record):
        self.log_events.append('%s-%s' % (record.levelname, record.getMessage()))


logging.handlers.LdtpCustomLog = LdtpCustomLog
_custom_logger = logging.handlers.LdtpCustomLog()
_custom_logger.setLevel(logging.ERROR)
logger = logging.getLogger('')
logger.addHandler(_custom_logger)
LDTP_LOG_MEMINFO = 60
LDTP_LOG_CPUINFO = 61
logging.addLevelName(LDTP_LOG_MEMINFO, 'MEMINFO')
logging.addLevelName(LDTP_LOG_CPUINFO, 'CPUINFO')

class ProcessStats(threading.Thread):
    """
    Capturing Memory and CPU Utilization statistics for an application and its related processes
    NOTE: You have to install python-psutil package
    EXAMPLE USAGE:

    xstats = ProcessStats('evolution', 2)
    # Start Logging by calling start
    xstats.start()
    # Stop the process statistics gathering thread by calling the stopstats method
    xstats.stop()
    """

    def __init__(self, appname, interval=2):
        """
        Start memory and CPU monitoring, with the time interval between
        each process scan

        @param appname: Process name, ex: firefox-bin.
        @type appname: string
        @param interval: Time interval between each process scan
        @type interval: float
        """
        if not importPsUtil:
            raise LdtpServerException('python-psutil package is not installed')
        threading.Thread.__init__(self)
        self._appname = appname
        self._interval = interval
        self._stop = False
        self.running = True

    def __del__(self):
        self._stop = False
        self.running = False

    def get_cpu_memory_stat(self):
        proc_list = []
        for p in psutil.process_iter():
            if self._stop:
                self.running = False
                return proc_list
            if not re.match(fnmatch.translate(self._appname), p.name, re.U | re.L):
                continue
            proc_list.append(p)

        return proc_list

    def run(self):
        while not self._stop:
            for p in self.get_cpu_memory_stat():
                try:
                    logger.log(LDTP_LOG_MEMINFO, '%s(%s) - %s' % (
                     p.name, str(p.pid), p.get_memory_percent()))
                    logger.log(LDTP_LOG_CPUINFO, '%s(%s) - %s' % (
                     p.name, str(p.pid), p.get_cpu_percent()))
                except psutil.AccessDenied:
                    pass

            try:
                time.sleep(self._interval)
            except KeyboardInterrupt:
                self._stop = True

    def stop(self):
        self._stop = True
        self.running = False


class Utils(object):

    def __init__(self):
        self._appmap = {}
        self._windows = {}
        self._obj_timeout = 5
        self._window_timeout = 30
        self._app_under_test = None
        self._custom_logger = _custom_logger
        self._running_apps = atomac.NativeUIElement._getRunningApps()
        if os.environ.has_key('LDTP_DEBUG'):
            self._ldtp_debug = True
            self._custom_logger.setLevel(logging.DEBUG)
        else:
            self._ldtp_debug = False
        return

    def _listMethods(self):
        _methods = []
        for symbol in dir(self):
            if symbol.startswith('_'):
                continue
            _methods.append(symbol)

        return _methods

    def _methodHelp(self, method):
        return getattr(self, method).__doc__

    def _dispatch(self, method, args):
        try:
            return getattr(self, method)(*args)
        except:
            if self._ldtp_debug:
                print traceback.format_exc()
            raise

    def _get_front_most_window(self):
        front_app = atomac.NativeUIElement.getFrontmostApp()
        return front_app.windows()[0]

    def _ldtpize_accessible(self, acc):
        """
        Get LDTP format accessibile name

        @param acc: Accessible handle
        @type acc: object

        @return: object type, stripped object name (associated / direct),
                        associated label
        @rtype: tuple
        """
        actual_role = self._get_role(acc)
        label = self._get_title(acc)
        if re.match('AXWindow', actual_role, re.M | re.U | re.L):
            strip = '( |\\n)'
        else:
            strip = '( |:|\\.|_|\\n)'
        if label:
            if not isinstance(label, unicode):
                label = '%s' % label
            label = re.sub(strip, '', label)
        role = abbreviated_roles.get(actual_role, 'ukn')
        if self._ldtp_debug and role == 'ukn':
            print (
             actual_role, acc)
        return (
         role, label)

    def _glob_match(self, pattern, string):
        """
        Match given string, by escaping regex characters
        """
        return bool(re.match(fnmatch.translate(pattern), string, re.M | re.U | re.L))

    def _match_name_to_appmap(self, name, acc):
        if not name:
            return 0
        if self._glob_match(name, acc['obj_index']):
            return 1
        if self._glob_match(name, acc['label']):
            return 1
        role = acc['class']
        if role == 'frame' or role == 'dialog' or role == 'window':
            strip = '( |\n)'
        else:
            strip = '( |:|\\.|_|\n)'
        obj_name = re.sub(strip, '', name)
        if acc['label']:
            _tmp_name = re.sub(strip, '', acc['label'])
            if self._glob_match(obj_name, _tmp_name):
                return 1
        return 0

    def _insert_obj(self, obj_dict, obj, parent, child_index):
        ldtpized_name = self._ldtpize_accessible(obj)
        if ldtpized_name[0] in self._ldtpized_obj_index:
            self._ldtpized_obj_index[ldtpized_name[0]] += 1
        else:
            self._ldtpized_obj_index[ldtpized_name[0]] = 0
        try:
            key = '%s%s' % (ldtpized_name[0], ldtpized_name[1])
        except UnicodeEncodeError:
            key = '%s%s' % (ldtpized_name[0],
             ldtpized_name[1].decode('utf-8'))

        if not ldtpized_name[1]:
            index = 0
            key = '%s%d' % (ldtpized_name[0], index)
        else:
            index = 1
        while obj_dict.has_key(key):
            try:
                key = '%s%s%d' % (ldtpized_name[0],
                 ldtpized_name[1], index)
            except UnicodeEncodeError:
                key = '%s%s%d' % (ldtpized_name[0],
                 ldtpized_name[1].decode('utf-8'), index)

            index += 1

        if ldtpized_name[0] == 'frm':
            obj_index = '%s#%d' % (ldtpized_name[0],
             self._ldtpized_obj_index[ldtpized_name[0]])
        else:
            obj_index = '%s#%d' % (ldtpized_name[0],
             self._ldtpized_obj_index[ldtpized_name[0]])
        if parent in obj_dict:
            _current_children = obj_dict[parent]['children']
            if _current_children:
                _current_children = '%s %s' % (_current_children, key)
            else:
                _current_children = key
            obj_dict[parent]['children'] = _current_children
        actual_role = self._get_role(obj)
        obj_dict[key] = {'obj': obj, 'class': ldtp_class_type.get(actual_role, actual_role), 
           'label': ldtpized_name[1], 
           'parent': parent, 
           'children': '', 
           'child_index': child_index, 
           'obj_index': obj_index}
        return key

    def _get_windows(self, force_remap=False):
        if not force_remap and self._windows:
            return self._windows
        self._update_apps()
        windows = {}
        self._ldtpized_obj_index = {}
        for gui in set(self._running_apps):
            if self._app_under_test and self._app_under_test != gui.bundleIdentifier() and self._app_under_test != gui.localizedName():
                continue
            pid = gui.processIdentifier()
            app = atomac.getAppRefByPid(pid)
            app_windows = app.windows()
            try:
                if not app_windows and app.AXRole == 'AXApplication':
                    key = self._insert_obj(windows, app, '', -1)
                    windows[key]['app'] = app
                    continue
            except (atomac._a11y.ErrorAPIDisabled, atomac._a11y.ErrorCannotComplete):
                pass

            for window in app_windows:
                if not window:
                    continue
                key = self._insert_obj(windows, window, '', -1)
                windows[key]['app'] = app

        self._windows = windows
        return windows

    def _get_title(self, obj):
        title = ''
        role = ''
        try:
            role = obj.AXRole
            desc = obj.AXRoleDescription
            if re.match('(AXStaticText|AXRadioButton|AXButton)', role, re.M | re.U | re.L) and (desc == 'text' or desc == 'radio button' or desc == 'button') and obj.AXValue:
                return obj.AXValue
        except:
            pass

        try:
            checkBox = re.match('AXCheckBox', role, re.M | re.U | re.L)
            if checkBox:
                try:
                    title = obj.AXHelp
                except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
                    pass

            if not title:
                title = obj.AXTitle
        except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
            try:
                text = re.match('(AXTextField|AXTextArea)', role, re.M | re.U | re.L)
                if text:
                    title = obj.AXFilename
                elif not re.match('(AXTabGroup)', role, re.M | re.U | re.L):
                    if re.match('(AXScrollBar)', role, re.M | re.U | re.L):
                        title = ''
                    else:
                        title = obj.AXValue
            except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
                if re.match('AXButton', role, re.M | re.U | re.L):
                    try:
                        title = obj.AXDescription
                        if title:
                            return title
                    except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
                        pass

                try:
                    if not re.match('(AXList|AXTable)', role, re.M | re.U | re.L):
                        title = obj.AXRoleDescription
                except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
                    pass

        if title or re.match('(AXButton|AXCheckBox)', role, re.M | re.U | re.L):
            try:
                title = obj.AXRoleDescription
                if title:
                    return title
            except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
                pass

        else:
            if re.match('(AXStaticText)', role, re.M | re.U | re.L):
                try:
                    title = obj.AXValue
                    if title:
                        return title
                except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
                    pass

            return ''
        return title

    def _get_role(self, obj):
        role = ''
        try:
            role = obj.AXRole
        except (atomac._a11y.ErrorUnsupported, atomac._a11y.Error):
            pass

        return role

    def _update_apps(self):
        self._running_apps = atomac.NativeUIElement._getRunningApps()

    def _singleclick(self, window_name, object_name):
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        size = self._getobjectsize(object_handle)
        self._grabfocus(object_handle)
        self.wait(0.5)
        self.generatemouseevent(size[0] + size[2] / 2, size[1] + size[3] / 2, 'b1c')
        return 1

    def _grabfocus(self, handle):
        if not handle:
            raise LdtpServerException('Invalid handle')
        if handle.AXRole == 'AXWindow':
            handle.Raise()
        else:
            handle.AXWindow.Raise()
            handle.activate()
        return 1

    def _getobjectsize(self, handle):
        if not handle:
            raise LdtpServerException('Invalid handle')
        x, y = handle.AXPosition
        width, height = handle.AXSize
        return (x, y, width, height)

    def _get_window_handle(self, window_name, wait_for_window=True):
        if not window_name:
            raise LdtpServerException('Invalid argument passed to window_name')
        orig_window_name = window_name
        window_obj = (None, None, None)
        strip = '( |\\n)'
        if not isinstance(window_name, unicode):
            window_name = '%s' % window_name
        stripped_window_name = re.sub(strip, '', window_name)
        window_name = fnmatch.translate(window_name)
        stripped_window_name = fnmatch.translate(stripped_window_name)
        windows = self._get_windows()

        def _internal_get_window_handle(windows):
            for window in windows:
                label = windows[window]['label']
                strip = '( |\\n)'
                if not isinstance(label, unicode):
                    label = '%s' % label
                stripped_label = re.sub(strip, '', label)
                if re.match(window_name, window) or re.match(window_name, label) or re.match(window_name, stripped_label) or re.match(stripped_window_name, window) or re.match(stripped_window_name, label) or re.match(stripped_window_name, stripped_label):
                    return (
                     windows[window]['obj'], window, windows[window]['app'])

            return (None, None, None)

        if wait_for_window:
            window_timeout = self._obj_timeout
        else:
            window_timeout = 1
        for retry in range(0, window_timeout):
            window_obj = _internal_get_window_handle(windows)
            if window_obj[0]:
                return window_obj
            if window_timeout <= 1:
                break
            time.sleep(1)
            windows = self._get_windows(True)

        if not window_obj[0]:
            raise LdtpServerException('Unable to find window "%s"' % orig_window_name)
        return window_obj

    def _get_object_handle(self, window_name, obj_name, obj_type=None, wait_for_object=True):
        try:
            return self._internal_get_object_handle(window_name, obj_name, obj_type, wait_for_object)
        except atomac._a11y.ErrorInvalidUIElement:
            self._windows = {}
            return self._internal_get_object_handle(window_name, obj_name, obj_type, wait_for_object)

    def _internal_get_object_handle(self, window_name, obj_name, obj_type=None, wait_for_object=True):
        try:
            obj = self._get_object_map(window_name, obj_name, obj_type, wait_for_object)
            object_handle = obj['obj']
            object_handle.AXWindow.AXRole
        except (atomac._a11y.ErrorCannotComplete, atomac._a11y.ErrorUnsupported,
         atomac._a11y.ErrorInvalidUIElement, AttributeError):
            self._windows = {}
            obj = self._get_object_map(window_name, obj_name, obj_type, wait_for_object, True)

        return obj['obj']

    def _get_object_map(self, window_name, obj_name, obj_type=None, wait_for_object=True, force_remap=False):
        if not window_name:
            raise LdtpServerException('Unable to find window %s' % window_name)
        window_handle, ldtp_window_name, app = self._get_window_handle(window_name, wait_for_object)
        if not window_handle:
            raise LdtpServerException('Unable to find window %s' % window_name)
        strip = '( |:|\\.|_|\\n)'
        if not isinstance(obj_name, unicode):
            obj_name = '%s' % obj_name
        stripped_obj_name = re.sub(strip, '', obj_name)
        obj_name = fnmatch.translate(obj_name)
        stripped_obj_name = fnmatch.translate(stripped_obj_name)
        object_list = self._get_appmap(window_handle, ldtp_window_name, force_remap)

        def _internal_get_object_handle(object_list):
            for obj in object_list:
                if obj_type and object_list[obj]['class'] != obj_type:
                    continue
                label = object_list[obj]['label']
                strip = '( |:|\\.|_|\\n)'
                if not isinstance(label, unicode):
                    label = '%s' % label
                stripped_label = re.sub(strip, '', label)
                if re.match(obj_name, obj) or re.match(obj_name, label) or re.match(obj_name, stripped_label) or re.match(stripped_obj_name, obj) or re.match(stripped_obj_name, label) or re.match(stripped_obj_name, stripped_label):
                    return object_list[obj]

        if wait_for_object:
            obj_timeout = self._obj_timeout
        else:
            obj_timeout = 1
        for retry in range(0, obj_timeout):
            obj = _internal_get_object_handle(object_list)
            if obj:
                return obj
            if obj_timeout <= 1:
                break
            time.sleep(1)
            object_list = self._get_appmap(window_handle, ldtp_window_name, True)

        raise LdtpServerException('Unable to find object %s' % obj_name)

    def _populate_appmap(self, obj_dict, obj, parent, child_index):
        index = -1
        if obj:
            if child_index != -1:
                parent = self._insert_obj(obj_dict, obj, parent, child_index)
            try:
                if not obj.AXChildren:
                    return
            except atomac._a11y.Error:
                return

            for child in obj.AXChildren:
                index += 1
                if not child:
                    continue
                self._populate_appmap(obj_dict, child, parent, index)

    def _get_appmap(self, window_handle, window_name, force_remap=False):
        if not window_handle or not window_name:
            return {}
        if not force_remap and self._appmap.has_key(window_name):
            return self._appmap[window_name]
        obj_dict = {}
        self._ldtpized_obj_index = {}
        self._populate_appmap(obj_dict, window_handle, '', -1)
        self._appmap[window_name] = obj_dict
        return obj_dict

    def _get_menu_handle(self, window_name, object_name, wait_for_window=True):
        window_handle, name, app = self._get_window_handle(window_name, wait_for_window)
        if not window_handle:
            raise LdtpServerException('Unable to find window %s' % window_name)
        menu = re.sub('mnu', '', object_name)
        if re.match('^\\d', menu):
            obj_dict = self._get_appmap(window_handle, name)
            return obj_dict[object_name]['obj']
        menu_handle = app.menuItem(menu)
        if menu_handle:
            return menu_handle
        menu_handle_list = window_handle.findAllR(AXRole='AXMenu')
        for menu_handle in menu_handle_list:
            sub_menu_handle = self._get_sub_menu_handle(menu_handle, object_name)
            if sub_menu_handle:
                return sub_menu_handle

        raise LdtpServerException('Unable to find menu %s' % object_name)

    def _get_sub_menu_handle(self, children, menu):
        strip = '( |:|\\.|_|\\n)'
        tmp_menu = fnmatch.translate(menu)
        stripped_menu = fnmatch.translate(re.sub(strip, '', menu))
        for current_menu in children.AXChildren:
            role, label = self._ldtpize_accessible(current_menu)
            if re.match(tmp_menu, label) or re.match(tmp_menu, '%s%s' % (role, label)) or re.match(stripped_menu, label) or re.match(stripped_menu, '%s%s' % (role, label)):
                return current_menu

        raise LdtpServerException('Unable to find menu %s' % menu)

    def _internal_menu_handler(self, menu_handle, menu_list, perform_action=False):
        if not menu_handle or not menu_list:
            raise LdtpServerException('Unable to find menu %s' % [0])
        for menu in menu_list:
            if not menu_handle.AXChildren:
                try:
                    menu_handle.Press()
                except atomac._a11y.ErrorCannotComplete:
                    pass

            children = menu_handle.AXChildren[0]
            if not children:
                raise LdtpServerException('Unable to find menu %s' % menu)
            menu_handle = self._get_sub_menu_handle(children, menu)
            if perform_action and menu_list[(-1)] != menu:
                if not menu_handle.AXEnabled:
                    menu_handle.Cancel()
                    raise LdtpServerException('Object %s state disabled' % menu)
                    menu_handle.Press()
                    self.wait(1)
            if not menu_handle:
                raise LdtpServerException('Unable to find menu %s' % menu)

        return menu_handle