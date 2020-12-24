# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/scan.py
# Compiled at: 2020-04-09 19:08:42
# Size of source mod 2**32: 4852 bytes
import ast, importlib, inspect, sys

def recursive(func):
    """ decorator to make visitor work recursive """

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    __doc__ = 'To detect unused import using ast'
    ignore_imports = ['__future__', '__doc__']
    ignore_names = ['print']

    def __init__(self, source=None):
        self.names = []
        self.imports = []
        self.classes = []
        self.functions = []
        if source:
            self.run_visit(source)

    @recursive
    def visit_ClassDef(self, node):
        for function_node in [body for body in node.body]:
            if isinstance(function_node, ast.FunctionDef):
                function_node.class_def = True

        self.classes.append({'lineno':node.lineno,  'name':node.name})

    @recursive
    def visit_FunctionDef(self, node):
        if not hasattr(node, 'class_def'):
            self.functions.append({'lineno':node.lineno,  'name':node.name})

    @recursive
    def visit_Import(self, node):
        star = False
        module_name = None
        module = None
        if hasattr(node, 'module'):
            module_name = node.module
        for alias in node.names:
            if alias.asname:
                name = alias.asname
            else:
                name = alias.name
            package = module_name or alias.name
            if package not in self.ignore_imports:
                if name == '*':
                    star = True
                    name = package
                try:
                    module = importlib.import_module(package)
                except (ModuleNotFoundError, ImportError, ValueError):
                    pass

                self.imports.append({'lineno':node.lineno, 
                 'name':name, 
                 'star':star, 
                 'module':module})

    @recursive
    def visit_ImportFrom(self, node):
        if node.module not in self.ignore_imports:
            self.visit_Import(node)

    @recursive
    def visit_Name(self, node):
        if node.id not in self.ignore_names:
            self.names.append({'lineno':node.lineno,  'name':node.id})

    @recursive
    def visit_Attribute--- This code section failed: ---

 L.  84         0  BUILD_LIST_0          0 
                2  STORE_FAST               'local_attr'

 L.  85         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'node'
                8  LOAD_STR                 'attr'
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L.  86        14  LOAD_FAST                'local_attr'
               16  LOAD_ATTR                append
               18  LOAD_FAST                'node'
               20  LOAD_ATTR                attr
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  POP_TOP          
             26_0  COME_FROM            12  '12'

 L.  87        26  SETUP_LOOP          176  'to 176'

 L.  88        28  LOAD_GLOBAL              hasattr
               30  LOAD_FAST                'node'
               32  LOAD_STR                 'value'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  POP_JUMP_IF_FALSE   170  'to 170'

 L.  89        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'node'
               42  LOAD_ATTR                value
               44  LOAD_GLOBAL              ast
               46  LOAD_ATTR                Attribute
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  POP_JUMP_IF_FALSE    82  'to 82'

 L.  90        52  LOAD_FAST                'node'
               54  LOAD_ATTR                value
               56  STORE_FAST               'node'

 L.  91        58  LOAD_GLOBAL              hasattr
               60  LOAD_FAST                'node'
               62  LOAD_STR                 'attr'
               64  CALL_FUNCTION_2       2  '2 positional arguments'
               66  POP_JUMP_IF_FALSE   168  'to 168'

 L.  92        68  LOAD_FAST                'local_attr'
               70  LOAD_ATTR                append
               72  LOAD_FAST                'node'
               74  LOAD_ATTR                attr
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  POP_TOP          
               80  JUMP_ABSOLUTE       172  'to 172'
               82  ELSE                     '168'

 L.  93        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'node'
               86  LOAD_ATTR                value
               88  LOAD_GLOBAL              ast
               90  LOAD_ATTR                Call
               92  CALL_FUNCTION_2       2  '2 positional arguments'
               94  POP_JUMP_IF_FALSE   132  'to 132'

 L.  94        96  LOAD_FAST                'node'
               98  LOAD_ATTR                value
              100  STORE_FAST               'node'

 L.  95       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'node'
              106  LOAD_ATTR                func
              108  LOAD_GLOBAL              ast
              110  LOAD_ATTR                Name
              112  CALL_FUNCTION_2       2  '2 positional arguments'
              114  POP_JUMP_IF_FALSE   168  'to 168'

 L.  96       116  LOAD_FAST                'local_attr'
              118  LOAD_ATTR                append
              120  LOAD_FAST                'node'
              122  LOAD_ATTR                func
              124  LOAD_ATTR                id
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  POP_TOP          
              130  JUMP_ABSOLUTE       172  'to 172'
              132  ELSE                     '168'

 L.  97       132  LOAD_GLOBAL              isinstance
              134  LOAD_FAST                'node'
              136  LOAD_ATTR                value
              138  LOAD_GLOBAL              ast
              140  LOAD_ATTR                Name
              142  CALL_FUNCTION_2       2  '2 positional arguments'
              144  POP_JUMP_IF_FALSE   166  'to 166'

 L.  98       146  LOAD_FAST                'node'
              148  LOAD_ATTR                value
              150  STORE_FAST               'node'

 L.  99       152  LOAD_FAST                'local_attr'
              154  LOAD_ATTR                append
              156  LOAD_FAST                'node'
              158  LOAD_ATTR                id
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  POP_TOP          
              164  JUMP_ABSOLUTE       172  'to 172'
              166  ELSE                     '168'

 L. 101       166  BREAK_LOOP       
            168_0  COME_FROM           114  '114'
            168_1  COME_FROM            66  '66'
              168  JUMP_BACK            28  'to 28'
              170  ELSE                     '172'

 L. 103       170  BREAK_LOOP       
              172  JUMP_BACK            28  'to 28'
              174  POP_BLOCK        
            176_0  COME_FROM_LOOP       26  '26'

 L. 104       176  LOAD_FAST                'local_attr'
              178  LOAD_ATTR                reverse
              180  CALL_FUNCTION_0       0  '0 positional arguments'
              182  POP_TOP          

 L. 105       184  LOAD_FAST                'self'
              186  LOAD_ATTR                names
              188  LOAD_ATTR                append

 L. 106       190  LOAD_FAST                'node'
              192  LOAD_ATTR                lineno
              194  LOAD_STR                 '.'
              196  LOAD_ATTR                join
              198  LOAD_FAST                'local_attr'
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  LOAD_CONST               ('lineno', 'name')
              204  BUILD_CONST_KEY_MAP_2     2 
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  POP_TOP          

Parse error at or near `ELSE' instruction at offset 170

    def imp_star_True(self, imp):
        if imp['module']:
            if imp['module'].__name__ not in sys.builtin_module_names:
                to_ = {to_cfv['name'] for to_cfv in self.names}
                try:
                    s = self.__class__(inspect.getsource(imp['module']))
                except OSError:
                    imp['modules'] = []

                imp['modules'] = sorted({cfv for cfv in {from_cfv['name'] for from_cfv in s.names + s.classes + s.functions} if cfv in to_})
        else:
            imp['modules'] = []
        return imp

    def imp_star_False(self, imp):
        for name in self.names:
            if '.'.join(name['name'].split('.')[:len(imp['name'].split('.'))]) == imp['name']:
                break
        else:
            return imp

    def get_unused_imports(self):
        for imp in self.imports:
            res = getattr(self, f"imp_star_{imp['star']}")(imp)
            if res:
                yield res

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear
        self.imports.clear
        self.classes.clear
        self.functions.clear