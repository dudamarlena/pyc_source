# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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

    def _read--- This code section failed: ---

 L.  19         0  SETUP_FINALLY        42  'to 42'

 L.  20         2  LOAD_GLOBAL              tokenize
                4  LOAD_METHOD              open
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           32  'to 32'
               12  STORE_FAST               'stream'

 L.  21        14  LOAD_FAST                'stream'
               16  LOAD_METHOD              read
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'source'

 L.  22        22  LOAD_FAST                'stream'
               24  LOAD_ATTR                encoding
               26  STORE_FAST               'encoding'
               28  POP_BLOCK        
               30  BEGIN_FINALLY    
             32_0  COME_FROM_WITH       10  '10'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      
               38  POP_BLOCK        
               40  JUMP_FORWARD         96  'to 96'
             42_0  COME_FROM_FINALLY     0  '0'

 L.  23        42  DUP_TOP          
               44  LOAD_GLOBAL              OSError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    94  'to 94'
               50  POP_TOP          
               52  STORE_FAST               'exc'
               54  POP_TOP          
               56  SETUP_FINALLY        82  'to 82'

 L.  24        58  LOAD_GLOBAL              print
               60  LOAD_FAST                'exc'
               62  FORMAT_VALUE          0  ''
               64  LOAD_STR                 " Can't read"
               66  BUILD_STRING_2        2 
               68  CALL_FUNCTION_1       1  ''
               70  POP_TOP          

 L.  25        72  POP_BLOCK        
               74  POP_EXCEPT       
               76  CALL_FINALLY         82  'to 82'
               78  LOAD_CONST               ('', 'utf-8')
               80  RETURN_VALUE     
             82_0  COME_FROM            76  '76'
             82_1  COME_FROM_FINALLY    56  '56'
               82  LOAD_CONST               None
               84  STORE_FAST               'exc'
               86  DELETE_FAST              'exc'
               88  END_FINALLY      
               90  POP_EXCEPT       
               92  JUMP_FORWARD        104  'to 104'
             94_0  COME_FROM            48  '48'
               94  END_FINALLY      
             96_0  COME_FROM            40  '40'

 L.  27        96  LOAD_FAST                'source'
               98  LOAD_FAST                'encoding'
              100  BUILD_TUPLE_2         2 
              102  RETURN_VALUE     
            104_0  COME_FROM            92  '92'

Parse error at or near `CALL_FINALLY' instruction at offset 76

    def _list_paths(self, start, pattern='**/*.py'):
        start = Path(start)

        def _is_excluded(path):
            for pattern_exclude in self.config.exclude:
                if fnmatch.fnmatch(path, pattern_exclude):
                    return True
                return False

        if not start.is_dir:
            _is_excluded(start) or (yield start)
        else:
            for dir_ in start.iterdir:
                for path in _is_excluded(dir_) or dir_.globpattern:
                    if not _is_excluded(path):
                        (yield path)

    def refactor(self, source):
        self.scanner.run_visitsource
        modules = [module for module in self.scanner.get_unused_imports]
        self.scanner.clear
        return self.refactor_tool.refactor_string(source, modules)

    def refactor_file(self, path, apply=False):
        path = Path(path)
        source, encoding = self._readpath
        result = self.refactorsource
        if apply:
            path.write_text(result, encoding=encoding)
        else:
            return result

    def diff(self, source):
        return tuple(difflib.unified_diff(source.splitlines, self.refactorsource.splitlines))

    def diff_file(self, path):
        source, _ = self._readpath
        try:
            result = self.refactor_file(path, apply=False)
        except ParseError:
            print(f"\x1b[91m Invalid python file '{path}'\x1b[00m")
            return tuple()
        else:
            return tuple(difflib.unified_diff((source.splitlines),
              (result.splitlines), fromfile=(str(path))))