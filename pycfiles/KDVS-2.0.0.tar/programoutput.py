# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grzegorz/eclipse-workspacePython/pplus/doc/sphinxext/sphinxcontrib/programoutput.py
# Compiled at: 2013-06-07 13:26:36
"""
    sphinxcontrib.programoutput
    ===========================

    This extension provides a directive to include the output of commands as
    literal block while building the docs.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys, shlex
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict, namedtuple
from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives import flag, unchanged, nonnegative_int
__version__ = b'0.5'

class program_output(nodes.Element):
    pass


def _slice(value):
    parts = [ int(v.strip()) for v in value.split(b',') ]
    if len(parts) > 2:
        raise ValueError(b'too many slice parts')
    return tuple((parts + [None] * 2)[:2])


class ProgramOutputDirective(rst.Directive):
    has_content = False
    final_argument_whitespace = True
    required_arguments = 1
    option_spec = dict(shell=flag, prompt=flag, nostderr=flag, ellipsis=_slice, extraargs=unchanged, returncode=nonnegative_int)

    def run(self):
        node = program_output()
        node.line = self.lineno
        node[b'command'] = self.arguments[0]
        if self.name == b'command-output':
            node[b'show_prompt'] = True
        else:
            node[b'show_prompt'] = b'prompt' in self.options
        node[b'hide_standard_error'] = b'nostderr' in self.options
        node[b'extraargs'] = self.options.get(b'extraargs', b'')
        node[b'use_shell'] = b'shell' in self.options
        node[b'returncode'] = self.options.get(b'returncode', 0)
        if b'ellipsis' in self.options:
            node[b'strip_lines'] = self.options[b'ellipsis']
        return [
         node]


_Command = namedtuple(b'Command', b'command shell hide_standard_error')

class Command(_Command):
    """
    A command to be executed.
    """

    def __new__(cls, command, shell=False, hide_standard_error=False):
        if isinstance(command, list):
            command = tuple(command)
        return _Command.__new__(cls, command, shell, hide_standard_error)

    @classmethod
    def from_program_output_node(cls, node):
        """
        Create a command from a :class:`program_output` node.
        """
        extraargs = node.get(b'extraargs', b'')
        command = (node[b'command'] + b' ' + extraargs).strip()
        return cls(command, node[b'use_shell'], node[b'hide_standard_error'])

    def execute(self):
        """
        Execute this command.

        Return the :class:`~subprocess.Popen` object representing the running
        command.
        """
        if isinstance(self.command, unicode):
            command = self.command.encode(sys.getfilesystemencoding())
        else:
            command = self.command
        if isinstance(command, basestring) and not self.shell:
            command = shlex.split(command)
        return Popen(command, shell=self.shell, stdout=PIPE, stderr=PIPE if self.hide_standard_error else STDOUT)

    def get_output(self):
        """
        Get the output of this command.

        Return a tuple ``(returncode, output)``.  ``returncode`` is the
        integral return code of the process, ``output`` is the output as
        unicode string, with final trailing spaces and new lines stripped.
        """
        process = self.execute()
        output = process.communicate()[0].decode(sys.getfilesystemencoding()).rstrip()
        return (process.returncode, output)

    def __str__(self):
        if isinstance(self.command, tuple):
            return repr(list(self.command))
        return repr(self.command)


class ProgramOutputCache(defaultdict):
    """
    Execute command and cache their output.

    This class is a mapping.  Its keys are :class:`Command` objects represeting
    command invocations.  Its values are tuples of the form ``(returncode,
    output)``, where ``returncode`` is the integral return code of the command,
    and ``output`` is the output as unicode string.

    The first time, a key is retrieved from this object, the command is
    invoked, and its result is cached.  Subsequent access to the same key
    returns the cached value.
    """

    def __missing__(self, command):
        """
        Called, if a command was not found in the cache.

        ``command`` is an instance of :class:`Command`.
        """
        result = command.get_output()
        self[command] = result
        return result


def run_programs(app, doctree):
    """
    Execute all programs represented by ``program_output`` nodes in
    ``doctree``.  Each ``program_output`` node in ``doctree`` is then
    replaced with a node, that represents the output of this program.

    The program output is retrieved from the cache in
    ``app.env.programoutput_cache``.
    """
    if app.config.programoutput_use_ansi:
        from sphinxcontrib.ansi import ansi_literal_block
        node_class = ansi_literal_block
    else:
        node_class = nodes.literal_block
    cache = app.env.programoutput_cache
    for node in doctree.traverse(program_output):
        command = Command.from_program_output_node(node)
        try:
            returncode, output = cache[command]
        except EnvironmentError as error:
            error_message = (b'Command {0} failed: {1}').format(command, error)
            error_node = doctree.reporter.error(error_message, base_node=node)
            node.replace_self(error_node)
        else:
            if returncode != node[b'returncode']:
                app.warn((b'Unexpected return code {0} from command {1}').format(returncode, command))
            if b'strip_lines' in node:
                lines = output.splitlines()
                start, stop = node[b'strip_lines']
                lines[start:stop] = [b'...']
                output = (b'\n').join(lines)
            if node[b'show_prompt']:
                tmpl = app.config.programoutput_prompt_template
                output = tmpl.format(command=node[b'command'], output=output, returncode=returncode)
            new_node = node_class(output, output)
            new_node[b'language'] = b'text'
            node.replace_self(new_node)


def init_cache(app):
    """
    Initialize the cache for program output at
    ``app.env.programoutput_cache``, if not already present (e.g. being
    loaded from a pickled environment).

    The cache is of type :class:`ProgramOutputCache`.
    """
    if not hasattr(app.env, b'programoutput_cache'):
        app.env.programoutput_cache = ProgramOutputCache()


def setup(app):
    app.add_config_value(b'programoutput_use_ansi', False, b'env')
    app.add_config_value(b'programoutput_prompt_template', b'$ {command}\n{output}', b'env')
    app.add_directive(b'program-output', ProgramOutputDirective)
    app.add_directive(b'command-output', ProgramOutputDirective)
    app.connect(b'builder-inited', init_cache)
    app.connect(b'doctree-read', run_programs)