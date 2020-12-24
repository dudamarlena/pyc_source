# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/clikan.py
# Compiled at: 2020-04-15 12:52:21
# Size of source mod 2**32: 9597 bytes
import click, yaml, os
from terminaltables import SingleTable
import sys
from textwrap import wrap
import collections, datetime, configparser, pkg_resources
VERSION = pkg_resources.require('clikan')[0].version

class Config(object):
    """Config"""

    def __init__(self):
        self.path = os.getcwd()
        self.aliases = {}

    def read_config(self, filename):
        parser = configparser.RawConfigParser()
        parser.read([filename])
        try:
            self.aliases.update(parser.items('aliases'))
        except configparser.NoSectionError:
            pass


pass_config = click.make_pass_decorator(Config, ensure=True)

class AliasedGroup(click.Group):
    """AliasedGroup"""

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        else:
            cfg = ctx.ensure_object(Config)
            if cmd_name in cfg.aliases:
                actual_cmd = cfg.aliases[cmd_name]
                return click.Group.get_command(self, ctx, actual_cmd)
            matches = [x for x in self.list_commands(ctx) if x.lower().startswith(cmd_name.lower())]
            return matches or None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def read_config(ctx, param, value):
    """Callback that is used whenever --config is passed.  We use this to
    always load the correct config.  This means that the config is loaded
    even if the group itself never executes so our aliases stay always
    available.
    """
    cfg = ctx.ensure_object(Config)
    if value is None:
        value = os.path.join(os.path.dirname(__file__), 'aliases.ini')
    cfg.read_config(value)
    return value


@click.version_option(VERSION)
@click.command(cls=AliasedGroup)
def clikan():
    """clikan: CLI personal kanban """
    pass


@clikan.command()
def configure--- This code section failed: ---

 L.  84         0  LOAD_STR                 '%s/.clikan.dat'
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                environ
                6  LOAD_STR                 'HOME'
                8  BINARY_SUBSCR    
               10  BINARY_MODULO    
               12  STORE_FAST               'path'

 L.  85        14  LOAD_GLOBAL              open
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                environ
               20  LOAD_STR                 'HOME'
               22  BINARY_SUBSCR    
               24  LOAD_STR                 '/.clikan.yaml'
               26  BINARY_ADD       
               28  LOAD_STR                 'w'
               30  CALL_FUNCTION_2       2  ''
               32  SETUP_WITH           60  'to 60'
               34  STORE_FAST               'outfile'

 L.  86        36  LOAD_GLOBAL              yaml
               38  LOAD_ATTR                dump
               40  LOAD_STR                 'clikan_data'
               42  LOAD_FAST                'path'
               44  BUILD_MAP_1           1 
               46  LOAD_FAST                'outfile'
               48  LOAD_CONST               False
               50  LOAD_CONST               ('default_flow_style',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  POP_TOP          
               56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_WITH       32  '32'
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      

 L.  87        66  LOAD_GLOBAL              click
               68  LOAD_METHOD              echo
               70  LOAD_STR                 'Creating %s'
               72  LOAD_FAST                'path'
               74  BINARY_MODULO    
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 58


@clikan.command()
@click.option('--task', prompt=True)
def new(task):
    """Create new task and put it in todo"""
    if len(task) > 40:
        click.echo('Task must be shorter than 40 chars. Brevity counts.')
    else:
        config = read_config_yaml()
        dd = read_data(config)
        todos, inprogs, dones = split_itemsconfigdd
        if 'limits' in config and 'todo' in config['limits'] and int(config['limits']['todo']) <= len(todos):
            click.echo('No new todos, limit reached already.')
        else:
            od = collections.OrderedDict(sorted(dd['data'].items()))
            new_id = 1
            if bool(od):
                new_id = next(reversed(od)) + 1
                dd['data'].update({new_id: ['todo', task, timestamp(), timestamp()]})
            else:
                dd['data'].update({1: ['todo', task, timestamp(), timestamp()]})
            click.echo('Creating new task w/ id: %d -> %s' % (new_id, task))
            write_dataconfigdd


@clikan.command()
@click.option('--id', prompt=True)
def remove(id):
    """Remove task from clikan"""
    config = read_config_yaml()
    dd = read_data(config)
    item = dd['data'].get(int(id))
    if item is None:
        click.echo('No existing task with that id.')
    else:
        item[0] = 'deleted'
        item[2] = timestamp()
        dd['deleted'].update({int(id): item})
        dd['data'].pop(int(id))
        write_dataconfigdd
        click.echo('Removed task %d.' % int(id))


@clikan.command()
@click.option('--id', prompt=True)
def promote(id):
    """Promote task"""
    config = read_config_yaml()
    dd = read_data(config)
    todos, inprogs, dones = split_itemsconfigdd
    item = dd['data'].get(int(id))
    if item[0] == 'todo':
        if 'limits' in config and 'wip' in config['limits'] and int(config['limits']['wip']) <= len(inprogs):
            click.echo('No new tasks, limit reached already.')
        else:
            click.echo('Promoting task %s to in-progress.' % id)
            dd['data'][int(id)] = ['inprogress', item[1], timestamp(), item[3]]
            write_dataconfigdd
    elif item[0] == 'inprogress':
        click.echo('Promoting task %s to done.' % id)
        dd['data'][int(id)] = ['done', item[1], timestamp(), item[3]]
        write_dataconfigdd
    else:
        click.echo('Already done, can not promote %s' % id)


@clikan.command()
@click.option('--id', prompt=True)
def regress(id):
    """Regress task"""
    config = read_config_yaml()
    dd = read_data(config)
    item = dd['data'].get(int(id))
    if item[0] == 'done':
        click.echo('Regressing task %s to in-progress.' % id)
        dd['data'][int(id)] = ['inprogress', item[1], timestamp(), item[3]]
        write_dataconfigdd
    elif item[0] == 'inprogress':
        click.echo('Regressing task %s to todo.' % id)
        dd['data'][int(id)] = ['todo', item[1], timestamp(), item[3]]
        write_dataconfigdd
    else:
        click.echo('Already in todo, can not regress %s' % id)


@clikan.command()
def display():
    """clikan display"""
    config = read_config_yaml()
    dd = read_data(config)
    todos, inprogs, dones = split_itemsconfigdd
    if 'limits' in config and 'done' in config['limits']:
        dones = dones[0:int(config['limits']['done'])]
    else:
        dones = dones[0:10]
    todos = '\n'.join([str(x) for x in todos])
    inprogs = '\n'.join([str(x) for x in inprogs])
    dones = '\n'.join([str(x) for x in dones])
    td = [
     [
      'todo', 'in-progress', 'done'],
     [
      '', '', '']]
    table = SingleTabletd'clikan'
    table.inner_heading_row_border = False
    table.inner_row_border = True
    table.justify_columns = {0:'center',  1:'center',  2:'center'}
    max_width = table.column_max_width(0)
    wrapped_string = '\n'.join(['\n'.join(wrap(line, max_width, break_long_words=False,
      replace_whitespace=False)) for line in todos.splitlines() if line.strip() != ''])
    table.table_data[1][0] = wrapped_string
    max_width = table.column_max_width(1)
    wrapped_inprogs = '\n'.join(['\n'.join(wrap(line, max_width, break_long_words=False,
      replace_whitespace=False)) for line in inprogs.splitlines() if line.strip() != ''])
    table.table_data[1][1] = wrapped_inprogs
    max_width = table.column_max_width(2)
    wrapped_dones = '\n'.join(['\n'.join(wrap(line, max_width, break_long_words=False,
      replace_whitespace=False)) for line in dones.splitlines() if line.strip() != ''])
    table.table_data[1][2] = wrapped_dones
    print(table.table)


def read_data--- This code section failed: ---

 L. 232         0  SETUP_FINALLY       126  'to 126'

 L. 233         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'config'
                6  LOAD_STR                 'clikan_data'
                8  BINARY_SUBSCR    
               10  LOAD_STR                 'r'
               12  CALL_FUNCTION_2       2  ''
               14  SETUP_WITH          116  'to 116'
               16  STORE_FAST               'stream'

 L. 234        18  SETUP_FINALLY        52  'to 52'

 L. 235        20  LOAD_GLOBAL              yaml
               22  LOAD_ATTR                load
               24  LOAD_FAST                'stream'
               26  LOAD_GLOBAL              yaml
               28  LOAD_ATTR                FullLoader
               30  LOAD_CONST               ('Loader',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  POP_BLOCK        
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    18  '18'

 L. 236        52  DUP_TOP          
               54  LOAD_GLOBAL              yaml
               56  LOAD_ATTR                YAMLError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   110  'to 110'
               62  POP_TOP          
               64  STORE_FAST               'exc'
               66  POP_TOP          
               68  SETUP_FINALLY        98  'to 98'

 L. 237        70  LOAD_GLOBAL              print
               72  LOAD_STR                 'Ensure %s exists, as you specified it as the clikan data file.'
               74  LOAD_FAST                'config'
               76  LOAD_STR                 'clikan_data'
               78  BINARY_SUBSCR    
               80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          

 L. 238        86  LOAD_GLOBAL              print
               88  LOAD_FAST                'exc'
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
             98_0  COME_FROM_FINALLY    68  '68'
               98  LOAD_CONST               None
              100  STORE_FAST               'exc'
              102  DELETE_FAST              'exc'
              104  END_FINALLY      
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            60  '60'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_WITH       14  '14'
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  END_FINALLY      
              122  POP_BLOCK        
              124  JUMP_FORWARD        244  'to 244'
            126_0  COME_FROM_FINALLY     0  '0'

 L. 239       126  DUP_TOP          
              128  LOAD_GLOBAL              IOError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   242  'to 242'
              134  POP_TOP          
              136  STORE_FAST               'exc'
              138  POP_TOP          
              140  SETUP_FINALLY       230  'to 230'

 L. 240       142  LOAD_GLOBAL              click
              144  LOAD_METHOD              echo
              146  LOAD_STR                 'No data, initializing data file.'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L. 241       152  LOAD_GLOBAL              write_data
              154  LOAD_FAST                'config'
              156  BUILD_MAP_0           0 
              158  BUILD_MAP_0           0 
              160  LOAD_CONST               ('data', 'deleted')
              162  BUILD_CONST_KEY_MAP_2     2 
              164  CALL_FUNCTION_2       2  ''
              166  POP_TOP          

 L. 242       168  LOAD_GLOBAL              open
              170  LOAD_FAST                'config'
              172  LOAD_STR                 'clikan_data'
              174  BINARY_SUBSCR    
              176  LOAD_STR                 'r'
              178  CALL_FUNCTION_2       2  ''
              180  SETUP_WITH          220  'to 220'
              182  STORE_FAST               'stream'

 L. 243       184  LOAD_GLOBAL              yaml
              186  LOAD_ATTR                load
              188  LOAD_FAST                'stream'
              190  LOAD_GLOBAL              yaml
              192  LOAD_ATTR                FullLoader
              194  LOAD_CONST               ('Loader',)
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  POP_BLOCK        
              200  ROT_TWO          
              202  BEGIN_FINALLY    
              204  WITH_CLEANUP_START
              206  WITH_CLEANUP_FINISH
              208  POP_FINALLY           0  ''
              210  ROT_FOUR         
              212  POP_BLOCK        
              214  POP_EXCEPT       
              216  CALL_FINALLY        230  'to 230'
              218  RETURN_VALUE     
            220_0  COME_FROM_WITH      180  '180'
              220  WITH_CLEANUP_START
              222  WITH_CLEANUP_FINISH
              224  END_FINALLY      
              226  POP_BLOCK        
              228  BEGIN_FINALLY    
            230_0  COME_FROM           216  '216'
            230_1  COME_FROM_FINALLY   140  '140'
              230  LOAD_CONST               None
              232  STORE_FAST               'exc'
              234  DELETE_FAST              'exc'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           132  '132'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           124  '124'

Parse error at or near `POP_BLOCK' instruction at offset 36


def write_data--- This code section failed: ---

 L. 247         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'config'
                4  LOAD_STR                 'clikan_data'
                6  BINARY_SUBSCR    
                8  LOAD_STR                 'w'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           36  'to 36'
               14  STORE_FAST               'outfile'

 L. 248        16  LOAD_GLOBAL              yaml
               18  LOAD_ATTR                dump
               20  LOAD_FAST                'data'
               22  LOAD_FAST                'outfile'
               24  LOAD_CONST               False
               26  LOAD_CONST               ('default_flow_style',)
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  POP_TOP          
               32  POP_BLOCK        
               34  BEGIN_FINALLY    
             36_0  COME_FROM_WITH       12  '12'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 34


def read_config_yaml--- This code section failed: ---

 L. 253         0  SETUP_FINALLY       124  'to 124'

 L. 254         2  LOAD_GLOBAL              open
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                environ
                8  LOAD_STR                 'HOME'
               10  BINARY_SUBSCR    
               12  LOAD_STR                 '/.clikan.yaml'
               14  BINARY_ADD       
               16  LOAD_STR                 'r'
               18  CALL_FUNCTION_2       2  ''
               20  SETUP_WITH          114  'to 114'
               22  STORE_FAST               'stream'

 L. 255        24  SETUP_FINALLY        58  'to 58'

 L. 256        26  LOAD_GLOBAL              yaml
               28  LOAD_ATTR                load
               30  LOAD_FAST                'stream'
               32  LOAD_GLOBAL              yaml
               34  LOAD_ATTR                FullLoader
               36  LOAD_CONST               ('Loader',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  POP_BLOCK        
               42  POP_BLOCK        
               44  ROT_TWO          
               46  BEGIN_FINALLY    
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  POP_FINALLY           0  ''
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    24  '24'

 L. 257        58  DUP_TOP          
               60  LOAD_GLOBAL              yaml
               62  LOAD_ATTR                YAMLError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   108  'to 108'
               68  POP_TOP          
               70  STORE_FAST               'exc'
               72  POP_TOP          
               74  SETUP_FINALLY        96  'to 96'

 L. 258        76  LOAD_GLOBAL              print
               78  LOAD_STR                 'Ensure ~/.clikan.yaml is valid, expected YAML.'
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          

 L. 259        84  LOAD_GLOBAL              sys
               86  LOAD_METHOD              exit
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  BEGIN_FINALLY    
             96_0  COME_FROM_FINALLY    74  '74'
               96  LOAD_CONST               None
               98  STORE_FAST               'exc'
              100  DELETE_FAST              'exc'
              102  END_FINALLY      
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            66  '66'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM_WITH       20  '20'
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      
              120  POP_BLOCK        
              122  JUMP_FORWARD        174  'to 174'
            124_0  COME_FROM_FINALLY     0  '0'

 L. 260       124  DUP_TOP          
              126  LOAD_GLOBAL              IOError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   172  'to 172'
              132  POP_TOP          
              134  STORE_FAST               'exc'
              136  POP_TOP          
              138  SETUP_FINALLY       160  'to 160'

 L. 261       140  LOAD_GLOBAL              print
              142  LOAD_STR                 'Ensure ~/.clikan.yaml exists and is valid.'
              144  CALL_FUNCTION_1       1  ''
              146  POP_TOP          

 L. 262       148  LOAD_GLOBAL              sys
              150  LOAD_METHOD              exit
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          
              156  POP_BLOCK        
              158  BEGIN_FINALLY    
            160_0  COME_FROM_FINALLY   138  '138'
              160  LOAD_CONST               None
              162  STORE_FAST               'exc'
              164  DELETE_FAST              'exc'
              166  END_FINALLY      
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           130  '130'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           122  '122'

Parse error at or near `POP_BLOCK' instruction at offset 42


def split_items(config, dd):
    todos = []
    inprogs = []
    dones = []
    for key, value in dd['data'].items():
        if value[0] == 'todo':
            todos.append('[%d] %s' % (key, value[1]))
        elif value[0] == 'inprogress':
            inprogs.append('[%d] %s' % (key, value[1]))
        else:
            dones.insert(0, '[%d] %s' % (key, value[1]))

    return (todos, inprogs, dones)


def timestamp():
    return '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())