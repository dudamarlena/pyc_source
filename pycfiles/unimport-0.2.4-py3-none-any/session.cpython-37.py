# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/session.py
# Compiled at: 2020-04-14 12:53:51
# Size of source mod 2**32: 2469 bytes
import difflib, fnmatch, tokenize
from lib2to3.pgen2.parse import ParseError
from pathlib import Path
from unimport.config import Config
from unimport.refactor import RefactorTool
from unimport.scan import Scanner

class Session:

    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.scanner = Scanner()
        self.refactor_tool = RefactorTool()

    def _read(self, path):
        try:
            with tokenize.open(path) as (stream):
                source = stream.read()
                encoding = stream.encoding
        except OSError as exc:
            try:
                print(f"{exc} Can't read")
                return ('', 'utf-8')
            finally:
                exc = None
                del exc

        else:
            return (
             source, encoding)

    def _list_paths(self, start, pattern='**/*.py'):
        start = Path(start)

        def _is_excluded(path):
            for pattern_exclude in self.config.exclude:
                if fnmatch.fnmatch(path, pattern_exclude):
                    return True

            return False

        if not start.is_dir():
            _is_excluded(start) or (yield start)
        else:
            for dir_ in start.iterdir():
                if not _is_excluded(dir_):
                    for path in dir_.glob(pattern):
                        if not _is_excluded(path):
                            yield path

    def refactor(self, source):
        self.scanner.run_visit(source)
        modules = [module for module in self.scanner.get_unused_imports()]
        self.scanner.clear()
        return self.refactor_tool.refactor_string(source, modules)

    def refactor_file(self, path, apply=False):
        path = Path(path)
        source, encoding = self._read(path)
        result = self.refactor(source)
        if apply:
            path.write_text(result, encoding=encoding)
        else:
            return result

    def diff(self, source):
        return tuple(difflib.unified_diff(source.splitlines(), self.refactor(source).splitlines()))

    def diff_file(self, path):
        source, _ = self._read(path)
        try:
            result = self.refactor_file(path, apply=False)
        except ParseError:
            print(f"\x1b[91m Invalid python file '{path}'\x1b[00m")
            return tuple()
        else:
            return tuple(difflib.unified_diff((source.splitlines()),
              (result.splitlines()), fromfile=(str(path))))