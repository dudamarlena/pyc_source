# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/contrib/completers/filesystem.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 3760 bytes
from __future__ import unicode_literals
from prompt_tool_kit.completion import Completer, Completion
import os
__all__ = ('PathCompleter', 'ExecutableCompleter')

class PathCompleter(Completer):
    """PathCompleter"""

    def __init__(self, only_directories=False, get_paths=None, file_filter=None, min_input_len=0, expanduser=False):
        if not get_paths is None:
            if not callable(get_paths):
                raise AssertionError
        else:
            if not file_filter is None:
                if not callable(file_filter):
                    raise AssertionError
            elif not isinstance(min_input_len, int):
                raise AssertionError
            assert isinstance(expanduser, bool)
        self.only_directories = only_directories
        self.get_paths = get_paths or (lambda : ['.'])
        self.file_filter = file_filter or (lambda _: True)
        self.min_input_len = min_input_len
        self.expanduser = expanduser

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if len(text) < self.min_input_len:
            return
        try:
            if self.expanduser:
                text = os.path.expanduser(text)
            else:
                dirname = os.path.dirname(text)
                if dirname:
                    directories = [os.path.dirname(os.path.join(p, text)) for p in self.get_paths()]
                else:
                    directories = self.get_paths()
            prefix = os.path.basename(text)
            filenames = []
            for directory in directories:
                if os.path.isdir(directory):
                    for filename in os.listdir(directory):
                        if filename.startswith(prefix):
                            filenames.append((directory, filename))

            filenames = sorted(filenames, key=(lambda k: k[1]))
            for directory, filename in filenames:
                completion = filename[len(prefix):]
                full_name = os.path.join(directory, filename)
                if os.path.isdir(full_name):
                    filename += '/'
                else:
                    if self.only_directories:
                        continue
                if not self.file_filter(full_name):
                    pass
                else:
                    yield Completion(completion, 0, display=filename)

        except OSError:
            pass


class ExecutableCompleter(PathCompleter):
    """ExecutableCompleter"""

    def __init__(self):
        (
         PathCompleter.__init__(self,
           only_directories=False,
           min_input_len=1,
           get_paths=(lambda : os.environ.get('PATH', '').split(os.pathsep)),
           file_filter=(lambda name: os.access(name, os.X_OK)),
           expanduser=True),)