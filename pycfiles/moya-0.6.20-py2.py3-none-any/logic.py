# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/logic.py
# Compiled at: 2017-09-02 09:14:06
"""
The 'engine' behind Moya Code.

"""
from __future__ import unicode_literals
from .elements import ElementBase
from .context.missing import is_missing
from .context.errors import SubstitutionError
from .console import Console, ConsoleHighlighter
from .context.expression import ExpressionError
from .errors import LogicError, StartupFailedError
from .compat import text_type, implements_iterator, next_method_name
from .moyaexceptions import *
from . import trace
import sys, logging
from threading import RLock
from operator import truth
try:
    import readline
except ImportError:
    pass

log = logging.getLogger(b'moya.runtime')
debug_lock = RLock()
if sys.platform == b'darwin':
    try:
        import pync
    except ImportError:

        def notify(title, message):
            pass


    else:

        def notify(title, message):
            try:
                pync.Notifier.notify(message, title=title)
            except:
                pass


else:
    try:
        import notify2
    except ImportError:

        def notify(title, message):
            pass


    else:

        def notify(title, message):
            """Show a notification message if notify2 is available"""
            try:
                if not notify2.is_initted():
                    notify2.init(b'moya')
                n = notify2.Notification(title, message, b'dialog-information')
                n.show()
            except:
                pass


def _breakpoint_notify(node, suppressed=False):
    """Show a notification message about this node"""
    node = getattr(node, b'__node__', node)
    message = b'in file "%s"' % node._location
    if suppressed:
        log.debug(b'<breakpoint> %s ignored', message)
    else:
        log.debug(b'<breakpoint> %s', message)
        notify(b'Moya debugger hit a breakpoint', message)


def debugging_notify():
    notify(b'Moya debugger started', b'Moya is now in debug mode, please see the console')


def is_debugging():
    """Check if the logic is currently debugging"""
    if not debug_lock.acquire(False):
        return True
    debug_lock.release()
    return False


class Pass(object):
    pass


class DebugBreak(Exception):

    def __init__(self, node):
        self.node = node


class LogicFlowException(Exception):
    pass


class BreakLoop(LogicFlowException):
    pass


class ContinueLoop(LogicFlowException):
    pass


class DeferMeta(object):
    is_call = False
    is_loop = False


@implements_iterator
class Defer(object):
    """Base for Defers"""
    __slots__ = [
     b'_meta', b'node', b'iter', b'app']

    def __init__(self, node, app=None):
        self._meta = DeferMeta()
        self.node = node
        self.iter = iter(self.get_nodes())
        self.app = app

    def __repr__(self):
        return b'<Defer %r>' % self.node

    def __next__(self):
        return next(self.iter)

    def __iter__(self):
        return self.get_nodes()

    def get_nodes(self):
        raise NotImplementedError

    def close(self):
        return self.iter.close()

    def throw(self, *args, **kwargs):
        return self.iter.throw(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self.iter.send(*args, **kwargs)


class DeferNode(Defer):
    """Defer to a new node"""
    __slots__ = []

    def __repr__(self):
        return b'<DeferNode %r>' % self.node

    def get_nodes(self):
        yield self.node


class DeferNodeContents(Defer):
    """Defer to the contexts of a node"""
    __slots__ = []

    def __repr__(self):
        return b'<DeferNodeContents %r>' % self.node

    def get_nodes(self):
        for child in self.node:
            if child._element_class == b'logic':
                yield child


class SkipNext(object):
    __slots__ = [
     b'_meta', b'element_types']

    def __init__(self, *element_types):
        self._meta = DeferMeta()
        self.element_types = element_types

    def __next__(self):
        pass

    def close(self):
        pass


class Unwind(LogicFlowException):
    pass


class EndLogic(LogicFlowException):

    def __init__(self, return_value=None):
        self.return_value = return_value


class SuppressException(Exception):
    pass


def debug(archive, context, root_node):
    run_logic_debug(archive, context, root_node, [
     root_node])


@implements_iterator
class NodeGenerator(object):
    __slots__ = [b'node', b'generator', b'_meta', b'_next']

    def __init__(self, node, generator):
        self.node = node
        self.generator = generator
        self._meta = node._meta
        self._next = getattr(generator, next_method_name, None)
        return

    def __repr__(self):
        return b'<generator for %s>' % self.node

    def __nonzero__(self):
        return truth(self._next)

    def __iter__(self):
        return self

    def __next__(self):
        return self._next()

    def close(self):
        return self.generator.close()

    def send(self, value):
        return self.generator.send(value)

    def throw(self, *args, **kwargs):
        return self.generator.throw(*args, **kwargs)


def close_generator(gen, _ElementBase=ElementBase):
    try:
        if not isinstance(gen, _ElementBase):
            gen.close()
    except Exception as e:
        log.exception(b'error in close_generator')


def _logic_loop(context, node_stack, debugging=False, debug_hook=None, on_exception=None):
    push_stack = node_stack.append
    pop_stack = node_stack.pop
    breakpoints_enabled = debugging
    skip = ()
    _NodeGenerator = NodeGenerator
    _SkipNext = SkipNext
    _ElementBase = ElementBase
    do_finalize = True

    def finalize_stack():
        while node_stack:
            node = pop_stack()
            close_generator(node)

    try:
        while node_stack:
            try:
                node = pop_stack()
                if isinstance(node, _SkipNext):
                    skip = node.element_types
                    continue
                if isinstance(node, _ElementBase):
                    if node._meta.logic_skip or node._element_type in skip:
                        continue
                    if debugging and debug_hook and not getattr(node, b'_debug_skip', False):
                        debugging, breakpoints_enabled = debug_hook(node)
                    if not node._ignore_skip:
                        skip = ()
                    if node.check(context):
                        result = node.logic(context)
                        if result:
                            push_stack(_NodeGenerator(node, result))
                else:
                    next_node = next(node, None)
                    if next_node:
                        push_stack(node)
                        push_stack(next_node)
            except MoyaException as moya_exception:
                callstack = context.get(b'._callstack', [])[:]
                exc_node = node
                exc_type = moya_exception.type
                while 1:
                    if node_stack:
                        enode = getattr(node, b'node', node)
                        if isinstance(enode, ElementBase):
                            if enode._meta.trap_exceptions:
                                if hasattr(enode, b'on_exception'):
                                    new_node = enode.on_exception(context, moya_exception)
                                    if new_node is not None:
                                        push_stack(new_node)
                                    break
                                moya_trace = trace.build(context, callstack, exc_node, moya_exception, sys.exc_info(), context.get(b'.request', None))
                                try:
                                    node.throw(LogicError(moya_exception, moya_trace))
                                except StopIteration:
                                    close_generator(node)
                                    node = pop_stack()

                                break
                            for sibling in enode.younger_siblings_of_type(('http://moyaproject.com',
                                                                           'catch')):
                                if sibling.check_exception_type(context, exc_type):
                                    close_generator(node)
                                    node = pop_stack()
                                    sibling.set_exception(context, moya_exception)
                                    push_stack(SkipNext(('http://moyaproject.com',
                                                         'else'), ('http://moyaproject.com',
                                                                   'elif')))
                                    push_stack(DeferNodeContents(sibling))
                                    break
                            else:
                                close_generator(node)
                                node = pop_stack()
                                continue

                            break
                        close_generator(node)
                        node = pop_stack()
                else:
                    close_generator(node)
                    if on_exception:
                        on_exception(callstack, exc_node, moya_exception)
                    request = context.get(b'.request', None)
                    moya_trace = trace.build(context, callstack, exc_node, moya_exception, sys.exc_info(), request)
                    raise LogicError(moya_exception, moya_trace)

            except BreakLoop:
                while node_stack:
                    node = pop_stack()
                    close_generator(node)
                    if node._meta.is_loop or node._meta.is_call:
                        break

            except ContinueLoop:
                while node_stack:
                    node = pop_stack()
                    if node._meta.is_loop or node._meta.is_call:
                        push_stack(node)
                        break
                    close_generator(node)

            except EndLogic as end_logic:
                while node_stack:
                    node = pop_stack()
                    if not node_stack:
                        break
                    close_generator(node)

                node.node._return_value = end_logic.return_value
                next(node, None)
            except Unwind:
                while node_stack:
                    node = pop_stack()
                    if node._meta.is_call:
                        push_stack(node)
                        break
                    close_generator(node)

            except DebugBreak:
                if breakpoints_enabled:
                    debugging = True
                    continue
                do_finalize = False
                raise
            except StartupFailedError:
                raise
            except SystemExit:
                raise
            except Exception as logic_exception:
                if on_exception:
                    on_exception(node_stack, node, logic_exception)
                request = context.get(b'.request', None)
                callstack = context.get(b'._callstack', [])[:]
                moya_trace = trace.build(context, None, node, logic_exception, sys.exc_info(), request)
                exc_node = node
                raise LogicError(logic_exception, moya_trace)

    finally:
        if do_finalize:
            finalize_stack()

    return


def run_logic(archive, context, root_node):
    node_stack = [
     root_node]
    try:
        _logic_loop(context, node_stack)
    except DebugBreak as debug_break:
        _breakpoint_notify(node_stack[(-1)].node, suppressed=archive.suppress_breakpoints)
        run_logic_debug(archive, context, debug_break.node, node_stack)


class _TracebackFile(object):

    def __init__(self):
        self.text = []

    def write(self, text):
        if not isinstance(text, text_type):
            text = text_type(text, b'utf-8')
        self.text.append(text)

    def getvalue(self):
        return (b'').join(self.text)


class ErrorLineHighlighter(ConsoleHighlighter):
    styles = {None: b'white', 
       b'tag': b'bold blue not dim', 
       b'attribute': b'cyan not bold', 
       b'string': b'yellow', 
       b'line': b'white'}
    highlights = [
     b'(?P<tag>\\<.*?\\>)',
     b'(?P<attribute>\\s\\S*?=\\".*?\\")',
     b'(?P<string>\\".*?\\")',
     b'^File \\"(?P<line>.*?)\\".*$']


def moya_traceback(stack, node, exc, console, message=b'Logic Error'):
    console.div(message, bold=True, fg=b'red')
    node = getattr(node, b'node', node)
    for s in stack:
        e = getattr(s, b'element', None)
        if e and e._code:
            file_line = b'File "%s", line %s, in %s' % (e._location, e.source_line or 0, e)
            console(ErrorLineHighlighter.highlight(file_line)).nl()
            console.xmlsnippet(e._code, e.source_line or 0, extralines=2)

    if hasattr(node, b'_location'):
        file_line = b'File "%s", line %s, in %s' % (node._location, getattr(node, b'source_line', 0) or 0, node)
        console(ErrorLineHighlighter.highlight(file_line)).nl()
        console.xmlsnippet(node._code, node.source_line or 0, extralines=2)
    if isinstance(exc, MoyaException):
        console.nl()(b'unhandled exception: ', fg=b'red', bold=True)((b'{}').format(exc.type), fg=b'magenta', bold=True)(b' ')((b'"{}"').format(exc.msg), fg=b'green').nl()
    elif isinstance(exc, (ExpressionError, SubstitutionError)):
        console.exception(exc, tb=False)
    else:
        console.nl()
        console.exception(exc, tb=not getattr(exc, b'hide_py_traceback', False))
    console.div()
    return


def render_moya_traceback(stack, node, exc, error_log=None):
    if error_log is None:
        error_log = log
    f = _TracebackFile()
    console = Console(f, nocolors=True)
    moya_traceback(stack, node, exc, console)
    text = f.getvalue()
    for line in text.splitlines():
        log.error(line)

    return


def run_logic_debug(archive, context, node, node_stack):
    from .console import Cell
    from .debugger import MoyaCmdDebugger
    from . import pilot
    console = pilot.console
    watches = []
    context[b'.pilot'] = pilot
    div_style = dict(bold=True, fg=b'black')
    cmd_shell = MoyaCmdDebugger(archive, console)
    break_node_stack = []

    def view(node):
        node = getattr(node, b'__node__', node)
        console.div()
        console(b'In file "%s"' % node._location).nl()
        try:
            if node._code:
                console.snippet(node._code, highlight_line=node.source_line).nl()
        except:
            raise
            console.text(b"can't display code for this location", italic=True)

    def where(node, params=b'3'):
        try:
            extralines = max(int(params), 0)
        except:
            extralines = 3

        extralines = max(extralines, 0)
        node = getattr(node, b'__node__', node)
        console.div()
        console(b'In file "%s"' % node._location).nl()
        if node._code:
            console.xmlsnippet(node._code, node.source_line or 0, extralines=extralines).nl()
        show_watches()

    def show_watches():
        if watches:
            watch_table = [
             (
              Cell(b'watch', bold=True), Cell(b'value', bold=True))]
            for watch in watches:
                try:
                    val = context.eval(watch)
                    if is_missing(val):
                        watch_table.append([watch, Cell(context.to_expr(val), italic=True)])
                    else:
                        watch_table.append([watch, context.to_expr(val)])
                except Exception as e:
                    watch_table.append([watch, Cell(e, bold=True, fg=b'red')])

            console.table(watch_table)

    def show_stack(node, stack=None, params=b'2'):
        try:
            extralines = max(int(params), 0)
        except:
            extralines = 2

        node = getattr(node, b'__node__', node)
        if stack is None:
            stack = context.get(b'._callstack', [])
        for s in stack:
            e = getattr(s, b'element', None)
            if e and e._code:
                console(b'File "%s", in %s' % (e._location, e)).nl()
                console.xmlsnippet(e._code, e.source_line or 0, extralines=extralines).nl()

        if hasattr(node, b'_location'):
            console(b'File "%s", in %s' % (node._location, node)).nl()
            console.xmlsnippet(node._code, node.source_line or 0, extralines=extralines).nl()
        return

    def show_exception(stack, node, exc):
        moya_traceback(context.get(b'._callstack', []), node, exc, console)
        exc._displayed = True
        debug_hook(node, error_analysis=True)

    def debug_hook(node, error_analysis=False):
        if not debugging:
            return (False, False)
        else:
            if archive.suppress_breakpoints:
                return (False, False)
            node = getattr(node, b'node', node)
            if break_node_stack:
                if node_stack != break_node_stack[:len(node_stack)]:
                    return (True, True)
                del break_node_stack[:]
            if node._element_type == ('http://moyaproject.com', 'text'):
                return (True, True)
            if not error_analysis:
                where(node)
            while 1:
                if isinstance(node, ElementBase):
                    if node.document.lib:
                        if not node.libname:
                            node_name = b'%s:%s' % (node.document.lib.long_name or b'', node.docid)
                        else:
                            node_name = b'%s#%s' % (node.document.lib.long_name or b'', node.libname)
                    else:
                        node_name = node.document.path
                else:
                    node_name = b''
                prompt = console(b'moya ', bold=True, fg=b'black', asstr=True) + console(node_name, bold=True, fg=b'blue', asstr=True) + console(b' > ', asstr=True)
                cmd_shell.prompt = prompt
                try:
                    cmd_shell.cmdloop()
                except KeyboardInterrupt:
                    console(b'^C', fg=b'green').nl()
                    return (False, False)
                except SystemExit:
                    console.div().nl()
                    return (False, False)
                except Exception as e:
                    console.exception(e, tb=True)
                    return (False, False)

                _cmd = cmd = getattr(cmd_shell, b'usercmd', None)
                if cmd is None:
                    console.div()
                    return (
                     False, False)
                if b' ' in cmd:
                    cmd, params = cmd.split(b' ', 1)
                else:
                    params = b''
                if cmd in ('s', 'step'):
                    return (True, True)
                if cmd in ('o', 'over'):
                    break_node_stack[:] = node_stack[:]
                    return (
                     True, True)
                if cmd in ('u', 'out'):
                    break_node_stack[:] = node_stack[:-1]
                    return (
                     True, True)
                if cmd in ('t', 'stack'):
                    console.div(b'Stack', bold=True)
                    show_stack(node, params=params)
                    continue
                else:
                    if cmd in ('c', 'cont', 'continue', 'EOF'):
                        if cmd == b'EOF':
                            console.nl()
                            return (
                             False, False)
                        console.div(b'continue', **div_style)
                        return (
                         False, True)
                    if cmd in ('watch', ):
                        if params:
                            watches.append(params.strip())
                            show_watches()
                        else:
                            del watches[:]
                            console(b'watches removed', italic=True).nl()
                        continue
                    else:
                        if cmd in ('winpdb', ):
                            try:
                                import rpdb2
                                rpdb2
                            except Exception:
                                console.text(b'rpdb2 is required to debug with WinPDB', fg=b'red', bold=True)
                            else:
                                context[b'._winpdb_debug'] = True
                                context[b'._winpdb_password'] = params.strip() or b'password'
                                console.text(b'A WinPDB breakpoint has been set on the next Python call', fg=b'green')
                                continue

                        elif cmd in ('v', 'view'):
                            view(node)
                            continue
                        elif cmd in ('w', 'where'):
                            where(node, params)
                            continue
                        elif cmd in ('e', 'eval'):
                            cmd_eval = params.strip()
                            if cmd_eval:
                                _cmd = cmd_eval
                            else:
                                cmd = params.strip()
                        else:
                            if cmd in ('r', 'run'):
                                archive.suppress_breakpoints = True
                                console.div(b'Ignoring all breakpoints for this session', bold=True, fg=b'green')
                                return (
                                 False, False)
                            if cmd in ('let', ):
                                if b'=' not in params:
                                    console.error(b"Must be a key/value pair (i.e. foo='bar')")
                                    continue
                                else:
                                    k, v = params.split(b'=', 1)
                                    k = k.strip()
                                    v = v.strip()
                                    try:
                                        context.set(k, context.eval(v))
                                    except Exception as e:
                                        console.obj(context, e)

                                    continue
                            elif cmd == b'exit':
                                import sys
                                console.div(b'Goodbye', bold=True)
                                sys.exit(0)
                        to_unicode = False
                        to_expr = False
                        to_repr = False
                        if _cmd.endswith(b'???'):
                            _cmd = _cmd[:-3]
                            to_repr = True
                        elif _cmd.endswith(b'??'):
                            _cmd = _cmd[:-2]
                            to_expr = True
                        elif _cmd.endswith(b'?'):
                            to_unicode = True
                            _cmd = _cmd[:-1]
                        try:
                            if not cmd:
                                val = context.capture_scope()
                            else:
                                val = context.eval(_cmd)
                        except SystemExit:
                            raise
                        except Exception as e:
                            console.exception(e)

                        try:
                            if to_unicode:
                                console.text(text_type(val))
                                continue
                            elif to_expr:
                                console.text(context.to_expr(val))
                                continue
                            elif to_repr:
                                console.text(repr(val))
                                continue
                            else:
                                console.obj(context, val)
                        except Exception as e:
                            console.exception(e)
                            continue

            return (
             True, True)

    debugging = True
    with debug_lock:
        while 1:
            try:
                _logic_loop(context, node_stack, debugging=debugging and not archive.suppress_breakpoints, debug_hook=debug_hook, on_exception=show_exception)
            except SystemExit:
                debugging = False
                raise
            except DebugBreak:
                debugging = False
            else:
                break

    return (
     False, False)