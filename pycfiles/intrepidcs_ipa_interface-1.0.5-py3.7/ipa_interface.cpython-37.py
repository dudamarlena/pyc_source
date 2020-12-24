# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intrepidcs/ipa_interface/ipa_interface.py
# Compiled at: 2019-11-15 12:22:11
# Size of source mod 2**32: 9077 bytes
import json
from importlib import import_module
from docopt import docopt

def ipa_init(script_name: str='script.py', version: str='1.0', message: str='') -> None:
    """
    * The ipa_init function allows you to set the the name and version information of
    * your script. This is allows command line help to display the information accurately.

    * Note ipa_init function must be called before any other ipa function for the change to
    * take affect
    """
    __read_args(script_name, version, message)


def get_data_files() -> [
 str]:
    """
    * The get_data_files function returns the data files used.

    * Note: If you are in desktop mode this function will display a the
    * file dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    """
    if hasattr(get_data_files, 'data_files'):
        return get_data_files.data_files
    desktop_options = {}
    desktop_options['filetypes'] = [
     ('Data files', '*.dat *.log *.mdf *.mf4 *.db'), ('all files', '.*')]
    desktop_options['title'] = 'Select list of input data files and click open.'
    desktop_options['defaultextension'] = '.db'
    get_data_files.data_files = __raise_if_none(__to_array_of_paths(__get_files('data_files', desktop_options)), 'data_files')
    return get_data_files.data_files


def get_config_files() -> [
 str]:
    """
    * The get_config_files function returns the config files used.

    * Note: If you are in desktop mode this function will display a the
    * file dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    """
    if hasattr(get_config_files, 'config_files'):
        return get_config_files.config_files
    desktop_options = {}
    desktop_options['filetypes'] = [
     ('Lookup files', '*.sl *.asl'), ('Signal Lookup files', '*.sl'),
     ('Aliased Signal Lookup files', '*.asl'), ('All files', '*.*')]
    desktop_options['title'] = 'Select script config file (*.als) and click open.'
    get_config_files.config_files = __raise_if_none(__to_array_of_paths(__get_files('config_files', desktop_options)), 'config_files')
    return get_config_files.config_files


def get_output_dir() -> str:
    """
    * The get_output_dir function returns the output directory that must be used.

    * Note: If you are in desktop mode this function will display a the
    * directory dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    """
    if hasattr(get_output_dir, 'output_dir'):
        return get_output_dir.output_dir
    desktop_options = {}
    get_output_dir.output_dir = __raise_if_none(__get_directory('output_dir', desktop_options), 'output_dir')
    return get_output_dir.output_dir


def get_previous_dir() -> str:
    """
    * The previous_dir function returns the previous runs output directory.

    * Note: If you are in desktop mode this function will display a the
    * directory dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    """
    if hasattr(get_output_dir, 'previous_dir'):
        return get_output_dir.output_dir
    desktop_options = {}
    get_output_dir.output_dir = __get_directory('previous_dir', desktop_options)
    return get_output_dir.output_dir


def update_progress(name: str='Master', percent: float=None, message: str=None) -> None:
    """
    * Allows the user to identify the prograss of the script

    * name: Is the of the progress bar master being the full script progress
    * percent: is a optional way to update progress.
    * message: is a optional way to update progress.
    """
    pass


def using_ipa_file() -> bool:
    """
    received ipa file as argument
    """
    return __is_using_ipa_file()


def get_attribute_from_file(path: str, attribute: str):
    """
    get attributes passed alongside the file path
    if attribute is not passed None is returned
    """
    ipa_file = __get_ipa_file()
    if ipa_file is None:
        return
    for file in ipa_file['data_files'] + ipa_file['config_files']:
        if file['path'] == path:
            if attribute in file:
                return file[attribute]
            return
    else:
        return


def __read_args(script_name='script.py', version='1.0', message=''):
    if not hasattr(__read_args, 'args'):
        args = '\n        {message}\nUsage:\n  {scriptPy}\n  {scriptPy} <IPA_FILE>\n  {scriptPy} [--data_files=<FILE>]... [--config_files=<FILE>]... [--previous_dir=<DIR>] --output_dir=<DIR>\n  {scriptPy} (-h | --help)\n  {scriptPy} --version\n\nOptions:\n  -h --help     Show this screen.\n  --version     Show version.\n  -d FILE --data_files=<FILE>   The data files that are used.\n  -c FILE --config_files=<FILE> The config files that are used.\n  -o DIR --output_dir=<DIR>   The output directory. This is required if the script output directory.\n  -p DIR --previous_dir=<DIR>   The previous run output directory. This is used if you want to use the results of the previous run as an input.\n'
        __read_args.args = docopt(args.format(scriptPy=script_name,
          message=message),
          version=version)
    return __read_args.args


def __listafy(argument):
    """make argument a list if it is not"""
    if not isinstance(argument, list):
        argument = [
         argument]
    return argument


def __is_strings(argument):
    return isinstance(argument, str)


def __is_list_of_strings(argument):
    if not isinstance(argument, list):
        return False
    return all((isinstance(item, str) for item in argument))


def __raise_if_none(argument, name: str):
    if argument is None:
        raise TypeError('the {name} argument is not included in IPA_FILE'.format(name=name))
    return argument


def __is_using_ipa_file():
    file = __read_args()['<IPA_FILE>']
    return type(file) is str and file != ''


def __is_using_comandline_args():
    return __read_args()['--output_dir'] is not None


def __is_using_display_args():
    return not __is_using_ipa_file() and not __is_using_comandline_args()


def __get_args():
    ipa_file = __get_ipa_file()
    if ipa_file is not None:
        return ipa_file
    return __read_args()


def __get_files(file_arg, desktop_options):
    args = __get_args()
    files = None
    if __is_using_comandline_args():
        file_arg = '--' + file_arg
        if file_arg in args:
            files = __listafy(args[file_arg])
        return files
    if __is_using_ipa_file():
        if file_arg in args:
            files = __listafy(args[file_arg])
        return files
    mtk = None
    mtk_filedialog = None
    try:
        mtk = import_module('tkinter')
        mtk_filedialog = import_module('tkinter.filedialog')
    except ModuleNotFoundError as err:
        try:
            raise err
        finally:
            err = None
            del err

    root = mtk.Tk()
    root.withdraw()
    root.focus_force()
    root.wm_attributes('-topmost', 1)
    return list((mtk_filedialog.askopenfilenames)(**desktop_options))


def __get_directory(dir_arg, desktop_options):
    args = __get_args()
    directory = None
    if __is_using_comandline_args():
        dir_arg = '--' + dir_arg
        if dir_arg in args:
            if __is_strings(args[dir_arg]):
                directory = args[dir_arg]
        return directory
    if __is_using_ipa_file():
        if dir_arg in args:
            if __is_strings(args[dir_arg]):
                directory = args[dir_arg]
            else:
                raise TypeError('the {dir_arg} argument is invalid'.format(dir_arg=dir_arg))
        return directory
    mtk = None
    mtk_filedialog = None
    try:
        mtk = import_module('tkinter')
        mtk_filedialog = import_module('tkinter.filedialog')
    except ModuleNotFoundError as err:
        try:
            raise err
        finally:
            err = None
            del err

    root = mtk.Tk()
    root.withdraw()
    root.focus_force()
    root.wm_attributes('-topmost', 1)
    return list((mtk_filedialog.askdirectory)(**desktop_options))


def __to_array_of_paths(path_object):
    if type(path_object) is list:
        paths = []
        for file in path_object:
            if type(file) is dict:
                if 'path' in file:
                    if type(file['path']) is str:
                        paths.append(file['path'])
            if type(file) is str:
                paths.append(file)

        return paths
    if type(path_object) is str:
        return [
         path_object]
    return []


def __get_ipa_file():
    if hasattr(__get_ipa_file, 'ipa_file'):
        return __get_ipa_file.ipa_file
    if __is_using_ipa_file():
        __get_ipa_file.ipa_file = json.load(open(__read_args()['<IPA_FILE>']))
        return __get_ipa_file.ipa_file