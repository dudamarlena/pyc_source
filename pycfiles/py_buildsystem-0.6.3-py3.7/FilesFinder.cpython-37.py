# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\FilesFinder\FilesFinder.py
# Compiled at: 2019-06-09 09:37:17
# Size of source mod 2**32: 5183 bytes
import re, os

class FilesFinder:

    def __init__(self, list_of_paths_to_search='', file_name_search_regex='.*', list_of_paths_to_exlude_from_search=None, search_subdirectories=True):
        self.set_search_paths(list_of_paths_to_search)
        self.set_filename_search_regex(file_name_search_regex)
        self.set_excluded_directiories(list_of_paths_to_exlude_from_search)
        self.set_search_subdirectories(search_subdirectories)

    def set_search_paths(self, list_of_paths_to_search):
        if (isinstance(list_of_paths_to_search, str) or isinstance)(list_of_paths_to_search, list):
            if not all((isinstance(path, str) for path in list_of_paths_to_search)):
                raise TypeError('list_of_paths_to_search must be a string or list of strings')
        elif isinstance(list_of_paths_to_search, str):
            self._FilesFinder__paths_to_search = [
             list_of_paths_to_search]
        else:
            self._FilesFinder__paths_to_search = list_of_paths_to_search

    def set_filename_search_regex(self, file_name_search_regex):
        if not isinstance(file_name_search_regex, str):
            raise TypeError("file name search regex must be a string not a'{}'".format(type(file_name_search_regex)))
        self._FilesFinder__file_name_search_regex = file_name_search_regex

    def set_excluded_directiories(self, list_of_paths_to_exlude_from_search):
        if not list_of_paths_to_exlude_from_search is None:
            if not isinstance(list_of_paths_to_exlude_from_search, str):
                raise isinstance(list_of_paths_to_exlude_from_search, list) and all((isinstance(path, str) for path in list_of_paths_to_exlude_from_search)) or TypeError('list_of_paths_to_exlude_from_search must be a string or list of strings')
        elif isinstance(list_of_paths_to_exlude_from_search, str):
            self._FilesFinder__list_of_paths_to_exlude_from_search = [
             list_of_paths_to_exlude_from_search]
        else:
            self._FilesFinder__list_of_paths_to_exlude_from_search = list_of_paths_to_exlude_from_search

    def set_search_subdirectories(self, search_subdirectories):
        if not isinstance(search_subdirectories, bool):
            raise TypeError("search_subdirectories must be a bool not a'{}'".format(type(search_subdirectories)))
        self._FilesFinder__search_subdirectories = search_subdirectories

    def search(self):
        _FilesFinder__compiled_regex = re.compile(self._FilesFinder__file_name_search_regex)
        _FilesFinder__found_files = []
        if self._FilesFinder__search_subdirectories is True:
            for directory in self._FilesFinder__paths_to_search:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if not self._FilesFinder__list_of_paths_to_exlude_from_search is None:
                            if any((_FilesFinder__excluded_path in os.path.join(root, file).replace('\\', '/') for _FilesFinder__excluded_path in self._FilesFinder__list_of_paths_to_exlude_from_search)) or _FilesFinder__compiled_regex.match(file) is not None:
                                _FilesFinder__found_files.append(os.path.join(root, file).replace('\\', '/'))

        else:
            for directory in self._FilesFinder__paths_to_search:
                for file in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, file)) and _FilesFinder__compiled_regex.match(file) is not None:
                        _FilesFinder__found_files.append(os.path.join(directory, file).replace('\\', '/'))

        return _FilesFinder__found_files

    def set_files_extentions(self, extentions):
        if (isinstance(extentions, str) or isinstance)(extentions, list):
            if not all((isinstance(path, str) for path in extentions)):
                raise TypeError('extentions must be a string or list of strings')
        elif isinstance(extentions, str):
            if extentions.startswith('*'):
                extentions = extentions[1:]
            self._FilesFinder__file_name_search_regex = '.*' + extentions.replace('.', '\\.') + '$'
        else:
            self._FilesFinder__file_name_search_regex = '.*('
            for extention in extentions:
                if extention.startswith('*'):
                    extention = extention[1:]
                self._FilesFinder__file_name_search_regex += '(' + extention.replace('.', '\\.') + ')|'

            self._FilesFinder__file_name_search_regex = self._FilesFinder__file_name_search_regex[:-1] + ')$'