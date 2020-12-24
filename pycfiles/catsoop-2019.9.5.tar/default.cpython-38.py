# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__HANDLERS__/default/default.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 88887 bytes
import os, re, json, time, uuid, random, shutil, string, hashlib, binascii, traceback, collections
from bs4 import BeautifulSoup
_prefix = 'cs_defaulthandler_'

def new_entry--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              str
                2  LOAD_GLOBAL              uuid
                4  LOAD_METHOD              uuid4
                6  CALL_METHOD_0         0  ''
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'id_'

 L.  48        12  LOAD_FAST                'context'
               14  LOAD_STR                 'cs_path_info'
               16  BINARY_SUBSCR    

 L.  49        18  LOAD_FAST                'context'
               20  LOAD_METHOD              get
               22  LOAD_STR                 'cs_username'
               24  LOAD_STR                 'None'
               26  CALL_METHOD_2         2  ''

 L.  50        28  LOAD_DEREF               'qname'
               30  BUILD_LIST_1          1 

 L.  51        32  LOAD_CLOSURE             'qname'
               34  BUILD_TUPLE_1         1 
               36  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               38  LOAD_STR                 'new_entry.<locals>.<dictcomp>'
               40  MAKE_FUNCTION_8          'closure'
               42  LOAD_FAST                'context'
               44  LOAD_GLOBAL              _n
               46  LOAD_STR                 'form'
               48  CALL_FUNCTION_1       1  ''
               50  BINARY_SUBSCR    
               52  LOAD_METHOD              items
               54  CALL_METHOD_0         0  ''
               56  GET_ITER         
               58  CALL_FUNCTION_1       1  ''

 L.  52        60  LOAD_GLOBAL              time
               62  LOAD_METHOD              time
               64  CALL_METHOD_0         0  ''

 L.  53        66  LOAD_FAST                'action'

 L.  47        68  LOAD_CONST               ('path', 'username', 'names', 'form', 'time', 'action')
               70  BUILD_CONST_KEY_MAP_6     6 
               72  STORE_FAST               'obj'

 L.  57        74  LOAD_FAST                'context'
               76  LOAD_STR                 'cs_session_data'
               78  BINARY_SUBSCR    
               80  STORE_FAST               'session'

 L.  58        82  LOAD_FAST                'session'
               84  LOAD_METHOD              get
               86  LOAD_STR                 'is_lti_user'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L.  59        92  LOAD_FAST                'session'
               94  LOAD_METHOD              get
               96  LOAD_STR                 'lti_data'
               98  CALL_METHOD_1         1  ''
              100  LOAD_FAST                'obj'
              102  LOAD_STR                 'lti_data'
              104  STORE_SUBSCR     
            106_0  COME_FROM            90  '90'

 L.  61       106  LOAD_FAST                'context'
              108  LOAD_STR                 'cs_storage_backend'
              110  BINARY_SUBSCR    
              112  STORE_FAST               '_store'

 L.  62       114  LOAD_FAST                '_store'
              116  LOAD_STR                 'fs'
              118  COMPARE_OP               ==
          120_122  POP_JUMP_IF_FALSE   264  'to 264'

 L.  64       124  LOAD_GLOBAL              os
              126  LOAD_ATTR                path
              128  LOAD_METHOD              join
              130  LOAD_FAST                'context'
              132  LOAD_STR                 'cs_data_root'
              134  BINARY_SUBSCR    
              136  LOAD_STR                 '_logs'
              138  LOAD_STR                 '_checker'
              140  LOAD_STR                 'staging'
              142  LOAD_FAST                'id_'
              144  CALL_METHOD_5         5  ''
              146  STORE_FAST               'loc'

 L.  65       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                makedirs
              152  LOAD_GLOBAL              os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              dirname
              158  LOAD_FAST                'loc'
              160  CALL_METHOD_1         1  ''
              162  LOAD_CONST               True
              164  LOAD_CONST               ('exist_ok',)
              166  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              168  POP_TOP          

 L.  66       170  LOAD_GLOBAL              open
              172  LOAD_FAST                'loc'
              174  LOAD_STR                 'wb'
              176  CALL_FUNCTION_2       2  ''
              178  SETUP_WITH          206  'to 206'
              180  STORE_FAST               'f'

 L.  67       182  LOAD_FAST                'f'
              184  LOAD_METHOD              write
              186  LOAD_FAST                'context'
              188  LOAD_STR                 'csm_cslog'
              190  BINARY_SUBSCR    
              192  LOAD_METHOD              prep
              194  LOAD_FAST                'obj'
              196  CALL_METHOD_1         1  ''
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          
              202  POP_BLOCK        
              204  BEGIN_FINALLY    
            206_0  COME_FROM_WITH      178  '178'
              206  WITH_CLEANUP_START
              208  WITH_CLEANUP_FINISH
              210  END_FINALLY      

 L.  68       212  LOAD_GLOBAL              os
              214  LOAD_ATTR                path
              216  LOAD_METHOD              join

 L.  69       218  LOAD_FAST                'context'
              220  LOAD_STR                 'cs_data_root'
              222  BINARY_SUBSCR    

 L.  70       224  LOAD_STR                 '_logs'

 L.  71       226  LOAD_STR                 '_checker'

 L.  72       228  LOAD_STR                 'queued'

 L.  73       230  LOAD_STR                 '%s_%s'
              232  LOAD_GLOBAL              time
              234  LOAD_METHOD              time
              236  CALL_METHOD_0         0  ''
              238  LOAD_FAST                'id_'
              240  BUILD_TUPLE_2         2 
              242  BINARY_MODULO    

 L.  68       244  CALL_METHOD_5         5  ''
              246  STORE_FAST               'newloc'

 L.  75       248  LOAD_GLOBAL              shutil
              250  LOAD_METHOD              move
              252  LOAD_FAST                'loc'
              254  LOAD_FAST                'newloc'
              256  CALL_METHOD_2         2  ''
              258  POP_TOP          

 L.  76       260  LOAD_FAST                'id_'
              262  RETURN_VALUE     
            264_0  COME_FROM           120  '120'

 L.  77       264  LOAD_FAST                '_store'
              266  LOAD_STR                 'postgres'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   424  'to 424'

 L.  78       274  LOAD_CONST               0
              276  LOAD_CONST               None
              278  IMPORT_NAME              psycopg2
              280  STORE_FAST               'psycopg2'

 L.  80       282  LOAD_FAST                'psycopg2'
              284  LOAD_ATTR                connect

 L.  81       286  LOAD_FAST                'context'
              288  LOAD_STR                 'cs_postgres_host'
              290  BINARY_SUBSCR    

 L.  82       292  LOAD_FAST                'context'
              294  LOAD_STR                 'cs_postgres_db'
              296  BINARY_SUBSCR    

 L.  83       298  LOAD_FAST                'context'
              300  LOAD_STR                 'cs_postgres_port'
              302  BINARY_SUBSCR    

 L.  84       304  LOAD_FAST                'context'
              306  LOAD_STR                 'cs_postgres_password'
              308  BINARY_SUBSCR    

 L.  85       310  LOAD_FAST                'context'
              312  LOAD_STR                 'cs_postgres_user'
              314  BINARY_SUBSCR    

 L.  80       316  LOAD_CONST               ('host', 'dbname', 'port', 'password', 'user')
              318  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              320  STORE_FAST               'conn'

 L.  87       322  LOAD_FAST                'conn'
              324  LOAD_METHOD              cursor
              326  CALL_METHOD_0         0  ''
              328  STORE_FAST               'c'

 L.  88       330  LOAD_STR                 'INSERT INTO checker (id, status, worker, created, updated, check_start, data) VALUES (%s,%s,%s,NOW(),NOW(),%s,%s) RETURNING *'
              332  STORE_FAST               'QUERY'

 L.  89       334  LOAD_FAST                'context'
              336  LOAD_STR                 'csm_cslog'
              338  BINARY_SUBSCR    
              340  LOAD_ATTR                prep
              342  STORE_FAST               '_prep'

 L.  90       344  LOAD_FAST                'context'
              346  LOAD_STR                 'cs_session_data'
              348  BINARY_SUBSCR    
              350  STORE_FAST               'session'

 L.  91       352  LOAD_FAST                'c'
              354  LOAD_METHOD              execute
              356  LOAD_FAST                'QUERY'
              358  LOAD_FAST                'id_'
              360  LOAD_STR                 'QUEUED'
              362  LOAD_CONST               None
              364  LOAD_CONST               None
              366  LOAD_FAST                'context'
              368  LOAD_STR                 'csm_cslog'
              370  BINARY_SUBSCR    
              372  LOAD_METHOD              prep
              374  LOAD_FAST                'obj'
              376  CALL_METHOD_1         1  ''
              378  BUILD_TUPLE_5         5 
              380  CALL_METHOD_2         2  ''
              382  POP_TOP          

 L.  92       384  LOAD_FAST                'c'
              386  LOAD_METHOD              fetchone
              388  CALL_METHOD_0         0  ''
              390  LOAD_CONST               0
              392  BINARY_SUBSCR    
              394  STORE_FAST               'result'

 L.  93       396  LOAD_FAST                'conn'
              398  LOAD_METHOD              commit
              400  CALL_METHOD_0         0  ''
              402  POP_TOP          

 L.  94       404  LOAD_FAST                'c'
              406  LOAD_METHOD              close
              408  CALL_METHOD_0         0  ''
              410  POP_TOP          

 L.  95       412  LOAD_FAST                'conn'
              414  LOAD_METHOD              close
              416  CALL_METHOD_0         0  ''
              418  POP_TOP          

 L.  96       420  LOAD_FAST                'result'
              422  RETURN_VALUE     
            424_0  COME_FROM           270  '270'

 L.  98       424  LOAD_GLOBAL              Exception
              426  LOAD_STR                 'Unknown storage backend: %r'
              428  LOAD_FAST                '_store'
              430  BINARY_MODULO    
              432  CALL_FUNCTION_1       1  ''
              434  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 36


def _n(n):
    return '%s%s' % (_prefix, n)


def _unknown_handler(action):
    return lambda x: 'Unknown Action: %s' % action


def _get(context, key, default, cast=lambda x: x):
    v = context.getkeydefault
    return cast(v(context) if isinstancevcollections.Callable else v)


def handle(context):
    pre_handle(context)
    mode_handlers = {'view':handle_view, 
     'submit':handle_submit, 
     'check':handle_check, 
     'save':handle_save, 
     'viewanswer':handle_viewanswer, 
     'clearanswer':handle_clearanswer, 
     'viewexplanation':handle_viewexplanation, 
     'content_only':handle_content_only, 
     'raw_html':handle_raw_html, 
     'copy':handle_copy, 
     'copy_seed':handle_copy_seed, 
     'activate':handle_activate, 
     'lock':handle_lock, 
     'unlock':handle_unlock, 
     'grade':handle_grade, 
     'passthrough':lambda c: '', 
     'new_seed':handle_new_seed, 
     'list_questions':handle_list_questions, 
     'get_state':handle_get_state, 
     'manage_groups':manage_groups, 
     'render_single_question':handle_single_question, 
     'stats':handle_stats, 
     'whdw':handle_whdw}
    action = context[_n('action')]
    return mode_handlers.getaction_unknown_handler(action)(context)


def handle_list_questions(context):
    types = {v[0]['qtype']:k for k, v in context[_n('name_map')].items}
    order = list(context[_n('name_map')])
    return make_return_json(context, {'order':order,  'types':types}, [])


def handle_get_state(context):
    ll = context[_n('last_log')]
    for i in ll:
        if isinstancell[i]set:
            ll[i] = list(ll[i])
        ll['scores'] = {}
        for k, v in ll.get'last_submit_id'{}.items:
            try:
                with openos.path.join(context['cs_data_root'], '_logs', '_checker', 'results', v[0], v[1], v)'rb' as (f):
                    row = context['csm_cslog'].unprepf.read
            except:
                row = None
            else:
                if row is None:
                    ll['scores'][k] = 0.0
                else:
                    ll['scores'][k] = row['score'] or 0.0
        else:
            return make_return_json(context, ll, [])


def handle_single_question(context):
    lastlog = context[_n('last_log')]
    lastsubmit = lastlog.get'last_submit'{}
    qname = context['cs_form'].get'name'None
    elt = context[_n('name_map')][qname]
    o = render_question(elt, context, lastsubmit, wrap=False)
    return (('200', 'OK'), {'Content-type': 'text/html'}, o)


def handle_copy_seed(context):
    if context[_n('impersonating')]:
        impersonated = context[_n('uname')]
        uname = context[_n('real_uname')]
        path = context['cs_path_info']
        logname = 'random_seed'
        stored = (context['csm_cslog'].most_recent)(
         impersonated, path, logname, None, **context[_n('log_kwargs')])
        (context['csm_cslog'].update_log)(
         uname, path, logname, stored, **context[_n('log_kwargs')])
    return handle_save(context)


def _new_random_seed(n=100):
    try:
        return os.urandomn
    except:
        return ''.join(random.choicestring.ascii_letters for i in range(n))


def handle_new_seed(context):
    uname = context[_n('uname')]
    (context['csm_cslog'].update_log)(
     uname, 
     (context['cs_path_info']), 
     'random_seed', 
     (_new_random_seed()), **context[_n('log_kwargs')])
    names = context[_n('question_names')]
    outdict = {}
    for name in names:
        outdict[name] = {'rerender': 'Please refresh the page'}
    else:
        return make_return_jsoncontextoutdict


def handle_activate(context):
    submitted_pass = context[_n('form')].get'activation_password'''
    if submitted_pass == context[_n('activation_password')]:
        newstate = dict(context[_n('last_log')])
        newstate['activated'] = True
        uname = context[_n('uname')]
        (context['csm_cslog'].overwrite_log)(
         uname, 
         (context['cs_path_info']), 
         'problemstate', 
         newstate, **context[_n('log_kwargs')])
        context[_n('last_log')] = newstate
    return handle_view(context)


def handle_copy(context):
    if context[_n('impersonating')]:
        context[_n('uname')] = context[_n('real_uname')]
        ll = (context['csm_cslog'].most_recent)(
         (context[_n('uname')]), 
         (context['cs_path_info']), 
         'problemstate', {}, **context[_n('log_kwargs')])
        context[_n('last_log')] = ll
    return handle_save(context)


def handle_activation_form(context):
    context['cs_content_header'] = 'Problem Activation'
    out = '<form method="POST">'
    out += '\nActivation Password: <input type="text" name="activation_password" value="" />\n&nbsp;\n<input type="submit" name="action" value="Activate" />'
    if 'admin' in context[_n('perms')]:
        pwd = context[_n('activation_password')]
        out += '\n<p><u>Staff:</u> password is <tt><font color="blue">%s</font></tt>' % pwd
    out += '</form>'
    p = context[_n('perms')]
    if 'submit' in p or 'submit_all' in p:
        log_actioncontext{'action': 'show_activation_form'}
    return out


def handle_raw_html(context):
    perms = context[_n('perms')]
    lastlog = context[_n('last_log')]
    lastsubmit = lastlog.get'last_submit'{}
    if _get(context, 'cs_auth_required', True, bool):
        if 'view' not in perms:
            if 'view_all' not in perms:
                return 'You are not allowed to view this page.'
    if _get(context, 'cs_require_activation', False, bool):
        if not lastlog.get'activated'False:
            return 'You must activate this page first.'
    due = context[_n('due')]
    timing = context[_n('timing')]
    if timing == -1:
        if 'view_all' not in perms:
            reltime = context['csm_time'].long_timestampcontext[_n('rel')]
            reltime = reltime.replace';'' at'
            return 'This page is not yet available.  It will become available on %s.' % reltime
    page = ''
    num_questions = len(context[_n('name_map')])
    if num_questions > 0:
        if _get(context, 'cs_show_due', True, bool):
            if context.get'cs_due_date''NEVER' != 'NEVER':
                duetime = context['csm_time'].long_timestampdue
                page += '<tutoronly><center>The questions below are due on %s.<br/>&nbsp;<br/></center></tutoronly>' % duetime
    for elt in context['cs_problem_spec']:
        if isinstanceeltstr:
            page += elt
        else:
            page += render_question(elt, context, lastsubmit)
    else:
        page += default_javascript(context)
        page += default_timer(context)
        context['cs_template'] = 'BASE/templates/empty.template'
        return page


def handle_content_only(context):
    perms = context[_n('perms')]
    lastlog = context[_n('last_log')]
    lastsubmit = lastlog.get'last_submit'{}
    if _get(context, 'cs_auth_required', True, bool):
        if 'view' not in perms:
            if 'view_all' not in perms:
                return 'You are not allowed to view this page.'
    if _get(context, 'cs_require_activation', False, bool):
        if not lastlog.get'activated'False:
            return 'You must activate this page first.'
    due = context[_n('due')]
    timing = context[_n('timing')]
    if timing == -1:
        if 'view_all' not in perms:
            reltime = context['csm_time'].long_timestampcontext[_n('rel')]
            reltime = reltime.replace';'' at'
            return 'This page is not yet available.  It will become available on %s.' % reltime
    page = ''
    num_questions = len(context[_n('name_map')])
    if num_questions > 0:
        if _get(context, 'cs_show_due', True, bool):
            if context.get'cs_due_date''NEVER' != 'NEVER':
                duetime = context['csm_time'].long_timestampdue
                page += '<tutoronly><center>The questions below are due on %s.<br/>&nbsp;<br/></center></tutoronly>' % duetime
    for elt in context['cs_problem_spec']:
        if isinstanceeltstr:
            page += elt
        else:
            page += render_question(elt, context, lastsubmit)
    else:
        page += default_javascript(context)
        page += default_timer(context)
        context['cs_template'] = 'BASE/templates/noborder.template'
        return page


def handle_view(context):
    perms = context[_n('perms')]
    lastlog = context[_n('last_log')]
    lastsubmit = lastlog.get'last_submit'{}
    if _get(context, 'cs_auth_required', True, bool):
        if 'view' not in perms:
            if 'view_all' not in perms:
                return 'You are not allowed to view this page.'
    if _get(context, 'cs_require_activation', False, bool):
        if not lastlog.get'activated'False:
            return handle_activation_form(context)
    due = context[_n('due')]
    timing = context[_n('timing')]
    if timing == -1:
        if 'view_all' not in perms:
            reltime = context['csm_time'].long_timestampcontext[_n('rel')]
            reltime = reltime.replace';'' at'
            return 'This page is not yet available.  It will become available on %s.' % reltime
    page = ''
    num_questions = len(context[_n('name_map')])
    if num_questions > 0:
        if _get(context, 'cs_show_due', True, bool):
            if context.get'cs_due_date''NEVER' != 'NEVER':
                duetime = context['csm_time'].long_timestampdue
                page += '<tutoronly><center>The questions below are due on %s.<br/>&nbsp;<br/></center></tutoronly>' % duetime
    js_loads = []
    for elt in context['cs_problem_spec']:
        if isinstanceeltstr:
            page += elt
        else:
            page += render_question(elt, context, lastsubmit)
            if 'js_files' in elt[0]:
                a = elt[0].get'defaults'{}
                a.updateelt[1]
                js_loads.extendelt[0]['js_files'](a)
            if js_loads:
                context['cs_scripts'] += '\n\n    <!--JS for questions-->\n    ' + '\n    '.join('<script type="text/javascript" src="%s"></script>' % context['csm_dispatch'].get_real_urlcontexti for i in js_loads)
            page += default_javascript(context)
            page += default_timer(context)
            return page


def get_manual_grading_entry(context, name):
    uname = context['cs_user_info'].get'username''None'
    log = (context['csm_cslog'].read_log)(
     uname, (context['cs_path_info']), 'problemgrades', **context[_n('log_kwargs')])
    out = None
    for i in log:
        if i['qname'] == name:
            out = i
        return out


def handle_clearanswer(context):
    names = context[_n('question_names')]
    due = context[_n('due')]
    lastlog = context[_n('last_log')]
    answerviewed = context[_n('answer_viewed')]
    explanationviewed = context[_n('explanation_viewed')]
    newstate = dict(lastlog)
    newstate['timestamp'] = context['cs_timestamp']
    if 'last_submit' not in newstate:
        newstate['last_submit'] = {}
    outdict = {}
    for name in names:
        if name.startswith'__':
            pass
        else:
            out = {}
            error = clearanswer_msg(context, context[_n('perms')], name)
            if error is not None:
                out['error_msg'] = error
                outdict[name] = out
            else:
                q, args = context[_n('name_map')][name]
                out['clear'] = True
                outdict[name] = out
                answerviewed.discardname
                explanationviewed.discardname
    else:
        newstate['answer_viewed'] = answerviewed
        newstate['explanation_viewed'] = explanationviewed
        uname = context[_n('uname')]
        (context['csm_cslog'].overwrite_log)(
         uname, 
         (context['cs_path_info']), 
         'problemstate', 
         newstate, **context[_n('log_kwargs')])
        duetime = context['csm_time'].detailed_timestampdue
        log_actioncontext{'action':'viewanswer', 
         'names':names, 
         'score':newstate.get'score'0.0, 
         'response':outdict, 
         'due_date':duetime}
        return make_return_jsoncontextoutdict


def explanation_display(x):
    return '<hr /><p><b>Explanation:</b></p>%s' % x


def handle_viewexplanation(context, outdict=None, skip_empty=False):
    """
    context: (dict) catsoop context
    outdict: (dict) output for each question, defaults to {}
    """
    names = context[_n('question_names')]
    due = context[_n('due')]
    lastlog = context[_n('last_log')]
    explanationviewed = context[_n('explanation_viewed')]
    loader = context['csm_loader']
    language = context['csm_language']
    newstate = dict(lastlog)
    newstate['timestamp'] = context['cs_timestamp']
    if 'last_submit' not in newstate:
        newstate['last_submit'] = {}
    outdict = outdict or {}
    for name in names:
        if name.startswith'__':
            pass
        else:
            out = outdict.getname{}
            q, args = context[_n('name_map')][name]
            if 'csq_explanation' not in args and skip_empty:
                pass
            else:
                error = viewexp_msg(context, context[_n('perms')], name)
                if error is not None:
                    out['error_msg'] = error
                    outdict[name] = out
                else:
                    exp = explanation_display(args['csq_explanation'])
                    out['explanation'] = language.source_transform_stringcontextexp
                    outdict[name] = out
                    explanationviewed.addname
    else:
        newstate['explanation_viewed'] = explanationviewed
        uname = context[_n('uname')]
        (context['csm_cslog'].overwrite_log)(
         uname, 
         (context['cs_path_info']), 
         'problemstate', 
         newstate, **context[_n('log_kwargs')])
        duetime = context['csm_time'].detailed_timestampdue
        log_actioncontext{'action':'viewanswer', 
         'names':names, 
         'score':newstate.get'score'0.0, 
         'response':outdict, 
         'due_date':duetime}
        return make_return_jsoncontextoutdict


def handle_viewanswer(context):
    names = context[_n('question_names')]
    due = context[_n('due')]
    lastlog = context[_n('last_log')]
    answerviewed = context[_n('answer_viewed')]
    loader = context['csm_loader']
    language = context['csm_language']
    newstate = dict(lastlog)
    newstate['timestamp'] = context['cs_timestamp']
    if 'last_submit' not in newstate:
        newstate['last_submit'] = {}
    outdict = {}
    for name in names:
        if name.startswith'__':
            pass
        else:
            out = {}
            error = viewanswer_msg(context, context[_n('perms')], name)
            if error is not None:
                out['error_msg'] = error
                outdict[name] = out
            else:
                q, args = context[_n('name_map')][name]
                ans = (q['answer_display'])(**args)
                out['answer'] = language.source_transform_stringcontextans
                outdict[name] = out
                answerviewed.addname
    else:
        newstate['answer_viewed'] = answerviewed
        uname = context[_n('uname')]
        (context['csm_cslog'].overwrite_log)(
         uname, 
         (context['cs_path_info']), 
         'problemstate', 
         newstate, **context[_n('log_kwargs')])
        duetime = context['csm_time'].detailed_timestampdue
        log_actioncontext{'action':'viewanswer', 
         'names':names, 
         'score':newstate.get'score'0.0, 
         'response':outdict, 
         'due_date':duetime}
        if context.get'cs_ui_config_flags'{}.get'auto_show_explanation_with_answer':
            context[_n('last_log')] = newstate
            return handle_viewexplanation(context, outdict, skip_empty=True)
        return make_return_jsoncontextoutdict


def handle_lock(context):
    names = context[_n('question_names')]
    due = context[_n('due')]
    lastlog = context[_n('last_log')]
    locked = context[_n('locked')]
    newstate = dict(lastlog)
    newstate['timestamp'] = context['cs_timestamp']
    if 'last_submit' not in newstate:
        newstate['last_submit'] = {}
    outdict = {}
    for name in names:
        if name.startswith'__':
            pass
        else:
            q, args = context[_n('name_map')][name]
            outdict[name] = {}
            locked.addname
            if 'lock' in _get_auto_view(args) and q.get'allow_viewanswer'True and _get(args, 'csq_allow_viewanswer', True, bool) and name not in newstate.get'answer_viewed'set():
                c = dict(context)
                c[_n('question_names')] = [name]
                o = json.loadshandle_viewanswer(c)[2]
                ll = context[_n('last_log')]
                newstate['answer_viewed'] = ll.get'answer_viewed'set()
                newstate['explanation_viewed'] = ll.get'explanation_viewed'set()
                outdict[name].updateo[name]
            newstate['locked'] = locked
            uname = context[_n('uname')]
            (context['csm_cslog'].overwrite_log)(
             uname, 
             (context['cs_path_info']), 
             'problemstate', 
             newstate, **context[_n('log_kwargs')])
            duetime = context['csm_time'].detailed_timestampdue
            log_actioncontext{'action':'lock', 
             'names':names, 
             'score':newstate.get'score'0.0, 
             'response':outdict, 
             'due_date':duetime}
            return make_return_jsoncontextoutdict


def handle_grade--- This code section failed: ---

 L. 752         0  LOAD_FAST                'context'
                2  LOAD_GLOBAL              _n
                4  LOAD_STR                 'question_names'
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_SUBSCR    
               10  STORE_FAST               'names'

 L. 753        12  LOAD_FAST                'context'
               14  LOAD_GLOBAL              _n
               16  LOAD_STR                 'perms'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_SUBSCR    
               22  STORE_FAST               'perms'

 L. 755        24  BUILD_LIST_0          0 
               26  STORE_FAST               'newentries'

 L. 756        28  BUILD_MAP_0           0 
               30  STORE_FAST               'outdict'

 L. 757        32  LOAD_FAST                'names'
               34  GET_ITER         
             36_0  COME_FROM            50  '50'
            36_38  FOR_ITER            358  'to 358'
               40  STORE_FAST               'name'

 L. 758        42  LOAD_FAST                'name'
               44  LOAD_METHOD              endswith
               46  LOAD_STR                 '_grading_score'
               48  CALL_METHOD_1         1  ''
               50  POP_JUMP_IF_TRUE     36  'to 36'
               52  LOAD_FAST                'name'
               54  LOAD_METHOD              endswith
               56  LOAD_STR                 '_grading_comments'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L. 759        62  JUMP_BACK            36  'to 36'
             64_0  COME_FROM            60  '60'

 L. 760        64  LOAD_GLOBAL              grade_msg
               66  LOAD_FAST                'context'
               68  LOAD_FAST                'perms'
               70  LOAD_FAST                'name'
               72  CALL_FUNCTION_3       3  ''
               74  STORE_FAST               'error'

 L. 761        76  LOAD_FAST                'error'
               78  LOAD_CONST               None
               80  COMPARE_OP               is-not
               82  POP_JUMP_IF_FALSE    98  'to 98'

 L. 762        84  LOAD_STR                 'error_msg'
               86  LOAD_FAST                'error'
               88  BUILD_MAP_1           1 
               90  LOAD_FAST                'outdict'
               92  LOAD_FAST                'name'
               94  STORE_SUBSCR     

 L. 763        96  JUMP_BACK            36  'to 36'
             98_0  COME_FROM            82  '82'

 L. 764        98  LOAD_FAST                'context'
              100  LOAD_GLOBAL              _n
              102  LOAD_STR                 'name_map'
              104  CALL_FUNCTION_1       1  ''
              106  BINARY_SUBSCR    
              108  LOAD_FAST                'name'
              110  BINARY_SUBSCR    
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               'q'
              116  STORE_FAST               'args'

 L. 765       118  LOAD_GLOBAL              float
              120  LOAD_FAST                'q'
              122  LOAD_STR                 'total_points'
              124  BINARY_SUBSCR    
              126  BUILD_TUPLE_0         0 
              128  LOAD_FAST                'args'
              130  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'npoints'

 L. 766       136  SETUP_FINALLY       194  'to 194'

 L. 767       138  LOAD_FAST                'context'
              140  LOAD_GLOBAL              _n
              142  LOAD_STR                 'form'
              144  CALL_FUNCTION_1       1  ''
              146  BINARY_SUBSCR    
              148  STORE_FAST               'f'

 L. 768       150  LOAD_FAST                'f'
              152  LOAD_METHOD              get
              154  LOAD_STR                 '%s_grading_score'
              156  LOAD_FAST                'name'
              158  BINARY_MODULO    
              160  LOAD_STR                 ''
              162  CALL_METHOD_2         2  ''
              164  STORE_FAST               'rawscore'

 L. 769       166  LOAD_FAST                'f'
              168  LOAD_METHOD              get
              170  LOAD_STR                 '%s_grading_comments'
              172  LOAD_FAST                'name'
              174  BINARY_MODULO    
              176  LOAD_STR                 ''
              178  CALL_METHOD_2         2  ''
              180  STORE_FAST               'comments'

 L. 770       182  LOAD_GLOBAL              float
              184  LOAD_FAST                'rawscore'
              186  CALL_FUNCTION_1       1  ''
              188  STORE_FAST               'score'
              190  POP_BLOCK        
              192  JUMP_FORWARD        230  'to 230'
            194_0  COME_FROM_FINALLY   136  '136'

 L. 771       194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L. 773       200  LOAD_STR                 'error_msg'

 L. 773       202  LOAD_STR                 'Invalid score: %s\n%s'
              204  LOAD_FAST                'rawscore'
              206  LOAD_FAST                'comments'
              208  BUILD_TUPLE_2         2 
              210  BINARY_MODULO    

 L. 772       212  BUILD_MAP_1           1 
              214  LOAD_FAST                'outdict'
              216  LOAD_FAST                'name'
              218  STORE_SUBSCR     

 L. 775       220  POP_EXCEPT       
              222  JUMP_BACK            36  'to 36'
              224  POP_EXCEPT       
              226  JUMP_FORWARD        230  'to 230'
              228  END_FINALLY      
            230_0  COME_FROM           226  '226'
            230_1  COME_FROM           192  '192'

 L. 776       230  LOAD_FAST                'newentries'
              232  LOAD_METHOD              append

 L. 778       234  LOAD_FAST                'name'

 L. 779       236  LOAD_FAST                'context'
              238  LOAD_GLOBAL              _n
              240  LOAD_STR                 'real_uname'
              242  CALL_FUNCTION_1       1  ''
              244  BINARY_SUBSCR    

 L. 780       246  LOAD_FAST                'score'
              248  LOAD_FAST                'npoints'
              250  BINARY_TRUE_DIVIDE

 L. 781       252  LOAD_FAST                'comments'

 L. 782       254  LOAD_FAST                'context'
              256  LOAD_STR                 'cs_timestamp'
              258  BINARY_SUBSCR    

 L. 777       260  LOAD_CONST               ('qname', 'grader', 'score', 'comments', 'timestamp')
              262  BUILD_CONST_KEY_MAP_5     5 

 L. 776       264  CALL_METHOD_1         1  ''
              266  POP_TOP          

 L. 785       268  LOAD_FAST                'context'
              270  LOAD_GLOBAL              _n
              272  LOAD_STR                 'name_map'
              274  CALL_FUNCTION_1       1  ''
              276  BINARY_SUBSCR    
              278  LOAD_FAST                'name'
              280  BINARY_SUBSCR    
              282  UNPACK_SEQUENCE_2     2 
              284  STORE_FAST               '_'
              286  STORE_FAST               'args'

 L. 787       288  LOAD_FAST                'context'
              290  LOAD_STR                 'csm_tutor'
              292  BINARY_SUBSCR    
              294  LOAD_ATTR                make_score_display

 L. 788       296  LOAD_FAST                'context'

 L. 788       298  LOAD_FAST                'args'

 L. 788       300  LOAD_FAST                'name'

 L. 788       302  LOAD_FAST                'score'
              304  LOAD_FAST                'npoints'
              306  BINARY_TRUE_DIVIDE

 L. 788       308  LOAD_FAST                'context'
              310  LOAD_GLOBAL              _n
              312  LOAD_STR                 'last_log'
              314  CALL_FUNCTION_1       1  ''
              316  BINARY_SUBSCR    

 L. 787       318  LOAD_CONST               ('last_log',)
              320  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'

 L. 790       322  LOAD_STR                 "<b>Grader's Comments:</b><br/><br/>%s"

 L. 791       324  LOAD_FAST                'context'
              326  LOAD_STR                 'csm_language'
              328  BINARY_SUBSCR    
              330  LOAD_METHOD              _md_format_string
              332  LOAD_FAST                'context'
              334  LOAD_FAST                'comments'
              336  CALL_METHOD_2         2  ''

 L. 790       338  BINARY_MODULO    

 L. 792       340  LOAD_FAST                'score'
              342  LOAD_FAST                'npoints'
              344  BINARY_TRUE_DIVIDE

 L. 786       346  LOAD_CONST               ('score_display', 'message', 'score')
              348  BUILD_CONST_KEY_MAP_3     3 
              350  LOAD_FAST                'outdict'
              352  LOAD_FAST                'name'
              354  STORE_SUBSCR     
              356  JUMP_BACK            36  'to 36'

 L. 796       358  LOAD_FAST                'context'
              360  LOAD_GLOBAL              _n
              362  LOAD_STR                 'uname'
              364  CALL_FUNCTION_1       1  ''
              366  BINARY_SUBSCR    
              368  STORE_FAST               'uname'

 L. 797       370  LOAD_FAST                'newentries'
              372  GET_ITER         
              374  FOR_ITER            418  'to 418'
              376  STORE_FAST               'i'

 L. 798       378  LOAD_FAST                'context'
              380  LOAD_STR                 'csm_cslog'
              382  BINARY_SUBSCR    
              384  LOAD_ATTR                update_log

 L. 799       386  LOAD_FAST                'uname'

 L. 800       388  LOAD_FAST                'context'
              390  LOAD_STR                 'cs_path_info'
              392  BINARY_SUBSCR    

 L. 801       394  LOAD_STR                 'problemgrades'

 L. 802       396  LOAD_FAST                'i'

 L. 798       398  BUILD_TUPLE_4         4 

 L. 803       400  LOAD_FAST                'context'
              402  LOAD_GLOBAL              _n
              404  LOAD_STR                 'log_kwargs'
              406  CALL_FUNCTION_1       1  ''
              408  BINARY_SUBSCR    

 L. 798       410  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              412  POP_TOP          
          414_416  JUMP_BACK           374  'to 374'

 L. 807       418  LOAD_GLOBAL              log_action

 L. 808       420  LOAD_FAST                'context'

 L. 810       422  LOAD_STR                 'grade'

 L. 811       424  LOAD_FAST                'names'

 L. 812       426  LOAD_FAST                'newentries'

 L. 813       428  LOAD_FAST                'context'
              430  LOAD_GLOBAL              _n
              432  LOAD_STR                 'real_uname'
              434  CALL_FUNCTION_1       1  ''
              436  BINARY_SUBSCR    

 L. 809       438  LOAD_CONST               ('action', 'names', 'scores', 'grader')
              440  BUILD_CONST_KEY_MAP_4     4 

 L. 807       442  CALL_FUNCTION_2       2  ''
              444  POP_TOP          

 L. 817       446  LOAD_GLOBAL              make_return_json
              448  LOAD_FAST                'context'
              450  LOAD_FAST                'outdict'
              452  LOAD_GLOBAL              list
              454  LOAD_FAST                'outdict'
              456  LOAD_METHOD              keys
              458  CALL_METHOD_0         0  ''
              460  CALL_FUNCTION_1       1  ''
              462  LOAD_CONST               ('names',)
              464  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              466  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 224


def handle_unlock(context):
    names = context[_n('question_names')]
    due = context[_n('due')]
    lastlog = context[_n('last_log')]
    locked = context[_n('locked')]
    newstate = dict(lastlog)
    newstate['timestamp'] = context['cs_timestamp']
    if 'last_submit' not in newstate:
        newstate['last_submit'] = {}
    outdict = {}
    for name in names:
        q, args = context[_n('name_map')][name]
        outdict[name] = {}
        locked.removename
    else:
        newstate['locked'] = locked
        uname = context[_n('uname')]
        (context['csm_cslog'].overwrite_log)(
         uname, 
         (context['cs_path_info']), 
         'problemstate', 
         newstate, **context[_n('log_kwargs')])
        duetime = context['csm_time'].detailed_timestampdue
        log_actioncontext{'action':'unlock', 
         'names':names, 
         'score':newstate.get'score'0.0, 
         'response':outdict, 
         'due_date':duetime}
        return make_return_jsoncontextoutdict


def handle_save--- This code section failed: ---

 L. 866         0  LOAD_DEREF               'context'
                2  LOAD_GLOBAL              _n
                4  LOAD_STR                 'question_names'
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_SUBSCR    
               10  STORE_FAST               'names'

 L. 867        12  LOAD_DEREF               'context'
               14  LOAD_GLOBAL              _n
               16  LOAD_STR                 'due'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_SUBSCR    
               22  STORE_FAST               'due'

 L. 869        24  LOAD_DEREF               'context'
               26  LOAD_GLOBAL              _n
               28  LOAD_STR                 'last_log'
               30  CALL_FUNCTION_1       1  ''
               32  BINARY_SUBSCR    
               34  STORE_FAST               'lastlog'

 L. 871        36  LOAD_GLOBAL              dict
               38  LOAD_FAST                'lastlog'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'newstate'

 L. 872        44  LOAD_DEREF               'context'
               46  LOAD_STR                 'cs_timestamp'
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'newstate'
               52  LOAD_STR                 'timestamp'
               54  STORE_SUBSCR     

 L. 873        56  LOAD_STR                 'last_submit'
               58  LOAD_FAST                'newstate'
               60  COMPARE_OP               not-in
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 874        64  BUILD_MAP_0           0 
               66  LOAD_FAST                'newstate'
               68  LOAD_STR                 'last_submit'
               70  STORE_SUBSCR     
             72_0  COME_FROM            62  '62'

 L. 876        72  BUILD_MAP_0           0 
               74  STORE_FAST               'outdict'

 L. 877        76  BUILD_LIST_0          0 
               78  STORE_FAST               'saved_names'

 L. 878        80  LOAD_FAST                'names'
               82  GET_ITER         
            84_86  FOR_ITER            428  'to 428'
               88  STORE_FAST               'name'

 L. 879        90  LOAD_DEREF               'context'
               92  LOAD_GLOBAL              _n
               94  LOAD_STR                 'form'
               96  CALL_FUNCTION_1       1  ''
               98  BINARY_SUBSCR    
              100  LOAD_METHOD              get
              102  LOAD_FAST                'name'
              104  LOAD_STR                 ''
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'sub'

 L. 880       110  BUILD_MAP_0           0 
              112  STORE_FAST               'out'

 L. 881       114  LOAD_FAST                'name'
              116  LOAD_METHOD              startswith
              118  LOAD_STR                 '__'
              120  CALL_METHOD_1         1  ''
              122  POP_JUMP_IF_FALSE   138  'to 138'

 L. 882       124  LOAD_FAST                'sub'
              126  LOAD_FAST                'newstate'
              128  LOAD_STR                 'last_submit'
              130  BINARY_SUBSCR    
              132  LOAD_FAST                'name'
              134  STORE_SUBSCR     

 L. 883       136  JUMP_BACK            84  'to 84'
            138_0  COME_FROM           122  '122'

 L. 885       138  LOAD_GLOBAL              save_msg
              140  LOAD_DEREF               'context'
              142  LOAD_DEREF               'context'
              144  LOAD_GLOBAL              _n
              146  LOAD_STR                 'perms'
              148  CALL_FUNCTION_1       1  ''
              150  BINARY_SUBSCR    
              152  LOAD_FAST                'name'
              154  CALL_FUNCTION_3       3  ''
              156  STORE_FAST               'error'

 L. 886       158  LOAD_FAST                'error'
              160  LOAD_CONST               None
              162  COMPARE_OP               is-not
              164  POP_JUMP_IF_FALSE   184  'to 184'

 L. 887       166  LOAD_FAST                'error'
              168  LOAD_FAST                'out'
              170  LOAD_STR                 'error_msg'
              172  STORE_SUBSCR     

 L. 888       174  LOAD_FAST                'out'
              176  LOAD_FAST                'outdict'
              178  LOAD_FAST                'name'
              180  STORE_SUBSCR     

 L. 889       182  JUMP_BACK            84  'to 84'
            184_0  COME_FROM           164  '164'

 L. 891       184  LOAD_DEREF               'context'
              186  LOAD_GLOBAL              _n
              188  LOAD_STR                 'name_map'
              190  CALL_FUNCTION_1       1  ''
              192  BINARY_SUBSCR    
              194  LOAD_METHOD              get
              196  LOAD_FAST                'name'
              198  CALL_METHOD_1         1  ''
              200  UNPACK_SEQUENCE_2     2 
              202  STORE_FAST               'question'
              204  STORE_FAST               'args'

 L. 893       206  LOAD_FAST                'saved_names'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'name'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 896       216  LOAD_FAST                'sub'
              218  LOAD_FAST                'newstate'
              220  LOAD_STR                 'last_submit'
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'name'
              226  STORE_SUBSCR     

 L. 898       228  LOAD_FAST                'args'
              230  LOAD_METHOD              get
              232  LOAD_STR                 'csq_rerender'
              234  LOAD_FAST                'question'
              236  LOAD_METHOD              get
              238  LOAD_STR                 'always_rerender'
              240  LOAD_CONST               False
              242  CALL_METHOD_2         2  ''
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'rerender'

 L. 899       248  LOAD_FAST                'rerender'
              250  LOAD_CONST               True
              252  COMPARE_OP               is
          254_256  POP_JUMP_IF_FALSE   320  'to 320'

 L. 900       258  LOAD_DEREF               'context'
              260  LOAD_STR                 'csm_language'
              262  BINARY_SUBSCR    
              264  LOAD_METHOD              source_transform_string

 L. 901       266  LOAD_DEREF               'context'

 L. 901       268  LOAD_FAST                'args'
              270  LOAD_METHOD              get
              272  LOAD_STR                 'csq_prompt'
              274  LOAD_STR                 ''
              276  CALL_METHOD_2         2  ''

 L. 900       278  CALL_METHOD_2         2  ''
              280  LOAD_FAST                'out'
              282  LOAD_STR                 'rerender'
              284  STORE_SUBSCR     

 L. 903       286  LOAD_FAST                'out'
              288  LOAD_STR                 'rerender'
              290  DUP_TOP_TWO      
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'question'
              296  LOAD_STR                 'render_html'
              298  BINARY_SUBSCR    
              300  LOAD_FAST                'newstate'
              302  LOAD_STR                 'last_submit'
              304  BINARY_SUBSCR    
              306  BUILD_TUPLE_1         1 
              308  LOAD_FAST                'args'
              310  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              312  INPLACE_ADD      
              314  ROT_THREE        
              316  STORE_SUBSCR     
              318  JUMP_FORWARD        334  'to 334'
            320_0  COME_FROM           254  '254'

 L. 904       320  LOAD_FAST                'rerender'
          322_324  POP_JUMP_IF_FALSE   334  'to 334'

 L. 905       326  LOAD_FAST                'rerender'
              328  LOAD_FAST                'out'
              330  LOAD_STR                 'rerender'
              332  STORE_SUBSCR     
            334_0  COME_FROM           322  '322'
            334_1  COME_FROM           318  '318'

 L. 907       334  LOAD_STR                 ''
              336  LOAD_FAST                'out'
              338  LOAD_STR                 'score_display'
              340  STORE_SUBSCR     

 L. 908       342  LOAD_STR                 ''
              344  LOAD_FAST                'out'
              346  LOAD_STR                 'message'
              348  STORE_SUBSCR     

 L. 909       350  LOAD_FAST                'out'
              352  LOAD_FAST                'outdict'
              354  LOAD_FAST                'name'
              356  STORE_SUBSCR     

 L. 912       358  LOAD_STR                 'score_displays'
              360  LOAD_FAST                'newstate'
              362  COMPARE_OP               not-in
          364_366  POP_JUMP_IF_FALSE   376  'to 376'

 L. 913       368  BUILD_MAP_0           0 
              370  LOAD_FAST                'newstate'
              372  LOAD_STR                 'score_displays'
              374  STORE_SUBSCR     
            376_0  COME_FROM           364  '364'

 L. 914       376  LOAD_STR                 'cached_responses'
              378  LOAD_FAST                'newstate'
              380  COMPARE_OP               not-in
          382_384  POP_JUMP_IF_FALSE   394  'to 394'

 L. 915       386  BUILD_MAP_0           0 
              388  LOAD_FAST                'newstate'
              390  LOAD_STR                 'cached_responses'
              392  STORE_SUBSCR     
            394_0  COME_FROM           382  '382'

 L. 916       394  LOAD_FAST                'out'
              396  LOAD_STR                 'score_display'
              398  BINARY_SUBSCR    
              400  LOAD_FAST                'newstate'
              402  LOAD_STR                 'score_displays'
              404  BINARY_SUBSCR    
              406  LOAD_FAST                'name'
              408  STORE_SUBSCR     

 L. 917       410  LOAD_FAST                'out'
              412  LOAD_STR                 'message'
              414  BINARY_SUBSCR    
              416  LOAD_FAST                'newstate'
              418  LOAD_STR                 'cached_responses'
              420  BINARY_SUBSCR    
              422  LOAD_FAST                'name'
              424  STORE_SUBSCR     
              426  JUMP_BACK            84  'to 84'

 L. 920       428  LOAD_GLOBAL              len
              430  LOAD_FAST                'saved_names'
              432  CALL_FUNCTION_1       1  ''
              434  LOAD_CONST               0
              436  COMPARE_OP               >
          438_440  POP_JUMP_IF_FALSE   554  'to 554'

 L. 921       442  LOAD_DEREF               'context'
              444  LOAD_GLOBAL              _n
              446  LOAD_STR                 'uname'
              448  CALL_FUNCTION_1       1  ''
              450  BINARY_SUBSCR    
              452  STORE_FAST               'uname'

 L. 922       454  LOAD_DEREF               'context'
              456  LOAD_STR                 'csm_cslog'
              458  BINARY_SUBSCR    
              460  LOAD_ATTR                overwrite_log

 L. 923       462  LOAD_FAST                'uname'

 L. 924       464  LOAD_DEREF               'context'
              466  LOAD_STR                 'cs_path_info'
              468  BINARY_SUBSCR    

 L. 925       470  LOAD_STR                 'problemstate'

 L. 926       472  LOAD_FAST                'newstate'

 L. 922       474  BUILD_TUPLE_4         4 

 L. 927       476  LOAD_DEREF               'context'
              478  LOAD_GLOBAL              _n
              480  LOAD_STR                 'log_kwargs'
              482  CALL_FUNCTION_1       1  ''
              484  BINARY_SUBSCR    

 L. 922       486  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              488  POP_TOP          

 L. 931       490  LOAD_DEREF               'context'
              492  LOAD_STR                 'csm_time'
              494  BINARY_SUBSCR    
              496  LOAD_METHOD              detailed_timestamp
              498  LOAD_FAST                'due'
              500  CALL_METHOD_1         1  ''
              502  STORE_FAST               'duetime'

 L. 932       504  LOAD_CLOSURE             'context'
              506  BUILD_TUPLE_1         1 
              508  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              510  LOAD_STR                 'handle_save.<locals>.<dictcomp>'
              512  MAKE_FUNCTION_8          'closure'
              514  LOAD_FAST                'saved_names'
              516  GET_ITER         
              518  CALL_FUNCTION_1       1  ''
              520  STORE_FAST               'subbed'

 L. 933       522  LOAD_GLOBAL              log_action

 L. 934       524  LOAD_DEREF               'context'

 L. 936       526  LOAD_STR                 'save'

 L. 937       528  LOAD_FAST                'saved_names'

 L. 938       530  LOAD_FAST                'subbed'

 L. 939       532  LOAD_FAST                'newstate'
              534  LOAD_METHOD              get
              536  LOAD_STR                 'score'
              538  LOAD_CONST               0.0
              540  CALL_METHOD_2         2  ''

 L. 940       542  LOAD_FAST                'outdict'

 L. 941       544  LOAD_FAST                'duetime'

 L. 935       546  LOAD_CONST               ('action', 'names', 'submitted', 'score', 'response', 'due_date')
              548  BUILD_CONST_KEY_MAP_6     6 

 L. 933       550  CALL_FUNCTION_2       2  ''
              552  POP_TOP          
            554_0  COME_FROM           438  '438'

 L. 945       554  LOAD_GLOBAL              make_return_json
              556  LOAD_DEREF               'context'
              558  LOAD_FAST                'outdict'
              560  CALL_FUNCTION_2       2  ''
              562  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 508


def handle_check--- This code section failed: ---

 L. 949         0  LOAD_DEREF               'context'
                2  LOAD_GLOBAL              _n
                4  LOAD_STR                 'question_names'
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_SUBSCR    
               10  STORE_FAST               'names'

 L. 950        12  LOAD_DEREF               'context'
               14  LOAD_GLOBAL              _n
               16  LOAD_STR                 'due'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_SUBSCR    
               22  STORE_FAST               'due'

 L. 952        24  LOAD_DEREF               'context'
               26  LOAD_GLOBAL              _n
               28  LOAD_STR                 'last_log'
               30  CALL_FUNCTION_1       1  ''
               32  BINARY_SUBSCR    
               34  STORE_FAST               'lastlog'

 L. 953        36  LOAD_DEREF               'context'
               38  LOAD_GLOBAL              _n
               40  LOAD_STR                 'name_map'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_SUBSCR    
               46  STORE_FAST               'namemap'

 L. 955        48  LOAD_GLOBAL              dict
               50  LOAD_FAST                'lastlog'
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'newstate'

 L. 956        56  LOAD_DEREF               'context'
               58  LOAD_STR                 'cs_timestamp'
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'newstate'
               64  LOAD_STR                 'timestamp'
               66  STORE_SUBSCR     

 L. 957        68  LOAD_STR                 'last_submit'
               70  LOAD_FAST                'newstate'
               72  COMPARE_OP               not-in
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L. 958        76  BUILD_MAP_0           0 
               78  LOAD_FAST                'newstate'
               80  LOAD_STR                 'last_submit'
               82  STORE_SUBSCR     
             84_0  COME_FROM            74  '74'

 L. 960        84  LOAD_GLOBAL              set
               86  CALL_FUNCTION_0       0  ''
               88  STORE_FAST               'names_done'

 L. 961        90  BUILD_MAP_0           0 
               92  STORE_FAST               'outdict'

 L. 963        94  BUILD_MAP_0           0 
               96  STORE_FAST               'entry_ids'

 L. 964        98  LOAD_STR                 'checker_ids'
              100  LOAD_FAST                'newstate'
              102  COMPARE_OP               not-in
              104  POP_JUMP_IF_FALSE   114  'to 114'

 L. 965       106  BUILD_MAP_0           0 
              108  LOAD_FAST                'newstate'
              110  LOAD_STR                 'checker_ids'
              112  STORE_SUBSCR     
            114_0  COME_FROM           104  '104'

 L. 966       114  LOAD_STR                 'last_submit'
              116  LOAD_FAST                'newstate'
              118  COMPARE_OP               not-in
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 967       122  BUILD_MAP_0           0 
              124  LOAD_FAST                'newstate'
              126  LOAD_STR                 'last_submit'
              128  STORE_SUBSCR     
            130_0  COME_FROM           120  '120'

 L. 968       130  LOAD_STR                 'last_submit_id'
              132  LOAD_FAST                'newstate'
              134  COMPARE_OP               not-in
              136  POP_JUMP_IF_FALSE   146  'to 146'

 L. 969       138  BUILD_MAP_0           0 
              140  LOAD_FAST                'newstate'
              142  LOAD_STR                 'last_submit_id'
              144  STORE_SUBSCR     
            146_0  COME_FROM           136  '136'

 L. 970       146  LOAD_STR                 'cached_responses'
              148  LOAD_FAST                'newstate'
              150  COMPARE_OP               not-in
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 971       154  BUILD_MAP_0           0 
              156  LOAD_FAST                'newstate'
              158  LOAD_STR                 'cached_responses'
              160  STORE_SUBSCR     
            162_0  COME_FROM           152  '152'

 L. 972       162  LOAD_STR                 'extra_data'
              164  LOAD_FAST                'newstate'
              166  COMPARE_OP               not-in
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L. 973       170  BUILD_MAP_0           0 
              172  LOAD_FAST                'newstate'
              174  LOAD_STR                 'extra_data'
              176  STORE_SUBSCR     
            178_0  COME_FROM           168  '168'

 L. 974       178  LOAD_STR                 'score_displays'
              180  LOAD_FAST                'newstate'
              182  COMPARE_OP               not-in
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 975       186  BUILD_MAP_0           0 
              188  LOAD_FAST                'newstate'
              190  LOAD_STR                 'score_displays'
              192  STORE_SUBSCR     
            194_0  COME_FROM           184  '184'

 L. 977       194  LOAD_FAST                'names'
              196  GET_ITER         
          198_200  FOR_ITER            730  'to 730'
              202  STORE_FAST               'name'

 L. 978       204  LOAD_FAST                'name'
              206  LOAD_METHOD              startswith
              208  LOAD_STR                 '__'
              210  CALL_METHOD_1         1  ''
              212  POP_JUMP_IF_FALSE   238  'to 238'

 L. 979       214  LOAD_FAST                'name'
              216  LOAD_CONST               2
              218  LOAD_CONST               None
              220  BUILD_SLICE_2         2 
              222  BINARY_SUBSCR    
              224  LOAD_METHOD              rsplit
              226  LOAD_STR                 '_'
              228  LOAD_CONST               1
              230  CALL_METHOD_2         2  ''
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    
              236  STORE_FAST               'name'
            238_0  COME_FROM           212  '212'

 L. 980       238  LOAD_FAST                'name'
              240  LOAD_FAST                'names_done'
              242  COMPARE_OP               in
              244  POP_JUMP_IF_FALSE   248  'to 248'

 L. 981       246  JUMP_BACK           198  'to 198'
            248_0  COME_FROM           244  '244'

 L. 982       248  BUILD_MAP_0           0 
              250  STORE_FAST               'out'

 L. 983       252  LOAD_DEREF               'context'
              254  LOAD_GLOBAL              _n
              256  LOAD_STR                 'form'
              258  CALL_FUNCTION_1       1  ''
              260  BINARY_SUBSCR    
              262  LOAD_METHOD              get
              264  LOAD_FAST                'name'
              266  LOAD_STR                 ''
              268  CALL_METHOD_2         2  ''
              270  STORE_FAST               'sub'

 L. 984       272  LOAD_GLOBAL              check_msg
              274  LOAD_DEREF               'context'
              276  LOAD_DEREF               'context'
              278  LOAD_GLOBAL              _n
              280  LOAD_STR                 'perms'
              282  CALL_FUNCTION_1       1  ''
              284  BINARY_SUBSCR    
              286  LOAD_FAST                'name'
              288  CALL_FUNCTION_3       3  ''
              290  STORE_FAST               'error'

 L. 985       292  LOAD_FAST                'error'
              294  LOAD_CONST               None
              296  COMPARE_OP               is-not
          298_300  POP_JUMP_IF_FALSE   324  'to 324'

 L. 986       302  LOAD_FAST                'error'
              304  LOAD_FAST                'out'
              306  LOAD_STR                 'error_msg'
              308  STORE_SUBSCR     

 L. 987       310  LOAD_FAST                'out'
              312  LOAD_FAST                'outdict'
              314  LOAD_FAST                'name'
              316  STORE_SUBSCR     

 L. 988       318  LOAD_CONST               False
              320  STORE_FAST               'submit_succeeded'

 L. 989       322  JUMP_BACK           198  'to 198'
            324_0  COME_FROM           298  '298'

 L. 992       324  LOAD_FAST                'sub'
              326  LOAD_FAST                'newstate'
              328  LOAD_STR                 'last_submit'
              330  BINARY_SUBSCR    
              332  LOAD_FAST                'name'
              334  STORE_SUBSCR     

 L. 993       336  LOAD_FAST                'namemap'
              338  LOAD_FAST                'name'
              340  BINARY_SUBSCR    
              342  UNPACK_SEQUENCE_2     2 
              344  STORE_FAST               'question'
              346  STORE_FAST               'args'

 L. 995       348  LOAD_GLOBAL              _get
              350  LOAD_FAST                'args'
              352  LOAD_STR                 'csq_grading_mode'
              354  LOAD_STR                 'auto'
              356  LOAD_GLOBAL              str
              358  CALL_FUNCTION_4       4  ''
              360  STORE_FAST               'grading_mode'

 L. 996       362  LOAD_FAST                'grading_mode'
              364  LOAD_STR                 'legacy'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   508  'to 508'

 L. 997       372  SETUP_FINALLY       402  'to 402'

 L. 998       374  LOAD_FAST                'question'
              376  LOAD_STR                 'handle_check'
              378  BINARY_SUBSCR    
              380  LOAD_DEREF               'context'
              382  LOAD_GLOBAL              _n
              384  LOAD_STR                 'form'
              386  CALL_FUNCTION_1       1  ''
              388  BINARY_SUBSCR    
              390  BUILD_TUPLE_1         1 
              392  LOAD_FAST                'args'
              394  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              396  STORE_FAST               'msg'
              398  POP_BLOCK        
              400  JUMP_FORWARD        422  'to 422'
            402_0  COME_FROM_FINALLY   372  '372'

 L. 999       402  POP_TOP          
              404  POP_TOP          
              406  POP_TOP          

 L.1000       408  LOAD_GLOBAL              exc_message
              410  LOAD_DEREF               'context'
              412  CALL_FUNCTION_1       1  ''
              414  STORE_FAST               'msg'
              416  POP_EXCEPT       
              418  JUMP_FORWARD        422  'to 422'
              420  END_FINALLY      
            422_0  COME_FROM           418  '418'
            422_1  COME_FROM           400  '400'

 L.1001       422  LOAD_STR                 ''
              424  LOAD_FAST                'out'
              426  LOAD_STR                 'score_display'
              428  STORE_SUBSCR     

 L.1002       430  LOAD_DEREF               'context'
              432  LOAD_STR                 'csm_language'
              434  BINARY_SUBSCR    
              436  LOAD_METHOD              handle_custom_tags
              438  LOAD_DEREF               'context'
              440  LOAD_FAST                'msg'
              442  CALL_METHOD_2         2  ''
              444  LOAD_FAST                'out'
              446  LOAD_STR                 'message'
              448  STORE_SUBSCR     

 L.1003       450  LOAD_FAST                'name'
              452  LOAD_FAST                'newstate'
              454  LOAD_METHOD              get
              456  LOAD_STR                 'checker_ids'
              458  BUILD_MAP_0           0 
              460  CALL_METHOD_2         2  ''
              462  COMPARE_OP               in
          464_466  POP_JUMP_IF_FALSE   478  'to 478'

 L.1004       468  LOAD_FAST                'newstate'
              470  LOAD_STR                 'checker_ids'
              472  BINARY_SUBSCR    
              474  LOAD_FAST                'name'
              476  DELETE_SUBSCR    
            478_0  COME_FROM           464  '464'

 L.1006       478  LOAD_FAST                'out'
              480  LOAD_STR                 'message'
              482  BINARY_SUBSCR    
              484  LOAD_FAST                'newstate'
              486  LOAD_STR                 'cached_responses'
              488  BINARY_SUBSCR    
              490  LOAD_FAST                'name'
              492  STORE_SUBSCR     

 L.1007       494  LOAD_STR                 ''
              496  LOAD_FAST                'newstate'
              498  LOAD_STR                 'score_displays'
              500  BINARY_SUBSCR    
              502  LOAD_FAST                'name'
              504  STORE_SUBSCR     
              506  JUMP_FORWARD        720  'to 720'
            508_0  COME_FROM           368  '368'

 L.1009       508  LOAD_GLOBAL              new_entry
              510  LOAD_DEREF               'context'
              512  LOAD_FAST                'name'
              514  LOAD_STR                 'check'
              516  CALL_FUNCTION_3       3  ''
              518  STORE_FAST               'magic'

 L.1011       520  LOAD_FAST                'magic'
              522  DUP_TOP          
              524  LOAD_FAST                'entry_ids'
              526  LOAD_FAST                'name'
              528  STORE_SUBSCR     
              530  STORE_FAST               'entry_id'

 L.1013       532  LOAD_FAST                'args'
              534  LOAD_METHOD              get
              536  LOAD_STR                 'csq_rerender'
              538  LOAD_FAST                'question'
              540  LOAD_METHOD              get
              542  LOAD_STR                 'always_rerender'
              544  LOAD_CONST               False
              546  CALL_METHOD_2         2  ''
              548  CALL_METHOD_2         2  ''
              550  STORE_FAST               'rerender'

 L.1014       552  LOAD_FAST                'rerender'
              554  LOAD_CONST               True
              556  COMPARE_OP               is
          558_560  POP_JUMP_IF_FALSE   588  'to 588'

 L.1015       562  LOAD_FAST                'question'
              564  LOAD_STR                 'render_html'
              566  BINARY_SUBSCR    

 L.1016       568  LOAD_FAST                'newstate'
              570  LOAD_STR                 'last_submit'
              572  BINARY_SUBSCR    

 L.1015       574  BUILD_TUPLE_1         1 

 L.1016       576  LOAD_FAST                'args'

 L.1015       578  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              580  LOAD_FAST                'out'
              582  LOAD_STR                 'rerender'
              584  STORE_SUBSCR     
              586  JUMP_FORWARD        602  'to 602'
            588_0  COME_FROM           558  '558'

 L.1018       588  LOAD_FAST                'rerender'
          590_592  POP_JUMP_IF_FALSE   602  'to 602'

 L.1019       594  LOAD_FAST                'rerender'
              596  LOAD_FAST                'out'
              598  LOAD_STR                 'rerender'
              600  STORE_SUBSCR     
            602_0  COME_FROM           590  '590'
            602_1  COME_FROM           586  '586'

 L.1021       602  LOAD_STR                 ''
              604  LOAD_FAST                'out'
              606  LOAD_STR                 'score_display'
              608  STORE_SUBSCR     

 L.1022       610  LOAD_GLOBAL              WEBSOCKET_RESPONSE

 L.1023       612  LOAD_FAST                'name'

 L.1024       614  LOAD_FAST                'entry_id'

 L.1025       616  LOAD_DEREF               'context'
              618  LOAD_STR                 'cs_checker_websocket'
              620  BINARY_SUBSCR    

 L.1026       622  LOAD_DEREF               'context'
              624  LOAD_STR                 'cs_loading_image'
              626  BINARY_SUBSCR    

 L.1029       628  LOAD_DEREF               'context'
              630  LOAD_METHOD              get
              632  LOAD_STR                 'cs_show_submission_id'
              634  LOAD_CONST               True
              636  CALL_METHOD_2         2  ''

 L.1028   638_640  POP_JUMP_IF_FALSE   646  'to 646'
              642  LOAD_STR                 ' style="display:none;"'
              644  JUMP_FORWARD        648  'to 648'
            646_0  COME_FROM           638  '638'

 L.1030       646  LOAD_STR                 ''
            648_0  COME_FROM           644  '644'

 L.1022       648  LOAD_CONST               ('name', 'magic', 'websocket', 'loading', 'id_css')
              650  BUILD_CONST_KEY_MAP_5     5 
              652  BINARY_MODULO    
              654  LOAD_FAST                'out'
              656  LOAD_STR                 'message'
              658  STORE_SUBSCR     

 L.1033       660  LOAD_FAST                'entry_id'
              662  LOAD_FAST                'out'
              664  LOAD_STR                 'magic'
              666  STORE_SUBSCR     

 L.1035       668  LOAD_FAST                'entry_id'
              670  LOAD_FAST                'newstate'
              672  LOAD_STR                 'checker_ids'
              674  BINARY_SUBSCR    
              676  LOAD_FAST                'name'
              678  STORE_SUBSCR     

 L.1036       680  LOAD_STR                 ''
              682  LOAD_FAST                'newstate'
              684  LOAD_STR                 'score_displays'
              686  BINARY_SUBSCR    
              688  LOAD_FAST                'name'
              690  STORE_SUBSCR     

 L.1037       692  LOAD_FAST                'name'
              694  LOAD_FAST                'newstate'
              696  LOAD_METHOD              get
              698  LOAD_STR                 'cached_responses'
              700  BUILD_MAP_0           0 
              702  CALL_METHOD_2         2  ''
              704  COMPARE_OP               in
          706_708  POP_JUMP_IF_FALSE   720  'to 720'

 L.1038       710  LOAD_FAST                'newstate'
              712  LOAD_STR                 'cached_responses'
              714  BINARY_SUBSCR    
              716  LOAD_FAST                'name'
              718  DELETE_SUBSCR    
            720_0  COME_FROM           706  '706'
            720_1  COME_FROM           506  '506'

 L.1040       720  LOAD_FAST                'out'
              722  LOAD_FAST                'outdict'
              724  LOAD_FAST                'name'
              726  STORE_SUBSCR     
              728  JUMP_BACK           198  'to 198'

 L.1043       730  LOAD_DEREF               'context'
              732  LOAD_GLOBAL              _n
              734  LOAD_STR                 'uname'
              736  CALL_FUNCTION_1       1  ''
              738  BINARY_SUBSCR    
              740  STORE_FAST               'uname'

 L.1044       742  LOAD_DEREF               'context'
              744  LOAD_STR                 'csm_cslog'
              746  BINARY_SUBSCR    
              748  LOAD_ATTR                overwrite_log

 L.1045       750  LOAD_FAST                'uname'

 L.1046       752  LOAD_DEREF               'context'
              754  LOAD_STR                 'cs_path_info'
              756  BINARY_SUBSCR    

 L.1047       758  LOAD_STR                 'problemstate'

 L.1048       760  LOAD_FAST                'newstate'

 L.1044       762  BUILD_TUPLE_4         4 

 L.1049       764  LOAD_DEREF               'context'
              766  LOAD_GLOBAL              _n
              768  LOAD_STR                 'log_kwargs'
              770  CALL_FUNCTION_1       1  ''
              772  BINARY_SUBSCR    

 L.1044       774  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              776  POP_TOP          

 L.1053       778  LOAD_DEREF               'context'
              780  LOAD_STR                 'csm_time'
              782  BINARY_SUBSCR    
              784  LOAD_METHOD              detailed_timestamp
              786  LOAD_FAST                'due'
              788  CALL_METHOD_1         1  ''
              790  STORE_FAST               'duetime'

 L.1054       792  LOAD_CLOSURE             'context'
              794  BUILD_TUPLE_1         1 
              796  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              798  LOAD_STR                 'handle_check.<locals>.<dictcomp>'
              800  MAKE_FUNCTION_8          'closure'
              802  LOAD_FAST                'names'
              804  GET_ITER         
              806  CALL_FUNCTION_1       1  ''
              808  STORE_FAST               'subbed'

 L.1055       810  LOAD_GLOBAL              log_action

 L.1056       812  LOAD_DEREF               'context'

 L.1058       814  LOAD_STR                 'check'

 L.1059       816  LOAD_FAST                'names'

 L.1060       818  LOAD_FAST                'subbed'

 L.1061       820  LOAD_FAST                'entry_ids'

 L.1062       822  LOAD_FAST                'duetime'

 L.1057       824  LOAD_CONST               ('action', 'names', 'submitted', 'checker_ids', 'due_date')
              826  BUILD_CONST_KEY_MAP_5     5 

 L.1055       828  CALL_FUNCTION_2       2  ''
              830  POP_TOP          

 L.1066       832  LOAD_GLOBAL              make_return_json
              834  LOAD_DEREF               'context'
              836  LOAD_FAST                'outdict'
              838  CALL_FUNCTION_2       2  ''
              840  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 796


def handle_submit--- This code section failed: ---

 L.1070         0  LOAD_DEREF               'context'
                2  LOAD_GLOBAL              _n
                4  LOAD_STR                 'question_names'
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_SUBSCR    
               10  STORE_FAST               'names'

 L.1071        12  LOAD_DEREF               'context'
               14  LOAD_GLOBAL              _n
               16  LOAD_STR                 'due'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_SUBSCR    
               22  STORE_FAST               'due'

 L.1072        24  LOAD_DEREF               'context'
               26  LOAD_GLOBAL              _n
               28  LOAD_STR                 'uname'
               30  CALL_FUNCTION_1       1  ''
               32  BINARY_SUBSCR    
               34  STORE_FAST               'uname'

 L.1074        36  LOAD_DEREF               'context'
               38  LOAD_GLOBAL              _n
               40  LOAD_STR                 'last_log'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_SUBSCR    
               46  STORE_FAST               'lastlog'

 L.1076        48  LOAD_DEREF               'context'
               50  LOAD_GLOBAL              _n
               52  LOAD_STR                 'nsubmits_used'
               54  CALL_FUNCTION_1       1  ''
               56  BINARY_SUBSCR    
               58  STORE_FAST               'nsubmits_used'

 L.1078        60  LOAD_DEREF               'context'
               62  LOAD_GLOBAL              _n
               64  LOAD_STR                 'name_map'
               66  CALL_FUNCTION_1       1  ''
               68  BINARY_SUBSCR    
               70  STORE_FAST               'namemap'

 L.1080        72  LOAD_GLOBAL              dict
               74  LOAD_FAST                'lastlog'
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'newstate'

 L.1082        80  LOAD_FAST                'newstate'
               82  LOAD_METHOD              get
               84  LOAD_STR                 'last_submit_times'
               86  BUILD_MAP_0           0 
               88  CALL_METHOD_2         2  ''
               90  LOAD_FAST                'newstate'
               92  LOAD_STR                 'last_submit_times'
               94  STORE_SUBSCR     

 L.1083        96  LOAD_DEREF               'context'
               98  LOAD_STR                 'cs_timestamp'
              100  BINARY_SUBSCR    
              102  LOAD_FAST                'newstate'
              104  LOAD_STR                 'timestamp'
              106  STORE_SUBSCR     

 L.1084       108  LOAD_STR                 'last_submit'
              110  LOAD_FAST                'newstate'
              112  COMPARE_OP               not-in
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.1085       116  BUILD_MAP_0           0 
              118  LOAD_FAST                'newstate'
              120  LOAD_STR                 'last_submit'
              122  STORE_SUBSCR     
            124_0  COME_FROM           114  '114'

 L.1086       124  LOAD_STR                 'last_submit_id'
              126  LOAD_FAST                'newstate'
              128  COMPARE_OP               not-in
              130  POP_JUMP_IF_FALSE   140  'to 140'

 L.1087       132  BUILD_MAP_0           0 
              134  LOAD_FAST                'newstate'
              136  LOAD_STR                 'last_submit_id'
              138  STORE_SUBSCR     
            140_0  COME_FROM           130  '130'

 L.1088       140  LOAD_STR                 'cached_responses'
              142  LOAD_FAST                'newstate'
              144  COMPARE_OP               not-in
              146  POP_JUMP_IF_FALSE   156  'to 156'

 L.1089       148  BUILD_MAP_0           0 
              150  LOAD_FAST                'newstate'
              152  LOAD_STR                 'cached_responses'
              154  STORE_SUBSCR     
            156_0  COME_FROM           146  '146'

 L.1090       156  LOAD_STR                 'checker_ids'
              158  LOAD_FAST                'newstate'
              160  COMPARE_OP               not-in
              162  POP_JUMP_IF_FALSE   172  'to 172'

 L.1091       164  BUILD_MAP_0           0 
              166  LOAD_FAST                'newstate'
              168  LOAD_STR                 'checker_ids'
              170  STORE_SUBSCR     
            172_0  COME_FROM           162  '162'

 L.1092       172  LOAD_STR                 'extra_data'
              174  LOAD_FAST                'newstate'
              176  COMPARE_OP               not-in
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L.1093       180  BUILD_MAP_0           0 
              182  LOAD_FAST                'newstate'
              184  LOAD_STR                 'extra_data'
              186  STORE_SUBSCR     
            188_0  COME_FROM           178  '178'

 L.1094       188  LOAD_STR                 'score_displays'
              190  LOAD_FAST                'newstate'
              192  COMPARE_OP               not-in
              194  POP_JUMP_IF_FALSE   204  'to 204'

 L.1095       196  BUILD_MAP_0           0 
              198  LOAD_FAST                'newstate'
              200  LOAD_STR                 'score_displays'
              202  STORE_SUBSCR     
            204_0  COME_FROM           194  '194'

 L.1097       204  LOAD_GLOBAL              set
              206  CALL_FUNCTION_0       0  ''
              208  STORE_FAST               'names_done'

 L.1098       210  BUILD_MAP_0           0 
              212  STORE_FAST               'outdict'

 L.1103       214  BUILD_MAP_0           0 
              216  STORE_FAST               'entry_ids'

 L.1104       218  LOAD_CONST               True
              220  STORE_FAST               'submit_succeeded'

 L.1105       222  BUILD_MAP_0           0 
              224  STORE_FAST               'scores'

 L.1106       226  BUILD_MAP_0           0 
              228  STORE_FAST               'messages'

 L.1107       230  LOAD_FAST                'names'
              232  GET_ITER         
          234_236  FOR_ITER           1492  'to 1492'
              238  STORE_FAST               'name'

 L.1108       240  LOAD_DEREF               'context'
              242  LOAD_GLOBAL              _n
              244  LOAD_STR                 'form'
              246  CALL_FUNCTION_1       1  ''
              248  BINARY_SUBSCR    
              250  LOAD_METHOD              get
              252  LOAD_FAST                'name'
              254  LOAD_STR                 ''
              256  CALL_METHOD_2         2  ''
              258  STORE_FAST               'sub'

 L.1109       260  LOAD_FAST                'name'
              262  LOAD_METHOD              startswith
              264  LOAD_STR                 '__'
              266  CALL_METHOD_1         1  ''
          268_270  POP_JUMP_IF_FALSE   308  'to 308'

 L.1110       272  LOAD_FAST                'sub'
              274  LOAD_FAST                'newstate'
              276  LOAD_STR                 'last_submit'
              278  BINARY_SUBSCR    
              280  LOAD_FAST                'name'
              282  STORE_SUBSCR     

 L.1111       284  LOAD_FAST                'name'
              286  LOAD_CONST               2
              288  LOAD_CONST               None
              290  BUILD_SLICE_2         2 
              292  BINARY_SUBSCR    
              294  LOAD_METHOD              rsplit
              296  LOAD_STR                 '_'
              298  LOAD_CONST               1
              300  CALL_METHOD_2         2  ''
              302  LOAD_CONST               0
              304  BINARY_SUBSCR    
              306  STORE_FAST               'name'
            308_0  COME_FROM           268  '268'

 L.1112       308  LOAD_FAST                'name'
              310  LOAD_FAST                'names_done'
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE   320  'to 320'

 L.1113       318  JUMP_BACK           234  'to 234'
            320_0  COME_FROM           314  '314'

 L.1115       320  LOAD_FAST                'names_done'
              322  LOAD_METHOD              add
              324  LOAD_FAST                'name'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          

 L.1116       330  BUILD_MAP_0           0 
              332  STORE_FAST               'out'

 L.1118       334  LOAD_GLOBAL              submit_msg
              336  LOAD_DEREF               'context'
              338  LOAD_DEREF               'context'
              340  LOAD_GLOBAL              _n
              342  LOAD_STR                 'perms'
              344  CALL_FUNCTION_1       1  ''
              346  BINARY_SUBSCR    
              348  LOAD_FAST                'name'
              350  CALL_FUNCTION_3       3  ''
              352  STORE_FAST               'error'

 L.1119       354  LOAD_FAST                'error'
              356  LOAD_CONST               None
              358  COMPARE_OP               is-not
          360_362  POP_JUMP_IF_FALSE   386  'to 386'

 L.1120       364  LOAD_FAST                'error'
              366  LOAD_FAST                'out'
              368  LOAD_STR                 'error_msg'
              370  STORE_SUBSCR     

 L.1121       372  LOAD_FAST                'out'
              374  LOAD_FAST                'outdict'
              376  LOAD_FAST                'name'
              378  STORE_SUBSCR     

 L.1122       380  LOAD_CONST               False
              382  STORE_FAST               'submit_succeeded'

 L.1123       384  JUMP_BACK           234  'to 234'
            386_0  COME_FROM           360  '360'

 L.1124       386  LOAD_FAST                'sub'
              388  LOAD_FAST                'newstate'
              390  LOAD_STR                 'last_submit'
              392  BINARY_SUBSCR    
              394  LOAD_FAST                'name'
              396  STORE_SUBSCR     

 L.1125       398  LOAD_DEREF               'context'
              400  LOAD_STR                 'cs_timestamp'
              402  BINARY_SUBSCR    
              404  LOAD_FAST                'newstate'
              406  LOAD_STR                 'last_submit_times'
              408  BINARY_SUBSCR    
              410  LOAD_FAST                'name'
              412  STORE_SUBSCR     

 L.1128       414  LOAD_FAST                'nsubmits_used'
              416  LOAD_METHOD              get
              418  LOAD_FAST                'name'
              420  LOAD_CONST               0
              422  CALL_METHOD_2         2  ''
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  LOAD_FAST                'nsubmits_used'
              430  LOAD_FAST                'name'
              432  STORE_SUBSCR     

 L.1130       434  LOAD_FAST                'namemap'
              436  LOAD_FAST                'name'
              438  BINARY_SUBSCR    
              440  UNPACK_SEQUENCE_2     2 
              442  STORE_FAST               'question'
              444  STORE_FAST               'args'

 L.1131       446  LOAD_GLOBAL              _get
              448  LOAD_FAST                'args'
              450  LOAD_STR                 'csq_grading_mode'
              452  LOAD_STR                 'auto'
              454  LOAD_GLOBAL              str
              456  CALL_FUNCTION_4       4  ''
              458  STORE_FAST               'grading_mode'

 L.1132       460  LOAD_FAST                'grading_mode'
              462  LOAD_STR                 'auto'
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   612  'to 612'

 L.1135       470  LOAD_GLOBAL              new_entry
              472  LOAD_DEREF               'context'
              474  LOAD_FAST                'name'
              476  LOAD_STR                 'submit'
              478  CALL_FUNCTION_3       3  ''
              480  STORE_FAST               'magic'

 L.1136       482  LOAD_FAST                'magic'
              484  DUP_TOP          
              486  LOAD_FAST                'entry_ids'
              488  LOAD_FAST                'name'
              490  STORE_SUBSCR     
              492  STORE_FAST               'entry_id'

 L.1137       494  LOAD_GLOBAL              WEBSOCKET_RESPONSE

 L.1138       496  LOAD_FAST                'name'

 L.1139       498  LOAD_FAST                'entry_id'

 L.1140       500  LOAD_DEREF               'context'
              502  LOAD_STR                 'cs_checker_websocket'
              504  BINARY_SUBSCR    

 L.1141       506  LOAD_DEREF               'context'
              508  LOAD_STR                 'cs_loading_image'
              510  BINARY_SUBSCR    

 L.1144       512  LOAD_DEREF               'context'
              514  LOAD_METHOD              get
              516  LOAD_STR                 'cs_show_submission_id'
              518  LOAD_CONST               True
              520  CALL_METHOD_2         2  ''

 L.1143   522_524  POP_JUMP_IF_FALSE   530  'to 530'
              526  LOAD_STR                 ' style="display:none;"'
              528  JUMP_FORWARD        532  'to 532'
            530_0  COME_FROM           522  '522'

 L.1145       530  LOAD_STR                 ''
            532_0  COME_FROM           528  '528'

 L.1137       532  LOAD_CONST               ('name', 'magic', 'websocket', 'loading', 'id_css')
              534  BUILD_CONST_KEY_MAP_5     5 
              536  BINARY_MODULO    
              538  LOAD_FAST                'out'
              540  LOAD_STR                 'message'
              542  STORE_SUBSCR     

 L.1148       544  LOAD_FAST                'entry_id'
              546  LOAD_FAST                'out'
              548  LOAD_STR                 'magic'
              550  STORE_SUBSCR     

 L.1149       552  LOAD_STR                 ''
              554  LOAD_FAST                'out'
              556  LOAD_STR                 'score_display'
              558  STORE_SUBSCR     

 L.1150       560  LOAD_FAST                'name'
              562  LOAD_FAST                'newstate'
              564  LOAD_STR                 'cached_responses'
              566  BINARY_SUBSCR    
              568  COMPARE_OP               in
          570_572  POP_JUMP_IF_FALSE   584  'to 584'

 L.1151       574  LOAD_FAST                'newstate'
              576  LOAD_STR                 'cached_responses'
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'name'
              582  DELETE_SUBSCR    
            584_0  COME_FROM           570  '570'

 L.1152       584  LOAD_FAST                'entry_id'
              586  LOAD_FAST                'newstate'
              588  LOAD_STR                 'checker_ids'
              590  BINARY_SUBSCR    
              592  LOAD_FAST                'name'
              594  STORE_SUBSCR     

 L.1153       596  LOAD_FAST                'entry_id'
              598  LOAD_FAST                'newstate'
              600  LOAD_STR                 'last_submit_id'
              602  BINARY_SUBSCR    
              604  LOAD_FAST                'name'
              606  STORE_SUBSCR     
          608_610  JUMP_FORWARD       1378  'to 1378'
            612_0  COME_FROM           466  '466'

 L.1154       612  LOAD_FAST                'grading_mode'
              614  LOAD_STR                 'legacy'
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE  1190  'to 1190'

 L.1157       622  LOAD_FAST                'name'
              624  LOAD_FAST                'newstate'
              626  LOAD_STR                 'checker_ids'
              628  BINARY_SUBSCR    
              630  COMPARE_OP               in
          632_634  POP_JUMP_IF_FALSE   646  'to 646'

 L.1158       636  LOAD_FAST                'newstate'
              638  LOAD_STR                 'checker_ids'
              640  BINARY_SUBSCR    
              642  LOAD_FAST                'name'
              644  DELETE_SUBSCR    
            646_0  COME_FROM           632  '632'

 L.1159       646  SETUP_FINALLY       716  'to 716'

 L.1160       648  LOAD_FAST                'question'
              650  LOAD_STR                 'handle_submission'
              652  BINARY_SUBSCR    
              654  LOAD_DEREF               'context'
              656  LOAD_GLOBAL              _n
              658  LOAD_STR                 'form'
              660  CALL_FUNCTION_1       1  ''
              662  BINARY_SUBSCR    
              664  BUILD_TUPLE_1         1 
              666  LOAD_FAST                'args'
              668  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              670  STORE_FAST               'resp'

 L.1161       672  LOAD_FAST                'resp'
              674  LOAD_STR                 'score'
              676  BINARY_SUBSCR    
              678  STORE_FAST               'score'

 L.1162       680  LOAD_DEREF               'context'
              682  LOAD_STR                 'csm_language'
              684  BINARY_SUBSCR    
              686  LOAD_METHOD              handle_custom_tags
              688  LOAD_DEREF               'context'
              690  LOAD_FAST                'resp'
              692  LOAD_STR                 'msg'
              694  BINARY_SUBSCR    
              696  CALL_METHOD_2         2  ''
              698  STORE_FAST               'msg'

 L.1163       700  LOAD_FAST                'resp'
              702  LOAD_METHOD              get
              704  LOAD_STR                 'extra_data'
              706  LOAD_CONST               None
              708  CALL_METHOD_2         2  ''
              710  STORE_FAST               'extra'
              712  POP_BLOCK        
              714  JUMP_FORWARD        748  'to 748'
            716_0  COME_FROM_FINALLY   646  '646'

 L.1164       716  POP_TOP          
              718  POP_TOP          
              720  POP_TOP          

 L.1165       722  BUILD_MAP_0           0 
              724  STORE_FAST               'resp'

 L.1166       726  LOAD_CONST               0.0
              728  STORE_FAST               'score'

 L.1167       730  LOAD_GLOBAL              exc_message
              732  LOAD_DEREF               'context'
              734  CALL_FUNCTION_1       1  ''
              736  STORE_FAST               'msg'

 L.1168       738  LOAD_CONST               None
              740  STORE_FAST               'extra'
              742  POP_EXCEPT       
              744  JUMP_FORWARD        748  'to 748'
              746  END_FINALLY      
            748_0  COME_FROM           744  '744'
            748_1  COME_FROM           714  '714'

 L.1171       748  LOAD_FAST                'score'

 L.1169       750  DUP_TOP          
              752  LOAD_FAST                'out'
              754  LOAD_STR                 'score'
              756  STORE_SUBSCR     
              758  DUP_TOP          
              760  LOAD_FAST                'scores'
              762  LOAD_FAST                'name'
              764  STORE_SUBSCR     
              766  LOAD_FAST                'newstate'
              768  LOAD_METHOD              setdefault
              770  LOAD_STR                 'scores'
              772  BUILD_MAP_0           0 
              774  CALL_METHOD_2         2  ''

 L.1170       776  LOAD_FAST                'name'

 L.1169       778  STORE_SUBSCR     

 L.1172       780  LOAD_FAST                'msg'
              782  DUP_TOP          
              784  LOAD_FAST                'out'
              786  LOAD_STR                 'message'
              788  STORE_SUBSCR     
              790  DUP_TOP          
              792  LOAD_FAST                'messages'
              794  LOAD_FAST                'name'
              796  STORE_SUBSCR     
              798  LOAD_FAST                'newstate'
              800  LOAD_STR                 'cached_responses'
              802  BINARY_SUBSCR    
              804  LOAD_FAST                'name'
              806  STORE_SUBSCR     

 L.1173       808  LOAD_DEREF               'context'
              810  LOAD_STR                 'csm_tutor'
              812  BINARY_SUBSCR    
              814  LOAD_ATTR                make_score_display

 L.1174       816  LOAD_DEREF               'context'

 L.1175       818  LOAD_FAST                'args'

 L.1176       820  LOAD_FAST                'name'

 L.1177       822  LOAD_FAST                'score'

 L.1178       824  LOAD_CONST               True

 L.1179       826  LOAD_DEREF               'context'
              828  LOAD_GLOBAL              _n
              830  LOAD_STR                 'last_log'
              832  CALL_FUNCTION_1       1  ''
              834  BINARY_SUBSCR    

 L.1173       836  LOAD_CONST               ('assume_submit', 'last_log')
              838  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              840  LOAD_FAST                'out'
              842  LOAD_STR                 'score_display'
              844  STORE_SUBSCR     

 L.1181       846  LOAD_FAST                'extra'
              848  DUP_TOP          
              850  LOAD_FAST                'newstate'
              852  LOAD_STR                 'extra_data'
              854  BINARY_SUBSCR    
              856  LOAD_FAST                'name'
              858  STORE_SUBSCR     
              860  LOAD_FAST                'out'
              862  LOAD_STR                 'extra_data'
              864  STORE_SUBSCR     

 L.1184       866  LOAD_FAST                'resp'
              868  LOAD_METHOD              get
              870  LOAD_STR                 'lock'
              872  LOAD_CONST               False
              874  CALL_METHOD_2         2  ''
          876_878  POP_JUMP_IF_FALSE   968  'to 968'

 L.1185       880  LOAD_GLOBAL              dict
              882  LOAD_DEREF               'context'
              884  CALL_FUNCTION_1       1  ''
              886  STORE_FAST               'c'

 L.1186       888  LOAD_FAST                'name'
              890  BUILD_LIST_1          1 
              892  LOAD_FAST                'c'
              894  LOAD_GLOBAL              _n
              896  LOAD_STR                 'question_names'
              898  CALL_FUNCTION_1       1  ''
              900  STORE_SUBSCR     

 L.1187       902  LOAD_GLOBAL              json
              904  LOAD_METHOD              loads
              906  LOAD_GLOBAL              handle_lock
              908  LOAD_FAST                'c'
              910  CALL_FUNCTION_1       1  ''
              912  LOAD_CONST               2
              914  BINARY_SUBSCR    
              916  CALL_METHOD_1         1  ''
              918  STORE_FAST               'o'

 L.1188       920  LOAD_DEREF               'context'
              922  LOAD_GLOBAL              _n
              924  LOAD_STR                 'last_log'
              926  CALL_FUNCTION_1       1  ''
              928  BINARY_SUBSCR    
              930  STORE_FAST               'll'

 L.1189       932  LOAD_FAST                'll'
              934  LOAD_METHOD              get
              936  LOAD_STR                 'locked'
              938  LOAD_GLOBAL              set
              940  CALL_FUNCTION_0       0  ''
              942  CALL_METHOD_2         2  ''
              944  LOAD_FAST                'newstate'
              946  LOAD_STR                 'locked'
              948  STORE_SUBSCR     

 L.1190       950  LOAD_FAST                'outdict'
              952  LOAD_FAST                'name'
              954  BINARY_SUBSCR    
              956  LOAD_METHOD              update
              958  LOAD_FAST                'o'
              960  LOAD_FAST                'name'
              962  BINARY_SUBSCR    
              964  CALL_METHOD_1         1  ''
              966  POP_TOP          
            968_0  COME_FROM           876  '876'

 L.1193       968  LOAD_STR                 'submit_all'
              970  LOAD_DEREF               'context'
              972  LOAD_GLOBAL              _n
              974  LOAD_STR                 'orig_perms'
              976  CALL_FUNCTION_1       1  ''
              978  BINARY_SUBSCR    
              980  COMPARE_OP               not-in
          982_984  POP_JUMP_IF_FALSE  1378  'to 1378'

 L.1194       986  LOAD_GLOBAL              nsubmits_left
              988  LOAD_DEREF               'context'
              990  LOAD_FAST                'name'
              992  CALL_FUNCTION_2       2  ''
              994  STORE_FAST               'x'

 L.1195       996  LOAD_FAST                'question'
              998  LOAD_METHOD              get
             1000  LOAD_STR                 'allow_viewanswer'
             1002  LOAD_CONST               True
             1004  CALL_METHOD_2         2  ''
         1006_1008  POP_JUMP_IF_FALSE  1378  'to 1378'

 L.1197      1010  LOAD_FAST                'out'
             1012  LOAD_STR                 'score'
             1014  BINARY_SUBSCR    
             1016  LOAD_CONST               1
             1018  COMPARE_OP               ==

 L.1195  1020_1022  POP_JUMP_IF_FALSE  1038  'to 1038'

 L.1197      1024  LOAD_STR                 'perfect'
             1026  LOAD_GLOBAL              _get_auto_view
             1028  LOAD_FAST                'args'
             1030  CALL_FUNCTION_1       1  ''
             1032  COMPARE_OP               in

 L.1195  1034_1036  POP_JUMP_IF_TRUE   1066  'to 1066'
           1038_0  COME_FROM          1020  '1020'

 L.1198      1038  LOAD_FAST                'x'
             1040  LOAD_CONST               0
             1042  BINARY_SUBSCR    
             1044  LOAD_CONST               0
             1046  COMPARE_OP               ==

 L.1195  1048_1050  POP_JUMP_IF_FALSE  1378  'to 1378'

 L.1198      1052  LOAD_STR                 'nosubmits'
             1054  LOAD_GLOBAL              _get_auto_view
             1056  LOAD_FAST                'args'
             1058  CALL_FUNCTION_1       1  ''
             1060  COMPARE_OP               in

 L.1195  1062_1064  POP_JUMP_IF_FALSE  1378  'to 1378'
           1066_0  COME_FROM          1034  '1034'

 L.1200      1066  LOAD_GLOBAL              _get
             1068  LOAD_FAST                'args'
             1070  LOAD_STR                 'csq_allow_viewanswer'
             1072  LOAD_CONST               True
             1074  LOAD_GLOBAL              bool
             1076  CALL_FUNCTION_4       4  ''

 L.1195  1078_1080  POP_JUMP_IF_FALSE  1378  'to 1378'

 L.1203      1082  LOAD_GLOBAL              dict
             1084  LOAD_DEREF               'context'
             1086  CALL_FUNCTION_1       1  ''
             1088  STORE_FAST               'c'

 L.1204      1090  LOAD_FAST                'name'
             1092  BUILD_LIST_1          1 
             1094  LOAD_FAST                'c'
             1096  LOAD_GLOBAL              _n
             1098  LOAD_STR                 'question_names'
             1100  CALL_FUNCTION_1       1  ''
             1102  STORE_SUBSCR     

 L.1205      1104  LOAD_GLOBAL              json
             1106  LOAD_METHOD              loads
             1108  LOAD_GLOBAL              handle_viewanswer
             1110  LOAD_FAST                'c'
             1112  CALL_FUNCTION_1       1  ''
             1114  LOAD_CONST               2
             1116  BINARY_SUBSCR    
             1118  CALL_METHOD_1         1  ''
             1120  STORE_FAST               'o'

 L.1206      1122  LOAD_DEREF               'context'
             1124  LOAD_GLOBAL              _n
             1126  LOAD_STR                 'last_log'
             1128  CALL_FUNCTION_1       1  ''
             1130  BINARY_SUBSCR    
             1132  STORE_FAST               'll'

 L.1207      1134  LOAD_FAST                'll'
             1136  LOAD_METHOD              get
             1138  LOAD_STR                 'answer_viewed'
             1140  LOAD_GLOBAL              set
             1142  CALL_FUNCTION_0       0  ''
             1144  CALL_METHOD_2         2  ''
             1146  LOAD_FAST                'newstate'
             1148  LOAD_STR                 'answer_viewed'
             1150  STORE_SUBSCR     

 L.1208      1152  LOAD_FAST                'll'
             1154  LOAD_METHOD              get
             1156  LOAD_STR                 'explanation_viewed'
             1158  LOAD_GLOBAL              set
             1160  CALL_FUNCTION_0       0  ''
             1162  CALL_METHOD_2         2  ''
             1164  LOAD_FAST                'newstate'
             1166  LOAD_STR                 'explanation_viewed'
             1168  STORE_SUBSCR     

 L.1209      1170  LOAD_FAST                'outdict'
             1172  LOAD_FAST                'name'
             1174  BINARY_SUBSCR    
             1176  LOAD_METHOD              update
             1178  LOAD_FAST                'o'
             1180  LOAD_FAST                'name'
             1182  BINARY_SUBSCR    
             1184  CALL_METHOD_1         1  ''
             1186  POP_TOP          
             1188  JUMP_FORWARD       1378  'to 1378'
           1190_0  COME_FROM           618  '618'

 L.1210      1190  LOAD_FAST                'grading_mode'
             1192  LOAD_STR                 'manual'
             1194  COMPARE_OP               ==
         1196_1198  POP_JUMP_IF_FALSE  1288  'to 1288'

 L.1212      1200  LOAD_STR                 'Submission received for manual grading.'
             1202  LOAD_FAST                'out'
             1204  LOAD_STR                 'message'
             1206  STORE_SUBSCR     

 L.1213      1208  LOAD_DEREF               'context'
             1210  LOAD_STR                 'csm_tutor'
             1212  BINARY_SUBSCR    
             1214  LOAD_ATTR                make_score_display

 L.1214      1216  LOAD_DEREF               'context'

 L.1215      1218  LOAD_FAST                'args'

 L.1216      1220  LOAD_FAST                'name'

 L.1217      1222  LOAD_CONST               None

 L.1218      1224  LOAD_CONST               True

 L.1219      1226  LOAD_DEREF               'context'
             1228  LOAD_GLOBAL              _n
             1230  LOAD_STR                 'last_log'
             1232  CALL_FUNCTION_1       1  ''
             1234  BINARY_SUBSCR    

 L.1213      1236  LOAD_CONST               ('assume_submit', 'last_log')
             1238  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1240  LOAD_FAST                'out'
             1242  LOAD_STR                 'score_display'
             1244  STORE_SUBSCR     

 L.1221      1246  LOAD_FAST                'name'
             1248  LOAD_FAST                'newstate'
             1250  LOAD_STR                 'checker_ids'
             1252  BINARY_SUBSCR    
             1254  COMPARE_OP               in
         1256_1258  POP_JUMP_IF_FALSE  1270  'to 1270'

 L.1222      1260  LOAD_FAST                'newstate'
             1262  LOAD_STR                 'checker_ids'
             1264  BINARY_SUBSCR    
             1266  LOAD_FAST                'name'
             1268  DELETE_SUBSCR    
           1270_0  COME_FROM          1256  '1256'

 L.1223      1270  LOAD_FAST                'out'
             1272  LOAD_STR                 'message'
             1274  BINARY_SUBSCR    
             1276  LOAD_FAST                'newstate'
             1278  LOAD_STR                 'cached_responses'
             1280  BINARY_SUBSCR    
             1282  LOAD_FAST                'name'
             1284  STORE_SUBSCR     
             1286  JUMP_FORWARD       1378  'to 1378'
           1288_0  COME_FROM          1196  '1196'

 L.1226      1288  LOAD_STR                 '<font color="red">Unknown grading mode: %s.  Please contact staff.</font>'

 L.1227      1290  LOAD_FAST                'grading_mode'

 L.1226      1292  BINARY_MODULO    

 L.1225      1294  LOAD_FAST                'out'
             1296  LOAD_STR                 'message'
             1298  STORE_SUBSCR     

 L.1229      1300  LOAD_DEREF               'context'
             1302  LOAD_STR                 'csm_tutor'
             1304  BINARY_SUBSCR    
             1306  LOAD_ATTR                make_score_display

 L.1230      1308  LOAD_DEREF               'context'

 L.1231      1310  LOAD_FAST                'args'

 L.1232      1312  LOAD_FAST                'name'

 L.1233      1314  LOAD_CONST               0.0

 L.1234      1316  LOAD_CONST               True

 L.1235      1318  LOAD_DEREF               'context'
             1320  LOAD_GLOBAL              _n
             1322  LOAD_STR                 'last_log'
             1324  CALL_FUNCTION_1       1  ''
             1326  BINARY_SUBSCR    

 L.1229      1328  LOAD_CONST               ('assume_submit', 'last_log')
             1330  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1332  LOAD_FAST                'out'
             1334  LOAD_STR                 'score_display'
             1336  STORE_SUBSCR     

 L.1237      1338  LOAD_FAST                'name'
             1340  LOAD_FAST                'newstate'
             1342  LOAD_STR                 'checker_ids'
             1344  BINARY_SUBSCR    
             1346  COMPARE_OP               in
         1348_1350  POP_JUMP_IF_FALSE  1362  'to 1362'

 L.1238      1352  LOAD_FAST                'newstate'
             1354  LOAD_STR                 'checker_ids'
             1356  BINARY_SUBSCR    
             1358  LOAD_FAST                'name'
             1360  DELETE_SUBSCR    
           1362_0  COME_FROM          1348  '1348'

 L.1239      1362  LOAD_FAST                'out'
             1364  LOAD_STR                 'message'
             1366  BINARY_SUBSCR    
             1368  LOAD_FAST                'newstate'
             1370  LOAD_STR                 'cached_responses'
             1372  BINARY_SUBSCR    
             1374  LOAD_FAST                'name'
             1376  STORE_SUBSCR     
           1378_0  COME_FROM          1286  '1286'
           1378_1  COME_FROM          1188  '1188'
           1378_2  COME_FROM          1078  '1078'
           1378_3  COME_FROM          1062  '1062'
           1378_4  COME_FROM          1048  '1048'
           1378_5  COME_FROM          1006  '1006'
           1378_6  COME_FROM           982  '982'
           1378_7  COME_FROM           608  '608'

 L.1241      1378  LOAD_FAST                'submit_succeeded'
         1380_1382  POP_JUMP_IF_FALSE  1396  'to 1396'

 L.1242      1384  LOAD_DEREF               'context'
             1386  LOAD_STR                 'cs_timestamp'
             1388  BINARY_SUBSCR    
             1390  LOAD_FAST                'newstate'
             1392  LOAD_STR                 'last_submit_time'
             1394  STORE_SUBSCR     
           1396_0  COME_FROM          1380  '1380'

 L.1243      1396  LOAD_FAST                'args'
             1398  LOAD_METHOD              get
             1400  LOAD_STR                 'csq_rerender'
             1402  LOAD_FAST                'question'
             1404  LOAD_METHOD              get
             1406  LOAD_STR                 'always_rerender'
             1408  LOAD_CONST               False
             1410  CALL_METHOD_2         2  ''
             1412  CALL_METHOD_2         2  ''
             1414  STORE_FAST               'rerender'

 L.1244      1416  LOAD_FAST                'rerender'
             1418  LOAD_CONST               True
             1420  COMPARE_OP               is
         1422_1424  POP_JUMP_IF_FALSE  1452  'to 1452'

 L.1245      1426  LOAD_FAST                'question'
             1428  LOAD_STR                 'render_html'
             1430  BINARY_SUBSCR    
             1432  LOAD_FAST                'newstate'
             1434  LOAD_STR                 'last_submit'
             1436  BINARY_SUBSCR    
             1438  BUILD_TUPLE_1         1 
             1440  LOAD_FAST                'args'
             1442  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1444  LOAD_FAST                'out'
             1446  LOAD_STR                 'rerender'
             1448  STORE_SUBSCR     
             1450  JUMP_FORWARD       1466  'to 1466'
           1452_0  COME_FROM          1422  '1422'

 L.1246      1452  LOAD_FAST                'rerender'
         1454_1456  POP_JUMP_IF_FALSE  1466  'to 1466'

 L.1247      1458  LOAD_FAST                'rerender'
             1460  LOAD_FAST                'out'
             1462  LOAD_STR                 'rerender'
             1464  STORE_SUBSCR     
           1466_0  COME_FROM          1454  '1454'
           1466_1  COME_FROM          1450  '1450'

 L.1249      1466  LOAD_FAST                'out'
             1468  LOAD_FAST                'outdict'
             1470  LOAD_FAST                'name'
             1472  STORE_SUBSCR     

 L.1252      1474  LOAD_FAST                'out'
             1476  LOAD_STR                 'score_display'
             1478  BINARY_SUBSCR    
             1480  LOAD_FAST                'newstate'
             1482  LOAD_STR                 'score_displays'
             1484  BINARY_SUBSCR    
             1486  LOAD_FAST                'name'
             1488  STORE_SUBSCR     
             1490  JUMP_BACK           234  'to 234'

 L.1254      1492  LOAD_FAST                'nsubmits_used'
             1494  DUP_TOP          
             1496  LOAD_DEREF               'context'
             1498  LOAD_GLOBAL              _n
             1500  LOAD_STR                 'nsubmits_used'
             1502  CALL_FUNCTION_1       1  ''
             1504  STORE_SUBSCR     
             1506  LOAD_FAST                'newstate'
             1508  LOAD_STR                 'nsubmits_used'
             1510  STORE_SUBSCR     

 L.1257      1512  LOAD_DEREF               'context'
             1514  LOAD_STR                 'csm_cslog'
             1516  BINARY_SUBSCR    
             1518  LOAD_ATTR                overwrite_log

 L.1258      1520  LOAD_FAST                'uname'

 L.1259      1522  LOAD_DEREF               'context'
             1524  LOAD_STR                 'cs_path_info'
             1526  BINARY_SUBSCR    

 L.1260      1528  LOAD_STR                 'problemstate'

 L.1261      1530  LOAD_FAST                'newstate'

 L.1257      1532  BUILD_TUPLE_4         4 

 L.1262      1534  LOAD_DEREF               'context'
             1536  LOAD_GLOBAL              _n
             1538  LOAD_STR                 'log_kwargs'
             1540  CALL_FUNCTION_1       1  ''
             1542  BINARY_SUBSCR    

 L.1257      1544  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1546  POP_TOP          

 L.1266      1548  LOAD_DEREF               'context'
             1550  LOAD_STR                 'csm_time'
             1552  BINARY_SUBSCR    
             1554  LOAD_METHOD              detailed_timestamp
             1556  LOAD_FAST                'due'
             1558  CALL_METHOD_1         1  ''
             1560  STORE_FAST               'duetime'

 L.1267      1562  LOAD_CLOSURE             'context'
             1564  BUILD_TUPLE_1         1 
             1566  LOAD_DICTCOMP            '<code_object <dictcomp>>'
             1568  LOAD_STR                 'handle_submit.<locals>.<dictcomp>'
             1570  MAKE_FUNCTION_8          'closure'
             1572  LOAD_FAST                'names'
             1574  GET_ITER         
             1576  CALL_FUNCTION_1       1  ''
             1578  STORE_FAST               'subbed'

 L.1268      1580  LOAD_GLOBAL              log_action

 L.1269      1582  LOAD_DEREF               'context'

 L.1271      1584  LOAD_STR                 'submit'

 L.1272      1586  LOAD_FAST                'names'

 L.1273      1588  LOAD_FAST                'subbed'

 L.1274      1590  LOAD_FAST                'entry_ids'
         1592_1594  JUMP_IF_TRUE_OR_POP  1598  'to 1598'
             1596  LOAD_CONST               None
           1598_0  COME_FROM          1592  '1592'

 L.1275      1598  LOAD_FAST                'scores'
         1600_1602  JUMP_IF_TRUE_OR_POP  1606  'to 1606'
             1604  LOAD_CONST               None
           1606_0  COME_FROM          1600  '1600'

 L.1276      1606  LOAD_FAST                'messages'
         1608_1610  JUMP_IF_TRUE_OR_POP  1614  'to 1614'
             1612  LOAD_CONST               None
           1614_0  COME_FROM          1608  '1608'

 L.1277      1614  LOAD_FAST                'duetime'

 L.1270      1616  LOAD_CONST               ('action', 'names', 'submitted', 'checker_ids', 'scores', 'messages', 'due_date')
             1618  BUILD_CONST_KEY_MAP_7     7 

 L.1268      1620  CALL_FUNCTION_2       2  ''
             1622  POP_TOP          

 L.1281      1624  LOAD_DEREF               'context'
             1626  LOAD_STR                 'csm_loader'
             1628  BINARY_SUBSCR    
             1630  LOAD_METHOD              run_plugins

 L.1282      1632  LOAD_DEREF               'context'

 L.1282      1634  LOAD_DEREF               'context'
             1636  LOAD_STR                 'cs_course'
             1638  BINARY_SUBSCR    

 L.1282      1640  LOAD_STR                 'post_submit'

 L.1282      1642  LOAD_DEREF               'context'

 L.1281      1644  CALL_METHOD_4         4  ''
             1646  POP_TOP          

 L.1285      1648  LOAD_GLOBAL              make_return_json
             1650  LOAD_DEREF               'context'
             1652  LOAD_FAST                'outdict'
             1654  CALL_FUNCTION_2       2  ''
             1656  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 1566


def manage_groups(context):
    if context['cs_light_color'] is None:
        context['cs_light_color'] = compute_light_color(context['cs_base_color'])
    perms = context['cs_user_info'].get'permissions'[]
    if 'groups' not in perms:
        if 'admin' not in perms:
            return 'You are not allowed to view this page.'
    section = context['cs_user_info'].get'section'None
    default_section = context.get'cs_default_section''default'
    all_sections = context.get'cs_sections'[]
    if len(all_sections) == 0:
        all_sections = {default_section: 'Default Section'}
    if section is None:
        section = default_section
    hdr = 'Group Assignments for %s, Section <span id="cs_groups_section">%s</span>'
    hdr %= (context['cs_original_path'], section)
    context['cs_content_header'] = hdr
    out = '\nShow Current Groups for Section:\n<select name="section" id="section">'
    for i in sorted(all_sections):
        s = ' selected' if str(i) == str(section) else ''
        out += '\n<option value="%s"%s>%s</option>' % (i, s, i)
    else:
        out += '\n</select>'
        out += '\n<p>\n<h2>Groups:</h2>\n<div id="cs_groups_table" border="1" align="left">\nLoading...\n</div>'
        out += '\n<p>\n<h2>Make New Partnership:</h2>\nStudent 1: <select name="cs_groups_name1" id="cs_groups_name1"></select>&nbsp;\nStudent 2: <select name="cs_groups_name2" id="cs_groups_name2"></select>&nbsp;\n<button class="btn btn-catsoop" id="cs_groups_newpartners">Partner Students</button></p>'
        out += '\n<p>\n<h2>Add Student to Group:</h2>\nStudent: <select name="cs_groups_nameadd" id="cs_groups_nameadd"></select>&nbsp;\nGroup: <select name="cs_groups_groupadd" id="cs_groups_groupadd"></select>&nbsp;\n<button class="btn btn-catsoop" id="cs_groups_addtogroup">Add to Group</button></p>'
        out += '\n<p><h2>Randomly assign groups</h2>\n<button class="btn btn-catsoop" id="cs_groups_reassign">Reassign Groups</button></p>'
        all_group_names = context.get'cs_group_names'None
        if all_group_names is None:
            all_group_names = mapstrrange(100)
        else:
            all_group_names = sorted(all_group_names)
        all_group_names = list(all_group_names)
        out += '\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ncatsoop.group_names = %s\n// @license-end\n</script>' % all_group_names
        out += '\n<script type="text/javascript" src="_handler/default/cs_groups.js"></script>'
        return out + default_javascript(context)


def clearanswer_msg(context, perms, name):
    namemap = context[_n('name_map')]
    timing = context[_n('timing')]
    ansviewed = context[_n('answer_viewed')]
    i = context[_n('impersonating')]
    _, qargs = namemap[name]
    error = None
    if 'submit' not in perms and 'submit_all' not in perms:
        error = 'You are not allowed undo your viewing of the answer to this question.'
    else:
        if name not in ansviewed:
            error = 'You have not viewed the answer for this question.'
        else:
            if name not in namemap:
                error = 'No question with name %s.  Please refresh before submitting.' % name
            else:
                if 'submit_all' not in perms:
                    if timing == -1:
                        if not i:
                            error = 'This question is not yet available.'
                    if not qargs.get'csq_allow_submit_after_answer_viewed'False:
                        error = 'You are not allowed to undo your viewing of the answer to this question.'
    return error


def viewexp_msg(context, perms, name):
    namemap = context[_n('name_map')]
    timing = context[_n('timing')]
    ansviewed = context[_n('answer_viewed')]
    expviewed = context[_n('explanation_viewed')]
    _, qargs = namemap[name]
    error = None
    if 'submit' not in perms and 'submit_all' not in perms:
        error = 'You are not allowed to view the answer to this question.'
    else:
        if name not in ansviewed:
            error = 'You have not yet viewed the answer for this question.'
        else:
            if name in expviewed:
                error = 'You have already viewed the explanation for this question.'
            else:
                if name not in namemap:
                    error = 'No question with name %s.  Please refresh before submitting.' % name
                else:
                    if 'submit_all' not in perms and timing == -1:
                        error = 'This question is not yet available.'
                    else:
                        if not _get(qargs, 'csq_allow_viewexplanation', True, bool):
                            error = 'Viewing explanations is not allowed for this question.'
                        else:
                            q, args = namemap[name]
                            if 'csq_explanation' not in args:
                                error = 'No explanation supplied for this question.'
    return error


def viewanswer_msg(context, perms, name):
    namemap = context[_n('name_map')]
    timing = context[_n('timing')]
    ansviewed = context[_n('answer_viewed')]
    i = context[_n('impersonating')]
    _, qargs = namemap[name]
    error = None
    if not _.get'allow_viewanswer'True:
        error = 'You cannot view the answer to this type of question.'
    else:
        if 'submit' not in perms and 'submit_all' not in perms:
            error = 'You are not allowed to view the answer to this question.'
        else:
            if name in ansviewed:
                error = 'You have already viewed the answer for this question.'
            else:
                if name not in namemap:
                    error = 'No question with name %s.  Please refresh before submitting.' % name
                else:
                    if 'submit_all' not in perms:
                        if timing == -1:
                            error = i or 'This question is not yet available.'
                        else:
                            error = _get(qargs, 'csq_allow_viewanswer', True, bool) or 'Viewing the answer is not allowed for this question.'
    return error


def save_msg(context, perms, name):
    namemap = context[_n('name_map')]
    timing = context[_n('timing')]
    i = context[_n('impersonating')]
    _, qargs = namemap[name]
    error = None
    if not _.get'allow_save'True:
        error = 'You cannot save this type of question.'
    else:
        if 'submit' not in perms and 'submit_all' not in perms:
            error = 'You are not allowed to check answers to this question.'
        else:
            if name not in namemap:
                error = 'No question with name %s.  Please refresh before submitting.' % name
            else:
                if 'submit_all' not in perms:
                    if timing == -1:
                        error = i or 'This question is not yet available.'
                    else:
                        if name in context[_n('locked')]:
                            error = 'You are not allowed to save for this question (it has been locked).'
                        else:
                            if (_get(qargs, 'csq_allow_submit_after_answer_viewed', False, bool) or name) in context[_n('answer_viewed')]:
                                error = 'You are not allowed to save to this question after viewing the answer.'
                            else:
                                if timing == 1 and _get(context, 'cs_auto_lock', False, bool):
                                    error = 'You are not allowed to save after the deadline for this question.'
                                else:
                                    error = _get(qargs, 'csq_allow_save', True, bool) or 'Saving is not allowed for this question.'
    return error


def check_msg(context, perms, name):
    namemap = context[_n('name_map')]
    timing = context[_n('timing')]
    i = context[_n('impersonating')]
    _, qargs = namemap[name]
    error = None
    if 'submit' not in perms and 'submit_all' not in perms:
        error = 'You are not allowed to check answers to this question.'
    else:
        if name not in namemap:
            error = 'No question with name %s.  Please refresh before submitting.' % name
        else:
            if namemap[name][0].get'handle_check'None is None:
                error = 'This question type does not support checking.'
            else:
                if 'submit_all' not in perms:
                    if timing == -1:
                        error = i or 'This question is not yet available.'
                    else:
                        if name in context[_n('locked')]:
                            error = 'You are not allowed to check answers to this question.'
                        else:
                            if (_get(qargs, 'csq_allow_submit_after_answer_viewed', False, bool) or name) in context[_n('answer_viewed')]:
                                error = 'You are not allowed to check answers to this question after viewing the answer.'
                            else:
                                if timing == 1 and _get(context, 'cs_auto_lock', False, bool):
                                    error = 'You are not allowed to check after the deadline for this problem.'
                                else:
                                    error = _get(qargs, 'csq_allow_check', True, bool) or 'Checking is not allowed for this question.'
    return error


def grade_msg(context, perms, name):
    namemap = context[_n('name_map')]
    _, qargs = namemap[name]
    if 'grade' not in perms:
        return 'You are not allowed to grade exercises.'


def submit_msg(context, perms, name):
    if name.startswith'__':
        name = name[2:].rsplit'_'1[0]
    else:
        namemap = context[_n('name_map')]
        timing = context[_n('timing')]
        i = context[_n('impersonating')]
        _, qargs = namemap[name]
        error = None
        if not _.get'allow_submit'True:
            error = 'You cannot submit this type of question.'
        if not _.get'allow_self_submit'True:
            if 'real_user' not in context['cs_user_info']:
                error = 'You cannot submit this type of question yourself.'
    if 'submit' not in perms:
        if 'submit_all' not in perms:
            error = 'You are not allowed to submit answers to this question.'
        else:
            if name not in namemap:
                error = 'No question with name %s.  Please refresh before submitting.' % name
            else:
                if 'submit_all' not in perms:
                    if timing == -1:
                        error = i or 'This question is not yet open for submissions.'
                    else:
                        if _get(context, 'cs_auto_lock', False, bool):
                            if timing == 1:
                                error = 'Submissions are not allowed after the deadline for this question'
                            else:
                                if name in context[_n('locked')]:
                                    error = 'You are not allowed to submit to this question.'
                                else:
                                    if not _get(qargs, 'csq_allow_submit_after_answer_viewed', False, bool):
                                        if name in context[_n('answer_viewed')]:
                                            error = 'You are not allowed to submit to this question because you have already viewed the answer.'
                            if not _get(qargs, 'csq_allow_submit', True, bool):
                                if 'csq_nosubmit_message' in qargs:
                                    if context[_n('action')] != 'view':
                                        error = qargs['csq_nosubmit_message'](qargs)
                        else:
                            error = 'Submissions are not allowed for this question.'
    else:
        if (_get(qargs, 'csq_grading_mode', 'auto', str) == 'manual' or context['csm_tutor'].get_manual_grading_entrycontextname) is not None:
            error = 'You are not allowed to submit after a previous submission has been graded.'
        else:
            nleft, _ = nsubmits_leftcontextname
            if nleft <= 0:
                error = 'You have used all of your allowed submissions for this question.'
            return error


def log_action(context, log_entry):
    uname = context[_n('uname')]
    entry = {'action':context[_n('action')], 
     'timestamp':context['cs_timestamp'], 
     'user_info':context['cs_user_info']}
    entry.updatelog_entry
    (context['csm_cslog'].update_log)(
     uname, 
     (context['cs_path_info']), 
     'problemactions', 
     entry, **context[_n('log_kwargs')])


def simple_return_json(val):
    content = json.dumps(val, separators=(',', ':'))
    length = str(len(content))
    retcode = ('200', 'OK')
    headers = {'Content-type':'application/json',  'Content-length':length}
    return (retcode, headers, content)


def make_return_json(context, ret, names=None):
    names = context[_n('question_names')] if names is None else names
    names = set(((i[2:].rsplit'_'1[0] if i.startswith'__' else i) for i in names))
    ctx2 = dict(context)
    if ctx2[_n('action')] != 'view':
        ctx2[_n('action')] = 'view'
    for name in names:
        ret[name]['nsubmits_left'] = (
         nsubmits_leftcontextname[1],)
        ret[name]['buttons'] = make_buttonsctx2name
    else:
        return simple_return_json(ret)


def render_question(elt, context, lastsubmit, wrap=True):
    q, args = elt
    name = args['csq_name']
    lastlog = context[_n('last_log')]
    answer_viewed = context[_n('answer_viewed')]
    if wrap:
        out = '\n<!--START question %s -->' % name
    else:
        out = ''
    if wrap:
        if q.get'indiv'True:
            if args.get'csq_indiv'True:
                out += '\n<div class="question question-%s" id="cs_qdiv_%s" style="position: static">' % (
                 q['qtype'], name)
    else:
        out += '\n<div id="%s_rendered_question">\n' % name
        out += context['csm_language'].source_transform_stringcontextargs.get'csq_prompt'''
        out += (q['render_html'])(lastsubmit, **args)
        out += '\n</div>'
        out += '<div>'
        out += '\n<span id="%s_buttons">' % name + make_buttonscontextname + '</span>'
        out += '\n<span id="%s_loading_wrapper">\n<span id="%s_loading" style="display:none;"><img src="%s"/></span>\n</span>' % (
         name, name, context['cs_loading_image'])
        out += '\n<span id="%s_score_display">' % args['csq_name'] + context['csm_tutor'].make_score_display(context,
          args, name, None, last_log=(context[_n('last_log')])) + '</span>'
        out += '\n<div id="%s_nsubmits_left" class="nsubmits_left">' % name + nsubmits_leftcontextname[1] + '</div>'
        out += '</div>'
        if name in answer_viewed:
            answerclass = ' class="solution"'
            showanswer = True
        else:
            if context[_n('impersonating')]:
                answerclass = ' class="impsolution"'
                showanswer = True
            else:
                answerclass = ''
                showanswer = False
    out += '\n<div id="%s_solution_container"%s>' % (args['csq_name'], answerclass)
    out += '\n<div id="%s_solution">' % args['csq_name']
    if showanswer:
        ans = (q['answer_display'])(**args)
        out += '\n'
        out += context['csm_language'].source_transform_stringcontextans
    else:
        out += '\n</div>'
        out += '\n<div id="%s_solution_explanation">' % name
        if name in context[_n('explanation_viewed')]:
            if args.get'csq_explanation''' != '':
                exp = explanation_display(args['csq_explanation'])
                out += context['csm_language'].source_transform_stringcontextexp
        out += '\n</div>'
        out += '\n</div>'
        out += '\n<div id="%s_message">' % args['csq_name']
        gmode = _get(args, 'csq_grading_mode', 'auto', str)
        message = context[_n('last_log')].get'cached_responses'{}.getname''
        magic = context[_n('last_log')].get'checker_ids'{}.getnameNone
        if magic is not None:
            checker_loc = os.path.join(context['cs_data_root'], '_logs', '_checker', 'results', magic[0], magic[1], magic)
            if os.path.isfilechecker_loc:
                with openchecker_loc'rb' as (f):
                    result = context['csm_cslog'].unprepf.read
                message = '\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ndocument.getElementById("%s_score_display").innerHTML = %r;\n// @license-end\n</script>' % (
                 name, result['score_box'])
                try:
                    result['response'] = result['response'].decode
                except:
                    pass
                else:
                    message += '\n' + result['response']
            else:
                message = WEBSOCKET_RESPONSE % {'name':name, 
                 'magic':magic, 
                 'websocket':context['cs_checker_websocket'], 
                 'loading':context['cs_loading_image'], 
                 'id_css':' style="display:none;"' if context.get'cs_show_submission_id'True else ''}
    if gmode == 'manual':
        q, args = context[_n('name_map')][name]
        lastlog = context['csm_tutor'].get_manual_grading_entrycontextname or {}
        lastscore = lastlog.get'score'''
        tpoints = (q['total_points'])(**args)
        comments = (context['csm_tutor'].get_manual_grading_entrycontextname or {}).get'comments'None
        if comments is not None:
            comments = context['csm_language']._md_format_stringcontextcomments
        try:
            score_output = lastscore * tpoints
        except:
            score_output = ''
        else:
            if comments is not None:
                message = "<b>Score:</b> %s (out of %s)<br><br><b>Grader's Comments:</b><br/>%s" % (
                 score_output, tpoints, comments)
    out += message + '</div>'
    if wrap:
        if q.get'indiv'True:
            if args.get'csq_indiv'True:
                out += '\n</div>'
    if wrap:
        out += '\n<!--END question %s -->\n' % args['csq_name']
    return out


def nsubmits_left(context, name):
    nused = context[_n('nsubmits_used')].getname0
    q, args = context[_n('name_map')][name]
    return q.get'allow_submit'True and q.get'allow_self_submit'True or (0, '')
    info = q.get'defaults'{}
    info.updateargs
    nsubmits = info.get'csq_nsubmits'None
    if nsubmits is None:
        nsubmits = context.get'cs_nsubmits_default'float('inf')
    perms = context[_n('orig_perms')]
    if 'submit' not in perms:
        if 'submit_all' not in perms:
            return (0, '')
    nleft = max0(nsubmits - nused)
    for regex, nchecks in context['cs_user_info'].get'nsubmits_extra'[]:
        if re.matchregex'.'.join(context['cs_path_info'][1:] + [name]):
            nleft += nchecks
        nmsg = info.get'csq_nsubmits_message'None
        if nmsg is None:
            if nleft < float('inf'):
                msg = '<i>You have %d submission%s remaining.</i>' % (
                 nleft,
                 's' if nleft != 1 else '')
            else:
                msg = '<i>You have infinitely many submissions remaining.</i>'
        else:
            msg = nmsg(nsubmits, nused, nleft)
        if 'submit_all' in perms:
            msg = 'As staff, you are always allowed to submit.  If you were a student, you would see the following:<br/>%s' % msg
        return (max0nleft, msg)


def button_text(x, msg):
    if x is None:
        return msg
    return


_button_map = {'submit':(
  submit_msg, 'Submit'), 
 'save':(
  save_msg, 'Save'), 
 'viewanswer':(
  viewanswer_msg, 'View Answer'), 
 'clearanswer':(
  clearanswer_msg, 'Clear Answer'), 
 'viewexplanation':(
  viewexp_msg, 'View Explanation'), 
 'check':(
  check_msg, True)}

def make_buttons(context, name):
    uname = context[_n('uname')]
    rp = context[_n('perms')]
    p = context[_n('orig_perms')]
    i = context[_n('impersonating')]
    q, args = context[_n('name_map')][name]
    nsubmits, _ = nsubmits_leftcontextname
    buttons = {'copy_seed':None, 
     'copy':None,  'new_seed':None}
    buttons['new_seed'] = 'New Random Seed' if ('submit_all' in p and context.get'cs_random_inited'False) else None
    abuttons = {'copy_seed':'Copy Random Seed' if context.get'cs_random_inited'False else None, 
     'copy':'Copy to My Account', 
     'lock':None, 
     'unlock':None}
    for b, (func, text) in list(_button_map.items):
        buttons[b] = button_textfunc(context, p, name)text
        abuttons[b] = button_textfunc(context, rp, name)text
    else:
        for d in (
         buttons, abuttons):
            if d['check']:
                d['check'] = q.get'checktext''Check'
            if name in context[_n('locked')]:
                abuttons['unlock'] = 'Unlock'
            else:
                abuttons['lock'] = 'Lock'
            aout = ''
            if i:
                for k in {'save', 'check', 'submit'}:
                    if buttons[k] is not None:
                        abuttons[k] = None
                else:
                    if abuttons[k] is not None:
                        abuttons[k] += ' (as %s)' % uname
                    for k in ('viewanswer', 'clearanswer', 'viewexplanation'):
                        if buttons[k] is not None:
                            abuttons[k] = None

            else:
                if abuttons[k] is not None:
                    abuttons[k] += ' (for %s)' % uname
                aout = '<div><b><font color="red">Admin Buttons:</font></b><br/>'
                for k in ('copy', 'copy_seed', 'check', 'save', 'submit', 'viewanswer',
                          'viewexplanation', 'clearanswer', 'lock', 'unlock'):
                    x = {'b':abuttons[k], 
                     'k':k,  'n':name}
                    if abuttons[k] is not None:
                        aout += '\n<button id="%(n)s_%(k)s" class="%(k)s btn btn-danger" onclick="catsoop.%(k)s(\'%(n)s\');">%(b)s</button>' % x
                    gmode = _get(args, 'csq_grading_mode', 'auto', str)
                    if gmode == 'manual':
                        lastlog = context['csm_tutor'].get_manual_grading_entrycontextname or {}
                        lastscore = lastlog.get'score'''
                        lastcomments = lastlog.get'comments'''
                        tpoints = (q['total_points'])(**args)
                        try:
                            output = lastscore * tpoints
                        except:
                            output = ''
                        else:
                            aout += '<br/><b><font color="red">Grading:</font></b><table border="0" width="100%%"><tr><td align="right" width="30%%"><font color="red">Points Earned (out of %2.2f):</font></td><td><input type="text" value="%s" size="5" style="border-color: red;" id="%s_grading_score" name="%s_grading_score" /></td></tr><tr><td align="right"><font color="red">Comments:</font></td><td><textarea rows="5" id="%s_grading_comments" name="%s_grading_comments" style="width: 100%%; border-color: red;">%s</textarea></td></tr><tr><td></td><td><button class="grade" style="background-color: #FFD9D9; border-color: red;" onclick="catsoop.grade(\'%s\');">Submit Grade</button></td></tr></table>' % (
                             tpoints, output, name, name, name, name, lastcomments, name)
                        aout += '</div>'
                    else:
                        out = ''
                        for k in ('check', 'save', 'submit', 'viewanswer', 'viewexplanation',
                                  'clearanswer', 'new_seed'):
                            x = {'b':buttons[k], 
                             'k':k,  'n':name,  's':''}
                            heb = context.get'cs_ui_config_flags'{}.get'highlight_explanation_button'
                            if k == 'viewexplanation':
                                if heb:
                                    color = 'blue'
                                    if heb is not True:
                                        color = heb
                                    x['s'] = 'background-color:%s;' % color

                    if buttons[k] is not None:
                        out += '\n<button id="%(n)s_%(k)s" class="%(k)s btn btn-catsoop" style="margin-top: 10px;%(s)s" onclick="catsoop.%(k)s(\'%(n)s\');">%(b)s</button>' % x
                    return out + aout


def pre_handle(context):
    if context['cs_storage_backend'] == 'postgres':
        context[_n('log_kwargs')] = {'connection': context['cs_postgres_connection']}
    else:
        context[_n('log_kwargs')] = {}
    context[_n('name_map')] = collections.OrderedDict
    for elt in context['cs_problem_spec']:
        if isinstanceelttuple:
            m = elt[1]
            context[_n('name_map')][m['csq_name']] = elt
            if 'init' in elt[0]:
                a = elt[0].get'defaults'{}
                a.updateelt[1]
                elt[0]['init'](a)
    else:
        user_info = context.get'cs_user_info'{}
        uname = user_info.get'username''None'
        real = user_info.get'real_user'user_info
        context[_n('role')] = real.get'role''None'
        context[_n('section')] = real.get'section'None
        context[_n('perms')] = real.get'permissions'[]
        context[_n('orig_perms')] = user_info.get'permissions'[]
        context[_n('uname')] = uname
        context[_n('real_uname')] = real.get'username'uname
        context[_n('impersonating')] = context[_n('uname')] != context[_n('real_uname')]
        r = context[_n('rel')] = context['csm_tutor'].get_release_datecontext
        d = context[_n('due')] = context['csm_tutor'].get_due_datecontext
        n = context['csm_time'].from_detailed_timestampcontext['cs_timestamp']
        context[_n('now')] = n
        context[_n('timing')] = -1 if n <= r else 0 if n <= d else 1
        if _get(context, 'cs_require_activation', False, bool):
            pwd = _get(context, 'cs_activation_password', 'password', str)
            context[_n('activation_password')] = pwd
        loghead = '___'.joincontext['cs_path_info'][1:]
        ll = (context['csm_cslog'].most_recent)(
         uname, (context['cs_path_info']), 'problemstate', {}, **context[_n('log_kwargs')])
        _cs_group_path = context.get'cs_groups_to_use'context['cs_path_info']
        context[_n('all_groups')] = context['csm_groups'].list_groupscontext_cs_group_path
        context[_n('group')] = context['csm_groups'].get_groupcontext_cs_group_pathunamecontext[_n('all_groups')]
        _ag = context[_n('all_groups')]
        _g = context[_n('group')]
        context[_n('group_members')] = _gm = _ag.get_g[0]{}.get_g[1][]
        if uname not in _gm:
            _gm.appenduname
        context[_n('last_log')] = ll
        context[_n('locked')] = set(ll.get'locked'set())
        context[_n('answer_viewed')] = set(ll.get'answer_viewed'set())
        context[_n('explanation_viewed')] = set(ll.get'explanation_viewed'set())
        context[_n('nsubmits_used')] = ll.get'nsubmits_used'{}
        context[_n('action')] = context['cs_form'].get'action''view'.lower
        if context[_n('action')] in ('view', 'activate', 'passthrough', 'list_questions',
                                     'get_state', 'manage_groups', 'render_single_question'):
            context[_n('form')] = context['cs_form']
        else:
            names = context['cs_form'].get'names''[]'
        context[_n('question_names')] = json.loadsnames
        context[_n('form')] = json.loadscontext['cs_form'].get'data''{}'

    if context['cs_upload_management'] == 'file':
        for name, value in context[_n('form')].items:
            if name == '__names__':
                pass
            elif isinstancevaluelist:
                data = csm_thirdparty.data_uri.DataURIvalue[1].data
                if context['csm_cslog'].ENCRYPT_KEY is not None:
                    seed = context['cs_path_info'][0] if context['cs_path_info'] else context['cs_path_info']
                    _path = [context['csm_cslog']._eirepr(seed) for i in context['cs_path_info']]
                else:
                    _path = context['cs_path_info']
                value[0] = value[0].replace'<'''.replace'>'''.replace'"'''.replace'"'''
                hstring = hashlib.sha256data.hexdigest
                info = {'filename':value[0], 
                 'username':context['cs_username'], 
                 'time':context['csm_time'].detailed_timestampcontext['cs_now'], 
                 'question':name, 
                 'hash':hstring}
                h = '%s%s' % (uuid.uuid4.hex, hstring)
                disk_fname = '_csfile.%s' % h
                if context['cs_storage_backend'] == 'fs':
                    dir_ = (os.path.join)(context['cs_data_root'], '_logs', '_uploads', *_path)
                    os.makedirs(dir_, exist_ok=True)
                    dirname = os.path.joindir_disk_fname
                    os.makedirs(dirname, exist_ok=True)
                    with openos.path.joindirname'content''wb' as (f):
                        f.writecontext['csm_cslog'].compress_encryptdata
                    with openos.path.joindirname'info''wb' as (f):
                        f.writecontext['csm_cslog'].prepinfo
                    value[1] = dirname

        if context['cs_storage_backend'] == 'postgres':
            with context['cs_postgres_connection'].cursor as (c):
                c.execute'INSERT INTO uploads (id, info, content) VALUES (%s, %s, %s)'(
                 h,
                 context['csm_cslog'].prepinfo,
                 context['csm_cslog'].compress_encryptdata)
            value[1] = h
    else:
        if context['cs_upload_management'] == 'db':
            pass
        else:
            raise Exception('unknown upload management style: %r' % context['cs_upload_management'])


def _get_auto_view(context):
    ava = context.get'csq_auto_viewanswer'False
    if ava is True:
        ava = set(['nosubmits', 'perfect', 'lock'])
    else:
        if isinstanceavastr:
            ava = set([ava])
        else:
            if not ava:
                ava = set()
    return ava


def default_javascript(context):
    namemap = context[_n('name_map')]
    if 'submit_all' in context[_n('perms')]:
        skip_alert = list(namemap.keys)
    else:
        skipper = 'csq_allow_submit_after_answer_viewed'
        skip_alert = [name for name, (q, args) in list(namemap.items) if _get(args, skipper, False, bool)]
    out = '\n<script type="text/javascript" src="_handler/default/cs_ajax.js"></script>\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ncatsoop.all_questions = %(allqs)r;\ncatsoop.username = %(uname)s;\ncatsoop.api_token = %(secret)s;\ncatsoop.this_path = %(path)r;\ncatsoop.path_info = %(pathinfo)r;\ncatsoop.course = %(course)s;\ncatsoop.url_root = %(root)r;\n'
    if len(namemap) > 0:
        out += 'catsoop.imp = %(imp)r;\ncatsoop.skip_alert = %(skipalert)s;\ncatsoop.viewans_confirm = "Are you sure?  Viewing the answer will prevent any further submissions to this question.  Press \'OK\' to view the answer, or press \'Cancel\' if you have changed your mind.";\n'
    out += '\n// @license-end'
    out += '</script>'
    api_tok = 'null'
    uname = 'null'
    given_tok = context.get'cs_user_info'{}.get'api_token'None
    if given_tok is not None:
        api_tok = repr(given_tok)
    given_uname = context.get'cs_user_info'{}.get'username'None
    if given_uname is not None:
        uname = repr(given_uname)
    return out % {'skipalert':json.dumpsskip_alert, 
     'allqs':list(context[_n('name_map')].keys), 
     'user':context[_n('real_uname')], 
     'path':'/'.join[context['cs_url_root']] + context['cs_path_info'], 
     'imp':context[_n('uname')] if context[_n('impersonating')] else '', 
     'secret':api_tok, 
     'course':repr(context['cs_course']) if context['cs_course'] else 'null', 
     'pathinfo':context['cs_path_info'], 
     'root':context['cs_url_root'], 
     'uname':uname}


def default_timer(context):
    out = ''
    if not _get(context, 'cs_auto_lock', False, bool):
        return out
    if len(context[_n('locked')]) >= len(context[_n('name_map')]):
        return out
    if context[_n('now')] > context[_n('due')]:
        out += '\n<script type="text/javascript">'
        out += '\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3'
        out += "\ncatsoop.ajaxrequest(catsoop.all_questions,'lock');"
        out += '\n// @license-end'
        out += '\n</script>'
        return out
    out += '\n<script type="text/javascript">'
    out += '\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3'
    out += '\ncatsoop.timer_now = %d;\ncatsoop.timer_due = %d;\ncatsoop.time_url = %r;' % (
     context['csm_time'].unixcontext[_n('now')],
     context['csm_time'].unixcontext[_n('due')],
     context['cs_url_root'] + '/_util/time')
    out += '\n// @license-end'
    out += '\n</script>'
    out += '<script type="text/javascript" src="_handler/default/cs_timer.js"></script>'
    return out


def exc_message(context):
    exc = traceback.format_exc
    exc = context['csm_errors'].clear_infocontextexc
    return '<p><font color="red"><b>CAT-SOOP ERROR:</b><pre>%s</pre></font>' % exc


def _get_scores(context):
    section = str(context.get'cs_form'{}.get'section'context.get'cs_user_info'.get'section''default')
    user = context['csm_user']
    usernames = user.list_all_userscontextcontext['cs_course']
    users = [user.read_user_filecontextcontext['cs_course']username{} for username in usernames]
    no_section = context.get'cs_whdw_no_section'False
    students = [user for user in users if user.get'role'None in ('Student', 'SLA') and (no_section or str(user.get'section''default') == section)]
    questions = context[_n('name_map')]
    scores = collections.OrderedDict
    for name, question in questions.items:
        if not context.get'cs_whdw_filter'(lambda q: True)(question):
            pass
        else:
            counts = {}
            for student in students:
                username = student.get'username''None'
                log = (context['csm_cslog'].most_recent)(
                 username, 
                 (context['cs_path_info']), 
                 'problemstate', {}, **context[_n('log_kwargs')])
                log = context['csm_tutor'].compute_page_statscontextusernamecontext['cs_path_info']['state']['state']
                score = log.get'scores'{}.getnameNone
                counts[username] = score
            else:
                scores[name] = counts

    else:
        return scores


def handle_stats(context):
    perms = context['cs_user_info'].get'permissions'[]
    if 'whdw' not in perms:
        return 'You are not allowed to view this page.'
    section = str(context.get'cs_form'{}.get'section'context.get'cs_user_info'.get'section''default')
    questions = context[_n('name_map')]
    stats = collections.OrderedDict
    groups = context['csm_groups'].list_groupscontextcontext['cs_path_info'].getsectionNone
    if groups:
        total = len(groups)
        for name, scores in _get_scores(context).items:
            counts = {'completed':0, 
             'attempted':0,  'not tried':0}
            for members in groups.values:
                score = min((scores.getmemberNone for member in members),
                  key=(lambda x:                 if x is None:
-1 # Avoid dead code: x))
                if score is None:
                    counts['not tried'] += 1
                elif score == 1:
                    counts['completed'] += 1
                else:
                    counts['attempted'] += 1
            else:
                stats[name] = counts

    else:
        total = 0
        for name, scores in _get_scores(context).items:
            counts = {'completed':0, 
             'attempted':0,  'not tried':0}
            for score in scores.values:
                if score is None:
                    counts['not tried'] += 1
                elif score == 1:
                    counts['completed'] += 1
                else:
                    counts['attempted'] += 1
            else:
                stats[name] = counts
                total = maxtotalsum(counts.values)

        else:
            soup = BeautifulSoup'''html.parser'
            table = soup.new_tag'table'
            table['class'] = 'table table-bordered'
            header = soup.new_tag'tr'
            for heading in ('name', 'completed', 'attempted', 'not tried'):
                th = soup.new_tag'th'
                th.string = heading
                header.appendth
            else:
                table.appendheader
                for name, counts in stats.items:
                    tr = soup.new_tag'tr'
                    td = soup.new_tag'td'
                    a = soup.new_tag('a',
                      href=('?section={}&action=whdw&question={}'.formatsectionname))
                    qargs = questions[name][1]
                    a.string = qargs.get'csq_display_name'name
                    td.appenda
                    td['class'] = 'text-left'
                    tr.appendtd
                    for key in ('completed', 'attempted', 'not tried'):
                        td = soup.new_tag'td'
                        td.string = '{count}/{total} ({percent:.2%})'.format(count=(counts[key]),
                          total=total,
                          percent=(counts[key] / total if total != 0 else 0))
                        td['class'] = 'text-right'
                        tr.appendtd
                    else:
                        table.appendtr

                else:
                    soup.appendtable
                    return str(soup)


def _real_name(context, username):
    return ((context['csm_cslog'].most_recent)(
     '_extra_info', [], username, None, **context[_n('log_kwargs')]) or {}).get'name'None


def _whdw_name(context, username):
    real_name = _real_namecontextusername
    if real_name:
        return '{} (<a href="?as={}" target="_blank">{}</a>)'.format(real_name, username, username)
    return username


def handle_whdw(context):
    perms = context['cs_user_info'].get'permissions'[]
    if 'whdw' not in perms:
        return 'You are not allowed to view this page.'
    section = str(context.get'cs_form'{}.get'section'context.get'cs_user_info'.get'section''default')
    question = context['cs_form']['question']
    qtype, qargs = context[_n('name_map')][question]
    display_name = qargs.get'csq_display_name'qargs['csq_name']
    context['cs_content_header'] += ' | {}'.formatdisplay_name
    scores = _get_scores(context)[question]
    groups = context['csm_groups'].list_groupscontextcontext['cs_path_info'].getsectionNone
    soup = BeautifulSoup'''html.parser'
    if groups:
        css = soup.new_tag'style'
        css.string = '        .whdw-cell {\n          border: 1px white solid;\n        }\n\n        .whdw-not-tried {\n          background-color: #ff6961;\n          color: black;\n        }\n\n        .whdw-attempted {\n          background-color: #ffb347;\n          color: black;\n        }\n\n        .whdw-completed {\n          background-color: #77dd77;\n          color: black;\n        }\n\n        .whdw-cell ul {\n          padding-left: 5px;\n        }\n        '
        soup.appendcss
        grid = soup.new_tag'div'
        grid['class'] = 'row'
        for group, members in sorted(groups.items):
            min_score = min((scores.getmemberNone for member in members),
              key=(lambda x:             if x is None:
-1 # Avoid dead code: x))
            cell = soup.new_tag'div'
            cell['class'] = 'col-sm-3 whdw-cell {}'.format{None:'whdw-not-tried', 
             1:'whdw-completed'}.getmin_score'whdw-attempted'
            grid.appendcell
            header = soup.new_tag'div'
            header['class'] = 'text-center'
            header.string = '{}'.formatgroup
            cell.appendheader
            people = soup.new_tag'ul'
            header['class'] = 'text-center'
            for member in members:
                m = soup.new_tag'li'
                name = soup.new_tag'span'
                name.insert1BeautifulSoup_whdw_namecontextmember'html.parser'
                m.appendname
                score = soup.new_tag'span'
                score['class'] = 'pull-right'
                score.string = str(scores.getmemberNone)
                m.appendscore
                people.appendm
            else:
                cell.appendpeople

        else:
            soup.appendgrid
            return str(soup)

    states = {'completed':[],  'attempted':[],  'not tried':[]}
    for username, score in scores.items:
        if score is None:
            state = 'not tried'
        else:
            if score == 1:
                state = 'completed'
            else:
                state = 'attempted'
        states[state].appendusername
    else:
        for state in ('not tried', 'attempted', 'completed'):
            usernames = states[state]
            h3 = soup.new_tag'h3'
            h3.string = '{} ({})'.formatstatelen(states[state])
            soup.appendh3
            grid = soup.new_tag'div'
            grid['class'] = 'row'
            for username in sorted(usernames):
                cell = soup.new_tag'div'
                cell.insert1BeautifulSoup_whdw_namecontextusername'html.parser'
                cell['class'] = 'col-sm-2'
                grid.appendcell
            else:
                soup.appendgrid

        else:
            return str(soup)


WEBSOCKET_RESPONSE = '\n<div class="callout callout-default" id="cs_partialresults_%(name)s">\n  <div id="cs_partialresults_%(name)s_body">\n    <span id="cs_partialresults_%(name)s_message">Looking up your submission (id <code>%(magic)s</code>).  Watch here for updates.</span><br/>\n    <center><img src="%(loading)s"/></center>\n  </div>\n</div>\n<small%(id_css)s>ID: <code>%(magic)s</code></small>\n\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\nvar magic_%(name)s = %(magic)r;\nif (typeof ws_%(name)s != \'undefined\'){\n    ws_%(name)s.onclose = function(){}\n    ws_%(name)s.onmessage = function(){}\n    ws_%(name)s.close();\n    var ws_%(name)s = undefined;\n}\n\ndocument.getElementById(\'%(name)s_score_display\').innerHTML =  \'<img src="%(loading)s" style="vertical-align: -6px; margin-left: 5px;"/>\';\n\ndocument.querySelectorAll(\'#%(name)s_buttons button\').forEach(function(b){b.disabled = true});\n\nvar ws_%(name)s = new WebSocket(%(websocket)r);\n\nws_%(name)s.onopen = function(){\n    ws_%(name)s.send(JSON.stringify({type: "hello", magic: magic_%(name)s}));\n}\n\nws_%(name)s.onclose = function(){\n    if (this !== ws_%(name)s) return;\n    if (ws_%(name)s_state != 2){\n        var thediv = document.getElementById(\'cs_partialresults_%(name)s\')\n        thediv.innerHTML = \'Your connection to the server was lost.  Please reload the page.\';\n    }\n}\n\nvar ws_%(name)s_state = -1;\n\nws_%(name)s.onmessage = function(event){\n    var m = event.data;\n    var j = JSON.parse(m);\n    var thediv = document.getElementById(\'cs_partialresults_%(name)s\');\n    var themessage = document.getElementById(\'cs_partialresults_%(name)s_message\');\n    if (j.type == \'ping\'){\n        ws_%(name)s.send(JSON.stringify({type: \'pong\'}));\n    }else if (j.type == \'inqueue\'){\n        ws_%(name)s_state = 0;\n        try{clearInterval(ws_%(name)s_interval);}catch(err){}\n        thediv.classList = \'callout callout-warning\';\n        themessage.innerHTML = \'Your submission (id <code>%(magic)s</code>) is queued to be checked (position \' + j.position + \').\';\n        document.querySelectorAll(\'#%(name)s_buttons button\').forEach(function(b){b.disabled = false;});\n    }else if (j.type == \'running\'){\n        ws_%(name)s_state = 1;\n        try{clearInterval(ws_%(name)s_interval);}catch(err){}\n        thediv.classList = \'callout callout-info\';\n        themessage.innerHTML = \'Your submission is currently being checked<span id="%(name)s_ws_running_time"></span>.\';\n        document.querySelectorAll(\'#%(name)s_buttons button\').forEach(function(b){b.disabled = false;});\n        var sync = ((new Date()).valueOf()/1000 - j.now);\n        ws_%(name)s_interval = setInterval(function(){catsoop.setTimeSince("%(name)s",\n                                                                           j.started,\n                                                                           sync);}, 1000);\n    }else if (j.type == \'newresult\'){\n        ws_%(name)s_state = 2;\n        try{clearInterval(ws_%(name)s_interval);}catch(err){}\n        document.getElementById(\'%(name)s_score_display\').innerHTML = j.score_box;\n        thediv.classList = [];\n        thediv.innerHTML = j.response;\n        catsoop.render_all_math(thediv);\n        catsoop.run_all_scripts(\'cs_partialresults_%(name)s\');\n        document.querySelectorAll(\'#%(name)s_buttons button\').forEach(function(b){b.disabled = false;});\n    }\n}\n\nws_%(name)s.onerror = function(event){\n}\n// @license-end\n</script>\n'