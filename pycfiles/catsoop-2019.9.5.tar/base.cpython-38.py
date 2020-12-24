# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/__SANDBOXES__/base.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 7621 bytes
import os, re, ast, logging
LOGGER = logging.getLogger('cs')

def _execfile(*args):
    fn = args[0]
    with open(fn) as (f):
        c = compile(f.read(), fn, 'exec')
    exec(c, *args[1:])


def prep_code(code, test, **kwargs):
    code = code.strip()
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


def sandbox_run_code(context, code, options, count_opcodes=False, opcode_limit=None, result_as_string=False):
    s = context.get('csq_python_sandbox', 'remote')
    sandbox_file = os.path.join(context['cs_fs_root'], '__QTYPES__', 'pythoncode', '__SANDBOXES__', '%s.py' % s)
    LOGGER.info('[pythoncode.sandbox.base] sandbox_file=%s' % sandbox_file)
    opts = dict(DEFAULT_OPTIONS)
    opts.update(context.get('csq_sandbox_options', {}))
    opts.update(options)
    sandbox = dict(context)
    _execfile(sandbox_file, sandbox)
    try:
        return sandbox['run_code'](context,
          code,
          opts,
          count_opcodes=count_opcodes,
          opcode_limit=opcode_limit,
          result_as_string=result_as_string)
    except Exception as err:
        try:
            LOGGER.error('[pythoncode.sandbox.base] Failed to run_code, opts=%s, err=%s' % (
             opts, err))
            raise
        finally:
            err = None
            del err


def fix_error_msg(fname, err, offset, sub):
    sublen = sub.count('\n')

    def subber(m):
        g = m.groups()
        out = g[0]
        lineno = int(g[1])
        if lineno > offset + sublen + 1:
            out += 'File <Test Code>, line %d%s' % (lineno, g[2])
        else:
            if lineno < offset:
                out += 'File <Test Code Preamble>, line %d%s' % (lineno, g[2])
            else:
                out += 'File <User-Submitted Code>, line %d%s' % (lineno - offset, g[2])
        return out

    error_regex = re.compile('(.*?)File "%s", line ([0-9]+)(,?[\n]*)' % fname)
    err = error_regex.sub(subber, err)
    err = err.replace(fname, 'TEST FILE')
    e = err.split('\n')
    if len(e) > 15:
        err = '...ERROR OUTPUT TRUNCATED...\n\n' + '\n'.join(e[-10:])
    err = err.replace('[Subprocess exit code: 1]', '')
    err = re.compile('(.*?)File "app_main.py", line ([0-9]+)(,?[^\n]*)\n').sub('', err)
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
    options.update(context.get('csq_sandbox_options', {}))
    options.update(test.get('sandbox_options', {}))
    safe = safety_check(code, options['BADIMPORT'], options['BADVAR'])
    if isinstance(safe, tuple):
        return (
         '', 'On line %d: ' % safe[0] + safe[1], '')
    results = sandbox_run_code(context,
      prep_code(code, test, **context),
      options,
      count_opcodes=(test['count_opcodes']),
      opcode_limit=(test['opcode_limit']),
      result_as_string=(test['result_as_string']))
    err = truncate(results['err'], 'ERROR OUTPUT')
    err = fix_error_msg(results['fname'], err, context['csq_code_pre'].count('\n') + 2, code)
    out = truncate(results['out'], 'OUTPUT')
    return (out.strip(), err.strip(), results['info'])


def _ast_downward_search(node, testfunc):
    """
    recursive search through AST.  if a node causes testfunc to return true,
    then return that.  otherwise, return None
    """
    out = []
    if testfunc(node):
        out.append(node)
    for i in node._hz_children:
        out.extend(_ast_downward_search(i, testfunc))
    else:
        return out


def _prepare_ast(tree, parent=None):
    """
    stupid little piece of code to add a parent pointer to all nodes
    """
    tree._hz_parent = parent
    tree._hz_children = list(ast.iter_child_nodes(tree))
    for i in tree._hz_children:
        _prepare_ast(i, tree)


def _blacklist_variable(var, blacklist=None):
    blacklist = blacklist or []
    if var.id in blacklist:
        return 'Disallowed variable name: %s' % var.id
    return


def _blacklist_import(imp, blacklist=None):
    blacklist = blacklist or []
    if isinstance(imp, ast.ImportFrom):
        for i in blacklist:
            if re.match(i, imp.module):
                return 'Disallowed import from %s' % imp.module

    else:
        for n in [i.name for i in imp.names]:
            for i in blacklist:
                if re.match(i, n):
                    return 'Disallowed import: %s' % n


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
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

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
              126  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

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