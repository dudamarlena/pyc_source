# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/command.py
# Compiled at: 2015-10-10 07:08:46
from __future__ import unicode_literals, print_function
from ..elements.elementbase import ElementBase, Attribute
from .. import namespaces
from ..compat import text_type, implements_to_string
from ..errors import ElementError
from operator import itemgetter
import io

@implements_to_string
class FileReader(object):

    def __init__(self, element, path):
        self.element = element
        self.path = path

    def __call__(self, path):
        self.path = path

    def __str__(self):
        return (b"<filereader '{}'>").format(self.path)

    def __moyarepr__(self, context):
        return (b"<filereader '{}'>").format(self.path)

    @property
    def binary(self):
        try:
            with io.open(self.path, b'rb') as (f):
                return f.read()
        except IOError:
            raise ElementError((b'unable to read "{}"').format(self.path), element=self.element)

    @property
    def text(self):
        try:
            with io.open(self.path, b'rt') as (f):
                return f.read()
        except IOError:
            raise ElementError((b'unable to read "{}"').format(self.path), element=self.element)


class Command(ElementBase):
    """
    Defines a command accessible from the command line. To invoke a command enter its full app name after 'moya'. For example:

    [code]$ moya testapp#cmd.hello World
Hello, World!
    [/code]

    You can also get a list of available commands for an application, by supplying the app name followed by #. For example:

    [code]$ moya testapp#[/code]

    See [doc commands] for more information.

    """

    class Help:
        synopsis = b'define a command'
        example = b'\n        <command libname="cmd.hello" sypopsis="Greet someone on the commandline">\n            <signature>\n                <arg name="who" help="Who you want to greet">\n            </signature>\n            <echo>Hello, ${who}!</echo>\n        </command>\n        '

    _element_class = b'command'
    synopsis = Attribute(b'Command synopsis, displayed when you list commands')
    init = Attribute(b'Run this command as part of the init process?', type=b'boolean', default=False)
    priority = Attribute(b'Priority for init process (higher piority commands will be run first)', type=b'integer', default=0)

    class Meta:
        logic_skip = True

    def document_finalize(self, context):
        self._synopsis = self.synopsis(context)
        self._doc = None
        self._init = self.init(context)
        self._priority = self.priority(context)
        for doc in self.get_children(element_type=(namespaces.default, b'doc')):
            self._doc = doc.text

        self._signature = _signature = {b'options': [], b'arguments': [], b'switches': []}
        for signature in self.children(element_type=(namespaces.default, b'signature')):
            for element in signature.children(element_type=b'option'):
                params = element.get_all_parameters(context)
                _signature[b'options'].append(params)

            for element in signature.children(element_type=b'arg'):
                params = element.get_all_parameters(context)
                _signature[b'arguments'].append(params)

            for element in signature.children(element_type=b'switch'):
                params = element.get_all_parameters(context)
                _signature[b'switch'].append(params)

        _signature[b'options'].sort(key=itemgetter(b'name'))
        _signature[b'arguments'].sort(key=itemgetter(b'name'))
        _signature[b'switches'].sort(key=itemgetter(b'name'))
        _signature[b'alloptions'] = _signature[b'options'] + _signature[b'switches']
        _signature[b'alloptions'].sort(key=itemgetter(b'name'))
        return

    _types = {b'string': lambda el: text_type, 
       b'int': lambda el: int, 
       b'integer': lambda el: int, 
       b'float': lambda el: float, 
       b'file': lambda el: lambda p: FileReader(el, p)}

    def update_parser(self, parser, context):
        for signature in self.children(element_type=b'signature'):
            for element in signature.children(element_type=b'option'):
                params = element.get_parameters(context)
                if params.action:
                    parser.add_argument(b'--' + params.name, dest=params.name, default=params.default, help=params.help, action=params.action)
                else:
                    parser.add_argument(b'--' + params.name, dest=params.name, default=params.default, help=params.help, type=self._types[params.type](self))

            for element in signature.children(element_type=b'arg'):
                params = element.get_parameters(context)
                parser.add_argument(dest=params.name, nargs=params.nargs, help=params.help, metavar=params.metavar, type=self._types[params.type](self))


class Arg(ElementBase):
    """Defines an argument for a [link commands]command[/link]. An [tag]arg[/tag] tag must appear within the [tag]signature[/tag] tag for a command."""

    class Help:
        synopsis = b'add a positional argument to a command'
        example = b'\n        <!-- Should appear within a <signature> tag -->\n        <arg name="who" help="Who you want to greet">\n        '

    _element_class = b'command'
    name = Attribute(b'Argument name (the variable when the command is execute)')
    nargs = Attribute(b'Number of arguments to be consumed', default=None)
    help = Attribute(b'Argument help text', default=None)
    metavar = Attribute(b'Argument metavar (shown in the help)')
    type = Attribute(b'Type of argument', choices=[b'string', b'integer', b'float', b'file'], default=b'string')

    class Meta:
        logic_skip = True


class Option(ElementBase):
    """Defines an [i]option[/i] for a [tag]command[/tag]. Options may be added to the command line when a command is invoked. The following is an example of how an option is used:

    [code]$ moya testapp#cmd.optiontest --hobbit="bilbo"[/code]

    An [tag]option[/tag] tag must appear within a [tag]signature[/tag] tag.

    """

    class Help:
        synopsis = b'Add an option to a command'
        example = b'\n        <option name="hobbit" metavar="HOBBIT NAME" help="Your favorite hobbit" />\n        '

    _element_class = b'command'
    name = Attribute(b'Argument name')
    nargs = Attribute(b'Number of arguments', default=b'?')
    help = Attribute(b'Argument help text')
    default = Attribute(b'Default', default=None)
    metavar = Attribute(b'Argument metavar')
    action = Attribute(b'Action', default=None)
    type = Attribute(b'Type of argument', choices=[b'string', b'integer', b'float', b'file'], default=b'string')

    class Meta:
        logic_skip = True