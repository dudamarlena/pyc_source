# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/ui_context.py
# Compiled at: 2016-05-04 07:56:27
import shlex, sys
from . import config
from . import utils
from . import options
from .msg import common_err, common_info, common_warn
from . import ui_utils
from . import userdir

class Context(object):
    """
    Context is a cursor that marks the current
    location of the user in the UI hierarchy.
    It maintains a stack of UILevel objects, so
    level_stack[-1] is the current level.

    The Context is passed as the first parameter
    to any command.
    """

    def __init__(self, root):
        self.stack = [
         root]
        self._mark = 0
        self._in_transit = False
        self._wait_for_dc = False
        self.command_name = None
        self.command_args = None
        self.command_info = None
        self._rl_line = None
        self._rl_words = []
        return

    def run(self, line):
        """
        Execute the given command line.
        """
        line = line.strip()
        if not line or line.startswith('#'):
            return True
        self._mark = len(self.stack)
        self._in_transit = False
        self._wait_for_dc = False
        rv = True
        cmd = False
        try:
            tokens = shlex.split(line)
            while tokens:
                token, tokens = tokens[0], tokens[1:]
                self.command_name = token
                self.command_args = tokens
                self.command_info = self.current_level().get_child(token)
                if not self.command_info:
                    self.fatal_error('No such command')
                self.command_name = self.command_info.name
                if self.command_info.type == 'level':
                    self.enter_level(self.command_info.level)
                else:
                    cmd = True
                    break

            if cmd:
                rv = self.execute_command() is not False
        except ValueError as msg:
            if config.core.debug:
                import traceback
                traceback.print_exc()
            common_err('%s: %s' % (self.get_qualified_name(), msg))
            rv = False
        except IOError as msg:
            if config.core.debug:
                import traceback
                traceback.print_exc()
            common_err('%s: %s' % (self.get_qualified_name(), msg))
            rv = False

        if cmd or rv is False:
            rv = self._back_out() and rv
        if rv and self._wait_for_dc:
            return utils.wait4dc(self.command_name, not options.batch)
        return rv

    def complete(self, line):
        """
        Given a (partial) command line, returns
        a list of potential completions.
        A space at the end of the line is significant.
        """
        complete_next = line.endswith(' ')
        prev_stack = list(self.stack)
        prev_name = self.command_name
        prev_args = self.command_args
        prev_info = self.command_info
        try:
            line = line.strip()
            if not line or line.startswith('#'):
                return self.current_level().get_completions()
            try:
                tokens = shlex.split(line)
                if complete_next:
                    tokens += ['']
                while tokens:
                    token, tokens = tokens[0], tokens[1:]
                    self.command_name = token
                    self.command_args = tokens
                    self.command_info = self.current_level().get_child(token)
                    if not self.command_info:
                        return self.current_level().get_completions()
                    if self.command_info.type == 'level':
                        self.enter_level(self.command_info.level)
                    else:
                        ret = self.command_info.complete(self, tokens)
                        if tokens:
                            ret = [ t for t in ret if t.startswith(tokens[(-1)]) ]
                        return ret

                if self.previous_level():
                    return self.previous_level().get_completions()
                return self.current_level().get_completions()
            except ValueError:
                pass
            except IOError:
                pass

            return []
        finally:
            self.stack = prev_stack
            self.command_name = prev_name
            self.command_args = prev_args
            self.command_info = prev_info

    def setup_readline(self):
        import readline
        readline.set_history_length(100)
        for v in ('tab: complete', 'set skip-completed-text on'):
            readline.parse_and_bind(v)

        readline.set_completer(self.readline_completer)
        readline.set_completer_delims(' \t\n,')
        try:
            readline.read_history_file(userdir.HISTORY_FILE)
        except IOError:
            pass

    def clear_readline_cache(self):
        self._rl_line = None
        self._rl_words = []
        return

    def readline_completer(self, text, state):
        import readline

        def matching(word):
            """we are only completing the last word in the line"""
            return word.split()[(-1)].startswith(text)

        line = utils.get_line_buffer() + readline.get_line_buffer()
        if line != self._rl_line:
            try:
                self._rl_line = line
                completions = self.complete(line)
                if text:
                    self._rl_words = [ w for w in completions if matching(w) ]
                else:
                    self._rl_words = completions
            except Exception:
                self.clear_readline_cache()

        try:
            ret = self._rl_words[state]
        except IndexError:
            ret = None

        if not text or ret and line.split()[(-1)].endswith(ret):
            return ret + ' '
        else:
            return ret

    def current_level(self):
        return self.stack[(-1)]

    def previous_level(self):
        if len(self.stack) > 1:
            return self.stack[(-2)]
        else:
            return

    def enter_level(self, level):
        """
        Pushes an instance of the given UILevel
        subclass onto self.stack. Checks prerequirements
        for the level (if any).
        """
        if not options.interactive and not self.command_args:
            self._set_interactive()
        self._in_transit = True
        entry = level()
        if 'requires' in dir(entry) and not entry.requires():
            self.fatal_error('Missing requirements')
        self.stack.append(entry)
        self.clear_readline_cache()

    def _set_interactive(self):
        """Set the interactive option only if we're on a tty."""
        if utils.can_ask():
            options.interactive = True

    def execute_command(self):
        arglist = [
         self.current_level(), self] + self.command_args
        ui_utils.validate_arguments(self.command_info.function, arglist, nskip=2)
        self.check_skill_level(self.command_info.skill_level)
        rv = self.command_info.function(*arglist)
        if rv and self.should_wait():
            self._wait_for_dc = True
        return rv

    def should_wait(self):
        if not config.core.wait:
            return False
        if self.command_info.wait:
            return True
        by_level = self.current_level().should_wait()
        transit_or_noninteractive = self.is_in_transit() or not options.interactive
        return by_level and transit_or_noninteractive

    def is_in_transit(self):
        """
        TODO
        FIXME
        """
        return self._in_transit

    def check_skill_level(self, skill_level):
        levels_to = {0: 'operator', 1: 'administrator', 2: 'expert'}
        levels_from = {'operator': 0, 'administrator': 1, 'expert': 2}
        if levels_from.get(config.core.skill_level, 0) < skill_level:
            self.fatal_error('ACL %s skill level required' % levels_to.get(skill_level, 'other'))

    def get_command_name(self):
        """Returns name used to call the current command"""
        return self.command_name

    def get_qualified_name(self):
        """Returns level.command if level is not root"""
        names = ('.').join([ l.name for l in self.stack[1:] ])
        if names:
            return '%s.%s' % (names, self.get_command_name())
        return self.get_command_name()

    def get_command_info(self):
        """Returns the ChildInfo object for the current command or level"""
        return self.command_info

    def up(self):
        """
        Navigate up in the levels hierarchy
        """
        ok = True
        if len(self.stack) > 1:
            ok = self.current_level().end_game(no_questions_asked=self._in_transit) is not False
            self.stack.pop()
            self.clear_readline_cache()
        return ok

    def _back_out(self):
        """
        Restore the stack to the marked position
        """
        ok = True
        while self._mark > 0 and len(self.stack) > self._mark:
            ok = self.up() and ok

        return ok

    def save_stack(self):
        self._mark = len(self.stack)

    def quit(self, rc=0):
        """
        Exit from the top level
        """
        ok = self.current_level().end_game()
        if options.interactive and not options.batch:
            print 'bye'
        if ok is False and rc == 0:
            rc = 1
        sys.exit(rc)

    def level_name(self):
        """
        Returns the name of the current level.
        Returns 'root' if at the root level.
        """
        return self.current_level().name

    def prompt(self):
        """returns a prompt generated from the level stack"""
        return (' ').join(l.name for l in self.stack[1:])

    def previous_level_is(self, level_name):
        """
        Check call stack for previous level name
        """
        prev = self.previous_level()
        return prev and prev.name == level_name

    def error(self, msg):
        """
        Too easy to misremember and type error()
        when I meant fatal_error().
        """
        raise ValueError(msg)

    def fatal_error(self, msg):
        """
        TODO: Better error messages, with full context information
        Raise exception to get thrown out to run()
        """
        raise ValueError(msg)

    def error_message(self, msg):
        """
        Error message only, don't cancel execution of command
        """
        common_err('%s: %s' % (self.get_qualified_name(), msg))

    def warning(self, msg):
        common_warn('%s: %s' % (self.get_qualified_name(), msg))

    def info(self, msg):
        common_info('%s: %s' % (self.get_qualified_name(), msg))