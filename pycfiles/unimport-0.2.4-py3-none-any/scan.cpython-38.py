# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/scan.py
# Compiled at: 2020-04-15 15:57:37
# Size of source mod 2**32: 5831 bytes
import ast, importlib, inspect, sys

def recursive(func):
    """decorator to make visitor work recursive"""

    def wrapper(self, node):
        func(self, node)
        self.generic_visit(node)

    return wrapper


class Scanner(ast.NodeVisitor):
    __doc__ = 'To detect unused import using ast'
    ignore_imports = [
     '__future__', '__doc__']
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
        else:
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
                except (ModuleNotFoundError, ValueError):
                    pass
                else:
                    self.imports.append({'lineno':node.lineno, 
                     'name':name, 
                     'star':star, 
                     'module':module})

    @recursive
    def visit_ImportFrom(self, node):
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
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L.  86        14  LOAD_FAST                'local_attr'
               16  LOAD_METHOD              append
               18  LOAD_FAST                'node'
               20  LOAD_ATTR                attr
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            12  '12'

 L.  88        26  LOAD_GLOBAL              hasattr
               28  LOAD_FAST                'node'
               30  LOAD_STR                 'value'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE   172  'to 172'

 L.  89        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'node'
               40  LOAD_ATTR                value
               42  LOAD_GLOBAL              ast
               44  LOAD_ATTR                Attribute
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    80  'to 80'

 L.  90        50  LOAD_FAST                'node'
               52  LOAD_ATTR                value
               54  STORE_FAST               'node'

 L.  91        56  LOAD_GLOBAL              hasattr
               58  LOAD_FAST                'node'
               60  LOAD_STR                 'attr'
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE   166  'to 166'

 L.  92        66  LOAD_FAST                'local_attr'
               68  LOAD_METHOD              append
               70  LOAD_FAST                'node'
               72  LOAD_ATTR                attr
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_ABSOLUTE       170  'to 170'
             80_0  COME_FROM            48  '48'

 L.  93        80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'node'
               84  LOAD_ATTR                value
               86  LOAD_GLOBAL              ast
               88  LOAD_ATTR                Call
               90  CALL_FUNCTION_2       2  ''
               92  POP_JUMP_IF_FALSE   130  'to 130'

 L.  94        94  LOAD_FAST                'node'
               96  LOAD_ATTR                value
               98  STORE_FAST               'node'

 L.  95       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'node'
              104  LOAD_ATTR                func
              106  LOAD_GLOBAL              ast
              108  LOAD_ATTR                Name
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   166  'to 166'

 L.  96       114  LOAD_FAST                'local_attr'
              116  LOAD_METHOD              append
              118  LOAD_FAST                'node'
              120  LOAD_ATTR                func
              122  LOAD_ATTR                id
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  JUMP_ABSOLUTE       170  'to 170'
            130_0  COME_FROM            92  '92'

 L.  97       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                'node'
              134  LOAD_ATTR                value
              136  LOAD_GLOBAL              ast
              138  LOAD_ATTR                Name
              140  CALL_FUNCTION_2       2  ''
              142  POP_JUMP_IF_FALSE   172  'to 172'

 L.  98       144  LOAD_FAST                'node'
              146  LOAD_ATTR                value
              148  STORE_FAST               'node'

 L.  99       150  LOAD_FAST                'local_attr'
              152  LOAD_METHOD              append
              154  LOAD_FAST                'node'
              156  LOAD_ATTR                id
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
              162  JUMP_ABSOLUTE       170  'to 170'

 L. 101       164  BREAK_LOOP          172  'to 172'
            166_0  COME_FROM           112  '112'
            166_1  COME_FROM            64  '64'
              166  JUMP_BACK            26  'to 26'

 L. 103       168  BREAK_LOOP          172  'to 172'
              170  JUMP_BACK            26  'to 26'
            172_0  COME_FROM           142  '142'
            172_1  COME_FROM            34  '34'

 L. 104       172  LOAD_FAST                'local_attr'
              174  LOAD_METHOD              reverse
              176  CALL_METHOD_0         0  ''
              178  POP_TOP          

 L. 105       180  LOAD_FAST                'self'
              182  LOAD_ATTR                names
              184  LOAD_METHOD              append

 L. 106       186  LOAD_FAST                'node'
              188  LOAD_ATTR                lineno
              190  LOAD_STR                 '.'
              192  LOAD_METHOD              join
              194  LOAD_FAST                'local_attr'
              196  CALL_METHOD_1         1  ''
              198  LOAD_CONST               ('lineno', 'name')
              200  BUILD_CONST_KEY_MAP_2     2 

 L. 105       202  CALL_METHOD_1         1  ''
              204  POP_TOP          

Parse error at or near `BREAK_LOOP' instruction at offset 168

    def run_visit(self, source):
        self.visit(ast.parse(source))

    def clear(self):
        self.names.clear
        self.imports.clear
        self.classes.clear
        self.functions.clear

    def imp_star_True--- This code section failed: ---

 L. 119         0  LOAD_FAST                'imp'
                2  LOAD_STR                 'module'
                4  BINARY_SUBSCR    
                6  POP_JUMP_IF_FALSE   154  'to 154'

 L. 120         8  LOAD_FAST                'imp'
               10  LOAD_STR                 'module'
               12  BINARY_SUBSCR    
               14  LOAD_ATTR                __name__
               16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                builtin_module_names
               20  COMPARE_OP               not-in
               22  POP_JUMP_IF_FALSE   162  'to 162'

 L. 121        24  LOAD_SETCOMP             '<code_object <setcomp>>'
               26  LOAD_STR                 'Scanner.imp_star_True.<locals>.<setcomp>'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                names
               34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  STORE_DEREF              'to_'

 L. 122        40  SETUP_FINALLY        66  'to 66'

 L. 123        42  LOAD_FAST                'self'
               44  LOAD_METHOD              __class__
               46  LOAD_GLOBAL              inspect
               48  LOAD_METHOD              getsource
               50  LOAD_FAST                'imp'
               52  LOAD_STR                 'module'
               54  BINARY_SUBSCR    
               56  CALL_METHOD_1         1  ''
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               's'
               62  POP_BLOCK        
               64  JUMP_FORWARD         94  'to 94'
             66_0  COME_FROM_FINALLY    40  '40'

 L. 124        66  DUP_TOP          
               68  LOAD_GLOBAL              OSError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    92  'to 92'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 125        80  BUILD_LIST_0          0 
               82  LOAD_FAST                'imp'
               84  LOAD_STR                 'modules'
               86  STORE_SUBSCR     
               88  POP_EXCEPT       
               90  JUMP_ABSOLUTE       162  'to 162'
             92_0  COME_FROM            72  '72'
               92  END_FINALLY      
             94_0  COME_FROM            64  '64'

 L. 127        94  LOAD_FAST                's'
               96  LOAD_ATTR                classes
               98  LOAD_FAST                's'
              100  LOAD_ATTR                functions
              102  BINARY_ADD       
              104  LOAD_FAST                's'
              106  LOAD_ATTR                names
              108  BINARY_ADD       
              110  STORE_FAST               'all_object'

 L. 128       112  LOAD_SETCOMP             '<code_object <setcomp>>'
              114  LOAD_STR                 'Scanner.imp_star_True.<locals>.<setcomp>'
              116  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              118  LOAD_FAST                'all_object'
              120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'all_name'

 L. 129       126  LOAD_GLOBAL              sorted

 L. 130       128  LOAD_CLOSURE             'to_'
              130  BUILD_TUPLE_1         1 
              132  LOAD_SETCOMP             '<code_object <setcomp>>'
              134  LOAD_STR                 'Scanner.imp_star_True.<locals>.<setcomp>'
              136  MAKE_FUNCTION_8          'closure'
              138  LOAD_FAST                'all_name'
              140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''

 L. 129       144  CALL_FUNCTION_1       1  ''
              146  LOAD_FAST                'imp'
              148  LOAD_STR                 'modules'
              150  STORE_SUBSCR     
              152  JUMP_FORWARD        162  'to 162'
            154_0  COME_FROM             6  '6'

 L. 133       154  BUILD_LIST_0          0 
              156  LOAD_FAST                'imp'
              158  LOAD_STR                 'modules'
              160  STORE_SUBSCR     
            162_0  COME_FROM           152  '152'
            162_1  COME_FROM            22  '22'

 L. 134       162  LOAD_FAST                'imp'
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 132

    def imp_star_False(self, imp):
        for name in self.names:
            if self.is_import_name_match_name(name, imp):
                break
            return imp

    def is_import_name_match_name(self, name, imp):
        return name['name'].startswith(imp['name']) and imp['lineno'] < name['lineno']

    def get_unused_imports(self):
        for imp in self.imports:
            if self.is_duplicate(imp['name']):
                for name in self.names:
                    if self.is_import_name_match_name(name, imp) and not self.is_duplicate_used(name, imp):
                        break
                else:
                    (yield imp)

            else:
                res = getattr(self, f"imp_star_{imp['star']}")(imp)
                if res:
                    (yield res)

    def is_duplicate(self, name):
        return [imp['name'] for imp in self.imports].count(name) > 1

    def get_duplicate_imports(self):
        for imp in self.imports:
            if self.is_duplicate(imp['name']):
                (yield imp)

    def is_duplicate_used(self, name, imp):

        def find_nearest_imp(name):
            nearest = ''
            for dup_imp in self.get_duplicate_imports:
                if dup_imp['lineno'] < name['lineno'] and dup_imp['name'] == name['name']:
                    nearest = dup_imp
                return nearest

        return imp != find_nearest_imp(name)