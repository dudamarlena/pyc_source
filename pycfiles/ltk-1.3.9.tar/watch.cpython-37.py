# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/watch.py
# Compiled at: 2020-04-10 17:22:03
# Size of source mod 2**32: 22754 bytes
import ctypes
from ltk.actions.action import Action
from ltk.actions import add_action
from ltk.actions import request_action
from ltk.actions import download_action
import ltk.logger as logger
from ltk.utils import map_locale, restart, get_relative_path, log_error
from ltk.locales import locale_list
import time, requests
from requests.exceptions import ConnectionError
import os, re, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent
from ltk.watchhandler import WatchHandler
from ltk.git_auto import Git_Auto
import ltk.check_connection
DEFAULT_COMMIT_MESSAGE = 'Translations updated for '

def retry(logger, timeout=5, exec_type=None):
    if not exec_type:
        exec_type = [
         requests.exceptions.ConnectionError]

    def decorator(function):

        def wrapper(*args, **kwargs):
            while True:
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    try:
                        log_error(self.error_file_name, e)
                        if e.__class__ in exec_type:
                            logger.error('Connection has timed out. Retrying..')
                            time.sleep(timeout)
                        else:
                            raise e
                    finally:
                        e = None
                        del e

        return wrapper

    return decorator


def has_hidden_attribute(file_path):
    """ Detects if a file has hidden attributes """
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False

    return result


class WatchAction(Action):

    def __init__(self, path=None, timeout=60):
        Action.__init__(self, path, True, timeout)
        self.observers = []
        self.handler = WatchHandler()
        self.handler.on_modified = self._on_modified
        self.handler.on_created = self._on_created
        self.handler.on_moved = self._on_moved
        self.watch_queue = []
        self.locale_delimiter = None
        self.ignore_ext = []
        self.detected_locales = {}
        self.watch_folder = True
        self.timeout = timeout
        self.updated = {}
        self.git_auto = Git_Auto(path)
        self.polled_list = set([])
        self.force_poll = False
        self.add = add_action.AddAction(path)
        self.download = download_action.DownloadAction(path)
        self.root_path = path
        self.download_file_paths = set()

    def is_hidden_file--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              abspath
                6  LOAD_FAST                'file_path'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  LOAD_METHOD              replace
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                path
               16  LOAD_STR                 ''
               18  CALL_METHOD_2         2  '2 positional arguments'
               20  STORE_FAST               'name'

 L.  90        22  LOAD_GLOBAL              has_hidden_attribute
               24  LOAD_FAST                'file_path'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  POP_JUMP_IF_TRUE     54  'to 54'
               30  LOAD_STR                 'Thumbs.db'
               32  LOAD_FAST                'file_path'
               34  COMPARE_OP               in
               36  POP_JUMP_IF_TRUE     54  'to 54'
               38  LOAD_STR                 'ehthumbs.db'
               40  LOAD_FAST                'file_path'
               42  COMPARE_OP               in
               44  POP_JUMP_IF_TRUE     54  'to 54'
               46  LOAD_STR                 'desktop.ini'
               48  LOAD_FAST                'file_path'
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    58  'to 58'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            36  '36'
             54_2  COME_FROM            28  '28'

 L.  91        54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.  92        58  SETUP_LOOP          136  'to 136'
               60  LOAD_FAST                'name'
               62  LOAD_STR                 ''
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE   134  'to 134'

 L.  93        68  LOAD_FAST                'name'
               70  LOAD_METHOD              startswith
               72  LOAD_STR                 '.'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_JUMP_IF_TRUE     96  'to 96'
               78  LOAD_FAST                'name'
               80  LOAD_METHOD              startswith
               82  LOAD_STR                 '~'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_JUMP_IF_TRUE     96  'to 96'
               88  LOAD_FAST                'name'
               90  LOAD_STR                 '4913'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   100  'to 100'
             96_0  COME_FROM            86  '86'
             96_1  COME_FROM            76  '76'

 L.  94        96  LOAD_CONST               True
               98  RETURN_VALUE     
            100_0  COME_FROM            94  '94'

 L.  95       100  LOAD_FAST                'name'
              102  LOAD_METHOD              split
              104  LOAD_GLOBAL              os
              106  LOAD_ATTR                sep
              108  CALL_METHOD_1         1  '1 positional argument'
              110  LOAD_CONST               1
              112  LOAD_CONST               None
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  STORE_FAST               'name'

 L.  96       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                sep
              124  LOAD_METHOD              join
              126  LOAD_FAST                'name'
              128  CALL_METHOD_1         1  '1 positional argument'
              130  STORE_FAST               'name'
              132  JUMP_BACK            60  'to 60'
            134_0  COME_FROM            66  '66'
              134  POP_BLOCK        
            136_0  COME_FROM_LOOP       58  '58'

 L.  97       136  LOAD_CONST               False
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 138

    def is_translation(self, file_name):
        locales = locale_list
        if any(('.' + locale in file_name for locale in locales)):
            locales = {v:k for k, v in enumerate(locales) if v in file_name}.keys()
            replace_target = None
            for locale in locales:
                original = file_name
                file_name = file_name.replace('.' + locale)''
                if file_name != original:
                    replace_target = locale
                    break

            file_name = re.sub('\\.{2,}', '.', file_name)
            file_name = file_name.rstrip('.')
            doc = self.doc_manager.get_doc_by_prop'file_name'file_name.replaceself.path''
            replace_target = replace_target.replace'-''_'
            if doc:
                if 'locales' in doc:
                    if replace_target in doc['locales']:
                        return True
        return False

    def check_remote_doc_exist(self, fn, document_id=None):
        """ check if a document exists remotely """
        if not document_id:
            entry = self.doc_manager.get_doc_by_prop'file_name'fn
            document_id = entry['id']
        response = self.api.get_document(document_id)
        if response.status_code != 200:
            return False
        return True

    def _on_modified(self, event):
        """ Notify Lingotek cloud when a previously added file is modified """
        try:
            db_entries = self.doc_manager.get_all_entries()
            in_db = False
            fn = ''
            for entry in db_entries:
                if event.src_path.endswith(entry['file_name']):
                    fn = entry['file_name']
                    in_db = True

            if not event.is_directory:
                if in_db:
                    try:
                        if self.check_remote_doc_exist(fn):
                            if self.doc_manager.is_doc_modifiedfnself.path:
                                try:
                                    self.polled_list.remove(fn)
                                except Exception:
                                    pass

                                self.update_content(fn)
                    except KeyboardInterrupt:
                        for observer in self.observers:
                            observer.stop()

                    except ConnectionError:
                        print('Could not connect to remote server.')
                        restart()
                    except ValueError:
                        print(sys.exc_info()[1])
                        restart()

        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()

        except Exception as err:
            try:
                restart('Error on modified: ' + str(err) + '\nRestarting watch.')
            finally:
                err = None
                del err

    def _on_created(self, event):
        try:
            db_entries = self.doc_manager.get_all_entries()
            in_db = False
            fn = ''
            for entry in db_entries:
                if event.src_path.endswith(entry['file_name']):
                    fn = entry['file_name']
                    in_db = True

            if not event.is_directory:
                if in_db:
                    self._on_modified(event)
            else:
                file_path = event.src_path
                if file_path in self.download_file_paths:
                    self.download_file_paths.remove(file_path)
                    return
            if not self.is_hidden_file(file_path):
                if not self.is_translation(file_path):
                    relative_path = file_path.replaceself.path''
                    title = os.path.basename(os.path.normpath(file_path))
                    curr_ext = os.path.splitext(file_path)[1]
                    return curr_ext in self.ignore_ext or os.path.isfile(file_path) or None
                    try:
                        if self.doc_manager.is_doc_newrelative_pathself.root_path and self.watch_folder:
                            self.add_document(file_path, title, locale=(self.locale))
                        else:
                            if self.doc_manager.is_doc_modifiedrelative_pathself.path:
                                self.update_content(relative_path)
                            else:
                                return
                    except KeyboardInterrupt:
                        for observer in self.observers:
                            observer.stop()

                    except ConnectionError:
                        print('Could not connect to remote server.')
                        restart()
                    except ValueError:
                        print(sys.exc_info()[1])
                        restart()

                    doc = self.doc_manager.get_doc_by_prop'file_name'relative_path
                    if doc:
                        document_id = doc['id']
                    else:
                        return
                        if self.locale_delimiter:
                            try:
                                curr_locale = title.split(self.locale_delimiter)[(-2)]
                                fixed_locale = map_locale(curr_locale)
                                if fixed_locale:
                                    print('fixed locale: ', fixed_locale)
                                    self.detected_locales[document_id] = fixed_locale
                                else:
                                    logger.warning("This document's detected locale: {0} is not supported.".format(curr_locale))
                            except IndexError:
                                logger.warning('Cannot detect locales from file: {0}, not adding any locales'.format(title))

                        self.watch_add_targetrelative_pathdocument_id
        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()

    def _on_moved(self, event):
        """Used for programs, such as gedit, that modify documents by moving (overwriting)
        the previous document with the temporary file. Only the moved event contains the name of the
        destination file."""
        try:
            event = FileSystemEvent(event.dest_path)
            self._on_modified(event)
        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()

        except Exception as err:
            try:
                restart('Error on moved: ' + str(err) + '\nRestarting watch.')
            finally:
                err = None
                del err

    def get_watch_locales(self, document_id):
        """ determine the locales that should be added for a watched doc """
        locales = []
        if self.detected_locales:
            try:
                locales = [
                 self.detected_locales[document_id]]
            except KeyError:
                logger.error('Something went wrong. Could not detect a locale')

            return locales
        entry = self.doc_manager.get_doc_by_prop'id'document_id
        try:
            locales = [locale for locale in self.watch_locales if locale not in entry['locales']]
        except KeyError:
            locales = self.watch_locales

        return locales

    def watch_add_target(self, file_name, document_id):
        if not file_name:
            title = self.doc_manager.get_doc_by_prop'id'document_id
        else:
            title = os.path.basename(file_name)
        if document_id not in self.watch_queue:
            self.watch_queue.append(document_id)
        if self.check_remote_doc_existtitledocument_id:
            locales_to_add = self.get_watch_locales(document_id)
            if locales_to_add == ['[]']:
                locales_to_add = []
            if self.api.get_document(document_id):
                request = request_action.RequestAction(self.path, title, file_name, locales_to_add, None, None, None, None, document_id, True)
                if request.target_action():
                    if document_id in self.watch_queue:
                        self.watch_queue.remove(document_id)

    def process_queue(self):
        """do stuff with documents in queue (currently just add targets)"""
        for document_id in self.watch_queue:
            self.watch_add_targetNonedocument_id

    def update_content(self, relative_path):
        if self.update_document_action(os.path.joinself.pathrelative_path):
            self.updated[relative_path] = 0
            logger.info('Updating remote content: {0}'.format(relative_path))

    def check_modified(self, doc):
        old_date = doc['last_mod']
        response = self.api.get_document(doc['id'])
        if response.status_code == 200:
            new_date = response.json()['properties']['modified_date']
        else:
            print('Document not found on Lingotek Cloud: ' + str(doc['name']))
            return False
            if int(old_date) < int(str(new_date)[0:10]):
                return True
            return False

    @retry(logger)
    def poll_remote(self):
        """ poll lingotek servers to check if translation is finished """
        if self.auto_format_option == 'on':
            autoFormat = True
        else:
            autoFormat = False
        documents = self.doc_manager.get_all_entries()
        git_commit_message = DEFAULT_COMMIT_MESSAGE
        for doc in documents:
            doc_id = doc['id']
            if doc_id in self.watch_queue:
                continue
            file_name = doc['file_name']
            if file_name in self.updated:
                if self.updated[file_name] > 3:
                    self.updated.popfile_nameNone
                else:
                    self.updated[file_name] += self.timeout
                    continue
            try:
                downloaded = doc['downloaded']
            except KeyError:
                downloaded = []
                self.doc_manager.update_document('downloaded', downloaded, doc_id)

            if file_name not in self.polled_list or self.force_poll:
                locale_progress = self.import_locale_info(doc_id, poll=True)
                for locale in locale_progress:
                    progress = locale_progress[locale]
                    if progress == 100:
                        if locale not in downloaded:
                            logger.info('Translation completed ({0} - {1})\n'.formatfile_namelocale)
                            if self.locale_delimiter:
                                locale = locale.replace'_''-'
                                download_file_path = self.download.download_action(doc_id, locale, autoFormat, xliff=False, locale_ext=False)
                            else:
                                locale = locale.replace'_''-'
                                if self.clone_option == 'on':
                                    download_file_path = self.download.download_action(doc_id, locale, autoFormat, xliff=False, locale_ext=False)
                                else:
                                    download_file_path = self.download.download_action(doc_id, locale, autoFormat)
                            self.download_file_paths.add(download_file_path)
                    if progress != 100 and locale in downloaded:
                        self.doc_manager.remove_element_in_prop(doc_id, 'downloaded', locale)

                if set(locale_progress.keys()) == set(downloaded) and all((value == 100 for value in locale_progress.values())):
                    self.polled_list.add(file_name)

    def complete_path(self, file_location):
        abspath = os.path.abspath(file_location)
        print
        return abspath.rstrip(os.sep)

    def watch_action(self, ignore, delimiter=None, no_folders=False, force_poll=False):
        watch_paths = None
        if not watch_paths:
            watch_paths = self.folder_manager.get_file_names()
            for i in range(len(watch_paths)):
                watch_paths[i] = get_relative_path(self.path, watch_paths[i])

        else:
            watch_paths_list = []
            for path in watch_paths:
                watch_paths_list.append(path.rstrip(os.sep))

            watch_paths = watch_paths_list
        if len(watch_paths):
            if not no_folders:
                self.watch_folder = True
            else:
                watch_paths = [
                 os.getcwd()]
        elif self.watch_folder:
            watch_message = 'Watching for updates in '
            for i in range(len(watch_paths)):
                watch_paths[i] = self.complete_path(watch_paths[i])
                watch_message += '{0}'.format(watch_paths[i])
                if i < len(watch_paths) - 1:
                    watch_message += ' '

            print(watch_message)
        else:
            print('Watching for updates to added documents')
        if force_poll:
            self.force_poll = True
        self.ignore_ext.extend(ignore)
        self.locale_delimiter = delimiter
        for watch_path in watch_paths:
            observer = Observer()
            observer.schedule((self.handler), path=watch_path, recursive=True)
            try:
                observer.start()
            except OSError as e:
                try:
                    logger.warning('Watching too many items, please be more specific by using ltk add on the files and folders that should be watched')
                    return
                finally:
                    e = None
                    del e

            self.observers.append(observer)

        queue_timeout = 3
        try:
            while True:
                if ltk.check_connection.check_for_connection():
                    self.poll_remote()
                    current_timeout = self.timeout
                    while len(self.watch_queue) and current_timeout > 0:
                        self.process_queue()
                        time.sleep(queue_timeout)
                        current_timeout -= queue_timeout

                time.sleep(current_timeout)

        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()

        for observer in self.observers:
            observer.join()