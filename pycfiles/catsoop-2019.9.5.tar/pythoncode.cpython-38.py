# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/pythoncode.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 23412 bytes
import os, ast, json, logging, traceback, collections.abc
from base64 import b64encode
from urllib.parse import urlencode
LOGGER = logging.getLogger('cs')

def _execfile(*args):
    fn = args[0]
    with open(fn) as (f):
        c = compile(f.read(), fn, 'exec')
    exec(c, *args[1:])


def get_sandbox(context):
    base = os.path.join(context['cs_fs_root'], '__QTYPES__', 'pythoncode', '__SANDBOXES__', 'base.py')
    _execfile(base, context)


def js_files(info):
    if info['csq_interface'] == 'ace':
        return [
         'BASE/scripts/ace/ace.js']
    return []


def html_format(string):
    s = string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\t', '    ').splitlines(False)
    jx = 0
    for ix, line in enumerate(s):
        for jx, char in enumerate(line):
            if char != ' ':
                break
            s[ix] = '&nbsp;' * jx + line[jx:]
        else:
            return '<br/>'.join(s)


defaults = {'csq_input_check':lambda x: None, 
 'csq_code_pre':'', 
 'csq_code_post':'', 
 'csq_initial':'pass  # Your code here', 
 'csq_soln':'print("Hello, World!")', 
 'csq_tests':[],  'csq_hint':lambda score, code, info: '', 
 'csq_log_keypresses':True, 
 'csq_variable_blacklist':[],  'csq_import_blacklist':[],  'csq_cpu_limit':2, 
 'csq_nproc_limit':0, 
 'csq_memory_limit':32000000.0, 
 'csq_interface':'ace', 
 'csq_rows':14, 
 'csq_font_size':16, 
 'csq_always_show_tests':False, 
 'csq_test_defaults':{},  'csq_use_simple_checker':False, 
 'csq_result_as_string':False}

class NoResult:
    pass


def _default_check_function(sub, soln):
    sub = sub.get('result', NoResult)
    soln = soln.get('result', NoResult)
    return sub == soln and sub is not NoResult


def _default_simple_check_function(sub, soln):
    return sub == soln


def _default_string_check_function(sub, soln):
    return ast.literal_eval(sub) == ast.literal_eval(soln)


test_defaults = {'npoints':1, 
 'code':'', 
 'code_pre':'', 
 'variable':'ans', 
 'description':'', 
 'include':False, 
 'include_soln':False, 
 'include_description':False, 
 'grade':True, 
 'show_description':True, 
 'show_code':True, 
 'show_stderr':True, 
 'transform_output':lambda x: '<tt style="white-space: pre-wrap">%s</tt>' % (
  html_format(repr(x)),), 
 'sandbox_options':{},  'count_opcodes':False, 
 'opcode_limit':None, 
 'show_timing':False, 
 'show_opcode_count':False}

def init(info):
    if info['csq_interface'] == 'upload':
        info['csq_rerender'] = True


def total_points(**info):
    if 'csq_npoints' in info:
        return info['csq_npoints']
    return total_test_points(**info)


def total_test_points(**info):
    bak = info['csq_tests']
    info['csq_tests'] = []
    for i in bak:
        info['csq_tests'].append(dict(test_defaults))
        info['csq_tests'][(-1)].update(info['csq_test_defaults'])
        info['csq_tests'][(-1)].update(i)
    else:
        return sum((i['npoints'] for i in info['csq_tests']))


checktext = 'Run Code'

def handle_check(submissions, **info):
    try:
        code = info['csm_loader'].get_file_data(info, submissions, info['csq_name'])
        code = code.decode().replace('\r\n', '\n')
    except:
        return {'score':0, 
         'msg':'<div class="bs-callout bs-callout-danger"><span class="text-danger"><b>Error:</b> Unable to decode the specified file.  Is this the file you intended to upload?</span></div>'}
    else:
        code = '\n\n'.join(['import os\nos.unlink(__file__)', info['csq_code_pre'], code])
        get_sandbox(info)
        results = info['sandbox_run_code'](info, code, info.get('csq_sandbox_options', {}))
        err = info['fix_error_msg'](results['fname'], results['err'], info['csq_code_pre'].count('\n') + 2, code)
        complete = results.get('info', {}).get('complete', False)
        trunc = False
        outlines = results['out'].split('\n')
        if len(outlines) > 10:
            trunc = True
            outlines = outlines[:10]
        out = '\n'.join(outlines)
        if len(out) >= 5000:
            trunc = True
            out = out[:5000]
        if trunc:
            out += '\n\n...OUTPUT TRUNCATED...'
        timeout = False
        if not complete:
            if 'SIGTERM' in err:
                timeout = True
                err = 'Your code did not run to completion, but no error message was returned.\nThis normally means that your code contains an infinite loop or otherwise took too long to run.'
        msg = '<div class="response">'
        if not timeout:
            msg += '<p><b>'
            if complete:
                msg += '<font color="darkgreen">Your code ran to completion.</font>'
            else:
                msg += '<font color="red">Your code did not run to completion.</font>'
            msg += '</b></p>'
        if out != '':
            msg += '\n<p><b>Your code produced the following output:</b>'
            msg += '<br/><pre>%s</pre></p>' % html_format(out)
        if err != '':
            if not timeout:
                msg += '\n<p><b>Your code produced an error:</b>'
            msg += "\n<br/><font color='red'><tt>%s</tt></font></p>" % html_format(err)
        msg += '</div>'
        return msg


def handle_submission--- This code section failed: ---

 L. 223         0  SETUP_FINALLY        44  'to 44'

 L. 224         2  LOAD_FAST                'info'
                4  LOAD_STR                 'csm_loader'
                6  BINARY_SUBSCR    
                8  LOAD_METHOD              get_file_data
               10  LOAD_FAST                'info'
               12  LOAD_FAST                'submissions'
               14  LOAD_FAST                'info'
               16  LOAD_STR                 'csq_name'
               18  BINARY_SUBSCR    
               20  CALL_METHOD_3         3  ''
               22  STORE_FAST               'code'

 L. 225        24  LOAD_FAST                'code'
               26  LOAD_METHOD              decode
               28  CALL_METHOD_0         0  ''
               30  LOAD_METHOD              replace
               32  LOAD_STR                 '\r\n'
               34  LOAD_STR                 '\n'
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'code'
               40  POP_BLOCK        
               42  JUMP_FORWARD        114  'to 114'
             44_0  COME_FROM_FINALLY     0  '0'

 L. 226        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE   112  'to 112'
               52  POP_TOP          
               54  STORE_FAST               'err'
               56  POP_TOP          
               58  SETUP_FINALLY       100  'to 100'

 L. 227        60  LOAD_GLOBAL              LOGGER
               62  LOAD_METHOD              warn

 L. 228        64  LOAD_STR                 "[pythoncode] handle_submission error '%s', traceback=%s"

 L. 229        66  LOAD_FAST                'err'
               68  LOAD_GLOBAL              traceback
               70  LOAD_METHOD              format_exc
               72  CALL_METHOD_0         0  ''
               74  BUILD_TUPLE_2         2 

 L. 228        76  BINARY_MODULO    

 L. 227        78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 232        82  LOAD_CONST               0

 L. 233        84  LOAD_STR                 '<div class="bs-callout bs-callout-danger"><span class="text-danger"><b>Error:</b> Unable to decode the specified file.  Is this the file you intended to upload?</span></div>'

 L. 231        86  LOAD_CONST               ('score', 'msg')
               88  BUILD_CONST_KEY_MAP_2     2 
               90  ROT_FOUR         
               92  POP_BLOCK        
               94  POP_EXCEPT       
               96  CALL_FINALLY        100  'to 100'
               98  RETURN_VALUE     
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM_FINALLY    58  '58'
              100  LOAD_CONST               None
              102  STORE_FAST               'err'
              104  DELETE_FAST              'err'
              106  END_FINALLY      
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            50  '50'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            42  '42'

 L. 235       114  LOAD_FAST                'info'
              116  LOAD_STR                 'csq_use_simple_checker'
              118  BINARY_SUBSCR    
              120  POP_JUMP_IF_FALSE   142  'to 142'

 L. 236       122  LOAD_FAST                'info'
              124  LOAD_STR                 'csq_result_as_string'
              126  BINARY_SUBSCR    
              128  POP_JUMP_IF_FALSE   136  'to 136'

 L. 237       130  LOAD_GLOBAL              _default_string_check_function
              132  STORE_FAST               'default_checker'
              134  JUMP_ABSOLUTE       146  'to 146'
            136_0  COME_FROM           128  '128'

 L. 239       136  LOAD_GLOBAL              _default_simple_check_function
              138  STORE_FAST               'default_checker'
              140  JUMP_FORWARD        146  'to 146'
            142_0  COME_FROM           120  '120'

 L. 241       142  LOAD_GLOBAL              _default_check_function
              144  STORE_FAST               'default_checker'
            146_0  COME_FROM           140  '140'

 L. 242       146  LOAD_LISTCOMP            '<code_object <listcomp>>'
              148  LOAD_STR                 'handle_submission.<locals>.<listcomp>'
              150  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              152  LOAD_FAST                'info'
              154  LOAD_STR                 'csq_tests'
              156  BINARY_SUBSCR    
              158  GET_ITER         
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'tests'

 L. 243       164  LOAD_GLOBAL              zip
              166  LOAD_FAST                'tests'
              168  LOAD_FAST                'info'
              170  LOAD_STR                 'csq_tests'
              172  BINARY_SUBSCR    
              174  CALL_FUNCTION_2       2  ''
              176  GET_ITER         
              178  FOR_ITER            212  'to 212'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'i'
              184  STORE_FAST               'j'

 L. 244       186  LOAD_FAST                'i'
              188  LOAD_METHOD              update
              190  LOAD_FAST                'info'
              192  LOAD_STR                 'csq_test_defaults'
              194  BINARY_SUBSCR    
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 245       200  LOAD_FAST                'i'
              202  LOAD_METHOD              update
              204  LOAD_FAST                'j'
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          
              210  JUMP_BACK           178  'to 178'

 L. 246       212  LOAD_LISTCOMP            '<code_object <listcomp>>'
              214  LOAD_STR                 'handle_submission.<locals>.<listcomp>'
              216  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              218  LOAD_FAST                'tests'
              220  GET_ITER         
              222  CALL_FUNCTION_1       1  ''
              224  STORE_FAST               'show_tests'

 L. 247       226  LOAD_GLOBAL              len
              228  LOAD_FAST                'show_tests'
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_CONST               0
              234  COMPARE_OP               >
          236_238  POP_JUMP_IF_FALSE   254  'to 254'

 L. 248       240  LOAD_FAST                'code'
              242  LOAD_METHOD              rsplit
              244  LOAD_STR                 '### Test Cases'
              246  CALL_METHOD_1         1  ''
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  STORE_FAST               'code'
            254_0  COME_FROM           236  '236'

 L. 250       254  LOAD_FAST                'info'
              256  LOAD_STR                 'csq_input_check'
              258  BINARY_SUBSCR    
              260  LOAD_FAST                'code'
              262  CALL_FUNCTION_1       1  ''
              264  STORE_FAST               'inp'

 L. 251       266  LOAD_FAST                'inp'
              268  LOAD_CONST               None
              270  COMPARE_OP               is-not
          272_274  POP_JUMP_IF_FALSE   294  'to 294'

 L. 252       276  LOAD_STR                 '<div class="response"><font color="red">%s</font></div>'
              278  LOAD_FAST                'inp'
              280  BINARY_MODULO    
              282  STORE_FAST               'msg'

 L. 253       284  LOAD_CONST               0
              286  LOAD_FAST                'msg'
              288  LOAD_CONST               ('score', 'msg')
              290  BUILD_CONST_KEY_MAP_2     2 
              292  RETURN_VALUE     
            294_0  COME_FROM           272  '272'

 L. 255       294  LOAD_FAST                'info'
              296  LOAD_STR                 'csq_tests'
              298  BINARY_SUBSCR    
              300  STORE_FAST               'bak'

 L. 256       302  BUILD_LIST_0          0 
              304  LOAD_FAST                'info'
              306  LOAD_STR                 'csq_tests'
              308  STORE_SUBSCR     

 L. 257       310  LOAD_FAST                'bak'
              312  GET_ITER         
            314_0  COME_FROM           356  '356'
              314  FOR_ITER            378  'to 378'
              316  STORE_FAST               'i'

 L. 258       318  LOAD_GLOBAL              dict
              320  LOAD_GLOBAL              test_defaults
              322  CALL_FUNCTION_1       1  ''
              324  STORE_FAST               'new'

 L. 259       326  LOAD_FAST                'i'
              328  LOAD_METHOD              update
              330  LOAD_FAST                'info'
              332  LOAD_STR                 'csq_test_defaults'
              334  BINARY_SUBSCR    
              336  CALL_METHOD_1         1  ''
              338  POP_TOP          

 L. 260       340  LOAD_FAST                'new'
              342  LOAD_METHOD              update
              344  LOAD_FAST                'i'
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          

 L. 261       350  LOAD_FAST                'new'
              352  LOAD_STR                 'grade'
              354  BINARY_SUBSCR    
          356_358  POP_JUMP_IF_FALSE   314  'to 314'

 L. 262       360  LOAD_FAST                'info'
              362  LOAD_STR                 'csq_tests'
              364  BINARY_SUBSCR    
              366  LOAD_METHOD              append
              368  LOAD_FAST                'new'
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
          374_376  JUMP_BACK           314  'to 314'

 L. 264       378  LOAD_GLOBAL              get_sandbox
              380  LOAD_FAST                'info'
              382  CALL_FUNCTION_1       1  ''
              384  POP_TOP          

 L. 266       386  LOAD_CONST               0
              388  STORE_FAST               'score'

 L. 267       390  LOAD_FAST                'info'
              392  LOAD_STR                 'csq_always_show_tests'
              394  BINARY_SUBSCR    
          396_398  POP_JUMP_IF_FALSE   406  'to 406'

 L. 268       400  LOAD_STR                 ''
              402  STORE_FAST               'msg'
              404  JUMP_FORWARD        410  'to 410'
            406_0  COME_FROM           396  '396'

 L. 271       406  LOAD_STR                 '\n<br/><button onclick="if(this.nextSibling.style.display === \'none\'){this.nextSibling.style.display = \'block\';}else{this.nextSibling.style.display = \'none\';}" class="btn btn-catsoop">Show/Hide Detailed Results</button>'

 L. 270       408  STORE_FAST               'msg'
            410_0  COME_FROM           404  '404'

 L. 274       410  LOAD_FAST                'msg'

 L. 275       412  LOAD_STR                 '<div class="response" id="%s_result_showhide" %s><h2>Test Results:</h2>'

 L. 277       414  LOAD_FAST                'info'
              416  LOAD_STR                 'csq_name'
              418  BINARY_SUBSCR    

 L. 278       420  LOAD_FAST                'info'
              422  LOAD_STR                 'csq_always_show_tests'
              424  BINARY_SUBSCR    
          426_428  POP_JUMP_IF_TRUE    434  'to 434'
              430  LOAD_STR                 'style="display:none"'
              432  JUMP_FORWARD        436  'to 436'
            434_0  COME_FROM           426  '426'
              434  LOAD_STR                 ''
            436_0  COME_FROM           432  '432'

 L. 276       436  BUILD_TUPLE_2         2 

 L. 274       438  BINARY_MODULO    
              440  INPLACE_ADD      
              442  STORE_FAST               'msg'

 L. 280       444  BUILD_LIST_0          0 
              446  STORE_FAST               'test_results'

 L. 281       448  LOAD_CONST               1
              450  STORE_FAST               'count'

 L. 282       452  LOAD_FAST                'info'
              454  LOAD_STR                 'csq_tests'
              456  BINARY_SUBSCR    
              458  GET_ITER         
          460_462  FOR_ITER           1928  'to 1928'
              464  STORE_DEREF              'test'

 L. 283       466  LOAD_DEREF               'test'
              468  LOAD_METHOD              get

 L. 284       470  LOAD_STR                 'result_as_string'

 L. 284       472  LOAD_FAST                'info'
              474  LOAD_METHOD              get
              476  LOAD_STR                 'csq_result_as_string'
              478  LOAD_CONST               False
              480  CALL_METHOD_2         2  ''

 L. 283       482  CALL_METHOD_2         2  ''
              484  LOAD_DEREF               'test'
              486  LOAD_STR                 'result_as_string'
              488  STORE_SUBSCR     

 L. 286       490  LOAD_FAST                'info'
              492  LOAD_STR                 'sandbox_run_test'
              494  BINARY_SUBSCR    
              496  LOAD_FAST                'info'
              498  LOAD_FAST                'code'
              500  LOAD_DEREF               'test'
              502  CALL_FUNCTION_3       3  ''
              504  UNPACK_SEQUENCE_3     3 
              506  STORE_FAST               'out'
              508  STORE_FAST               'err'
              510  STORE_FAST               'log'

 L. 287       512  LOAD_STR                 'cached_result'
              514  LOAD_DEREF               'test'
              516  COMPARE_OP               in
          518_520  POP_JUMP_IF_FALSE   540  'to 540'

 L. 288       522  LOAD_GLOBAL              repr
              524  LOAD_DEREF               'test'
              526  LOAD_STR                 'cached_result'
              528  BINARY_SUBSCR    
              530  CALL_FUNCTION_1       1  ''
              532  STORE_FAST               'log_s'

 L. 289       534  LOAD_STR                 'Loaded cached result'
              536  STORE_FAST               'err_s'
              538  JUMP_FORWARD        566  'to 566'
            540_0  COME_FROM           518  '518'

 L. 291       540  LOAD_FAST                'info'
              542  LOAD_STR                 'sandbox_run_test'
              544  BINARY_SUBSCR    
              546  LOAD_FAST                'info'
              548  LOAD_FAST                'info'
              550  LOAD_STR                 'csq_soln'
              552  BINARY_SUBSCR    
              554  LOAD_DEREF               'test'
              556  CALL_FUNCTION_3       3  ''
              558  UNPACK_SEQUENCE_3     3 
              560  STORE_FAST               'out_s'
              562  STORE_FAST               'err_s'
              564  STORE_FAST               'log_s'
            566_0  COME_FROM           538  '538'

 L. 292       566  LOAD_FAST                'count'
              568  LOAD_CONST               1
              570  COMPARE_OP               !=
          572_574  POP_JUMP_IF_FALSE   584  'to 584'

 L. 293       576  LOAD_FAST                'msg'
              578  LOAD_STR                 '\n<p></p><hr/><p></p>'
              580  INPLACE_ADD      
              582  STORE_FAST               'msg'
            584_0  COME_FROM           572  '572'

 L. 294       584  LOAD_FAST                'msg'
              586  LOAD_STR                 '\n<center><h3>Test %02d</h3>'
              588  LOAD_FAST                'count'
              590  BINARY_MODULO    
              592  INPLACE_ADD      
              594  STORE_FAST               'msg'

 L. 295       596  LOAD_DEREF               'test'
              598  LOAD_STR                 'show_description'
              600  BINARY_SUBSCR    
          602_604  POP_JUMP_IF_FALSE   622  'to 622'

 L. 296       606  LOAD_FAST                'msg'
              608  LOAD_STR                 '\n<i>%s</i>'
              610  LOAD_DEREF               'test'
              612  LOAD_STR                 'description'
              614  BINARY_SUBSCR    
              616  BINARY_MODULO    
              618  INPLACE_ADD      
              620  STORE_FAST               'msg'
            622_0  COME_FROM           602  '602'

 L. 297       622  LOAD_FAST                'msg'
              624  LOAD_STR                 '</center><p></p>'
              626  INPLACE_ADD      
              628  STORE_FAST               'msg'

 L. 298       630  LOAD_DEREF               'test'
              632  LOAD_STR                 'show_code'
              634  BINARY_SUBSCR    
          636_638  POP_JUMP_IF_FALSE   724  'to 724'

 L. 299       640  LOAD_LISTCOMP            '<code_object <listcomp>>'
              642  LOAD_STR                 'handle_submission.<locals>.<listcomp>'
              644  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 300       646  LOAD_GLOBAL              map
              648  LOAD_CLOSURE             'test'
              650  BUILD_TUPLE_1         1 
              652  LOAD_LAMBDA              '<code_object <lambda>>'
              654  LOAD_STR                 'handle_submission.<locals>.<lambda>'
              656  MAKE_FUNCTION_8          'closure'
              658  LOAD_STR                 'code_pre'
              660  LOAD_STR                 'code'
              662  BUILD_LIST_2          2 
              664  CALL_FUNCTION_2       2  ''

 L. 299       666  GET_ITER         
              668  CALL_FUNCTION_1       1  ''
              670  STORE_FAST               'html_code_pieces'

 L. 302       672  LOAD_FAST                'html_code_pieces'
              674  LOAD_METHOD              insert
              676  LOAD_CONST               1
              678  LOAD_STR                 '#Your Code Here'
              680  CALL_METHOD_2         2  ''
              682  POP_TOP          

 L. 303       684  LOAD_STR                 '<br/>'
              686  LOAD_METHOD              join
              688  LOAD_GENEXPR             '<code_object <genexpr>>'
              690  LOAD_STR                 'handle_submission.<locals>.<genexpr>'
              692  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              694  LOAD_FAST                'html_code_pieces'
              696  GET_ITER         
              698  CALL_FUNCTION_1       1  ''
              700  CALL_METHOD_1         1  ''
              702  STORE_FAST               'html_code'

 L. 304       704  LOAD_FAST                'msg'
              706  LOAD_STR                 '\nThe test case was:<br/>\n<p><tt>%s</tt></p>'
              708  LOAD_FAST                'html_code'
              710  BINARY_MODULO    
              712  INPLACE_ADD      
              714  STORE_FAST               'msg'

 L. 305       716  LOAD_FAST                'msg'
              718  LOAD_STR                 '<p>&nbsp;</p>'
              720  INPLACE_ADD      
              722  STORE_FAST               'msg'
            724_0  COME_FROM           636  '636'

 L. 307       724  LOAD_FAST                'log'
              726  LOAD_FAST                'out'
              728  LOAD_FAST                'err'
              730  LOAD_CONST               ('details', 'out', 'err')
              732  BUILD_CONST_KEY_MAP_3     3 
              734  STORE_FAST               'result'

 L. 308       736  LOAD_FAST                'log_s'
              738  LOAD_FAST                'out_s'
              740  LOAD_FAST                'err_s'
              742  LOAD_CONST               ('details', 'out', 'err')
              744  BUILD_CONST_KEY_MAP_3     3 
              746  STORE_FAST               'result_s'

 L. 309       748  LOAD_DEREF               'test'
              750  LOAD_STR                 'variable'
              752  BINARY_SUBSCR    
              754  LOAD_CONST               None
              756  COMPARE_OP               is-not
          758_760  POP_JUMP_IF_FALSE   818  'to 818'

 L. 310       762  LOAD_STR                 'result'
              764  LOAD_FAST                'log'
              766  COMPARE_OP               in
          768_770  POP_JUMP_IF_FALSE   790  'to 790'

 L. 311       772  LOAD_FAST                'log'
              774  LOAD_STR                 'result'
              776  BINARY_SUBSCR    
              778  LOAD_FAST                'result'
              780  LOAD_STR                 'result'
              782  STORE_SUBSCR     

 L. 312       784  LOAD_FAST                'log'
              786  LOAD_STR                 'result'
              788  DELETE_SUBSCR    
            790_0  COME_FROM           768  '768'

 L. 313       790  LOAD_STR                 'result'
              792  LOAD_FAST                'log_s'
              794  COMPARE_OP               in
          796_798  POP_JUMP_IF_FALSE   818  'to 818'

 L. 314       800  LOAD_FAST                'log_s'
              802  LOAD_STR                 'result'
              804  BINARY_SUBSCR    
              806  LOAD_FAST                'result_s'
              808  LOAD_STR                 'result'
              810  STORE_SUBSCR     

 L. 315       812  LOAD_FAST                'log_s'
              814  LOAD_STR                 'result'
              816  DELETE_SUBSCR    
            818_0  COME_FROM           796  '796'
            818_1  COME_FROM           758  '758'

 L. 317       818  LOAD_DEREF               'test'
              820  LOAD_METHOD              get
              822  LOAD_STR                 'check_function'
              824  LOAD_FAST                'default_checker'
              826  CALL_METHOD_2         2  ''
              828  STORE_FAST               'checker'

 L. 318       830  SETUP_FINALLY       876  'to 876'

 L. 319       832  LOAD_FAST                'info'
              834  LOAD_STR                 'csq_use_simple_checker'
              836  BINARY_SUBSCR    
          838_840  POP_JUMP_IF_FALSE   862  'to 862'

 L. 321       842  LOAD_FAST                'checker'
              844  LOAD_FAST                'result'
              846  LOAD_STR                 'result'
              848  BINARY_SUBSCR    
              850  LOAD_FAST                'result_s'
              852  LOAD_STR                 'result'
              854  BINARY_SUBSCR    
              856  CALL_FUNCTION_2       2  ''
              858  STORE_FAST               'check_result'
              860  JUMP_FORWARD        872  'to 872'
            862_0  COME_FROM           838  '838'

 L. 323       862  LOAD_FAST                'checker'
              864  LOAD_FAST                'result'
              866  LOAD_FAST                'result_s'
              868  CALL_FUNCTION_2       2  ''
              870  STORE_FAST               'check_result'
            872_0  COME_FROM           860  '860'
              872  POP_BLOCK        
              874  JUMP_FORWARD        892  'to 892'
            876_0  COME_FROM_FINALLY   830  '830'

 L. 324       876  POP_TOP          
              878  POP_TOP          
              880  POP_TOP          

 L. 325       882  LOAD_CONST               0.0
              884  STORE_FAST               'check_result'
              886  POP_EXCEPT       
              888  JUMP_FORWARD        892  'to 892'
              890  END_FINALLY      
            892_0  COME_FROM           888  '888'
            892_1  COME_FROM           874  '874'

 L. 327       892  LOAD_GLOBAL              isinstance
              894  LOAD_FAST                'check_result'
              896  LOAD_GLOBAL              collections
              898  LOAD_ATTR                abc
              900  LOAD_ATTR                Mapping
              902  CALL_FUNCTION_2       2  ''
          904_906  POP_JUMP_IF_FALSE   926  'to 926'

 L. 328       908  LOAD_FAST                'check_result'
              910  LOAD_STR                 'score'
              912  BINARY_SUBSCR    
              914  STORE_FAST               'percentage'

 L. 329       916  LOAD_FAST                'check_result'
              918  LOAD_STR                 'msg'
              920  BINARY_SUBSCR    
              922  STORE_FAST               'extra_msg'
              924  JUMP_FORWARD        960  'to 960'
            926_0  COME_FROM           904  '904'

 L. 330       926  LOAD_GLOBAL              isinstance
              928  LOAD_FAST                'check_result'
              930  LOAD_GLOBAL              collections
              932  LOAD_ATTR                abc
              934  LOAD_ATTR                Sequence
              936  CALL_FUNCTION_2       2  ''
          938_940  POP_JUMP_IF_FALSE   952  'to 952'

 L. 331       942  LOAD_FAST                'check_result'
              944  UNPACK_SEQUENCE_2     2 
              946  STORE_FAST               'percentage'
              948  STORE_FAST               'extra_msg'
              950  JUMP_FORWARD        960  'to 960'
            952_0  COME_FROM           938  '938'

 L. 333       952  LOAD_FAST                'check_result'
              954  STORE_FAST               'percentage'

 L. 334       956  LOAD_STR                 ''
              958  STORE_FAST               'extra_msg'
            960_0  COME_FROM           950  '950'
            960_1  COME_FROM           924  '924'

 L. 336       960  LOAD_FAST                'test_results'
              962  LOAD_METHOD              append
              964  LOAD_FAST                'percentage'
              966  CALL_METHOD_1         1  ''
              968  POP_TOP          

 L. 338       970  LOAD_CONST               None
              972  STORE_FAST               'imfile'

 L. 339       974  LOAD_FAST                'percentage'
              976  LOAD_CONST               1.0
              978  COMPARE_OP               ==
          980_982  POP_JUMP_IF_FALSE   994  'to 994'

 L. 340       984  LOAD_FAST                'info'
              986  LOAD_STR                 'cs_check_image'
              988  BINARY_SUBSCR    
              990  STORE_FAST               'imfile'
              992  JUMP_FORWARD       1012  'to 1012'
            994_0  COME_FROM           980  '980'

 L. 341       994  LOAD_FAST                'percentage'
              996  LOAD_CONST               0.0
              998  COMPARE_OP               ==
         1000_1002  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 342      1004  LOAD_FAST                'info'
             1006  LOAD_STR                 'cs_cross_image'
             1008  BINARY_SUBSCR    
             1010  STORE_FAST               'imfile'
           1012_0  COME_FROM          1000  '1000'
           1012_1  COME_FROM           992  '992'

 L. 344      1012  LOAD_FAST                'score'
             1014  LOAD_FAST                'percentage'
             1016  LOAD_DEREF               'test'
             1018  LOAD_STR                 'npoints'
             1020  BINARY_SUBSCR    
             1022  BINARY_MULTIPLY  
             1024  INPLACE_ADD      
             1026  STORE_FAST               'score'

 L. 346      1028  LOAD_DEREF               'test'
             1030  LOAD_STR                 'variable'
             1032  BINARY_SUBSCR    
             1034  LOAD_CONST               None
             1036  COMPARE_OP               is-not
             1038  STORE_FAST               'expected_variable'

 L. 347      1040  LOAD_FAST                'result_s'
             1042  BUILD_MAP_0           0 
             1044  COMPARE_OP               !=
             1046  STORE_FAST               'solution_ran'

 L. 348      1048  LOAD_FAST                'result'
             1050  BUILD_MAP_0           0 
             1052  COMPARE_OP               !=
             1054  STORE_FAST               'submission_ran'

 L. 349      1056  LOAD_DEREF               'test'
             1058  LOAD_STR                 'show_code'
             1060  BINARY_SUBSCR    
             1062  STORE_FAST               'show_code'

 L. 350      1064  LOAD_FAST                'result_s'
             1066  LOAD_STR                 'err'
             1068  BINARY_SUBSCR    
             1070  LOAD_STR                 ''
             1072  COMPARE_OP               !=
             1074  STORE_FAST               'error_in_solution'

 L. 351      1076  LOAD_FAST                'result'
             1078  LOAD_STR                 'err'
             1080  BINARY_SUBSCR    
             1082  LOAD_STR                 ''
             1084  COMPARE_OP               !=
             1086  STORE_FAST               'error_in_submission'

 L. 352      1088  LOAD_FAST                'result_s'
             1090  LOAD_STR                 'out'
             1092  BINARY_SUBSCR    
             1094  LOAD_STR                 ''
             1096  COMPARE_OP               !=
             1098  STORE_FAST               'solution_produced_output'

 L. 353      1100  LOAD_FAST                'result'
             1102  LOAD_STR                 'out'
             1104  BINARY_SUBSCR    
             1106  LOAD_STR                 ''
             1108  COMPARE_OP               !=
             1110  STORE_FAST               'submission_produced_output'

 L. 354      1112  LOAD_STR                 'result'
             1114  LOAD_FAST                'result'
             1116  COMPARE_OP               in
             1118  STORE_FAST               'got_submission_result'

 L. 355      1120  LOAD_STR                 'result'
             1122  LOAD_FAST                'result_s'
             1124  COMPARE_OP               in
             1126  STORE_FAST               'got_solution_result'

 L. 356      1128  LOAD_FAST                'imfile'
             1130  LOAD_CONST               None
             1132  COMPARE_OP               is
         1134_1136  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 357      1138  LOAD_STR                 ''
             1140  STORE_FAST               'image'
             1142  JUMP_FORWARD       1152  'to 1152'
           1144_0  COME_FROM          1134  '1134'

 L. 359      1144  LOAD_STR                 "<img src='%s' />"
             1146  LOAD_FAST                'imfile'
             1148  BINARY_MODULO    
             1150  STORE_FAST               'image'
           1152_0  COME_FROM          1142  '1142'

 L. 362      1152  LOAD_DEREF               'test'
             1154  LOAD_STR                 'show_timing'
             1156  BINARY_SUBSCR    
             1158  LOAD_CONST               True
             1160  COMPARE_OP               ==
         1162_1164  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 363      1166  LOAD_STR                 '%.06f'
             1168  LOAD_DEREF               'test'
             1170  LOAD_STR                 'show_timing'
             1172  STORE_SUBSCR     
           1174_0  COME_FROM          1162  '1162'

 L. 364      1174  LOAD_DEREF               'test'
             1176  LOAD_STR                 'show_timing'
             1178  BINARY_SUBSCR    
         1180_1182  JUMP_IF_FALSE_OR_POP  1194  'to 1194'
             1184  LOAD_STR                 'duration'
             1186  LOAD_FAST                'result_s'
             1188  LOAD_STR                 'details'
             1190  BINARY_SUBSCR    
             1192  COMPARE_OP               in
           1194_0  COME_FROM          1180  '1180'
             1194  STORE_FAST               'do_timing'

 L. 365      1196  LOAD_DEREF               'test'
             1198  LOAD_STR                 'show_opcode_count'
             1200  BINARY_SUBSCR    
         1202_1204  JUMP_IF_FALSE_OR_POP  1216  'to 1216'
             1206  LOAD_STR                 'opcode_count'
             1208  LOAD_FAST                'result_s'
             1210  LOAD_STR                 'details'
             1212  BINARY_SUBSCR    
             1214  COMPARE_OP               in
           1216_0  COME_FROM          1202  '1202'
             1216  STORE_FAST               'do_opcount'

 L. 366      1218  LOAD_FAST                'do_timing'
         1220_1222  POP_JUMP_IF_TRUE   1230  'to 1230'
             1224  LOAD_FAST                'do_opcount'
         1226_1228  POP_JUMP_IF_FALSE  1238  'to 1238'
           1230_0  COME_FROM          1220  '1220'

 L. 367      1230  LOAD_FAST                'msg'
             1232  LOAD_STR                 '\n<p>'
             1234  INPLACE_ADD      
             1236  STORE_FAST               'msg'
           1238_0  COME_FROM          1226  '1226'

 L. 368      1238  LOAD_FAST                'do_timing'
         1240_1242  POP_JUMP_IF_FALSE  1276  'to 1276'

 L. 369      1244  LOAD_FAST                'result_s'
             1246  LOAD_STR                 'details'
             1248  BINARY_SUBSCR    
             1250  LOAD_STR                 'duration'
             1252  BINARY_SUBSCR    
             1254  STORE_FAST               '_timing'

 L. 370      1256  LOAD_FAST                'msg'

 L. 371      1258  LOAD_STR                 '\nOur solution ran for %s seconds.'
             1260  LOAD_DEREF               'test'
             1262  LOAD_STR                 'show_timing'
             1264  BINARY_SUBSCR    
             1266  BINARY_MODULO    

 L. 372      1268  LOAD_FAST                '_timing'

 L. 370      1270  BINARY_MODULO    
             1272  INPLACE_ADD      
             1274  STORE_FAST               'msg'
           1276_0  COME_FROM          1240  '1240'

 L. 373      1276  LOAD_FAST                'do_timing'
         1278_1280  POP_JUMP_IF_FALSE  1296  'to 1296'
             1282  LOAD_FAST                'do_opcount'
         1284_1286  POP_JUMP_IF_FALSE  1296  'to 1296'

 L. 374      1288  LOAD_FAST                'msg'
             1290  LOAD_STR                 '\n<br/>'
             1292  INPLACE_ADD      
             1294  STORE_FAST               'msg'
           1296_0  COME_FROM          1284  '1284'
           1296_1  COME_FROM          1278  '1278'

 L. 375      1296  LOAD_FAST                'do_opcount'
         1298_1300  POP_JUMP_IF_FALSE  1326  'to 1326'

 L. 376      1302  LOAD_FAST                'result_s'
             1304  LOAD_STR                 'details'
             1306  BINARY_SUBSCR    
             1308  LOAD_STR                 'opcode_count'
             1310  BINARY_SUBSCR    
             1312  STORE_FAST               '_opcount'

 L. 377      1314  LOAD_FAST                'msg'
             1316  LOAD_STR                 '\nOur solution executed %s Python opcodes.<br/>'
             1318  LOAD_FAST                '_opcount'
             1320  BINARY_MODULO    
             1322  INPLACE_ADD      
             1324  STORE_FAST               'msg'
           1326_0  COME_FROM          1298  '1298'

 L. 378      1326  LOAD_FAST                'do_timing'
         1328_1330  POP_JUMP_IF_TRUE   1338  'to 1338'
             1332  LOAD_FAST                'do_opcount'
         1334_1336  POP_JUMP_IF_FALSE  1346  'to 1346'
           1338_0  COME_FROM          1328  '1328'

 L. 379      1338  LOAD_FAST                'msg'
             1340  LOAD_STR                 '\n</p>'
             1342  INPLACE_ADD      
             1344  STORE_FAST               'msg'
           1346_0  COME_FROM          1334  '1334'

 L. 381      1346  LOAD_FAST                'expected_variable'
         1348_1350  POP_JUMP_IF_FALSE  1426  'to 1426'
             1352  LOAD_FAST                'show_code'
         1354_1356  POP_JUMP_IF_FALSE  1426  'to 1426'

 L. 382      1358  LOAD_FAST                'got_solution_result'
         1360_1362  POP_JUMP_IF_FALSE  1410  'to 1410'

 L. 383      1364  LOAD_FAST                'msg'

 L. 384      1366  LOAD_STR                 '\n<p>Our solution produced the following value for <tt>%s</tt>:'

 L. 385      1368  LOAD_DEREF               'test'
             1370  LOAD_STR                 'variable'
             1372  BINARY_SUBSCR    

 L. 383      1374  BINARY_MODULO    
             1376  INPLACE_ADD      
             1378  STORE_FAST               'msg'

 L. 386      1380  LOAD_DEREF               'test'
             1382  LOAD_STR                 'transform_output'
             1384  BINARY_SUBSCR    
             1386  LOAD_FAST                'result_s'
             1388  LOAD_STR                 'result'
             1390  BINARY_SUBSCR    
             1392  CALL_FUNCTION_1       1  ''
             1394  STORE_FAST               'm'

 L. 387      1396  LOAD_FAST                'msg'
             1398  LOAD_STR                 "\n<br/><font color='blue'>%s</font></p>"
             1400  LOAD_FAST                'm'
             1402  BINARY_MODULO    
             1404  INPLACE_ADD      
             1406  STORE_FAST               'msg'
             1408  JUMP_FORWARD       1426  'to 1426'
           1410_0  COME_FROM          1360  '1360'

 L. 389      1410  LOAD_FAST                'msg'

 L. 390      1412  LOAD_STR                 '\n<p>Our solution did not produce a value for <tt>%s</tt>.</p>'

 L. 391      1414  LOAD_DEREF               'test'
             1416  LOAD_STR                 'variable'
             1418  BINARY_SUBSCR    

 L. 389      1420  BINARY_MODULO    
             1422  INPLACE_ADD      
             1424  STORE_FAST               'msg'
           1426_0  COME_FROM          1408  '1408'
           1426_1  COME_FROM          1354  '1354'
           1426_2  COME_FROM          1348  '1348'

 L. 393      1426  LOAD_FAST                'solution_produced_output'
         1428_1430  POP_JUMP_IF_FALSE  1466  'to 1466'
             1432  LOAD_FAST                'show_code'
         1434_1436  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 394      1438  LOAD_FAST                'msg'
             1440  LOAD_STR                 '\n<p>Our code produced the following output:'
             1442  INPLACE_ADD      
             1444  STORE_FAST               'msg'

 L. 395      1446  LOAD_FAST                'msg'
             1448  LOAD_STR                 '<br/><pre>%s</pre></p>'
             1450  LOAD_GLOBAL              html_format
             1452  LOAD_FAST                'result_s'
             1454  LOAD_STR                 'out'
             1456  BINARY_SUBSCR    
             1458  CALL_FUNCTION_1       1  ''
             1460  BINARY_MODULO    
             1462  INPLACE_ADD      
             1464  STORE_FAST               'msg'
           1466_0  COME_FROM          1434  '1434'
           1466_1  COME_FROM          1428  '1428'

 L. 397      1466  LOAD_FAST                'error_in_solution'
         1468_1470  POP_JUMP_IF_FALSE  1514  'to 1514'
             1472  LOAD_DEREF               'test'
             1474  LOAD_STR                 'show_stderr'
             1476  BINARY_SUBSCR    
         1478_1480  POP_JUMP_IF_FALSE  1514  'to 1514'

 L. 398      1482  LOAD_FAST                'msg'
             1484  LOAD_STR                 '\n<p><b>OOPS!</b> Our code produced an error:'
             1486  INPLACE_ADD      
             1488  STORE_FAST               'msg'

 L. 399      1490  LOAD_GLOBAL              html_format
             1492  LOAD_FAST                'result_s'
             1494  LOAD_STR                 'err'
             1496  BINARY_SUBSCR    
             1498  CALL_FUNCTION_1       1  ''
             1500  STORE_FAST               'e'

 L. 400      1502  LOAD_FAST                'msg'
             1504  LOAD_STR                 "\n<br/><font color='red'><tt>%s</tt></font></p>"
             1506  LOAD_FAST                'e'
             1508  BINARY_MODULO    
             1510  INPLACE_ADD      
             1512  STORE_FAST               'msg'
           1514_0  COME_FROM          1478  '1478'
           1514_1  COME_FROM          1468  '1468'

 L. 402      1514  LOAD_FAST                'show_code'
         1516_1518  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 403      1520  LOAD_FAST                'msg'
             1522  LOAD_STR                 '<p>&nbsp;</p>'
             1524  INPLACE_ADD      
             1526  STORE_FAST               'msg'
           1528_0  COME_FROM          1516  '1516'

 L. 406      1528  LOAD_DEREF               'test'
             1530  LOAD_STR                 'show_timing'
             1532  BINARY_SUBSCR    
         1534_1536  JUMP_IF_FALSE_OR_POP  1548  'to 1548'
             1538  LOAD_STR                 'duration'
             1540  LOAD_FAST                'result'
             1542  LOAD_STR                 'details'
             1544  BINARY_SUBSCR    
             1546  COMPARE_OP               in
           1548_0  COME_FROM          1534  '1534'
             1548  STORE_FAST               'do_timing'

 L. 407      1550  LOAD_DEREF               'test'
             1552  LOAD_STR                 'show_opcode_count'
             1554  BINARY_SUBSCR    
         1556_1558  JUMP_IF_FALSE_OR_POP  1570  'to 1570'
             1560  LOAD_STR                 'opcode_count'
             1562  LOAD_FAST                'result'
             1564  LOAD_STR                 'details'
             1566  BINARY_SUBSCR    
             1568  COMPARE_OP               in
           1570_0  COME_FROM          1556  '1556'
             1570  STORE_FAST               'do_opcount'

 L. 408      1572  LOAD_FAST                'do_timing'
         1574_1576  POP_JUMP_IF_TRUE   1584  'to 1584'
             1578  LOAD_FAST                'do_opcount'
         1580_1582  POP_JUMP_IF_FALSE  1592  'to 1592'
           1584_0  COME_FROM          1574  '1574'

 L. 409      1584  LOAD_FAST                'msg'
             1586  LOAD_STR                 '\n<p>'
             1588  INPLACE_ADD      
             1590  STORE_FAST               'msg'
           1592_0  COME_FROM          1580  '1580'

 L. 410      1592  LOAD_FAST                'do_timing'
         1594_1596  POP_JUMP_IF_FALSE  1630  'to 1630'

 L. 411      1598  LOAD_FAST                'result'
             1600  LOAD_STR                 'details'
             1602  BINARY_SUBSCR    
             1604  LOAD_STR                 'duration'
             1606  BINARY_SUBSCR    
             1608  STORE_FAST               '_timing'

 L. 412      1610  LOAD_FAST                'msg'

 L. 413      1612  LOAD_STR                 '\nYour solution ran for %s seconds.'
             1614  LOAD_DEREF               'test'
             1616  LOAD_STR                 'show_timing'
             1618  BINARY_SUBSCR    
             1620  BINARY_MODULO    

 L. 414      1622  LOAD_FAST                '_timing'

 L. 412      1624  BINARY_MODULO    
             1626  INPLACE_ADD      
             1628  STORE_FAST               'msg'
           1630_0  COME_FROM          1594  '1594'

 L. 415      1630  LOAD_FAST                'do_timing'
         1632_1634  POP_JUMP_IF_FALSE  1650  'to 1650'
             1636  LOAD_FAST                'do_opcount'
         1638_1640  POP_JUMP_IF_FALSE  1650  'to 1650'

 L. 416      1642  LOAD_FAST                'msg'
             1644  LOAD_STR                 '\n<br/>'
             1646  INPLACE_ADD      
             1648  STORE_FAST               'msg'
           1650_0  COME_FROM          1638  '1638'
           1650_1  COME_FROM          1632  '1632'

 L. 417      1650  LOAD_FAST                'do_opcount'
         1652_1654  POP_JUMP_IF_FALSE  1680  'to 1680'

 L. 418      1656  LOAD_FAST                'result'
             1658  LOAD_STR                 'details'
             1660  BINARY_SUBSCR    
             1662  LOAD_STR                 'opcode_count'
             1664  BINARY_SUBSCR    
             1666  STORE_FAST               '_opcount'

 L. 419      1668  LOAD_FAST                'msg'
             1670  LOAD_STR                 '\nYour code executed %d Python opcodes.<br/>'
             1672  LOAD_FAST                '_opcount'
             1674  BINARY_MODULO    
             1676  INPLACE_ADD      
             1678  STORE_FAST               'msg'
           1680_0  COME_FROM          1652  '1652'

 L. 420      1680  LOAD_FAST                'do_timing'
         1682_1684  POP_JUMP_IF_TRUE   1692  'to 1692'
             1686  LOAD_FAST                'do_opcount'
         1688_1690  POP_JUMP_IF_FALSE  1700  'to 1700'
           1692_0  COME_FROM          1682  '1682'

 L. 421      1692  LOAD_FAST                'msg'
             1694  LOAD_STR                 '\n</p>'
             1696  INPLACE_ADD      
             1698  STORE_FAST               'msg'
           1700_0  COME_FROM          1688  '1688'

 L. 423      1700  LOAD_FAST                'expected_variable'
         1702_1704  POP_JUMP_IF_FALSE  1786  'to 1786'
             1706  LOAD_FAST                'show_code'
         1708_1710  POP_JUMP_IF_FALSE  1786  'to 1786'

 L. 424      1712  LOAD_FAST                'got_submission_result'
         1714_1716  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 425      1718  LOAD_FAST                'msg'

 L. 426      1720  LOAD_STR                 '\n<p>Your submission produced the following value for <tt>%s</tt>:'

 L. 427      1722  LOAD_DEREF               'test'
             1724  LOAD_STR                 'variable'
             1726  BINARY_SUBSCR    

 L. 425      1728  BINARY_MODULO    
             1730  INPLACE_ADD      
             1732  STORE_FAST               'msg'

 L. 428      1734  LOAD_DEREF               'test'
             1736  LOAD_STR                 'transform_output'
             1738  BINARY_SUBSCR    
             1740  LOAD_FAST                'result'
             1742  LOAD_STR                 'result'
             1744  BINARY_SUBSCR    
             1746  CALL_FUNCTION_1       1  ''
             1748  STORE_FAST               'm'

 L. 429      1750  LOAD_FAST                'msg'
             1752  LOAD_STR                 "\n<br/><font color='blue'>%s</font>%s</p>"
             1754  LOAD_FAST                'm'
             1756  LOAD_FAST                'image'
             1758  BUILD_TUPLE_2         2 
             1760  BINARY_MODULO    
             1762  INPLACE_ADD      
             1764  STORE_FAST               'msg'
             1766  JUMP_FORWARD       1784  'to 1784'
           1768_0  COME_FROM          1714  '1714'

 L. 431      1768  LOAD_FAST                'msg'

 L. 432      1770  LOAD_STR                 '\n<p>Your submission did not produce a value for <tt>%s</tt>.</p>'

 L. 433      1772  LOAD_DEREF               'test'
             1774  LOAD_STR                 'variable'
             1776  BINARY_SUBSCR    

 L. 431      1778  BINARY_MODULO    
             1780  INPLACE_ADD      
             1782  STORE_FAST               'msg'
           1784_0  COME_FROM          1766  '1766'
             1784  JUMP_FORWARD       1798  'to 1798'
           1786_0  COME_FROM          1708  '1708'
           1786_1  COME_FROM          1702  '1702'

 L. 435      1786  LOAD_FAST                'msg'
             1788  LOAD_STR                 '\n<center>%s</center>'
             1790  LOAD_FAST                'image'
             1792  BINARY_MODULO    
             1794  INPLACE_ADD      
             1796  STORE_FAST               'msg'
           1798_0  COME_FROM          1784  '1784'

 L. 437      1798  LOAD_FAST                'submission_produced_output'
         1800_1802  POP_JUMP_IF_FALSE  1838  'to 1838'
             1804  LOAD_FAST                'show_code'
         1806_1808  POP_JUMP_IF_FALSE  1838  'to 1838'

 L. 438      1810  LOAD_FAST                'msg'
             1812  LOAD_STR                 '\n<p>Your code produced the following output:'
             1814  INPLACE_ADD      
             1816  STORE_FAST               'msg'

 L. 439      1818  LOAD_FAST                'msg'
             1820  LOAD_STR                 '<br/><pre>%s</pre></p>'
             1822  LOAD_GLOBAL              html_format
             1824  LOAD_FAST                'result'
             1826  LOAD_STR                 'out'
             1828  BINARY_SUBSCR    
             1830  CALL_FUNCTION_1       1  ''
             1832  BINARY_MODULO    
             1834  INPLACE_ADD      
             1836  STORE_FAST               'msg'
           1838_0  COME_FROM          1806  '1806'
           1838_1  COME_FROM          1800  '1800'

 L. 441      1838  LOAD_FAST                'error_in_submission'
         1840_1842  POP_JUMP_IF_FALSE  1898  'to 1898'
             1844  LOAD_DEREF               'test'
             1846  LOAD_STR                 'show_stderr'
             1848  BINARY_SUBSCR    
         1850_1852  POP_JUMP_IF_FALSE  1898  'to 1898'

 L. 442      1854  LOAD_FAST                'msg'
             1856  LOAD_STR                 '\n<p>Your submission produced an error:'
             1858  INPLACE_ADD      
             1860  STORE_FAST               'msg'

 L. 443      1862  LOAD_GLOBAL              html_format
             1864  LOAD_FAST                'result'
             1866  LOAD_STR                 'err'
             1868  BINARY_SUBSCR    
             1870  CALL_FUNCTION_1       1  ''
             1872  STORE_FAST               'e'

 L. 444      1874  LOAD_FAST                'msg'
             1876  LOAD_STR                 "\n<br/><font color='red'><tt>%s</tt></font></p>"
             1878  LOAD_FAST                'e'
             1880  BINARY_MODULO    
             1882  INPLACE_ADD      
             1884  STORE_FAST               'msg'

 L. 445      1886  LOAD_FAST                'msg'
             1888  LOAD_STR                 '\n<br/><center>%s</center>'
             1890  LOAD_FAST                'image'
             1892  BINARY_MODULO    
             1894  INPLACE_ADD      
             1896  STORE_FAST               'msg'
           1898_0  COME_FROM          1850  '1850'
           1898_1  COME_FROM          1840  '1840'

 L. 447      1898  LOAD_FAST                'extra_msg'
         1900_1902  POP_JUMP_IF_FALSE  1916  'to 1916'

 L. 448      1904  LOAD_FAST                'msg'
             1906  LOAD_STR                 '\n<p>%s</p>'
             1908  LOAD_FAST                'extra_msg'
             1910  BINARY_MODULO    
             1912  INPLACE_ADD      
             1914  STORE_FAST               'msg'
           1916_0  COME_FROM          1900  '1900'

 L. 450      1916  LOAD_FAST                'count'
             1918  LOAD_CONST               1
             1920  INPLACE_ADD      
             1922  STORE_FAST               'count'
         1924_1926  JUMP_BACK           460  'to 460'

 L. 452      1928  LOAD_FAST                'msg'
             1930  LOAD_STR                 '\n</div>'
             1932  INPLACE_ADD      
             1934  STORE_FAST               'msg'

 L. 453      1936  LOAD_GLOBAL              total_test_points
             1938  BUILD_TUPLE_0         0 
             1940  LOAD_FAST                'info'
             1942  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1944  STORE_FAST               'tp'

 L. 454      1946  LOAD_FAST                'tp'
             1948  LOAD_CONST               0
             1950  COMPARE_OP               !=
         1952_1954  POP_JUMP_IF_FALSE  1968  'to 1968'
             1956  LOAD_GLOBAL              float
             1958  LOAD_FAST                'score'
             1960  CALL_FUNCTION_1       1  ''
             1962  LOAD_FAST                'tp'
             1964  BINARY_TRUE_DIVIDE
             1966  JUMP_FORWARD       1970  'to 1970'
           1968_0  COME_FROM          1952  '1952'
             1968  LOAD_CONST               0
           1970_0  COME_FROM          1966  '1966'
             1970  STORE_FAST               'overall'

 L. 455      1972  LOAD_FAST                'info'
             1974  LOAD_METHOD              get
             1976  LOAD_STR                 'csq_hint'
             1978  CALL_METHOD_1         1  ''
             1980  STORE_FAST               'hint_func'

 L. 456      1982  LOAD_FAST                'hint_func'
         1984_1986  POP_JUMP_IF_FALSE  2094  'to 2094'

 L. 457      1988  SETUP_FINALLY      2034  'to 2034'

 L. 458      1990  LOAD_FAST                'hint_func'
             1992  LOAD_FAST                'test_results'
             1994  LOAD_FAST                'code'
             1996  LOAD_FAST                'info'
             1998  CALL_FUNCTION_3       3  ''
             2000  STORE_FAST               'hint'

 L. 459      2002  LOAD_FAST                'msg'
             2004  LOAD_FAST                'hint'
         2006_2008  JUMP_IF_TRUE_OR_POP  2012  'to 2012'
             2010  LOAD_STR                 ''
           2012_0  COME_FROM          2006  '2006'
             2012  INPLACE_ADD      
             2014  STORE_FAST               'msg'

 L. 460      2016  LOAD_GLOBAL              LOGGER
             2018  LOAD_METHOD              debug
             2020  LOAD_STR                 '[pythoncode] hint=%s'
             2022  LOAD_FAST                'hint'
             2024  BINARY_MODULO    
             2026  CALL_METHOD_1         1  ''
             2028  POP_TOP          
             2030  POP_BLOCK        
             2032  JUMP_FORWARD       2094  'to 2094'
           2034_0  COME_FROM_FINALLY  1988  '1988'

 L. 461      2034  DUP_TOP          
             2036  LOAD_GLOBAL              Exception
             2038  COMPARE_OP               exception-match
         2040_2042  POP_JUMP_IF_FALSE  2092  'to 2092'
             2044  POP_TOP          
             2046  STORE_FAST               'err'
             2048  POP_TOP          
             2050  SETUP_FINALLY      2080  'to 2080'

 L. 462      2052  LOAD_GLOBAL              LOGGER
             2054  LOAD_METHOD              warn

 L. 463      2056  LOAD_STR                 '[pythoncode] hint function %s produced error=%s at %s'

 L. 464      2058  LOAD_FAST                'hint_func'
             2060  LOAD_FAST                'err'
             2062  LOAD_GLOBAL              traceback
             2064  LOAD_METHOD              format_exc
             2066  CALL_METHOD_0         0  ''
             2068  BUILD_TUPLE_3         3 

 L. 463      2070  BINARY_MODULO    

 L. 462      2072  CALL_METHOD_1         1  ''
             2074  POP_TOP          
             2076  POP_BLOCK        
             2078  BEGIN_FINALLY    
           2080_0  COME_FROM_FINALLY  2050  '2050'
             2080  LOAD_CONST               None
             2082  STORE_FAST               'err'
             2084  DELETE_FAST              'err'
             2086  END_FINALLY      
             2088  POP_EXCEPT       
             2090  JUMP_FORWARD       2094  'to 2094'
           2092_0  COME_FROM          2040  '2040'
             2092  END_FINALLY      
           2094_0  COME_FROM          2090  '2090'
           2094_1  COME_FROM          2032  '2032'
           2094_2  COME_FROM          1984  '1984'

 L. 467      2094  LOAD_STR                 '\n<br/>&nbsp;Your score on your most recent submission was: %01.02f%%'

 L. 468      2096  LOAD_FAST                'overall'
             2098  LOAD_CONST               100
             2100  BINARY_MULTIPLY  

 L. 467      2102  BINARY_MODULO    

 L. 469      2104  LOAD_FAST                'msg'

 L. 466      2106  BINARY_ADD       
             2108  STORE_FAST               'msg'

 L. 470      2110  LOAD_FAST                'overall'
             2112  LOAD_FAST                'msg'
             2114  LOAD_CONST               ('score', 'msg')
             2116  BUILD_CONST_KEY_MAP_2     2 
             2118  STORE_FAST               'out'

 L. 471      2120  LOAD_FAST                'out'
             2122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 92


def make_initial_display(info):
    init = info['csq_initial']
    tests = [dict(test_defaults) for i in info['csq_tests']]
    for i, j in zip(tests, info['csq_tests']):
        i.update(j)
    else:
        show_tests = [i for i in tests if i['include']]
        l = len(show_tests) - 1
        if l > -1:
            init += '\n\n\n### Test Cases:\n'
        get_sandbox(info)
        for ix, i in enumerate(show_tests):
            i['result_as_string'] = i.get('result_as_string', info.get('csq_result_as_string', False))
            init += '\n# Test Case %d' % (ix + 1)
            if i['include_soln']:
                if 'cached_result' in i:
                    log_s = i['cached_result']
                else:
                    out_s, err_s, log_s = info['sandbox_run_test'](info, info['csq_soln'], i)
                init += ' (Should print: %s)' % log_s
            init += '\n'
            if i['include_description']:
                init += '# %s\n' % i['description']
            init += i['code']
            if info.get('csq_python3', True):
                init += '\nprint("Test Case %d:", %s)' % (ix + 1, i['variable'])
                if i['include_soln']:
                    init += '\nprint("Expected:", %s)' % (log_s,)
                else:
                    init += '\nprint "Test Case %d:", %s' % (ix + 1, i['variable'])
                if i['include_soln']:
                    init += '\nprint "Expected:", %s' % (log_s,)
                if ix != l:
                    init += '\n'
            return init


def render_html_textarea(last_log, **info):
    return (tutor.question('bigbox')[0]['render_html'])(last_log, **info)


def render_html_upload(last_log, **info):
    name = info['csq_name']
    init = last_log.get(name, (None, info['csq_initial']))
    if isinstance(init, str):
        fname = ''
    else:
        fname, init = init
    params = {'name':name,  'init':str(init), 
     'safeinit':(init or '').replace('<', '&lt;'), 
     'b64init':b64encode(make_initial_display(info).encode()).decode(), 
     'dl':' download="%s"' % info['csq_skeleton_name'] if 'csq_skeleton_name' in info else 'download'}
    out = ''
    if info.get('csq_show_skeleton', True):
        out += '\n<a href="data:text/plain;base64,%(b64init)s" target="_blank"%(dl)s>Code Skeleton</a><br />' % params
    if last_log.get(name, None) is not None:
        try:
            fname, loc = last_log[name]
            loc = os.path.basename(loc)
            _path = info['cs_path_info']
            if info['csm_cslog'].ENCRYPT_KEY is not None:
                seed = info['cs_path_info'][0] if info['cs_path_info'] else info['cs_path_info']
                _path = [info['csm_cslog']._e(i, repr(seed)) for i in info['cs_path_info']]
            else:
                _path = info['cs_path_info']
            qstring = urlencode({'path':json.dumps(_path),  'fname':loc})
            out += '<br/>'
            safe_fname = fname.replace('<', '').replace('>', '').replace('"', '').replace("'", '')
            out += '<a href="%s/_util/get_upload?%s" download="%s">Download Most Recent Submission</a><br/>' % (
             info['cs_url_root'], qstring, safe_fname)
        except:
            pass

    out += '\n<input type="file" style="display: none" id=%(name)s name="%(name)s" />' % params
    out += '\n<button class="btn btn-catsoop" id="%s_select_button">Select File</button>&nbsp;\n<tt><span id="%s_selected_file">No file selected</span></tt>' % (
     name, name)
    out += '\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ndocument.getElementById(\'%s\').value = \'\';\ndocument.getElementById(\'%s_select_button\').addEventListener(\'click\', function (){\n    document.getElementById("%s").click();\n});\ndocument.getElementById(\'%s\').addEventListener(\'change\', function (){\n    document.getElementById(\'%s_selected_file\').innerText = document.getElementById(\'%s\').value;\n});\n// @license-end\n</script>' % (
     name, name, name, name, name, name)
    return out


def render_html_ace(last_log, **info):
    name = info['csq_name']
    init = last_log.get(name, None)
    if init is None:
        init = make_initial_display(info)
    init = str(init)
    fontsize = info['csq_font_size']
    params = {'name':name, 
     'init':init, 
     'safeinit':init.replace('<', '&lt;'), 
     'height':info['csq_rows'] * fontsize + 4, 
     'fontsize':fontsize}
    return '\n<div class="ace_editor_wrapper" id="container%(name)s">\n<div id="editor%(name)s" name="editor%(name)s" class="embedded_ace_code">%(safeinit)s</div></div>\n<input type="hidden" name="%(name)s" id="%(name)s" />\n<input type="hidden" name="%(name)s_log" id="%(name)s_log" />\n<script type="text/javascript">\n    // @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\n    var log%(name)s = new Array();\n    var editor%(name)s = ace.edit("editor%(name)s");\n    editor%(name)s.setTheme("ace/theme/textmate");\n    editor%(name)s.getSession().setMode("ace/mode/python");\n    editor%(name)s.setShowFoldWidgets(false);\n    editor%(name)s.setValue(%(init)r)\n    document.getElementById("%(name)s").value = editor%(name)s.getValue();\n    editor%(name)s.on("change",function(e){\n        editor%(name)s.getSession().setUseSoftTabs(true);\n        document.getElementById("%(name)s").value = editor%(name)s.getValue();\n    });\n    editor%(name)s.clearSelection()\n    editor%(name)s.getSession().setUseSoftTabs(true);\n    editor%(name)s.on("paste",function(txt){editor%(name)s.getSession().setUseSoftTabs(false);});\n    editor%(name)s.getSession().setTabSize(4);\n    editor%(name)s.setFontSize("%(fontsize)spx");\n    document.getElementById("container%(name)s").style.height = "%(height)spx";\n    document.getElementById("editor%(name)s").style.height = "%(height)spx";\n    editor%(name)s.resize(true);\n    // @license-end\n</script>' % params


RENDERERS = {'textarea':render_html_textarea, 
 'ace':render_html_ace, 
 'upload':render_html_upload}

def render_html(last_log, **info):
    renderer = info['csq_interface']
    if renderer in RENDERERS:
        return (RENDERERS[renderer])((last_log or {}), **info)
    return "<font color='red'>Invalid <tt>pythoncode</tt> interface: %s</font>" % renderer


def answer_display(**info):
    out = 'Here is the solution we wrote:<br/>\n<pre><code id="%s_soln_highlight" class="lang-python">%s</code></pre>\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\nhljs.highlightBlock(document.getElementById("%s_soln_highlight"));\n// @license-end\n</script>' % (
     info['csq_name'], info['csq_soln'].replace('<', '&lt;'), info['csq_name'])
    return out