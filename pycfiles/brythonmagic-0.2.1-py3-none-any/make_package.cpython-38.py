# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\brython\make_package.py
# Compiled at: 2019-11-06 03:43:45
# Size of source mod 2**32: 4173 bytes
import json, os, re, time, ast
from . import python_minifier

class Visitor(ast.NodeVisitor):
    """Visitor"""

    def __init__(self, lib_path, package):
        self.imports = set()
        self.lib_path = lib_path
        self.package = package

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        if node.level > 0:
            package = self.package[:]
            level = node.level - 1
            if level:
                package.pop()
                level -= 1
            else:
                module = '.'.join(package)
                if node.module:
                    module += '.' + node.module
        else:
            module = node.module
        self.imports.add(module)
        for alias in node.names:
            if alias.name == '*':
                continue
            else:
                path = (os.path.join)(self.lib_path, *module.split('.'), *(
                 alias.name + '.py',))
                if os.path.exists(path):
                    self.imports.add(module + '.' + alias.name)


def make--- This code section failed: ---

 L.  47         0  LOAD_FAST                'package_name'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L.  48         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'package name is not specified'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  ''
             12_0  COME_FROM             2  '2'

 L.  49        12  LOAD_GLOBAL              print
               14  LOAD_STR                 'Generating package {}'
               16  LOAD_METHOD              format
               18  LOAD_FAST                'package_name'
               20  CALL_METHOD_1         1  ''
               22  CALL_FUNCTION_1       1  ''
               24  POP_TOP          

 L.  50        26  LOAD_STR                 '$timestamp'
               28  LOAD_GLOBAL              int
               30  LOAD_CONST               1000
               32  LOAD_GLOBAL              time
               34  LOAD_METHOD              time
               36  CALL_METHOD_0         0  ''
               38  BINARY_MULTIPLY  
               40  CALL_FUNCTION_1       1  ''
               42  BUILD_MAP_1           1 
               44  STORE_FAST               'VFS'

 L.  51        46  LOAD_GLOBAL              os
               48  LOAD_ATTR                path
               50  LOAD_METHOD              exists
               52  LOAD_GLOBAL              os
               54  LOAD_ATTR                path
               56  LOAD_METHOD              join
               58  LOAD_FAST                'package_path'
               60  LOAD_STR                 '__init__.py'
               62  CALL_METHOD_2         2  ''
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'has_init'

 L.  52        68  LOAD_CONST               0
               70  STORE_FAST               'nb'

 L.  53        72  LOAD_FAST                'exclude_dirs'
               74  LOAD_CONST               None
               76  COMPARE_OP               is
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L.  54        80  BUILD_LIST_0          0 
               82  STORE_FAST               'exclude_dirs'
             84_0  COME_FROM            78  '78'

 L.  55        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              walk
               88  LOAD_FAST                'package_path'
               90  CALL_METHOD_1         1  ''
               92  GET_ITER         
            94_96  FOR_ITER            562  'to 562'
               98  UNPACK_SEQUENCE_3     3 
              100  STORE_FAST               'dirpath'
              102  STORE_FAST               'dirnames'
              104  STORE_FAST               'filenames'

 L.  56       106  LOAD_CONST               False
              108  STORE_FAST               'flag'

 L.  57       110  LOAD_FAST                'dirpath'
              112  LOAD_METHOD              split
              114  LOAD_GLOBAL              os
              116  LOAD_ATTR                sep
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'root_elts'

 L.  58       122  LOAD_FAST                'exclude_dirs'
              124  GET_ITER         
            126_0  COME_FROM           136  '136'
              126  FOR_ITER            142  'to 142'
              128  STORE_FAST               'exclude'

 L.  59       130  LOAD_FAST                'exclude'
              132  LOAD_FAST                'root_elts'
              134  COMPARE_OP               in
              136  POP_JUMP_IF_FALSE   126  'to 126'

 L.  60       138  CONTINUE            126  'to 126'
              140  JUMP_BACK           126  'to 126'

 L.  61       142  LOAD_STR                 '__pycache__'
              144  LOAD_FAST                'dirnames'
              146  COMPARE_OP               in
              148  POP_JUMP_IF_FALSE   160  'to 160'

 L.  62       150  LOAD_FAST                'dirnames'
              152  LOAD_METHOD              remove
              154  LOAD_STR                 '__pycache__'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
            160_0  COME_FROM           148  '148'

 L.  64       160  LOAD_FAST                'dirpath'
              162  LOAD_FAST                'package_path'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   174  'to 174'

 L.  65       168  BUILD_LIST_0          0 
              170  STORE_FAST               'package'
              172  JUMP_FORWARD        202  'to 202'
            174_0  COME_FROM           166  '166'

 L.  67       174  LOAD_FAST                'dirpath'
              176  LOAD_GLOBAL              len
              178  LOAD_FAST                'package_path'
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_CONST               1
              184  BINARY_ADD       
              186  LOAD_CONST               None
              188  BUILD_SLICE_2         2 
              190  BINARY_SUBSCR    
              192  LOAD_METHOD              split
              194  LOAD_GLOBAL              os
              196  LOAD_ATTR                sep
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'package'
            202_0  COME_FROM           172  '172'

 L.  68       202  LOAD_FAST                'has_init'
              204  POP_JUMP_IF_FALSE   218  'to 218'

 L.  69       206  LOAD_FAST                'package'
              208  LOAD_METHOD              insert
              210  LOAD_CONST               0
              212  LOAD_FAST                'package_name'
              214  CALL_METHOD_2         2  ''
              216  POP_TOP          
            218_0  COME_FROM           204  '204'

 L.  71       218  LOAD_FAST                'filenames'
              220  GET_ITER         
          222_224  FOR_ITER            560  'to 560'
              226  STORE_FAST               'filename'

 L.  72       228  LOAD_GLOBAL              os
              230  LOAD_ATTR                path
              232  LOAD_METHOD              splitext
              234  LOAD_FAST                'filename'
              236  CALL_METHOD_1         1  ''
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               'name'
              242  STORE_FAST               'ext'

 L.  73       244  LOAD_FAST                'ext'
              246  LOAD_STR                 '.py'
              248  COMPARE_OP               !=
              250  POP_JUMP_IF_FALSE   254  'to 254'

 L.  74       252  JUMP_BACK           222  'to 222'
            254_0  COME_FROM           250  '250'

 L.  75       254  LOAD_FAST                'name'
              256  LOAD_METHOD              endswith
              258  LOAD_STR                 '__init__'
              260  CALL_METHOD_1         1  ''
              262  STORE_FAST               'is_package'

 L.  76       264  LOAD_FAST                'is_package'
          266_268  POP_JUMP_IF_FALSE   282  'to 282'

 L.  77       270  LOAD_STR                 '.'
              272  LOAD_METHOD              join
              274  LOAD_FAST                'package'
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'mod_name'
              280  JUMP_FORWARD        298  'to 298'
            282_0  COME_FROM           266  '266'

 L.  79       282  LOAD_STR                 '.'
              284  LOAD_METHOD              join
              286  LOAD_FAST                'package'
              288  LOAD_FAST                'name'
              290  BUILD_LIST_1          1 
              292  BINARY_ADD       
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'mod_name'
            298_0  COME_FROM           280  '280'

 L.  81       298  LOAD_FAST                'nb'
              300  LOAD_CONST               1
              302  INPLACE_ADD      
              304  STORE_FAST               'nb'

 L.  82       306  LOAD_GLOBAL              os
              308  LOAD_ATTR                path
              310  LOAD_METHOD              join
              312  LOAD_FAST                'dirpath'
              314  LOAD_FAST                'filename'
              316  CALL_METHOD_2         2  ''
              318  STORE_FAST               'absname'

 L.  83       320  LOAD_GLOBAL              open
              322  LOAD_FAST                'absname'
              324  LOAD_STR                 'utf-8'
              326  LOAD_CONST               ('encoding',)
              328  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              330  SETUP_WITH          346  'to 346'
              332  STORE_FAST               'f'

 L.  84       334  LOAD_FAST                'f'
              336  LOAD_METHOD              read
              338  CALL_METHOD_0         0  ''
              340  STORE_FAST               'data'
              342  POP_BLOCK        
              344  BEGIN_FINALLY    
            346_0  COME_FROM_WITH      330  '330'
              346  WITH_CLEANUP_START
              348  WITH_CLEANUP_FINISH
              350  END_FINALLY      

 L.  86       352  LOAD_GLOBAL              python_minifier
              354  LOAD_ATTR                minify
              356  LOAD_FAST                'data'
              358  LOAD_CONST               True
              360  LOAD_CONST               ('preserve_lines',)
              362  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              364  STORE_FAST               'data'

 L.  87       366  LOAD_FAST                'package'
              368  LOAD_CONST               None
              370  LOAD_CONST               None
              372  BUILD_SLICE_2         2 
              374  BINARY_SUBSCR    
              376  STORE_FAST               'path_elts'

 L.  88       378  LOAD_GLOBAL              os
              380  LOAD_ATTR                path
              382  LOAD_METHOD              basename
              384  LOAD_FAST                'filename'
              386  CALL_METHOD_1         1  ''
              388  LOAD_STR                 '__init__.py'
              390  COMPARE_OP               !=
          392_394  POP_JUMP_IF_FALSE   422  'to 422'

 L.  89       396  LOAD_FAST                'path_elts'
              398  LOAD_METHOD              append
              400  LOAD_GLOBAL              os
              402  LOAD_ATTR                path
              404  LOAD_METHOD              basename
              406  LOAD_FAST                'filename'
              408  CALL_METHOD_1         1  ''
              410  LOAD_CONST               None
              412  LOAD_CONST               -3
              414  BUILD_SLICE_2         2 
              416  BINARY_SUBSCR    
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          
            422_0  COME_FROM           392  '392'

 L.  90       422  LOAD_STR                 '.'
              424  LOAD_METHOD              join
              426  LOAD_FAST                'path_elts'
              428  CALL_METHOD_1         1  ''
              430  STORE_FAST               'fqname'

 L.  91       432  LOAD_GLOBAL              open
              434  LOAD_FAST                'absname'
              436  LOAD_STR                 'utf-8'
              438  LOAD_CONST               ('encoding',)
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              442  SETUP_WITH          498  'to 498'
              444  STORE_FAST               'f'

 L.  92       446  LOAD_GLOBAL              ast
              448  LOAD_METHOD              parse
              450  LOAD_FAST                'f'
              452  LOAD_METHOD              read
              454  CALL_METHOD_0         0  ''
              456  CALL_METHOD_1         1  ''
              458  STORE_FAST               'tree'

 L.  93       460  LOAD_GLOBAL              Visitor
              462  LOAD_FAST                'package_path'
              464  LOAD_FAST                'package'
              466  CALL_FUNCTION_2       2  ''
              468  STORE_FAST               'visitor'

 L.  94       470  LOAD_FAST                'visitor'
              472  LOAD_METHOD              visit
              474  LOAD_FAST                'tree'
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          

 L.  95       480  LOAD_GLOBAL              sorted
              482  LOAD_GLOBAL              list
              484  LOAD_FAST                'visitor'
              486  LOAD_ATTR                imports
              488  CALL_FUNCTION_1       1  ''
              490  CALL_FUNCTION_1       1  ''
              492  STORE_FAST               'imports'
              494  POP_BLOCK        
              496  BEGIN_FINALLY    
            498_0  COME_FROM_WITH      442  '442'
              498  WITH_CLEANUP_START
              500  WITH_CLEANUP_FINISH
              502  END_FINALLY      

 L.  97       504  LOAD_FAST                'is_package'
          506_508  POP_JUMP_IF_FALSE   528  'to 528'

 L.  98       510  LOAD_FAST                'ext'
              512  LOAD_FAST                'data'
              514  LOAD_FAST                'imports'
              516  LOAD_CONST               1
              518  BUILD_LIST_4          4 
              520  LOAD_FAST                'VFS'
              522  LOAD_FAST                'mod_name'
              524  STORE_SUBSCR     
              526  JUMP_FORWARD        542  'to 542'
            528_0  COME_FROM           506  '506'

 L. 100       528  LOAD_FAST                'ext'
              530  LOAD_FAST                'data'
              532  LOAD_FAST                'imports'
              534  BUILD_LIST_3          3 
              536  LOAD_FAST                'VFS'
              538  LOAD_FAST                'mod_name'
              540  STORE_SUBSCR     
            542_0  COME_FROM           526  '526'

 L. 102       542  LOAD_GLOBAL              print
              544  LOAD_STR                 'adding {} package {}'
              546  LOAD_METHOD              format
              548  LOAD_FAST                'mod_name'
              550  LOAD_FAST                'is_package'
              552  CALL_METHOD_2         2  ''
              554  CALL_FUNCTION_1       1  ''
              556  POP_TOP          
              558  JUMP_BACK           222  'to 222'
              560  JUMP_BACK            94  'to 94'

 L. 104       562  LOAD_FAST                'nb'
              564  LOAD_CONST               0
              566  COMPARE_OP               ==
          568_570  POP_JUMP_IF_FALSE   582  'to 582'

 L. 105       572  LOAD_GLOBAL              print
              574  LOAD_STR                 'No Python file found in current directory'
              576  CALL_FUNCTION_1       1  ''
              578  POP_TOP          
              580  JUMP_FORWARD        678  'to 678'
            582_0  COME_FROM           568  '568'

 L. 107       582  LOAD_GLOBAL              print
              584  LOAD_STR                 '{} files'
              586  LOAD_METHOD              format
              588  LOAD_FAST                'nb'
              590  CALL_METHOD_1         1  ''
              592  CALL_FUNCTION_1       1  ''
              594  POP_TOP          

 L. 108       596  LOAD_GLOBAL              open
              598  LOAD_GLOBAL              os
              600  LOAD_ATTR                path
              602  LOAD_METHOD              join
              604  LOAD_FAST                'package_path'
              606  LOAD_FAST                'package_name'
              608  LOAD_STR                 '.brython.js'
              610  BINARY_ADD       
              612  CALL_METHOD_2         2  ''

 L. 109       614  LOAD_STR                 'w'

 L. 109       616  LOAD_STR                 'utf-8'

 L. 108       618  LOAD_CONST               ('encoding',)
              620  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              622  SETUP_WITH          672  'to 672'

 L. 109       624  STORE_FAST               'out'

 L. 110       626  LOAD_FAST                'out'
              628  LOAD_METHOD              write
              630  LOAD_STR                 '__BRYTHON__.use_VFS = true;\n'
              632  CALL_METHOD_1         1  ''
              634  POP_TOP          

 L. 111       636  LOAD_FAST                'out'
              638  LOAD_METHOD              write
              640  LOAD_STR                 'var scripts = {}\n'
              642  LOAD_METHOD              format
              644  LOAD_GLOBAL              json
              646  LOAD_METHOD              dumps
              648  LOAD_FAST                'VFS'
              650  CALL_METHOD_1         1  ''
              652  CALL_METHOD_1         1  ''
              654  CALL_METHOD_1         1  ''
              656  POP_TOP          

 L. 112       658  LOAD_FAST                'out'
              660  LOAD_METHOD              write
              662  LOAD_STR                 '__BRYTHON__.update_VFS(scripts)\n'
              664  CALL_METHOD_1         1  ''
              666  POP_TOP          
              668  POP_BLOCK        
              670  BEGIN_FINALLY    
            672_0  COME_FROM_WITH      622  '622'
              672  WITH_CLEANUP_START
              674  WITH_CLEANUP_FINISH
              676  END_FINALLY      
            678_0  COME_FROM           580  '580'

Parse error at or near `BEGIN_FINALLY' instruction at offset 344


if __name__ == '__main__':
    import sys
    package_name = sys.argv[1] if len(sys.argv) > 1 else ''
    src_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    make(package_name, src_dir)