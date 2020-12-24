# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/cog_base.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 27197 bytes
"""
jishaku.cog_base
~~~~~~~~~~~~~~~~~

The Jishaku cog base, which contains most of the actual functionality of Jishaku.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import asyncio, collections, contextlib, datetime, inspect, io, itertools, os, os.path, re, time, traceback, typing, aiohttp, discord
from discord.ext import commands
from jishaku.codeblocks import Codeblock, codeblock_converter
from jishaku.exception_handling import ReplResponseReactor
from jishaku.flags import JISHAKU_RETAIN, SCOPE_PREFIX
from jishaku.functools import AsyncSender
from jishaku.models import copy_context_with
from jishaku.modules import ExtensionConverter
from jishaku.paginators import PaginatorInterface, WrappedFilePaginator, WrappedPaginator
from jishaku.repl import AsyncCodeExecutor, Scope, all_inspections, get_var_dict_from_ctx
from jishaku.shell import ShellReader
from jishaku.voice import BasicYouTubeDLSource, connected_check, playing_check, vc_check, youtube_dl
__all__ = ('JishakuBase', )
CommandTask = collections.namedtuple('CommandTask', 'index ctx task')

class JishakuBase(commands.Cog):
    __doc__ = "\n    The cog that includes Jishaku's Discord-facing default functionality.\n    "
    load_time = datetime.datetime.now()

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._scope = Scope()
        self.retain = JISHAKU_RETAIN
        self.last_result = None
        self.start_time = datetime.datetime.now()
        self.tasks = collections.deque()
        self.task_count = 0

    @property
    def scope(self):
        """
        Gets a scope for use in REPL.

        If retention is on, this is the internal stored scope,
        otherwise it is always a new Scope.
        """
        if self.retain:
            return self._scope
        else:
            return Scope()

    @contextlib.contextmanager
    def submit(self, ctx: commands.Context):
        """
        A context-manager that submits the current task to jishaku's task list
        and removes it afterwards.

        Parameters
        -----------
        ctx: commands.Context
            A Context object used to derive information about this command task.
        """
        self.task_count += 1
        cmdtask = CommandTask(self.task_count, ctx, asyncio.Task.current_task())
        self.tasks.append(cmdtask)
        try:
            yield cmdtask
        finally:
            if cmdtask in self.tasks:
                self.tasks.remove(cmdtask)

    async def cog_check(self, ctx: commands.Context):
        """
        Local check, makes all commands in this cog owner-only
        """
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner('You must own this bot to use Jishaku.')
        return True

    @commands.command(name='hide')
    async def jsk_hide(self, ctx: commands.Context):
        """
        Hides Jishaku from the help command.
        """
        if self.jsk.hidden:
            return await ctx.send('Jishaku is already hidden.')
        self.jsk.hidden = True
        await ctx.send('Jishaku is now hidden.')

    @commands.command(name='show')
    async def jsk_show(self, ctx: commands.Context):
        """
        Shows Jishaku in the help command.
        """
        if not self.jsk.hidden:
            return await ctx.send('Jishaku is already visible.')
        self.jsk.hidden = False
        await ctx.send('Jishaku is now visible.')

    @commands.command(name='tasks')
    async def jsk_tasks(self, ctx: commands.Context):
        """
        Shows the currently running jishaku tasks.
        """
        if not self.tasks:
            return await ctx.send('No currently running tasks.')
        else:
            paginator = commands.Paginator(max_size=1985)
            for task in self.tasks:
                paginator.add_line(f"{task.index}: `{task.ctx.command.qualified_name}`, invoked at {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")

            interface = PaginatorInterface((ctx.bot), paginator, owner=(ctx.author))
            return await interface.send_to(ctx)

    @commands.command(name='cancel')
    async def jsk_cancel(self, ctx: commands.Context, *, index: int):
        """
        Cancels a task with the given index.

        If the index passed is -1, will cancel the last task instead.
        """
        if not self.tasks:
            return await ctx.send('No tasks to cancel.')
        else:
            if index == -1:
                task = self.tasks.pop()
            else:
                task = discord.utils.get((self.tasks), index=index)
                if task:
                    self.tasks.remove(task)
                else:
                    return await ctx.send('Unknown task.')
            task.task.cancel()
            return await ctx.send(f"Cancelled task {task.index}: `{task.ctx.command.qualified_name}`, invoked at {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")

    @commands.command(name='load', aliases=['reload'])
    async def jsk_load(self, ctx: commands.Context, *extensions: ExtensionConverter):
        """
        Loads or reloads the given extension names.

        Reports any extensions that failed to load.
        """
        paginator = WrappedPaginator(prefix='', suffix='')
        for extension in (itertools.chain)(*extensions):
            method, icon = (self.bot.reload_extension, '🔁') if extension in self.bot.extensions else (
             self.bot.load_extension, '📥')
            try:
                method(extension)
            except Exception as exc:
                traceback_data = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__, 1))
                paginator.add_line(f"{icon}⚠ `{extension}`\n```py\n{traceback_data}\n```",
                  empty=True)
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.send(page)

    @commands.command(name='unload')
    async def jsk_unload(self, ctx: commands.Context, *extensions: ExtensionConverter):
        """
        Unloads the given extension names.

        Reports any extensions that failed to unload.
        """
        paginator = WrappedPaginator(prefix='', suffix='')
        icon = '📤'
        for extension in (itertools.chain)(*extensions):
            try:
                self.bot.unload_extension(extension)
            except Exception as exc:
                traceback_data = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__, 1))
                paginator.add_line(f"{icon}⚠ `{extension}`\n```py\n{traceback_data}\n```",
                  empty=True)
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.send(page)

    @commands.command(name='shutdown', aliases=['logout'])
    async def jsk_shutdown(self, ctx: commands.Context):
        """
        Logs this bot out.
        """
        await ctx.send('Logging out now⠴')
        await ctx.bot.logout()

    @commands.command(name='su')
    async def jsk_su(self, ctx: commands.Context, target: discord.User, *, command_string: str):
        """
        Run a command as someone else.

        This will try to resolve to a Member, but will use a User if it can't find one.
        """
        if ctx.guild:
            target = ctx.guild.get_member(target.id) or target
        alt_ctx = await copy_context_with(ctx, author=target, content=(ctx.prefix + command_string))
        if alt_ctx.command is None:
            if alt_ctx.invoked_with is None:
                return await ctx.send('This bot has been hard-configured to ignore this user.')
            return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')
        else:
            return await alt_ctx.command.invoke(alt_ctx)

    @commands.command(name='in')
    async def jsk_in(self, ctx: commands.Context, channel: discord.TextChannel, *, command_string: str):
        """
        Run a command as if it were run in a different channel.
        """
        alt_ctx = await copy_context_with(ctx, channel=channel, content=(ctx.prefix + command_string))
        if alt_ctx.command is None:
            return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')
        else:
            return await alt_ctx.command.invoke(alt_ctx)

    @commands.command(name='sudo')
    async def jsk_sudo(self, ctx: commands.Context, *, command_string: str):
        """
        Run a command bypassing all checks and cooldowns.

        This also bypasses permission checks so this has a high possibility of making commands raise exceptions.
        """
        alt_ctx = await copy_context_with(ctx, content=(ctx.prefix + command_string))
        if alt_ctx.command is None:
            return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')
        else:
            return await alt_ctx.command.reinvoke(alt_ctx)

    @commands.command(name='repeat')
    async def jsk_repeat(self, ctx: commands.Context, times: int, *, command_string: str):
        """
        Runs a command multiple times in a row.

        This acts like the command was invoked several times manually, so it obeys cooldowns.
        You can use this in conjunction with `jsk sudo` to bypass this.
        """
        with self.submit(ctx):
            for _ in range(times):
                alt_ctx = await copy_context_with(ctx, content=(ctx.prefix + command_string))
                if alt_ctx.command is None:
                    return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')
                await alt_ctx.command.reinvoke(alt_ctx)

    @commands.command(name='debug', aliases=['dbg'])
    async def jsk_debug(self, ctx: commands.Context, *, command_string: str):
        """
        Run a command timing execution and catching exceptions.
        """
        alt_ctx = await copy_context_with(ctx, content=(ctx.prefix + command_string))
        if alt_ctx.command is None:
            return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')
        else:
            start = time.perf_counter()
            async with ReplResponseReactor(ctx.message):
                with self.submit(ctx):
                    await alt_ctx.command.invoke(alt_ctx)
            end = time.perf_counter()
            return await ctx.send(f"Command `{alt_ctx.command.qualified_name}` finished in {end - start:.3f}s.")

    _JishakuBase__cat_line_regex = re.compile('(?:\\.\\/+)?(.+?)(?:#L?(\\d+)(?:\\-L?(\\d+))?)?$')

    @commands.command(name='cat')
    async def jsk_cat(self, ctx: commands.Context, argument: str):
        """
        Read out a file, using syntax highlighting if detected.

        Lines and linespans are supported by adding '#L12' or '#L12-14' etc to the end of the filename.
        """
        match = self._JishakuBase__cat_line_regex.search(argument)
        if not match:
            return await ctx.send("Couldn't parse this input.")
        path = match.group(1)
        line_span = None
        if match.group(2):
            start = int(match.group(2))
            line_span = (start, int(match.group(3) or start))
        if not os.path.exists(path) or os.path.isdir(path):
            return await ctx.send(f"`{path}`: No file by that name.")
        size = os.path.getsize(path)
        if size <= 0:
            return await ctx.send(f"`{path}`: Cowardly refusing to read a file with no size stat (it may be empty, endless or inaccessible).")
        if size > 52428800:
            return await ctx.send(f"`{path}`: Cowardly refusing to read a file >50MB.")
        try:
            with open(path, 'rb') as (file):
                paginator = WrappedFilePaginator(file, line_span=line_span, max_size=1985)
        except UnicodeDecodeError:
            return await ctx.send(f"`{path}`: Couldn't determine the encoding of this file.")
        except ValueError as exc:
            return await ctx.send(f"`{path}`: Couldn't read this file, {exc}")

        interface = PaginatorInterface((ctx.bot), paginator, owner=(ctx.author))
        await interface.send_to(ctx)

    @commands.command(name='curl')
    async def jsk_curl(self, ctx: commands.Context, url: str):
        """
        Download and display a text file from the internet.

        This command is similar to jsk cat, but accepts a URL.
        """
        url = url.lstrip('<').rstrip('>')
        async with ReplResponseReactor(ctx.message):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.read()
                    hints = (
                     response.content_type,
                     url)
                    code = response.status
            if not data:
                return await ctx.send(f"HTTP response was empty (status code {code}).")
            try:
                paginator = WrappedFilePaginator((io.BytesIO(data)), language_hints=hints, max_size=1985)
            except UnicodeDecodeError:
                return await ctx.send(f"Couldn't determine the encoding of the response. (status code {code})")
            except ValueError as exc:
                return await ctx.send(f"Couldn't read response (status code {code}), {exc}")

            interface = PaginatorInterface((ctx.bot), paginator, owner=(ctx.author))
            await interface.send_to(ctx)

    @commands.command(name='source', aliases=['src'])
    async def jsk_source(self, ctx: commands.Context, *, command_name: str):
        """
        Displays the source code for a command.
        """
        command = self.bot.get_command(command_name)
        if not command:
            return await ctx.send(f"Couldn't find command `{command_name}`.")
        try:
            source_lines, _ = inspect.getsourcelines(command.callback)
        except (TypeError, OSError):
            return await ctx.send(f"Was unable to retrieve the source for `{command}` for some reason.")
        else:
            source_lines = ''.join(source_lines).split('\n')
            paginator = WrappedPaginator(prefix='```py', suffix='```', max_size=1985)
            for line in source_lines:
                paginator.add_line(line)

            interface = PaginatorInterface((ctx.bot), paginator, owner=(ctx.author))
            await interface.send_to(ctx)

    @commands.command(name='retain')
    async def jsk_retain(self, ctx: commands.Context, *, toggle: bool=None):
        """
        Turn variable retention for REPL on or off.

        Provide no argument for current status.
        """
        if toggle is None:
            if self.retain:
                return await ctx.send('Variable retention is set to ON.')
            return await ctx.send('Variable retention is set to OFF.')
        else:
            if toggle:
                if self.retain:
                    return await ctx.send('Variable retention is already set to ON.')
                else:
                    self.retain = True
                    self._scope = Scope()
                    return await ctx.send('Variable retention is ON. Future REPL sessions will retain their scope.')
            if not self.retain:
                return await ctx.send('Variable retention is already set to OFF.')
            self.retain = False
            return await ctx.send('Variable retention is OFF. Future REPL sessions will dispose their scope when done.')

    @commands.command(name='py', aliases=['python'])
    async def jsk_python--- This code section failed: ---

 L. 480         0  LOAD_GLOBAL              get_var_dict_from_ctx
                2  LOAD_FAST                'ctx'
                4  LOAD_GLOBAL              SCOPE_PREFIX
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'arg_dict'

 L. 481        10  LOAD_FAST                'self'
               12  LOAD_ATTR                last_result
               14  LOAD_FAST                'arg_dict'
               16  LOAD_STR                 '_'
               18  STORE_SUBSCR     

 L. 483        20  LOAD_FAST                'self'
               22  LOAD_ATTR                scope
               24  STORE_FAST               'scope'

 L. 485        26  SETUP_FINALLY       442  'to 442'

 L. 486        30  LOAD_GLOBAL              ReplResponseReactor
               32  LOAD_FAST                'ctx'
               34  LOAD_ATTR                message
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    426  'to 426'
               50  POP_TOP          

 L. 487        52  LOAD_FAST                'self'
               54  LOAD_ATTR                submit
               56  LOAD_FAST                'ctx'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  SETUP_WITH          416  'to 416'
               64  POP_TOP          

 L. 488        66  LOAD_GLOBAL              AsyncCodeExecutor
               68  LOAD_FAST                'argument'
               70  LOAD_ATTR                content
               72  LOAD_FAST                'scope'
               74  LOAD_FAST                'arg_dict'
               76  LOAD_CONST               ('arg_dict',)
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'executor'

 L. 489        82  SETUP_LOOP          412  'to 412'
               86  LOAD_GLOBAL              AsyncSender
               88  LOAD_FAST                'executor'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  GET_AITER        
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  SETUP_EXCEPT        116  'to 116'
              100  GET_ANEXT        
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'send'
              110  STORE_FAST               'result'
              112  POP_BLOCK        
              114  JUMP_FORWARD        128  'to 128'
            116_0  COME_FROM_EXCEPT     98  '98'
              116  DUP_TOP          
              118  LOAD_GLOBAL              StopAsyncIteration
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_TRUE    400  'to 400'
              126  END_FINALLY      
            128_0  COME_FROM           114  '114'

 L. 490       128  LOAD_FAST                'result'
              130  LOAD_CONST               None
              132  COMPARE_OP               is
              134  POP_JUMP_IF_FALSE   138  'to 138'

 L. 491       136  CONTINUE             98  'to 98'
              138  ELSE                     '398'

 L. 493       138  LOAD_FAST                'result'
              140  LOAD_FAST                'self'
              142  STORE_ATTR               last_result

 L. 495       144  LOAD_GLOBAL              isinstance
              146  LOAD_FAST                'result'
              148  LOAD_GLOBAL              discord
              150  LOAD_ATTR                File
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  POP_JUMP_IF_FALSE   180  'to 180'

 L. 496       156  LOAD_FAST                'send'
              158  LOAD_FAST                'ctx'
              160  LOAD_ATTR                send
              162  LOAD_FAST                'result'
              164  LOAD_CONST               ('file',)
              166  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              168  GET_AWAITABLE    
              170  LOAD_CONST               None
              172  YIELD_FROM       
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  POP_TOP          
              178  JUMP_BACK            98  'to 98'
              180  ELSE                     '398'

 L. 497       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'result'
              184  LOAD_GLOBAL              discord
              186  LOAD_ATTR                Embed
              188  CALL_FUNCTION_2       2  '2 positional arguments'
              190  POP_JUMP_IF_FALSE   216  'to 216'

 L. 498       192  LOAD_FAST                'send'
              194  LOAD_FAST                'ctx'
              196  LOAD_ATTR                send
              198  LOAD_FAST                'result'
              200  LOAD_CONST               ('embed',)
              202  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              204  GET_AWAITABLE    
              206  LOAD_CONST               None
              208  YIELD_FROM       
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  POP_TOP          
              214  JUMP_BACK            98  'to 98'
              216  ELSE                     '398'

 L. 499       216  LOAD_GLOBAL              isinstance
              218  LOAD_FAST                'result'
              220  LOAD_GLOBAL              PaginatorInterface
              222  CALL_FUNCTION_2       2  '2 positional arguments'
              224  POP_JUMP_IF_FALSE   248  'to 248'

 L. 500       226  LOAD_FAST                'send'
              228  LOAD_FAST                'result'
              230  LOAD_ATTR                send_to
              232  LOAD_FAST                'ctx'
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  GET_AWAITABLE    
              238  LOAD_CONST               None
              240  YIELD_FROM       
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  POP_TOP          
              246  JUMP_BACK            98  'to 98'
              248  ELSE                     '398'

 L. 502       248  LOAD_GLOBAL              isinstance
              250  LOAD_FAST                'result'
              252  LOAD_GLOBAL              str
              254  CALL_FUNCTION_2       2  '2 positional arguments'
              256  POP_JUMP_IF_TRUE    268  'to 268'

 L. 504       260  LOAD_GLOBAL              repr
              262  LOAD_FAST                'result'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  STORE_FAST               'result'
            268_0  COME_FROM           256  '256'

 L. 506       268  LOAD_GLOBAL              len
              270  LOAD_FAST                'result'
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  LOAD_CONST               2000
              276  COMPARE_OP               >
              278  POP_JUMP_IF_FALSE   346  'to 346'

 L. 509       282  LOAD_GLOBAL              WrappedPaginator
              284  LOAD_STR                 '```py'
              286  LOAD_STR                 '```'
              288  LOAD_CONST               1985
              290  LOAD_CONST               ('prefix', 'suffix', 'max_size')
              292  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              294  STORE_FAST               'paginator'

 L. 511       296  LOAD_FAST                'paginator'
              298  LOAD_ATTR                add_line
              300  LOAD_FAST                'result'
              302  CALL_FUNCTION_1       1  '1 positional argument'
              304  POP_TOP          

 L. 513       306  LOAD_GLOBAL              PaginatorInterface
              308  LOAD_FAST                'ctx'
              310  LOAD_ATTR                bot
              312  LOAD_FAST                'paginator'
              314  LOAD_FAST                'ctx'
              316  LOAD_ATTR                author
              318  LOAD_CONST               ('owner',)
              320  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              322  STORE_FAST               'interface'

 L. 514       324  LOAD_FAST                'send'
              326  LOAD_FAST                'interface'
              328  LOAD_ATTR                send_to
              330  LOAD_FAST                'ctx'
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  GET_AWAITABLE    
              336  LOAD_CONST               None
              338  YIELD_FROM       
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  POP_TOP          
              344  JUMP_BACK            98  'to 98'
              346  ELSE                     '398'

 L. 516       346  LOAD_FAST                'result'
              348  LOAD_ATTR                strip
              350  CALL_FUNCTION_0       0  '0 positional arguments'
              352  LOAD_STR                 ''
              354  COMPARE_OP               ==
              356  POP_JUMP_IF_FALSE   364  'to 364'

 L. 517       360  LOAD_STR                 '\u200b'
              362  STORE_FAST               'result'
            364_0  COME_FROM           356  '356'

 L. 519       364  LOAD_FAST                'send'
              366  LOAD_FAST                'ctx'
              368  LOAD_ATTR                send
              370  LOAD_FAST                'result'
              372  LOAD_ATTR                replace
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                bot
              378  LOAD_ATTR                http
              380  LOAD_ATTR                token
              382  LOAD_STR                 '[token omitted]'
              384  CALL_FUNCTION_2       2  '2 positional arguments'
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  GET_AWAITABLE    
              390  LOAD_CONST               None
              392  YIELD_FROM       
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  POP_TOP          
              398  JUMP_BACK            98  'to 98'
            400_0  COME_FROM           122  '122'
              400  POP_TOP          
              402  POP_TOP          
              404  POP_TOP          
              406  POP_EXCEPT       
              408  POP_TOP          
              410  POP_BLOCK        
            412_0  COME_FROM_LOOP       82  '82'
              412  POP_BLOCK        
              414  LOAD_CONST               None
            416_0  COME_FROM_WITH       60  '60'
              416  WITH_CLEANUP_START
              418  WITH_CLEANUP_FINISH
              420  END_FINALLY      
              422  POP_BLOCK        
              424  LOAD_CONST               None
            426_0  COME_FROM_ASYNC_WITH    46  '46'
              426  WITH_CLEANUP_START
              428  GET_AWAITABLE    
              430  LOAD_CONST               None
              432  YIELD_FROM       
              434  WITH_CLEANUP_FINISH
              436  END_FINALLY      
              438  POP_BLOCK        
              440  LOAD_CONST               None
            442_0  COME_FROM_FINALLY    26  '26'

 L. 521       442  LOAD_FAST                'scope'
              444  LOAD_ATTR                clear_intersection
              446  LOAD_FAST                'arg_dict'
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  POP_TOP          
              452  END_FINALLY      

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 122

    @commands.command(name='py_inspect', aliases=['pyi', 'python_inspect', 'pythoninspect'])
    async def jsk_python_inspect--- This code section failed: ---

 L. 529         0  LOAD_GLOBAL              get_var_dict_from_ctx
                2  LOAD_FAST                'ctx'
                4  LOAD_GLOBAL              SCOPE_PREFIX
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'arg_dict'

 L. 530        10  LOAD_FAST                'self'
               12  LOAD_ATTR                last_result
               14  LOAD_FAST                'arg_dict'
               16  LOAD_STR                 '_'
               18  STORE_SUBSCR     

 L. 532        20  LOAD_FAST                'self'
               22  LOAD_ATTR                scope
               24  STORE_FAST               'scope'

 L. 534        26  SETUP_FINALLY       334  'to 334'

 L. 535        30  LOAD_GLOBAL              ReplResponseReactor
               32  LOAD_FAST                'ctx'
               34  LOAD_ATTR                message
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    318  'to 318'
               50  POP_TOP          

 L. 536        52  LOAD_FAST                'self'
               54  LOAD_ATTR                submit
               56  LOAD_FAST                'ctx'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  SETUP_WITH          308  'to 308'
               62  POP_TOP          

 L. 537        64  LOAD_GLOBAL              AsyncCodeExecutor
               66  LOAD_FAST                'argument'
               68  LOAD_ATTR                content
               70  LOAD_FAST                'scope'
               72  LOAD_FAST                'arg_dict'
               74  LOAD_CONST               ('arg_dict',)
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               'executor'

 L. 538        80  SETUP_LOOP          304  'to 304'
               82  LOAD_GLOBAL              AsyncSender
               84  LOAD_FAST                'executor'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  GET_AITER        
               90  LOAD_CONST               None
               92  YIELD_FROM       
               94  SETUP_EXCEPT        112  'to 112'
               96  GET_ANEXT        
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'send'
              106  STORE_FAST               'result'
              108  POP_BLOCK        
              110  JUMP_FORWARD        124  'to 124'
            112_0  COME_FROM_EXCEPT     94  '94'
              112  DUP_TOP          
              114  LOAD_GLOBAL              StopAsyncIteration
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_TRUE    292  'to 292'
              122  END_FINALLY      
            124_0  COME_FROM           110  '110'

 L. 539       124  LOAD_FAST                'result'
              126  LOAD_FAST                'self'
              128  STORE_ATTR               last_result

 L. 541       130  LOAD_GLOBAL              repr
              132  LOAD_FAST                'result'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  LOAD_ATTR                replace
              138  LOAD_STR                 '``'
              140  LOAD_STR                 '`\u200b`'
              142  CALL_FUNCTION_2       2  '2 positional arguments'
              144  LOAD_ATTR                replace
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                bot
              150  LOAD_ATTR                http
              152  LOAD_ATTR                token
              154  LOAD_STR                 '[token omitted]'
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  STORE_FAST               'header'

 L. 543       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'header'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  LOAD_CONST               485
              168  COMPARE_OP               >
              170  POP_JUMP_IF_FALSE   188  'to 188'

 L. 544       172  LOAD_FAST                'header'
              174  LOAD_CONST               0
              176  LOAD_CONST               482
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  LOAD_STR                 '...'
              184  BINARY_ADD       
              186  STORE_FAST               'header'
            188_0  COME_FROM           170  '170'

 L. 546       188  LOAD_GLOBAL              WrappedPaginator
              190  LOAD_STR                 '```prolog\n=== '
              192  LOAD_FAST                'header'
              194  FORMAT_VALUE          0  ''
              196  LOAD_STR                 ' ===\n'
              198  BUILD_STRING_3        3 
              200  LOAD_CONST               1985
              202  LOAD_CONST               ('prefix', 'max_size')
              204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              206  STORE_FAST               'paginator'

 L. 548       208  SETUP_LOOP          252  'to 252'
              210  LOAD_GLOBAL              all_inspections
              212  LOAD_FAST                'result'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  GET_ITER         
              218  FOR_ITER            250  'to 250'
              220  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST               'name'
              224  STORE_FAST               'res'

 L. 549       226  LOAD_FAST                'paginator'
              228  LOAD_ATTR                add_line
              230  LOAD_FAST                'name'
              232  LOAD_STR                 '16.16'
              234  FORMAT_VALUE_ATTR     4  ''
              236  LOAD_STR                 ' :: '
              238  LOAD_FAST                'res'
              240  FORMAT_VALUE          0  ''
              242  BUILD_STRING_3        3 
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  POP_TOP          
              248  JUMP_BACK           218  'to 218'
              250  POP_BLOCK        
            252_0  COME_FROM_LOOP      208  '208'

 L. 551       252  LOAD_GLOBAL              PaginatorInterface
              254  LOAD_FAST                'ctx'
              256  LOAD_ATTR                bot
              258  LOAD_FAST                'paginator'
              260  LOAD_FAST                'ctx'
              262  LOAD_ATTR                author
              264  LOAD_CONST               ('owner',)
              266  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              268  STORE_FAST               'interface'

 L. 552       270  LOAD_FAST                'send'
              272  LOAD_FAST                'interface'
              274  LOAD_ATTR                send_to
              276  LOAD_FAST                'ctx'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  GET_AWAITABLE    
              282  LOAD_CONST               None
              284  YIELD_FROM       
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  POP_TOP          
              290  JUMP_BACK            94  'to 94'
            292_0  COME_FROM           118  '118'
              292  POP_TOP          
              294  POP_TOP          
              296  POP_TOP          
              298  POP_EXCEPT       
              300  POP_TOP          
              302  POP_BLOCK        
            304_0  COME_FROM_LOOP       80  '80'
              304  POP_BLOCK        
              306  LOAD_CONST               None
            308_0  COME_FROM_WITH       60  '60'
              308  WITH_CLEANUP_START
              310  WITH_CLEANUP_FINISH
              312  END_FINALLY      
              314  POP_BLOCK        
              316  LOAD_CONST               None
            318_0  COME_FROM_ASYNC_WITH    46  '46'
              318  WITH_CLEANUP_START
              320  GET_AWAITABLE    
              322  LOAD_CONST               None
              324  YIELD_FROM       
              326  WITH_CLEANUP_FINISH
              328  END_FINALLY      
              330  POP_BLOCK        
              332  LOAD_CONST               None
            334_0  COME_FROM_FINALLY    26  '26'

 L. 554       334  LOAD_FAST                'scope'
              336  LOAD_ATTR                clear_intersection
              338  LOAD_FAST                'arg_dict'
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  POP_TOP          
              344  END_FINALLY      

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 118

    @commands.command(name='shell', aliases=['sh'])
    async def jsk_shell--- This code section failed: ---

 L. 566         0  LOAD_GLOBAL              ReplResponseReactor
                2  LOAD_FAST                'ctx'
                4  LOAD_ATTR                message
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  BEFORE_ASYNC_WITH
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  SETUP_ASYNC_WITH    236  'to 236'
               18  POP_TOP          

 L. 567        20  LOAD_FAST                'self'
               22  LOAD_ATTR                submit
               24  LOAD_FAST                'ctx'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  SETUP_WITH          226  'to 226'
               30  POP_TOP          

 L. 568        32  LOAD_GLOBAL              WrappedPaginator
               34  LOAD_STR                 '```sh'
               36  LOAD_CONST               1985
               38  LOAD_CONST               ('prefix', 'max_size')
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  STORE_FAST               'paginator'

 L. 569        44  LOAD_FAST                'paginator'
               46  LOAD_ATTR                add_line
               48  LOAD_STR                 '$ '
               50  LOAD_FAST                'argument'
               52  LOAD_ATTR                content
               54  FORMAT_VALUE          0  ''
               56  LOAD_STR                 '\n'
               58  BUILD_STRING_3        3 
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  POP_TOP          

 L. 571        64  LOAD_GLOBAL              PaginatorInterface
               66  LOAD_FAST                'ctx'
               68  LOAD_ATTR                bot
               70  LOAD_FAST                'paginator'
               72  LOAD_FAST                'ctx'
               74  LOAD_ATTR                author
               76  LOAD_CONST               ('owner',)
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'interface'

 L. 572        82  LOAD_FAST                'self'
               84  LOAD_ATTR                bot
               86  LOAD_ATTR                loop
               88  LOAD_ATTR                create_task
               90  LOAD_FAST                'interface'
               92  LOAD_ATTR                send_to
               94  LOAD_FAST                'ctx'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  POP_TOP          

 L. 574       102  LOAD_GLOBAL              ShellReader
              104  LOAD_FAST                'argument'
              106  LOAD_ATTR                content
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  SETUP_WITH          192  'to 192'
              112  STORE_FAST               'reader'

 L. 575       114  SETUP_LOOP          188  'to 188'
              116  LOAD_FAST                'reader'
              118  GET_AITER        
              120  LOAD_CONST               None
              122  YIELD_FROM       
              124  SETUP_EXCEPT        138  'to 138'
              126  GET_ANEXT        
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  STORE_FAST               'line'
              134  POP_BLOCK        
              136  JUMP_FORWARD        148  'to 148'
            138_0  COME_FROM_EXCEPT    124  '124'
              138  DUP_TOP          
              140  LOAD_GLOBAL              StopAsyncIteration
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_TRUE    176  'to 176'
              146  END_FINALLY      
            148_0  COME_FROM           136  '136'

 L. 576       148  LOAD_FAST                'interface'
              150  LOAD_ATTR                closed
              152  POP_JUMP_IF_FALSE   158  'to 158'

 L. 577       154  LOAD_CONST               None
              156  RETURN_END_IF    
            158_0  COME_FROM           152  '152'

 L. 578       158  LOAD_FAST                'interface'
              160  LOAD_ATTR                add_line
              162  LOAD_FAST                'line'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  GET_AWAITABLE    
              168  LOAD_CONST               None
              170  YIELD_FROM       
              172  POP_TOP          
              174  JUMP_BACK           124  'to 124'
            176_0  COME_FROM           144  '144'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          
              182  POP_EXCEPT       
              184  POP_TOP          
              186  POP_BLOCK        
            188_0  COME_FROM_LOOP      114  '114'
              188  POP_BLOCK        
              190  LOAD_CONST               None
            192_0  COME_FROM_WITH      110  '110'
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      

 L. 580       198  LOAD_FAST                'interface'
              200  LOAD_ATTR                add_line
              202  LOAD_STR                 '\n[status] Return code '
              204  LOAD_FAST                'reader'
              206  LOAD_ATTR                close_code
              208  FORMAT_VALUE          0  ''
              210  BUILD_STRING_2        2 
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  GET_AWAITABLE    
              216  LOAD_CONST               None
              218  YIELD_FROM       
              220  POP_TOP          
              222  POP_BLOCK        
              224  LOAD_CONST               None
            226_0  COME_FROM_WITH       28  '28'
              226  WITH_CLEANUP_START
              228  WITH_CLEANUP_FINISH
              230  END_FINALLY      
              232  POP_BLOCK        
              234  LOAD_CONST               None
            236_0  COME_FROM_ASYNC_WITH    16  '16'
              236  WITH_CLEANUP_START
              238  GET_AWAITABLE    
              240  LOAD_CONST               None
              242  YIELD_FROM       
              244  WITH_CLEANUP_FINISH
              246  END_FINALLY      

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 144

    @commands.command(name='git')
    async def jsk_git(self, ctx: commands.Context, *, argument: codeblock_converter):
        """
        Shortcut for 'jsk sh git'. Invokes the system shell.
        """
        return await ctx.invoke((self.jsk_shell), argument=(Codeblock(argument.language, 'git ' + argument.content)))

    @commands.group(name='voice', aliases=['vc'], invoke_without_command=True, ignore_extra=False)
    async def jsk_voice(self, ctx: commands.Context):
        """
        Voice-related commands.

        If invoked without subcommand, relays current voice state.
        """
        if await vc_check(ctx):
            return
        voice = ctx.guild.voice_client
        if not voice or not voice.is_connected():
            return await ctx.send('Not connected.')
        await ctx.send(f"Connected to {voice.channel.name}, {'paused' if voice.is_paused() else 'playing' if voice.is_playing() else 'idle'}.")

    @jsk_voice.command(name='join', aliases=['connect'])
    async def jsk_vc_join(self, ctx: commands.Context, *, destination: typing.Union[(discord.VoiceChannel, discord.Member)]=None):
        """
        Joins a voice channel, or moves to it if already connected.

        Passing a voice channel uses that voice channel.
        Passing a member will use that member's current voice channel.
        Passing nothing will use the author's voice channel.
        """
        if await vc_check(ctx):
            return
        else:
            destination = destination or ctx.author
            if isinstance(destination, discord.Member):
                if destination.voice:
                    if destination.voice.channel:
                        destination = destination.voice.channel
                else:
                    return await ctx.send('Member has no voice channel.')
            voice = ctx.guild.voice_client
            if voice:
                await voice.move_to(destination)
            else:
                await destination.connect(reconnect=True)
        await ctx.send(f"Connected to {destination.name}.")

    @jsk_voice.command(name='disconnect', aliases=['dc'])
    async def jsk_vc_disconnect(self, ctx: commands.Context):
        """
        Disconnects from the voice channel in this guild, if there is one.
        """
        if await connected_check(ctx):
            return
        voice = ctx.guild.voice_client
        await voice.disconnect()
        await ctx.send(f"Disconnected from {voice.channel.name}.")

    @jsk_voice.command(name='stop')
    async def jsk_vc_stop(self, ctx: commands.Context):
        """
        Stops running an audio source, if there is one.
        """
        if await playing_check(ctx):
            return
        voice = ctx.guild.voice_client
        voice.stop()
        await ctx.send(f"Stopped playing audio in {voice.channel.name}.")

    @jsk_voice.command(name='pause')
    async def jsk_vc_pause(self, ctx: commands.Context):
        """
        Pauses a running audio source, if there is one.
        """
        if await playing_check(ctx):
            return
        voice = ctx.guild.voice_client
        if voice.is_paused():
            return await ctx.send('Audio is already paused.')
        voice.pause()
        await ctx.send(f"Paused audio in {voice.channel.name}.")

    @jsk_voice.command(name='resume')
    async def jsk_vc_resume(self, ctx: commands.Context):
        """
        Resumes a running audio source, if there is one.
        """
        if await playing_check(ctx):
            return
        voice = ctx.guild.voice_client
        if not voice.is_paused():
            return await ctx.send('Audio is not paused.')
        voice.resume()
        await ctx.send(f"Resumed audio in {voice.channel.name}.")

    @jsk_voice.command(name='volume')
    async def jsk_vc_volume(self, ctx: commands.Context, *, percentage: float):
        """
        Adjusts the volume of an audio source if it is supported.
        """
        if await playing_check(ctx):
            return
        volume = max(0.0, min(1.0, percentage / 100))
        source = ctx.guild.voice_client.source
        if not isinstance(source, discord.PCMVolumeTransformer):
            return await ctx.send("This source doesn't support adjusting volume or the interface to do so is not exposed.")
        source.volume = volume
        await ctx.send(f"Volume set to {volume * 100:.2f}%")

    @jsk_voice.command(name='play', aliases=['play_local'])
    async def jsk_vc_play(self, ctx: commands.Context, *, uri: str):
        """
        Plays audio direct from a URI.

        Can be either a local file or an audio resource on the internet.
        """
        if await connected_check(ctx):
            return
        voice = ctx.guild.voice_client
        if voice.is_playing():
            voice.stop()
        uri = uri.lstrip('<').rstrip('>')
        voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(uri)))
        await ctx.send(f"Playing in {voice.channel.name}.")

    @jsk_voice.command(name='youtube_dl', aliases=['youtubedl', 'ytdl', 'yt'])
    async def jsk_vc_youtube_dl(self, ctx: commands.Context, *, url: str):
        """
        Plays audio from youtube_dl-compatible sources.
        """
        if await connected_check(ctx):
            return
        else:
            if not youtube_dl:
                return await ctx.send('youtube_dl is not installed.')
            voice = ctx.guild.voice_client
            if voice.is_playing():
                voice.stop()
        url = url.lstrip('<').rstrip('>')
        voice.play(discord.PCMVolumeTransformer(BasicYouTubeDLSource(url)))
        await ctx.send(f"Playing in {voice.channel.name}.")