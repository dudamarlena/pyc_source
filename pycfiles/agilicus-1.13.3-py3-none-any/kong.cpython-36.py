# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/kong.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 1085 bytes
import click
from kong.client import Kong, KongError
from .repo import RepoManager
from . import utils

@click.command()
@click.pass_context
@click.option('--namespace', default='dev', help='target namespace')
@click.option('--yes',
  is_flag=True, help='commit changes to kong',
  default=False)
def kong(ctx, namespace, yes):
    """Update the kong configuration
    """
    m = KongManager((ctx.obj['agile']), namespace=namespace)
    click.echo(utils.niceJson(m.create_kong(yes)))


class KongManager(RepoManager):

    def create_kong(self, yes):
        data = self.load_data('values.yaml')
        values = data.copy()
        manifest = self.manifest(values, 'kong.yaml')
        if yes:
            return self.wait(self.apply_kong(manifest))
        else:
            return manifest

    async def apply_kong--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL              Kong
                2  CALL_FUNCTION_0       0  ''
                4  BEFORE_ASYNC_WITH
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  SETUP_ASYNC_WITH     94  'to 94'
               14  STORE_FAST               'cli'

 L.  35        16  SETUP_EXCEPT         38  'to 38'

 L.  36        18  LOAD_FAST                'cli'
               20  LOAD_ATTR                apply_json
               22  LOAD_FAST                'manifest'
               24  CALL_FUNCTION_1       1  ''
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  STORE_FAST               'result'
               34  POP_BLOCK        
               36  JUMP_FORWARD         90  'to 90'
             38_0  COME_FROM_EXCEPT     16  '16'

 L.  37        38  DUP_TOP          
               40  LOAD_GLOBAL              KongError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    88  'to 88'
               46  POP_TOP          
               48  STORE_FAST               'exc'
               50  POP_TOP          
               52  SETUP_FINALLY        78  'to 78'

 L.  38        54  LOAD_GLOBAL              utils
               56  LOAD_ATTR                CommandError
               58  LOAD_STR                 'Kong Error: '
               60  LOAD_FAST                'exc'
               62  FORMAT_VALUE          0  ''
               64  BUILD_STRING_2        2 
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               None
               70  RAISE_VARARGS_2       2  ''
               72  POP_BLOCK        
               74  POP_EXCEPT       
               76  LOAD_CONST               None
             78_0  COME_FROM_FINALLY    52  '52'
               78  LOAD_CONST               None
               80  STORE_FAST               'exc'
               82  DELETE_FAST              'exc'
               84  END_FINALLY      
               86  JUMP_FORWARD         90  'to 90'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            36  '36'

 L.  39        90  LOAD_FAST                'result'
               92  RETURN_VALUE     
             94_0  COME_FROM_ASYNC_WITH    12  '12'
               94  WITH_CLEANUP_START
               96  GET_AWAITABLE    
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  WITH_CLEANUP_FINISH
              104  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 94_0