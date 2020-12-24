# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/__SANDBOXES__/base.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 7621 bytes
import os, re, ast, logging
LOGGER = logging.getLogger('cs')

def _execfile--- This code section failed: ---

 L.  26         0  LOAD_FAST                'args'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  STORE_FAST               'fn'

 L.  27         8  LOAD_GLOBAL              open
               10  LOAD_FAST                'fn'
               12  CALL_FUNCTION_1       1  ''
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'f'

 L.  28        18  LOAD_GLOBAL              compile
               20  LOAD_FAST                'f'
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  ''
               26  LOAD_FAST                'fn'
               28  LOAD_STR                 'exec'
               30  CALL_FUNCTION_3       3  ''
               32  STORE_FAST               'c'
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_WITH       14  '14'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L.  29        44  LOAD_GLOBAL              exec
               46  LOAD_FAST                'c'
               48  BUILD_TUPLE_1         1 
               50  LOAD_FAST                'args'
               52  LOAD_CONST               1
               54  LOAD_CONST               None
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               62  CALL_FUNCTION_EX      0  ''
               64  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 36


def prep_code(code, test, **kwargs):
    code = code.strip
    if test['variable'] is not None:
        footer = '_catsoop_answer = %s\nimport sys\nsys.settrace(None)' % test['variable']
    else:
        footer = None
    code = '\n\n'.join((
     'import os\nos.unlink(__file__)',
     kwargs['csq_code_pre'],
     test['code_pre'],
     code,
     'pass',
     kwargs['csq_code_post'],
     test['code'],
     footer))
    return code


def sandbox_run_code--- This code section failed: ---

 L.  67         0  LOAD_FAST                'context'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'csq_python_sandbox'
                6  LOAD_STR                 'remote'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               's'

 L.  68        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                path
               16  LOAD_METHOD              join

 L.  69        18  LOAD_FAST                'context'
               20  LOAD_STR                 'cs_fs_root'
               22  BINARY_SUBSCR    

 L.  69        24  LOAD_STR                 '__QTYPES__'

 L.  69        26  LOAD_STR                 'pythoncode'

 L.  69        28  LOAD_STR                 '__SANDBOXES__'

 L.  69        30  LOAD_STR                 '%s.py'
               32  LOAD_FAST                's'
               34  BINARY_MODULO    

 L.  68        36  CALL_METHOD_5         5  ''
               38  STORE_FAST               'sandbox_file'

 L.  72        40  LOAD_GLOBAL              LOGGER
               42  LOAD_METHOD              info
               44  LOAD_STR                 '[pythoncode.sandbox.base] sandbox_file=%s'
               46  LOAD_FAST                'sandbox_file'
               48  BINARY_MODULO    
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  73        54  LOAD_GLOBAL              dict
               56  LOAD_GLOBAL              DEFAULT_OPTIONS
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'opts'

 L.  74        62  LOAD_FAST                'opts'
               64  LOAD_METHOD              update
               66  LOAD_FAST                'context'
               68  LOAD_METHOD              get
               70  LOAD_STR                 'csq_sandbox_options'
               72  BUILD_MAP_0           0 
               74  CALL_METHOD_2         2  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.  75        80  LOAD_FAST                'opts'
               82  LOAD_METHOD              update
               84  LOAD_FAST                'options'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.  76        90  LOAD_GLOBAL              dict
               92  LOAD_FAST                'context'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'sandbox'

 L.  77        98  LOAD_GLOBAL              _execfile
              100  LOAD_FAST                'sandbox_file'
              102  LOAD_FAST                'sandbox'
              104  CALL_FUNCTION_2       2  ''
              106  POP_TOP          

 L.  78       108  SETUP_FINALLY       136  'to 136'

 L.  79       110  LOAD_FAST                'sandbox'
              112  LOAD_STR                 'run_code'
              114  BINARY_SUBSCR    

 L.  80       116  LOAD_FAST                'context'

 L.  81       118  LOAD_FAST                'code'

 L.  82       120  LOAD_FAST                'opts'

 L.  83       122  LOAD_FAST                'count_opcodes'

 L.  84       124  LOAD_FAST                'opcode_limit'

 L.  85       126  LOAD_FAST                'result_as_string'

 L.  79       128  LOAD_CONST               ('count_opcodes', 'opcode_limit', 'result_as_string')
              130  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              132  POP_BLOCK        
              134  RETURN_VALUE     
            136_0  COME_FROM_FINALLY   108  '108'

 L.  87       136  DUP_TOP          
              138  LOAD_GLOBAL              Exception
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   188  'to 188'
              144  POP_TOP          
              146  STORE_FAST               'err'
              148  POP_TOP          
              150  SETUP_FINALLY       176  'to 176'

 L.  88       152  LOAD_GLOBAL              LOGGER
              154  LOAD_METHOD              error

 L.  89       156  LOAD_STR                 '[pythoncode.sandbox.base] Failed to run_code, opts=%s, err=%s'

 L.  90       158  LOAD_FAST                'opts'
              160  LOAD_FAST                'err'
              162  BUILD_TUPLE_2         2 

 L.  89       164  BINARY_MODULO    

 L.  88       166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L.  92       170  RAISE_VARARGS_0       0  ''
              172  POP_BLOCK        
              174  BEGIN_FINALLY    
            176_0  COME_FROM_FINALLY   150  '150'
              176  LOAD_CONST               None
              178  STORE_FAST               'err'
              180  DELETE_FAST              'err'
              182  END_FINALLY      
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           142  '142'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'

Parse error at or near `DUP_TOP' instruction at offset 136


def fix_error_msg(fname, err, offset, sub):
    sublen = sub.count('\n')

    def subber(m):
        g = m.groups
        out = g[0]
        lineno = int(g[1])
        if lineno > offset + sublen + 1:
            out += 'File <Test Code>, line %d%s' % (lineno, g[2])
        elif lineno < offset:
            out += 'File <Test Code Preamble>, line %d%s' % (lineno, g[2])
        else:
            out += 'File <User-Submitted Code>, line %d%s' % (lineno - offset, g[2])
        return out

    error_regex = re.compile('(.*?)File "%s", line ([0-9]+)(,?[\n]*)' % fname)
    err = error_regex.subsubbererr
    err = err.replacefname'TEST FILE'
    e = err.split('\n')
    if len(e) > 15:
        err = '...ERROR OUTPUT TRUNCATED...\n\n' + '\n'.join(e[-10:])
    err = err.replace'[Subprocess exit code: 1]'''
    err = re.compile('(.*?)File "app_main.py", line ([0-9]+)(,?[^\n]*)\n').sub''err
    return err


DEFAULT_OPTIONS = {'CPUTIME':1, 
 'CLOCKTIME':1, 
 'MEMORY':33554432, 
 'FILESIZE':0, 
 'BADIMPORT':[],  'BADVAR':[],  'FILES':[],  'STDIN':''}

def truncate(out, name='OUTPUT'):
    outlines = out.split('\n')
    if len(outlines) > 15:
        outlines = outlines[:15] + ['...%s TRUNCATED...' % name]
    out = '\n'.join(outlines)
    if len(out) >= 5000:
        out = out[:5000] + '\n\n...%s TRUNCATED...' % name
    return out


def sandbox_run_test(context, code, test):
    options = dict(DEFAULT_OPTIONS)
    options.update(context.get'csq_sandbox_options'{})
    options.update(test.get'sandbox_options'{})
    safe = safety_checkcodeoptions['BADIMPORT']options['BADVAR']
    if isinstancesafetuple:
        return ('', 'On line %d: ' % safe[0] + safe[1], '')
    results = sandbox_run_code(context,
      prep_code(code, test, **context),
      options,
      count_opcodes=(test['count_opcodes']),
      opcode_limit=(test['opcode_limit']),
      result_as_string=(test['result_as_string']))
    err = truncateresults['err']'ERROR OUTPUT'
    err = fix_error_msg(results['fname'], err, context['csq_code_pre'].count('\n') + 2, code)
    out = truncateresults['out']'OUTPUT'
    return (
     out.strip, err.strip, results['info'])


def _ast_downward_search(node, testfunc):
    """
    recursive search through AST.  if a node causes testfunc to return true,
    then return that.  otherwise, return None
    """
    out = []
    if testfunc(node):
        out.append(node)
    for i in node._hz_children:
        out.extend(_ast_downward_searchitestfunc)

    return out


def _prepare_ast(tree, parent=None):
    """
    stupid little piece of code to add a parent pointer to all nodes
    """
    tree._hz_parent = parent
    tree._hz_children = list(ast.iter_child_nodes(tree))
    for i in tree._hz_children:
        _prepare_astitree


def _blacklist_variable(var, blacklist=None):
    blacklist = blacklist or 
    if var.id in blacklist:
        return 'Disallowed variable name: %s' % var.id
    return


def _blacklist_import--- This code section failed: ---

 L. 208         0  LOAD_FAST                'blacklist'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_LIST_0          0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'blacklist'

 L. 209         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'imp'
               12  LOAD_GLOBAL              ast
               14  LOAD_ATTR                ImportFrom
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    60  'to 60'

 L. 210        20  LOAD_FAST                'blacklist'
               22  GET_ITER         
             24_0  COME_FROM            40  '40'
               24  FOR_ITER             58  'to 58'
               26  STORE_FAST               'i'

 L. 211        28  LOAD_GLOBAL              re
               30  LOAD_METHOD              match
               32  LOAD_FAST                'i'
               34  LOAD_FAST                'imp'
               36  LOAD_ATTR                module
               38  CALL_METHOD_2         2  ''
               40  POP_JUMP_IF_FALSE    24  'to 24'

 L. 212        42  LOAD_STR                 'Disallowed import from %s'
               44  LOAD_FAST                'imp'
               46  LOAD_ATTR                module
               48  BINARY_MODULO    
               50  ROT_TWO          
               52  POP_TOP          
               54  RETURN_VALUE     
               56  JUMP_BACK            24  'to 24'
               58  JUMP_FORWARD        120  'to 120'
             60_0  COME_FROM            18  '18'

 L. 215        60  LOAD_LISTCOMP            '<code_object <listcomp>>'
               62  LOAD_STR                 '_blacklist_import.<locals>.<listcomp>'
               64  MAKE_FUNCTION_0          ''
               66  LOAD_FAST                'imp'
               68  LOAD_ATTR                names
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  GET_ITER         
               76  FOR_ITER            120  'to 120'
               78  STORE_FAST               'n'

 L. 216        80  LOAD_FAST                'blacklist'
               82  GET_ITER         
             84_0  COME_FROM            98  '98'
               84  FOR_ITER            118  'to 118'
               86  STORE_FAST               'i'

 L. 217        88  LOAD_GLOBAL              re
               90  LOAD_METHOD              match
               92  LOAD_FAST                'i'
               94  LOAD_FAST                'n'
               96  CALL_METHOD_2         2  ''
               98  POP_JUMP_IF_FALSE    84  'to 84'

 L. 218       100  LOAD_STR                 'Disallowed import: %s'
              102  LOAD_FAST                'n'
              104  BINARY_MODULO    
              106  ROT_TWO          
              108  POP_TOP          
              110  ROT_TWO          
              112  POP_TOP          
              114  RETURN_VALUE     
              116  JUMP_BACK            84  'to 84'
              118  JUMP_BACK            76  'to 76'
            120_0  COME_FROM            58  '58'

Parse error at or near `ROT_TWO' instruction at offset 110


def safety_check--- This code section failed: ---

 L. 225         0  LOAD_FAST                'code'
                2  LOAD_METHOD              replace
                4  LOAD_STR                 '\r\n'
                6  LOAD_STR                 '\n'
                8  CALL_METHOD_2         2  ''
               10  LOAD_METHOD              strip
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'code'

 L. 228        16  SETUP_FINALLY        40  'to 40'

 L. 229        18  LOAD_GLOBAL              ast
               20  LOAD_METHOD              parse
               22  LOAD_FAST                'code'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'tree'

 L. 230        28  LOAD_GLOBAL              _prepare_ast
               30  LOAD_FAST                'tree'
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD         54  'to 54'
             40_0  COME_FROM_FINALLY    16  '16'

 L. 231        40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 232        46  POP_EXCEPT       
               48  LOAD_STR                 'SYNTAX ERROR'
               50  RETURN_VALUE     
               52  END_FINALLY      
             54_0  COME_FROM            38  '38'

 L. 235        54  LOAD_GLOBAL              _ast_downward_search
               56  STORE_FAST               'search'

 L. 236        58  LOAD_FAST                'search'

 L. 237        60  LOAD_FAST                'tree'

 L. 238        62  LOAD_LAMBDA              '<code_object <lambda>>'
               64  LOAD_STR                 'safety_check.<locals>.<lambda>'
               66  MAKE_FUNCTION_0          ''

 L. 236        68  CALL_FUNCTION_2       2  ''
               70  STORE_FAST               'vars'

 L. 247        72  LOAD_FAST                'vars'
               74  JUMP_IF_TRUE_OR_POP    78  'to 78'
               76  BUILD_LIST_0          0 
             78_0  COME_FROM            74  '74'
               78  GET_ITER         
             80_0  COME_FROM           100  '100'
               80  FOR_ITER            118  'to 118'
               82  STORE_FAST               'var'

 L. 248        84  LOAD_GLOBAL              _blacklist_variable
               86  LOAD_FAST                'var'
               88  LOAD_FAST                'bad_variables'
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'res'

 L. 249        94  LOAD_FAST                'res'
               96  LOAD_CONST               None
               98  COMPARE_OP               is-not
              100  POP_JUMP_IF_FALSE    80  'to 80'

 L. 250       102  LOAD_FAST                'var'
              104  LOAD_ATTR                lineno
              106  LOAD_FAST                'res'
              108  BUILD_TUPLE_2         2 
              110  ROT_TWO          
              112  POP_TOP          
              114  RETURN_VALUE     
              116  JUMP_BACK            80  'to 80'

 L. 253       118  LOAD_GLOBAL              _ast_downward_search

 L. 254       120  LOAD_FAST                'tree'

 L. 254       122  LOAD_LAMBDA              '<code_object <lambda>>'
              124  LOAD_STR                 'safety_check.<locals>.<lambda>'
              126  MAKE_FUNCTION_0          ''

 L. 253       128  CALL_FUNCTION_2       2  ''
              130  STORE_FAST               'imports'

 L. 257       132  LOAD_FAST                'imports'
              134  JUMP_IF_TRUE_OR_POP   138  'to 138'
              136  BUILD_LIST_0          0 
            138_0  COME_FROM           134  '134'
              138  GET_ITER         
            140_0  COME_FROM           160  '160'
              140  FOR_ITER            178  'to 178'
              142  STORE_FAST               'imp'

 L. 258       144  LOAD_GLOBAL              _blacklist_import
              146  LOAD_FAST                'imp'
              148  LOAD_FAST                'bad_imports'
              150  CALL_FUNCTION_2       2  ''
              152  STORE_FAST               'res'

 L. 259       154  LOAD_FAST                'res'
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
              160  POP_JUMP_IF_FALSE   140  'to 140'

 L. 260       162  LOAD_FAST                'imp'
              164  LOAD_ATTR                lineno
              166  LOAD_FAST                'res'
              168  BUILD_TUPLE_2         2 
              170  ROT_TWO          
              172  POP_TOP          
              174  RETURN_VALUE     
              176  JUMP_BACK           140  'to 140'

Parse error at or near `LOAD_STR' instruction at offset 48