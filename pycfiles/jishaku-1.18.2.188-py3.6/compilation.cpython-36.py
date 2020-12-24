# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/repl/compilation.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 4012 bytes
"""
jishaku.repl.compilation
~~~~~~~~~~~~~~~~~~~~~~~~

Constants, functions and classes related to classifying, compiling and executing Python code.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import ast, asyncio, inspect, import_expression
from jishaku.functools import AsyncSender
from jishaku.repl.scope import Scope
from jishaku.repl.walkers import KeywordTransformer
CORO_CODE = '\nasync def _repl_coroutine({{0}}):\n    import asyncio\n    from importlib import import_module as {0}\n\n    import aiohttp\n    import discord\n    from discord.ext import commands\n\n    try:\n        import jishaku\n    except ImportError:\n        jishaku = None  # keep working even if in panic recovery mode\n\n    try:\n        pass\n    finally:\n        _async_executor.scope.globals.update(locals())\n'.format(import_expression.constants.IMPORTER)

def wrap_code(code: str, args: str='') -> ast.Module:
    """
    Compiles Python code into an async function or generator,
    and automatically adds return if the function body is a single evaluation.
    Also adds inline import expression support.
    """
    user_code = import_expression.parse(code, mode='exec')
    mod = import_expression.parse((CORO_CODE.format(args)), mode='exec')
    definition = mod.body[(-1)]
    if not isinstance(definition, ast.AsyncFunctionDef):
        raise AssertionError
    else:
        try_block = definition.body[(-1)]
        assert isinstance(try_block, ast.Try)
    try_block.body.extend(user_code.body)
    ast.fix_missing_locations(mod)
    KeywordTransformer().generic_visit(try_block)
    last_expr = try_block.body[(-1)]
    if not isinstance(last_expr, ast.Expr):
        return mod
    else:
        if not isinstance(last_expr.value, ast.Yield):
            yield_stmt = ast.Yield(last_expr.value)
            ast.copy_location(yield_stmt, last_expr)
            yield_expr = ast.Expr(yield_stmt)
            ast.copy_location(yield_expr, last_expr)
            try_block.body[-1] = yield_expr
        return mod


class AsyncCodeExecutor:
    __doc__ = "\n    Executes/evaluates Python code inside of an async function or generator.\n\n    Example\n    -------\n\n    .. code:: python3\n\n        total = 0\n\n        # prints 1, 2 and 3\n        async for x in AsyncCodeExecutor('yield 1; yield 2; yield 3'):\n            total += x\n            print(x)\n\n        # prints 6\n        print(total)\n    "
    __slots__ = ('args', 'arg_names', 'code', 'loop', 'scope')

    def __init__(self, code: str, scope: Scope=None, arg_dict: dict=None, loop: asyncio.BaseEventLoop=None):
        self.args = [
         self]
        self.arg_names = ['_async_executor']
        if arg_dict:
            for key, value in arg_dict.items():
                self.arg_names.append(key)
                self.args.append(value)

        self.code = wrap_code(code, args=(', '.join(self.arg_names)))
        self.scope = scope or Scope()
        self.loop = loop or asyncio.get_event_loop()

    def __aiter__(self):
        exec(compile(self.code, '<repl>', 'exec'), self.scope.globals, self.scope.locals)
        func_def = self.scope.locals.get('_repl_coroutine') or self.scope.globals['_repl_coroutine']
        return self.traverse(func_def)

    async def traverse--- This code section failed: ---

 L. 136         0  LOAD_GLOBAL              inspect
                2  LOAD_ATTR                isasyncgenfunction
                4  LOAD_FAST                'func'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  POP_JUMP_IF_FALSE    84  'to 84'

 L. 137        10  SETUP_LOOP          102  'to 102'
               12  LOAD_GLOBAL              AsyncSender
               14  LOAD_FAST                'func'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                args
               20  CALL_FUNCTION_EX      0  'positional arguments only'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  GET_AITER        
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  SETUP_EXCEPT         48  'to 48'
               32  GET_ANEXT        
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'send'
               42  STORE_FAST               'result'
               44  POP_BLOCK        
               46  JUMP_FORWARD         58  'to 58'
             48_0  COME_FROM_EXCEPT     30  '30'
               48  DUP_TOP          
               50  LOAD_GLOBAL              StopAsyncIteration
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_TRUE     70  'to 70'
               56  END_FINALLY      
             58_0  COME_FROM            46  '46'

 L. 138        58  LOAD_FAST                'send'
               60  LOAD_FAST                'result'
               62  YIELD_VALUE      
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  POP_TOP          
               68  JUMP_BACK            30  'to 30'
             70_0  COME_FROM            54  '54'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          
               76  POP_EXCEPT       
               78  POP_TOP          
               80  POP_BLOCK        
             82_0  COME_FROM_LOOP       10  '10'
               82  JUMP_FORWARD        102  'to 102'
               84  ELSE                     '102'

 L. 140        84  LOAD_FAST                'func'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                args
               90  CALL_FUNCTION_EX      0  'positional arguments only'
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  YIELD_VALUE      
              100  POP_TOP          
            102_0  COME_FROM            82  '82'

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 54