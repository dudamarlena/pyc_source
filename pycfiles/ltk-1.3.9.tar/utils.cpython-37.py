# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/utils.py
# Compiled at: 2020-01-30 14:00:13
# Size of source mod 2**32: 13792 bytes
import os, sys
from ltk.locales import default_locales, locale_list
import ltk.logger as logger
import time, logging, traceback
from ltk import exceptions
try:
    from blessings import Terminal
    term = Terminal()
except ImportError:
    term = False

class Enum(set):

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


def detect_format(file_name, get_mapper=False):
    format_mapper = {'.csv':'CSV', 
     '.dita':'DITA', 
     '.ditamap':'DITAMAP', 
     '.docx':'DOCX_OKAPI', 
     '.doc':'WORD_OKAPI', 
     '.dtd':'DTD', 
     '.xlsx':'XLSX_OKAPI', 
     '.idml':'IDML', 
     '.properties':'JAVA_PROPERTIES_OKAPI', 
     '.json':'JSON', 
     '.pdf':'PDF', 
     '.txt':'PLAINTEXT_OKAPI', 
     '.po':'PO', 
     '.ppt':'PPT_OKAPI', 
     '.pptx':'PPTX_OKAPI', 
     '.resx':'RESX', 
     '.regex':'REGEX', 
     '.rtf':'RTF_OKAPI', 
     '.srt':'SUBTITLE_RIP', 
     '.strings':'APPLE_STRINGS', 
     '.tsv':'TABLE', 
     '.ts':'TS', 
     '.xml':'XML_OKAPI'}
    format_mapper.update(dict.fromkeys(['.dox', '.c', '.h', '.cpp'], 'DOXYGEN'))
    format_mapper.update(dict.fromkeys(['.html', '.htm'], 'HTML_OKAPI'))
    format_mapper.update(dict.fromkeys(['.odp', '.otp'], 'ODP'))
    format_mapper.update(dict.fromkeys(['.ods', '.ots'], 'ODS'))
    format_mapper.update(dict.fromkeys(['.odt', '.ott'], 'ODT'))
    format_mapper.update(dict.fromkeys(['.yaml', '.yml'], 'RAILS_YAML'))
    format_mapper.update(dict.fromkeys(['.xliff', '.xlf'], 'XLIFF_OKAPI'))
    if get_mapper:
        return format_mapper
    name, extension = os.path.splitext(file_name)
    return format_mapper.get(extension.lower(), 'PLAINTEXT_OKAPI')


def map_locale(locale):
    """
    maps incorrectly formatted locales to valid locales for use with Lingotek API
    :param locale: incorrectly formatted locale
    :return: valid locale
    """
    try:
        return default_locales[locale]
    except KeyError:
        return


def restart(message='Restarting watch', interval=5):
    """Restarts the program. Used after exceptions. Otherwise, watch doesn't work anymore."""
    time.sleep(interval)
    print(message)
    cmd = 'ltk'
    for arg in sys.argv[1:]:
        cmd = cmd + ' ' + arg

    os.system(cmd)


def is_valid_locale(api, locale):
    """Returns true if the locale is found in Lingotek's remote list of locales or, if the api call fails, if the locale is found in the local list of locales."""
    valid_locales = []
    response = api.list_locales()
    remote_check = False
    if response.status_code == 200:
        remote_check = True
    locale_json = response.json()
    for entry in locale_json:
        valid_locales.append(locale_json[entry]['locale'])

    locales = []
    check_locale = locale.replace('-', '_')
    if not (remote_check and check_locale not in valid_locales):
        if not remote_check:
            if check_locale not in locale_list:
                return False
    return True


def get_valid_locales(api, entered_locales, operation_text):
    """Return the list of valid locales, checking locales either remotely or using a local list of locales."""
    valid_locales = []
    response = api.list_locales()
    remote_check = False
    if response.status_code == 200:
        remote_check = True
    else:
        locale_json = response.json()
        for entry in locale_json:
            valid_locales.append(locale_json[entry]['locale'])

        locales = []
        if not (len(entered_locales) == 0 or len(entered_locales)) == 1 or entered_locales[0] == '[]':
            logger.warning("No locales have been assigned to this document.  Please add them using 'ltk request'.")
        else:
            for locale in entered_locales:
                check_locale = locale.replace('-', '_')
                if not (remote_check and check_locale not in valid_locales):
                    if not remote_check:
                        if check_locale not in locale_list:
                            logger.warning('The locale code "' + str(locale) + '" failed to be ' + operation_text + ' since it is invalid (see "ltk list -l" for the list of valid codes).')
                    locales.append(locale)

    return locales


def get_translation_files(file_name, path, download_option, doc_manager):
    translation_files = []
    if download_option == 'same':
        downloads = doc_manager.get_doc_downloads(file_name)
        translation_files = find_translations(file_name, path, downloads)
    else:
        if download_option == 'folder':
            downloads = doc_manager.get_doc_downloads(file_name)
            entry = doc_manager.get_doc_by_prop('file_name', file_name)
            if entry:
                file_name = entry['name']
            translation_files = find_translations(file_name, path, downloads)
        else:
            if download_option == 'clone':
                entry = doc_manager.get_doc_by_prop('file_name', file_name)
                if entry:
                    file_name = entry['name']
                if os.path.isfile(os.path.join(path, file_name)):
                    translation_files.append(os.path.join(path, file_name))
    return translation_files


def find_translations(file_name, path, downloads):
    translation_files = []
    trans_file_name = ''
    for d in downloads:
        temp = file_name.split('.')
        trans_file_name = ''
        for idx, val in enumerate(temp):
            if idx == len(temp) - 2:
                trans_file_name = trans_file_name + val + '.'
                trans_file_name = trans_file_name + d + '.'
            else:
                trans_file_name += val
                if idx != len(temp) - 1:
                    trans_file_name += '.'
            if os.path.isfile(os.path.join(path, trans_file_name)):
                translation_files.append(os.path.join(path, trans_file_name))

    return translation_files


def raise_error(json, error_message, is_warning=False, doc_id=None, file_name=None):
    try:
        error = ''
        if json:
            error = json['messages'][0]
        if file_name:
            file_name = file_name.replace('Status of ', '')
        if file_name is not None:
            if doc_id is not None:
                error = error.replace(doc_id, file_name + ' (' + doc_id + ')')
        if error == 'Unknown error':
            error = error_message
        if not is_warning:
            raise exceptions.RequestFailedError(error)
        if error:
            error = error + '\n'
        logger.error(error + error_message)
    except (AttributeError, IndexError):
        if not is_warning:
            raise exceptions.RequestFailedError(error_message)
        logger.error(error_message)


def error(error_message):
    logger.error(error_message + '\n')


def underline(text):
    if term:
        print(term.underline(text))
    else:
        print(text)


def format_commit_message():
    pass


def check_response(response):
    try:
        if response:
            if response.text:
                if response.json():
                    return True
    except ValueError:
        logger.warning('Could not connect to Lingotek')
        return
    except json.decoder.JSONDecodeError:
        logger.warning('Could not connect to Lingotek')
        return


def remove_begin_slashes(path):
    index = 0
    for letter in path:
        if letter != os.sep:
            break
        index += 1

    if len(path) > index + 1:
        return path[index:]
    return ''
    return path


def remove_end_slashes(path):
    index = len(path) - 1
    for letter in reversed(path):
        if letter != os.sep:
            break
        index -= 1

    if index > 0:
        return path[:index - 1]
    return ''
    return path


def remove_last_folder_in_path(path):
    if len(path):
        split_path = path.split(os.sep)
        split_path = split_path[:len(split_path) - 1]
        return (os.path.join)(*split_path)
    return path


def get_relative_path(path_to_project_root, path):
    abs_path = os.path.dirname(os.path.join(path_to_project_root, path))
    relative_path = os.path.relpath(abs_path, os.getcwd())
    if relative_path == '..':
        if os.path.join(path_to_project_root, path) == os.getcwd():
            return '.'
    relative_file_path = os.path.join(relative_path, os.path.basename(path))
    split_path = relative_file_path.split(os.sep)
    if len(split_path) and split_path[0] == '.' or os.path.join(abs_path, os.path.basename(path)) in os.getcwd():
        relative_file_path = (os.path.join)(*split_path[1:])
    return relative_file_path


def log_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_str = ''
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    for line in tb_lines:
        tb_str += line + '\n'

    return tb_str


def log_error(error_file_name, e):
    try:
        with open(error_file_name, 'a') as (error_file):
            error_file.write(str(time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + str(log_traceback(e))))
    except IOError as e:
        try:
            print(e.errno)
            print(e)
        finally:
            e = None
            del e


def remove_powershell_formatting(args):
    if args != None:
        if isinstance(args, tuple):
            myTuple = ()
            if len(args) > 1:
                if isinstance(args, tuple):
                    for k in args:
                        k = remove_formatting(k)
                        myTuple = myTuple + (k,)

                    return myTuple
                for k, v in args:
                    k = (
                     remove_formatting(k),)
                    v = remove_formatting(v)
                    tup1 = k + (v,)
                    return myTuple + (tup1,)

                return myTuple + (tup1,)
            for tup in args:
                if isinstance(tup, tuple):
                    for k in tup:
                        k = remove_formatting(k)
                        myTuple = myTuple + (k,)

                    myTuple = (myTuple,)
                    return myTuple
                for k in args:
                    k = remove_formatting(k)
                    myTuple = (k,)

                return myTuple

            return args
        else:
            if isinstance(args, list):
                temp = []
                for k in args:
                    k = remove_formatting(k)
                    temp.append(k)

                return tuple(temp)
            if isinstance(args, str):
                temp = remove_formatting(args)
                return temp
            return args


def remove_formatting(f):
    if f.startswith('.\\'):
        f = f[2:]
        if f.endswith('\\'):
            f = f[:-1]
        if f.endswith('"'):
            f = f[:-1]
        return f
    return f


def yes_no_prompt(prompt, default_yes=False):
    try:
        confirm = 'none'
        prompt_message = prompt + (' [Y/n]: ' if default_yes else ' [y/N]: ')
        while confirm not in ('y', 'Y', 'n', 'N', ''):
            confirm = input(prompt_message)

        if confirm in ('y', 'Y'):
            return True
        if confirm in ('n', 'N'):
            return False
        return default_yes
    except KeyboardInterrupt:
        raise