# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Repos\TestLibs\pylibimport\pylibimport\lib_import.py
# Compiled at: 2020-05-04 01:17:51
# Size of source mod 2**32: 15060 bytes
import os, sys, contextlib, copy, tempfile, shutil, tarfile, importlib
import packaging.version as parse_version
import multiprocessing as mp
import pip._internal as pip_main
from .utils import make_import_name, get_name_version, is_python_package

class VersionImporter(object):
    """VersionImporter"""
    DEFAULT_PYTHON_EXTENSIONS = [
     '.py', '.pyc', '.pyd']

    def __init__(self, import_dir=None, target_dir=None, python_extensions=None, install_dependencies=False, reset_modules=True, **kwargs):
        """Initialize the library

        Args:
            import_dir (str)[None]: Name of the import directory.
            target_dir (str)[None]: Name of the directory to install the packages to.
            python_extensions (list)[None]: Available python extensions to try to import normally.
            install_dependencies (bool)[False]: If True .whl files will install dependencies into the target_dir.
            reset_modules (bool)[True]: Reset the state of sys.modules after importing.
                Dependencies will not be loaded into sys.modules.
            **kwargs (dict): Unused given named arguments.
        """
        if python_extensions is None:
            python_extensions = self.DEFAULT_PYTHON_EXTENSIONS
        self._target_dir = None
        self.import_dir = import_dir
        self.python_extensions = python_extensions
        self.install_dependencies = install_dependencies
        self.reset_modules = reset_modules
        self.paths = []
        self.modules = {}
        if target_dir is not None:
            self.init(target_dir)

    @property
    def target_dir(self):
        """Return the name of the target save directory."""
        return self._target_dir

    @target_dir.setter
    def target_dir(self, target_dir):
        self.init(target_dir)

    def init(self, target_dir=None):
        """Initialize this importer.

        Args:
            target_dir (str): Target directory. If None and self.target_dir is None use a temporary directory.
        """
        if target_dir is None:
            target_dir = self._target_dir
        elif target_dir is None:
            target_dir = os.path.join(tempfile.gettempdir(), 'pylibimport')
        elif os.path.isfile(target_dir):
            target_dir = os.path.dirname(target_dir)
        self.remove_path(self._target_dir)
        self._target_dir = str(target_dir)
        if not os.path.exists(self._target_dir):
            os.makedirs(self._target_dir)
        return self

    @staticmethod
    def remove_path(path, delete_path=False):
        """Remove the given path and sub paths. This also deletes the given path directory!"""
        if path is not None:
            for i in reversed(range(len(sys.path))):
                try:
                    if path in sys.path[i]:
                        sys.path.pop(i)
                except:
                    pass

            if delete_path:
                try:
                    shutil.rmtree(path, ignore_errors=True, onerror=None)
                except:
                    pass

    def add_path(self, path):
        """Add a path to sys.path and this.path."""
        if path not in sys.path:
            self.paths.append(path)
            sys.path.insert(0, path)

    @staticmethod
    def rename_module(from_, to):
        """Rename a module/package and all submodules/subpackages to a new name.

        The main downside of this approach is that dependencies are not renamed. So there could be a dependency
        conflict when importing packages with the same name. It may be better to just reset sys.modules after import.

        Args:
            from_ (str): Name of the package that has already been imported.
            to (str): New name for the package.
        """
        length = len(from_)
        for k in list(sys.modules):
            if k.startswith(from_):
                sys.modules[to + k[length:]] = sys.modules[k]
                del sys.modules[k]

    def add_module(self, import_name, module):
        """Add a module to the system modules."""
        sys.modules[import_name] = module

    @contextlib.contextmanager
    def original_system(self, new_path=None, reset_modules=True):
        """Context manager to reset sys.path and sys.modules to the previous state before the context operation.

        Args:
            new_path (str)[None]: Temporarily add a path to sys.path before the operation.
            reset_modules (bool)[True]: If True reset sys.modules back to the original sys.modules.
        """
        modules = sys.modules.copy()
        paths = copy.copy(sys.path)
        path_cache = sys.path_importer_cache.copy()
        if new_path:
            if new_path not in sys.path:
                sys.path.insert(0, new_path)
        yield
        if reset_modules:
            sys.modules = modules
        sys.path = paths
        sys.path_importer_cache = path_cache

    def iter_available_modules--- This code section failed: ---

 L. 153         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              listdir
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                import_dir
                8  CALL_METHOD_1         1  ''
               10  GET_ITER         
               12  FOR_ITER            176  'to 176'
               14  STORE_FAST               'item'

 L. 154        16  SETUP_FINALLY       146  'to 146'

 L. 155        18  LOAD_GLOBAL              os
               20  LOAD_ATTR                path
               22  LOAD_METHOD              join
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                import_dir
               28  LOAD_FAST                'item'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'path'

 L. 156        34  LOAD_GLOBAL              os
               36  LOAD_ATTR                path
               38  LOAD_METHOD              splitext
               40  LOAD_FAST                'item'
               42  CALL_METHOD_1         1  ''
               44  LOAD_CONST               -1
               46  BINARY_SUBSCR    
               48  LOAD_METHOD              lower
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'ext'

 L. 157        54  LOAD_FAST                'ext'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                python_extensions
               60  COMPARE_OP               in
               62  POP_JUMP_IF_TRUE    106  'to 106'

 L. 158        64  LOAD_FAST                'ext'
               66  LOAD_STR                 ''
               68  COMPARE_OP               ==

 L. 157        70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 158        72  LOAD_GLOBAL              is_python_package
               74  LOAD_FAST                'path'
               76  CALL_FUNCTION_1       1  ''

 L. 157        78  POP_JUMP_IF_TRUE    106  'to 106'
             80_0  COME_FROM            70  '70'

 L. 159        80  LOAD_FAST                'ext'
               82  LOAD_STR                 '.zip'
               84  COMPARE_OP               ==

 L. 157        86  POP_JUMP_IF_TRUE    106  'to 106'

 L. 159        88  LOAD_GLOBAL              tarfile
               90  LOAD_METHOD              is_tarfile
               92  LOAD_FAST                'path'
               94  CALL_METHOD_1         1  ''

 L. 157        96  POP_JUMP_IF_TRUE    106  'to 106'

 L. 159        98  LOAD_FAST                'ext'
              100  LOAD_STR                 '.whl'
              102  COMPARE_OP               ==

 L. 157       104  POP_JUMP_IF_FALSE   142  'to 142'
            106_0  COME_FROM            96  '96'
            106_1  COME_FROM            86  '86'
            106_2  COME_FROM            78  '78'
            106_3  COME_FROM            62  '62'

 L. 161       106  LOAD_GLOBAL              get_name_version
              108  LOAD_FAST                'path'
              110  CALL_FUNCTION_1       1  ''
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               'name'
              116  STORE_FAST               'version'

 L. 162       118  LOAD_GLOBAL              make_import_name
              120  LOAD_FAST                'name'
              122  LOAD_FAST                'version'
              124  CALL_FUNCTION_2       2  ''
              126  STORE_FAST               'import_name'

 L. 163       128  LOAD_FAST                'name'
              130  LOAD_FAST                'version'
              132  LOAD_FAST                'import_name'
              134  LOAD_FAST                'path'
              136  BUILD_TUPLE_4         4 
              138  YIELD_VALUE      
              140  POP_TOP          
            142_0  COME_FROM           104  '104'
              142  POP_BLOCK        
              144  JUMP_BACK            12  'to 12'
            146_0  COME_FROM_FINALLY    16  '16'

 L. 165       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  LOAD_GLOBAL              ValueError
              152  LOAD_GLOBAL              TypeError
              154  LOAD_GLOBAL              Exception
              156  BUILD_TUPLE_4         4 
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   172  'to 172'
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 166       168  POP_EXCEPT       
              170  JUMP_BACK            12  'to 12'
            172_0  COME_FROM           160  '160'
              172  END_FINALLY      
              174  JUMP_BACK            12  'to 12'

Parse error at or near `JUMP_BACK' instruction at offset 144

    def available_modules(self):
        """Return a list of importable packages."""
        return [import_name for n, v, import_name, path in self.iter_available_modules()]

    def find_module(self, module_name, version=None):
        """Return the import dir module path for the given module name, import_name, or path."""
        results = (None, None, None, None)
        for n, v, i, p in self.iter_available_modules():
            if not (i == module_name or p.endswith(module_name)):
                if not n == module_name or v == version:
                    return (
                     n, v, i, p)
            elif n == module_name:
                if results[1] is None or parse_version(v) > parse_version(results[1]):
                    results = (
                     n, v, i, p)
                if version is not None and results[1] != version:
                    return (None, None, None, None)
            return results

    def delete_module--- This code section failed: ---

 L. 197         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE    162  'to 162'

 L. 199        10  LOAD_FAST                'name'
               12  STORE_FAST               'module'

 L. 200        14  SETUP_FINALLY        32  'to 32'

 L. 201        16  LOAD_FAST                'module'
               18  LOAD_ATTR                __import_version__
               20  STORE_FAST               'version'

 L. 202        22  LOAD_FAST                'module'
               24  LOAD_ATTR                __module__
               26  STORE_FAST               'name'
               28  POP_BLOCK        
               30  JUMP_ABSOLUTE       182  'to 182'
             32_0  COME_FROM_FINALLY    14  '14'

 L. 203        32  DUP_TOP          
               34  LOAD_GLOBAL              AttributeError
               36  LOAD_GLOBAL              Exception
               38  BUILD_TUPLE_2         2 
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE   158  'to 158'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 204        50  SETUP_FINALLY        68  'to 68'

 L. 206        52  LOAD_FAST                'module'
               54  LOAD_ATTR                __version__
               56  STORE_FAST               'version'

 L. 207        58  LOAD_FAST                'module'
               60  LOAD_ATTR                __module__
               62  STORE_FAST               'name'
               64  POP_BLOCK        
               66  JUMP_FORWARD        154  'to 154'
             68_0  COME_FROM_FINALLY    50  '50'

 L. 208        68  DUP_TOP          
               70  LOAD_GLOBAL              AttributeError
               72  LOAD_GLOBAL              Exception
               74  BUILD_TUPLE_2         2 
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   152  'to 152'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 210        86  LOAD_CONST               None
               88  STORE_FAST               'name'

 L. 211        90  LOAD_FAST                'self'
               92  LOAD_ATTR                modules
               94  LOAD_METHOD              items
               96  CALL_METHOD_0         0  ''
               98  GET_ITER         
              100  FOR_ITER            148  'to 148'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'n'
              106  STORE_FAST               'vs'

 L. 212       108  LOAD_FAST                'vs'
              110  LOAD_METHOD              items
              112  CALL_METHOD_0         0  ''
              114  GET_ITER         
            116_0  COME_FROM           130  '130'
              116  FOR_ITER            146  'to 146'
              118  UNPACK_SEQUENCE_2     2 
              120  STORE_FAST               'v'
              122  STORE_FAST               'm'

 L. 213       124  LOAD_FAST                'm'
              126  LOAD_FAST                'module'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   116  'to 116'

 L. 214       132  LOAD_FAST                'n'
              134  STORE_FAST               'name'

 L. 215       136  LOAD_FAST                'v'
              138  STORE_FAST               'version'

 L. 216       140  POP_TOP          
              142  CONTINUE            100  'to 100'
              144  JUMP_BACK           116  'to 116'
              146  JUMP_BACK           100  'to 100'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM            78  '78'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM            66  '66'
              154  POP_EXCEPT       
              156  JUMP_ABSOLUTE       182  'to 182'
            158_0  COME_FROM            42  '42'
              158  END_FINALLY      
              160  JUMP_FORWARD        182  'to 182'
            162_0  COME_FROM             8  '8'

 L. 219       162  LOAD_FAST                'self'
              164  LOAD_METHOD              find_module
              166  LOAD_FAST                'name'
              168  LOAD_FAST                'version'
              170  CALL_METHOD_2         2  ''
              172  UNPACK_SEQUENCE_4     4 
              174  STORE_FAST               'name'
              176  STORE_FAST               'version'
              178  STORE_FAST               'import_name'
              180  STORE_FAST               'path'
            182_0  COME_FROM           160  '160'

 L. 222       182  LOAD_FAST                'name'
              184  LOAD_CONST               None
              186  COMPARE_OP               is
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 223       190  LOAD_FAST                'name'
              192  LOAD_FAST                'version'
              194  BUILD_TUPLE_2         2 
              196  RETURN_VALUE     
            198_0  COME_FROM           188  '188'

 L. 225       198  SETUP_FINALLY       216  'to 216'

 L. 226       200  LOAD_FAST                'self'
              202  LOAD_ATTR                modules
              204  LOAD_FAST                'name'
              206  BINARY_SUBSCR    
              208  LOAD_FAST                'version'
              210  DELETE_SUBSCR    
              212  POP_BLOCK        
              214  JUMP_FORWARD        228  'to 228'
            216_0  COME_FROM_FINALLY   198  '198'

 L. 227       216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 228       222  POP_EXCEPT       
              224  JUMP_FORWARD        228  'to 228'
              226  END_FINALLY      
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           214  '214'

 L. 229       228  SETUP_FINALLY       262  'to 262'

 L. 230       230  LOAD_GLOBAL              os
              232  LOAD_ATTR                path
              234  LOAD_METHOD              join
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                target_dir
              240  LOAD_FAST                'name'
              242  LOAD_FAST                'version'
              244  CALL_METHOD_3         3  ''
              246  STORE_FAST               'import_path'

 L. 231       248  LOAD_GLOBAL              shutil
              250  LOAD_METHOD              rmtree
              252  LOAD_FAST                'import_path'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  POP_BLOCK        
              260  JUMP_FORWARD        274  'to 274'
            262_0  COME_FROM_FINALLY   228  '228'

 L. 232       262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 233       268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           260  '260'

 L. 234       274  LOAD_FAST                'name'
              276  LOAD_FAST                'version'
              278  BUILD_TUPLE_2         2 
              280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 142

    def error(self, path, err):
        """Handle an import error."""
        raise err

    def import_module(self, name, version=None):
        """Import the given module or package."""
        orig_name = name
        orig_version = version
        name, version, import_name, path = self.find_module(orig_name, version=version)
        if path is None:
            version = orig_version
            if os.path.exists(orig_name):
                path = orig_name
                name, v = get_name_version(path)
                if version is None:
                    version = v
            else:
                self.error(orig_name, ModuleNotFoundError(orig_name))
                return
        if self.target_dir is None:
            self.init()
        module = self._import_modulenameversionpath
        if module is not None:
            return module
        ext = os.path.splitext(path)[(-1)].lower()
        if (ext in self.python_extensions or ext) == '':
            if is_python_package(path):
                return self.py_importnameversionpath
        if ext == '.zip' or tarfile.is_tarfile(path):
            return self.zip_importnameversionpath
        if ext == '.whl':
            return self.whl_installnameversionpath

    def _import_module--- This code section failed: ---

 L. 279         0  LOAD_FAST                'version'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 280         4  LOAD_STR                 '0.0.0'
                6  STORE_FAST               'version'
              8_0  COME_FROM             2  '2'

 L. 282         8  LOAD_FAST                'name'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                modules
               14  COMPARE_OP               in
               16  POP_JUMP_IF_FALSE    44  'to 44'

 L. 283        18  LOAD_FAST                'self'
               20  LOAD_ATTR                modules
               22  LOAD_FAST                'name'
               24  BINARY_SUBSCR    
               26  STORE_FAST               'modules'

 L. 284        28  LOAD_FAST                'version'
               30  LOAD_FAST                'modules'
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 285        36  LOAD_FAST                'modules'
               38  LOAD_FAST                'version'
               40  BINARY_SUBSCR    
               42  RETURN_VALUE     
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            16  '16'

 L. 288        44  LOAD_GLOBAL              os
               46  LOAD_ATTR                path
               48  LOAD_METHOD              join
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                target_dir
               54  LOAD_FAST                'name'
               56  LOAD_FAST                'version'
               58  CALL_METHOD_3         3  ''
               60  STORE_FAST               'import_path'

 L. 289        62  LOAD_GLOBAL              os
               64  LOAD_ATTR                path
               66  LOAD_METHOD              exists
               68  LOAD_FAST                'import_path'
               70  CALL_METHOD_1         1  ''
            72_74  POP_JUMP_IF_FALSE   276  'to 276'

 L. 290        76  SETUP_FINALLY       222  'to 222'

 L. 292        78  LOAD_FAST                'self'
               80  LOAD_ATTR                original_system
               82  LOAD_FAST                'import_path'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                reset_modules
               88  LOAD_CONST               ('reset_modules',)
               90  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               92  SETUP_WITH          110  'to 110'
               94  POP_TOP          

 L. 293        96  LOAD_GLOBAL              importlib
               98  LOAD_METHOD              import_module
              100  LOAD_FAST                'name'
              102  CALL_METHOD_1         1  ''
              104  STORE_FAST               'module'
              106  POP_BLOCK        
              108  BEGIN_FINALLY    
            110_0  COME_FROM_WITH       92  '92'
              110  WITH_CLEANUP_START
              112  WITH_CLEANUP_FINISH
              114  END_FINALLY      

 L. 296       116  LOAD_GLOBAL              make_import_name
              118  LOAD_FAST                'name'
              120  LOAD_FAST                'version'
              122  CALL_FUNCTION_2       2  ''
              124  STORE_FAST               'import_name'

 L. 297       126  LOAD_FAST                'self'
              128  LOAD_ATTR                reset_modules
              130  POP_JUMP_IF_TRUE    146  'to 146'

 L. 298       132  LOAD_FAST                'self'
              134  LOAD_METHOD              rename_module
              136  LOAD_FAST                'name'
              138  LOAD_FAST                'import_name'
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          
              144  JUMP_FORWARD        158  'to 158'
            146_0  COME_FROM           130  '130'

 L. 300       146  LOAD_FAST                'self'
              148  LOAD_METHOD              add_module
              150  LOAD_FAST                'import_name'
              152  LOAD_FAST                'module'
              154  CALL_METHOD_2         2  ''
              156  POP_TOP          
            158_0  COME_FROM           144  '144'

 L. 303       158  LOAD_FAST                'name'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                modules
              164  COMPARE_OP               not-in
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 304       168  BUILD_MAP_0           0 
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                modules
              174  LOAD_FAST                'name'
              176  STORE_SUBSCR     
            178_0  COME_FROM           166  '166'

 L. 305       178  LOAD_FAST                'module'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                modules
              184  LOAD_FAST                'name'
              186  BINARY_SUBSCR    
              188  LOAD_FAST                'version'
              190  STORE_SUBSCR     

 L. 308       192  SETUP_FINALLY       204  'to 204'

 L. 309       194  LOAD_FAST                'version'
              196  LOAD_FAST                'module'
              198  STORE_ATTR               __import_version__
              200  POP_BLOCK        
              202  JUMP_FORWARD        216  'to 216'
            204_0  COME_FROM_FINALLY   192  '192'

 L. 310       204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 311       210  POP_EXCEPT       
              212  JUMP_FORWARD        216  'to 216'
              214  END_FINALLY      
            216_0  COME_FROM           212  '212'
            216_1  COME_FROM           202  '202'

 L. 313       216  LOAD_FAST                'module'
              218  POP_BLOCK        
              220  RETURN_VALUE     
            222_0  COME_FROM_FINALLY    76  '76'

 L. 314       222  DUP_TOP          
              224  LOAD_GLOBAL              Exception
              226  COMPARE_OP               exception-match
          228_230  POP_JUMP_IF_FALSE   274  'to 274'
              232  POP_TOP          
              234  STORE_FAST               'err'
              236  POP_TOP          
              238  SETUP_FINALLY       262  'to 262'

 L. 315       240  LOAD_FAST                'self'
              242  LOAD_METHOD              error
              244  LOAD_FAST                'path'
              246  LOAD_FAST                'err'
              248  CALL_METHOD_2         2  ''
              250  POP_TOP          

 L. 316       252  POP_BLOCK        
              254  POP_EXCEPT       
              256  CALL_FINALLY        262  'to 262'
              258  LOAD_CONST               None
              260  RETURN_VALUE     
            262_0  COME_FROM           256  '256'
            262_1  COME_FROM_FINALLY   238  '238'
              262  LOAD_CONST               None
              264  STORE_FAST               'err'
              266  DELETE_FAST              'err'
              268  END_FINALLY      
              270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           228  '228'
              274  END_FINALLY      
            276_0  COME_FROM           272  '272'
            276_1  COME_FROM            72  '72'

Parse error at or near `POP_BLOCK' instruction at offset 218

    def py_import(self, name, version, path):
        """Return the normal python import."""
        import_path = os.path.joinself.target_dirnameversion
        os.path.exists(import_path) or os.makedirs(import_path)
        try:
            os.symlink(path, import_path, target_is_directory=(os.path.isdir(path)))
        except OSError:
            if os.path.isdir(path):
                shutil.copytree(path, import_path)
            else:
                shutil.copy(path, import_path)
        else:
            return self._import_modulenameversionpath

    def zip_import(self, name, version, path):
        """Import whl or zip files."""
        import_path = os.path.joinself.target_dirnameversion
        if not os.path.exists(import_path):
            os.makedirs(import_path)
            shutil.unpack_archive(path, import_path)
            if not any((p == name for p in os.listdir(import_path))):
                for p in os.listdir(import_path):
                    nested_path = os.path.join(import_path, p)
                    for np in os.listdir(nested_path):
                        shutil.move(os.path.join(nested_path, np), os.path.join(import_path, np))

        return self._import_modulenameversionpath

    def whl_install--- This code section failed: ---

 L. 361         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              join
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                target_dir
               10  LOAD_FAST                'name'
               12  LOAD_FAST                'version'
               14  CALL_METHOD_3         3  ''
               16  STORE_FAST               'import_path'

 L. 364        18  LOAD_FAST                'self'
               20  LOAD_ATTR                original_system
               22  LOAD_FAST                'import_path'
               24  LOAD_CONST               False
               26  LOAD_CONST               ('reset_modules',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  SETUP_WITH          192  'to 192'
               32  POP_TOP          

 L. 365        34  SETUP_FINALLY       126  'to 126'

 L. 366        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              exists
               42  LOAD_FAST                'import_path'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE    122  'to 122'

 L. 367        48  LOAD_GLOBAL              os
               50  LOAD_METHOD              makedirs
               52  LOAD_FAST                'import_path'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 368        58  LOAD_STR                 'install'
               60  LOAD_STR                 '--target'
               62  LOAD_FAST                'import_path'
               64  LOAD_FAST                'path'
               66  BUILD_LIST_4          4 
               68  STORE_FAST               'args'

 L. 369        70  LOAD_FAST                'self'
               72  LOAD_ATTR                install_dependencies
               74  POP_JUMP_IF_TRUE     88  'to 88'

 L. 370        76  LOAD_FAST                'args'
               78  LOAD_METHOD              insert
               80  LOAD_CONST               1
               82  LOAD_STR                 '--no-deps'
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          
             88_0  COME_FROM            74  '74'

 L. 373        88  LOAD_GLOBAL              mp
               90  LOAD_ATTR                Process
               92  LOAD_GLOBAL              pip_main
               94  LOAD_FAST                'args'
               96  BUILD_TUPLE_1         1 
               98  LOAD_STR                 'pip_install'
              100  LOAD_CONST               ('target', 'args', 'name')
              102  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              104  STORE_FAST               'proc'

 L. 374       106  LOAD_FAST                'proc'
              108  LOAD_METHOD              start
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          

 L. 375       114  LOAD_FAST                'proc'
              116  LOAD_METHOD              join
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          
            122_0  COME_FROM            46  '46'
              122  POP_BLOCK        
              124  JUMP_FORWARD        188  'to 188'
            126_0  COME_FROM_FINALLY    34  '34'

 L. 376       126  DUP_TOP          
              128  LOAD_GLOBAL              Exception
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   186  'to 186'
              134  POP_TOP          
              136  STORE_FAST               'err'
              138  POP_TOP          
              140  SETUP_FINALLY       174  'to 174'

 L. 377       142  LOAD_FAST                'self'
              144  LOAD_METHOD              error
              146  LOAD_FAST                'path'
              148  LOAD_FAST                'err'
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          

 L. 378       154  POP_BLOCK        
              156  POP_EXCEPT       
              158  CALL_FINALLY        174  'to 174'
              160  POP_BLOCK        
              162  BEGIN_FINALLY    
              164  WITH_CLEANUP_START
              166  WITH_CLEANUP_FINISH
              168  POP_FINALLY           0  ''
              170  LOAD_CONST               None
              172  RETURN_VALUE     
            174_0  COME_FROM           158  '158'
            174_1  COME_FROM_FINALLY   140  '140'
              174  LOAD_CONST               None
              176  STORE_FAST               'err'
              178  DELETE_FAST              'err'
              180  END_FINALLY      
              182  POP_EXCEPT       
              184  JUMP_FORWARD        188  'to 188'
            186_0  COME_FROM           132  '132'
              186  END_FINALLY      
            188_0  COME_FROM           184  '184'
            188_1  COME_FROM           124  '124'
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM_WITH       30  '30'
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      

 L. 380       198  LOAD_FAST                'self'
              200  LOAD_METHOD              _import_module
              202  LOAD_FAST                'name'
              204  LOAD_FAST                'version'
              206  LOAD_FAST                'path'
              208  CALL_METHOD_3         3  ''
              210  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 158

    def cleanup(self):
        """Properly close the tempfile directory."""
        try:
            self.remove_path((self.target_dir), delete_path=True)
        except:
            pass
        else:
            return self

    close = cleanup