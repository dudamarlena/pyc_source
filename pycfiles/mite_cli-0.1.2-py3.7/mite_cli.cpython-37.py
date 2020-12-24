# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/mite_cli.py
# Compiled at: 2018-11-22 05:43:57
# Size of source mod 2**32: 6522 bytes
import json, os, subprocess, sys, tempfile
from datetime import datetime
from datetime import date as d
import click, yaml
from mite import Mite, errors
if sys.version_info < (3, ):
    input = raw_input
MITE_DIR = os.path.expanduser('~/.mite')
INTERACTIVE_MSG = '(will be added interactively if it is not specified)'

def parse_date(inp):
    return datetime.strptime(inp, '%Y-%m-%d').date()


def has_config():
    return os.path.exists('{}/conf.yaml'.format(MITE_DIR))


def get_config():
    with open('{}/conf.yaml'.format(MITE_DIR)) as (f):
        return yaml.load(f.read())


def edit_subprocess(editor, txt):
    f, name = tempfile.mkstemp()
    os.write(f, bytes(txt, 'ascii'))
    os.close(f)
    rv = subprocess.check_call([editor, name])
    with open(name, 'r') as (f):
        contents = f.read()
    os.remove(name)
    return contents


def editor(txt=''):
    editor = os.environ.get('EDITOR', 'vi')
    return edit_subprocess(editor, txt)


def choose_from_list--- This code section failed: ---

 L.  55         0  LOAD_STR                 ''
                2  STORE_FAST               'chosen'

 L.  56         4  LOAD_GLOBAL              len
                6  LOAD_FAST                'lst'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  LOAD_CONST               1
               12  BINARY_ADD       
               14  STORE_FAST               'max_idx'

 L.  57        16  SETUP_LOOP           64  'to 64'
               18  LOAD_FAST                'chosen'
               20  LOAD_METHOD              isnumeric
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  POP_JUMP_IF_FALSE    52  'to 52'
               26  LOAD_CONST               0
               28  LOAD_GLOBAL              int
               30  LOAD_FAST                'chosen'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  DUP_TOP          
               36  ROT_THREE        
               38  COMPARE_OP               <
               40  POP_JUMP_IF_FALSE    50  'to 50'
               42  LOAD_FAST                'max_idx'
               44  COMPARE_OP               <=
               46  POP_JUMP_IF_TRUE     62  'to 62'
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            40  '40'
               50  POP_TOP          
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            24  '24'

 L.  58        52  LOAD_GLOBAL              input
               54  LOAD_STR                 '> '
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  STORE_FAST               'chosen'
               60  JUMP_BACK            18  'to 18'
             62_0  COME_FROM            46  '46'
               62  POP_BLOCK        
             64_0  COME_FROM_LOOP       16  '16'

 L.  60        64  LOAD_FAST                'lst'
               66  LOAD_GLOBAL              int
               68  LOAD_FAST                'chosen'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  LOAD_CONST               1
               74  BINARY_SUBTRACT  
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'key'
               80  BINARY_SUBSCR    
               82  LOAD_STR                 'id'
               84  BINARY_SUBSCR    
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 62


def get_project(mite):
    projects = mite.list_projects()
    customers = mite.list_customers()
    print(customers)
    print('Choose a project to add the entry to:')
    for idx, thng in enumerate(projects):
        project = thng['project']
        customer_name = ''
        cs = [c for c in customers if c['customer']['id'] == project['customer_id']]
        if cs:
            customer_name = cs[0]['customer']['name']
        print('[{}] {} ({})'.format(idx + 1, project['name'], customer_name))

    return choose_from_list(projects, 'project')


def get_service(mite):
    services = mite.list_services()
    print('Choose a service to add the entry to:')
    for idx, thng in enumerate(services):
        print('[{}] {}'.format(idx + 1, thng['service']['name']))

    return choose_from_list(services, 'service')


def get_entry--- This code section failed: ---

 L.  90         0  LOAD_GLOBAL              print
                2  LOAD_STR                 'Choose an entry:'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  POP_TOP          

 L.  91         8  LOAD_GLOBAL              list
               10  LOAD_GLOBAL              reversed
               12  LOAD_FAST                'mite'
               14  LOAD_ATTR                list_entries
               16  LOAD_STR                 'date'
               18  LOAD_CONST               ('sort',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  STORE_FAST               'entries'

 L.  92        28  SETUP_LOOP          116  'to 116'
               30  LOAD_GLOBAL              enumerate
               32  LOAD_FAST                'entries'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  GET_ITER         
               38  FOR_ITER            114  'to 114'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'idx'
               44  STORE_FAST               'thng'

 L.  93        46  LOAD_FAST                'thng'
               48  LOAD_STR                 'time_entry'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'thng'

 L.  94        54  LOAD_GLOBAL              print
               56  LOAD_STR                 '[{}] {}'
               58  LOAD_METHOD              format
               60  LOAD_FAST                'idx'
               62  LOAD_CONST               1
               64  BINARY_ADD       
               66  LOAD_FAST                'thng'
               68  LOAD_STR                 'date_at'
               70  BINARY_SUBSCR    
               72  CALL_METHOD_2         2  '2 positional arguments'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          

 L.  95        78  LOAD_GLOBAL              print
               80  LOAD_STR                 '\n'
               82  LOAD_METHOD              join
               84  LOAD_GENEXPR             '<code_object <genexpr>>'
               86  LOAD_STR                 'get_entry.<locals>.<genexpr>'
               88  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               90  LOAD_FAST                'thng'
               92  LOAD_STR                 'note'
               94  BINARY_SUBSCR    
               96  LOAD_METHOD              split
               98  LOAD_STR                 '\n'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  POP_TOP          
              112  JUMP_BACK            38  'to 38'
              114  POP_BLOCK        
            116_0  COME_FROM_LOOP       28  '28'

 L.  97       116  LOAD_STR                 ''
              118  STORE_FAST               'chosen'

 L.  98       120  SETUP_LOOP          172  'to 172'
              122  LOAD_FAST                'chosen'
              124  LOAD_METHOD              isnumeric
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  POP_JUMP_IF_FALSE   160  'to 160'
              130  LOAD_CONST               0
              132  LOAD_GLOBAL              int
              134  LOAD_FAST                'chosen'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  DUP_TOP          
              140  ROT_THREE        
              142  COMPARE_OP               <
              144  POP_JUMP_IF_FALSE   158  'to 158'
              146  LOAD_FAST                'idx'
              148  LOAD_CONST               1
              150  BINARY_ADD       
              152  COMPARE_OP               <=
              154  POP_JUMP_IF_TRUE    170  'to 170'
              156  JUMP_FORWARD        160  'to 160'
            158_0  COME_FROM           144  '144'
              158  POP_TOP          
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           128  '128'

 L.  99       160  LOAD_GLOBAL              input
              162  LOAD_STR                 '> '
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  STORE_FAST               'chosen'
              168  JUMP_BACK           122  'to 122'
            170_0  COME_FROM           154  '154'
              170  POP_BLOCK        
            172_0  COME_FROM_LOOP      120  '120'

 L. 101       172  LOAD_FAST                'entries'
              174  LOAD_GLOBAL              int
              176  LOAD_FAST                'chosen'
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  LOAD_CONST               1
              182  BINARY_SUBTRACT  
              184  BINARY_SUBSCR    
              186  LOAD_STR                 'time_entry'
              188  BINARY_SUBSCR    
              190  LOAD_STR                 'id'
              192  BINARY_SUBSCR    
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 170


@click.group()
@click.version_option('0.0.1')
@click.pass_context
def cli(ctx):
    ctx.obj = None
    if has_config():
        conf = get_config()
        ctx.obj = Mite(conf['team'], conf['api_key'])


@cli.command()
@click.pass_obj
def projects(mite):
    for proj in mite.list_projects():
        proj = proj['project']
        print('{}: {}'.format(proj['id'], proj['name']))


@cli.command()
@click.pass_obj
def services(mite):
    for serv in mite.list_services():
        serv = serv['service']
        print('{}: {}'.format(serv['id'], serv['name']))


@cli.command()
@click.pass_obj
def entries(mite):
    for entry in reversed(mite.list_entries(sort='date')):
        entry = entry['time_entry']
        print('{}: {}'.format(entry['id'], entry['date_at']))
        print('\n'.join(('   {}'.format(l) for l in entry['note'].split('\n'))))


@cli.command()
@click.option('--team', required=True, help='The team name on mite (corresponds to your subdomain).')
@click.option('--api-key', required=True, help='Your API key (you can generate it in your settings).')
def init(team, api_key):
    os.makedirs(MITE_DIR, exist_ok=True)
    with open('{}/conf.yaml'.format(MITE_DIR), 'w+') as (f):
        f.write(yaml.dump({'team':team,  'api_key':api_key}))


@cli.command()
@click.option('--date', default=None, help='The date in YYYY-MM-DD format.')
@click.option('--minutes', default=480, help='The number of minutes.')
@click.option('--project-id', default=None, help=('Project ID {}.'.format(INTERACTIVE_MSG)))
@click.option('--service-id', default=None, help=('Service ID {}.'.format(INTERACTIVE_MSG)))
@click.option('--note', default=None, help=('Body message {}.'.format(INTERACTIVE_MSG)))
@click.pass_obj
def add(mite, date, minutes, project_id, service_id, note):
    given_pid = True
    given_sid = True
    if not note:
        note = editor()
    if not project_id:
        given_pid = False
        project_id = get_project(mite)
    else:
        if not service_id:
            given_sid = False
            service_id = get_service(mite)
            print(project_id)
        if date:
            date = parse_date(date)
        else:
            date = d.today()
    res = mite.create_entry(date_at=(str(date)),
      minutes=minutes,
      note=note,
      project_id=project_id,
      service_id=service_id)
    print('Entry created for {}!'.format(date))
    if not given_pid:
        print('  Project ID: {}'.format(project_id))
    if not given_sid:
        print('  Service ID: {}'.format(service_id))


@cli.command()
@click.option('--id', default=0, help='The entry ID.')
@click.option('--date', default=None, help='The date in YYYY-MM-DD format.')
@click.option('--minutes', default=480, help='The number of minutes.')
@click.option('--project-id', default=None, help=('Project ID {}.'.format(INTERACTIVE_MSG)))
@click.option('--service-id', default=None, help=('Service ID {}.'.format(INTERACTIVE_MSG)))
@click.option('--note', default=None, help=('Body message {}.'.format(INTERACTIVE_MSG)))
@click.pass_obj
def edit(mite, id, date, minutes, project_id, service_id, note):
    if not id:
        id = get_entry(mite)
    else:
        entry = mite.get_entry(id)['time_entry']
        if not note:
            note = editor(entry['note'])
        if not project_id:
            project_id = entry['project_id']
        service_id = service_id or entry['service_id']
    date = parse_date(date or entry['date_at'])
    res = mite.edit_entry(id,
      date_at=(str(date)),
      minutes=minutes,
      note=note,
      project_id=project_id,
      service_id=service_id)
    print('Entry edited for {}!'.format(date))


if __name__ == '__main__':
    cli()