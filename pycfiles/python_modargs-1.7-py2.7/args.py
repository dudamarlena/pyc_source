# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/modargs/args.py
# Compiled at: 2012-12-21 17:36:19
"""
It's used very easily.  First, you write a module that is like
tests/commands.py.  Each function name BLAH_command implements a sub-command.
Then you use modargs.args.parse_and_run_command to parse the command line and
run the function that matches.

Note that the _command suffix is optional and configurable, but it is there
to disambiguate your commands so you can use Python reserved words and base
types as your command names.  Without it, you can do a list_command or a
for_command.

Your command then specifies its keyword arguments to indicate what has
reasonable defaults and what is required.  Give a value to the option
to indicate its default, and give a None setting to indicate it is required.
A good way to read this is it is your commands "default settings" and None
says "this option has no default setting".

Here's an example from modargs tests::

   def test_command(port=8825, host='127.0.0.1', debug=1, sender=None, to=None,
                 subject=None, body=None, file=False):

You can see this has subject, body, sender, and to as required options (they 
are None), and the rest have some default value.

With this the argument parser will parse the user's given arguments, and then
call your command function with those as keyword arguments, but after it has
fixed them up with the defaults you gave.  In the event that a user does
not give a required option, modargs.args will abort with an error telling them.

Options can also be specified multiple times to have their values collected as
a list. For example, in the above method, we could invoke it with
--to me@example.com --to you@example.com. When the test_command is invoked, to
will have the value ['me@example.com', 'you@example.com'].

Modargs's argument parser also accurately detects and parses integers, boolean
values, strings, emails, single word values, and can handle trailing arguments
after a -- argument.  This means you don't have to do conversion, it should be
the right type for what you expect.

modargs.args does not care if you use one dash (-help), two dashes (--help),
three dashes (---help) or a billion.  In all honesty, who gives a rat's ass,
just get the user to type something like a dash followed by a word and that's
good enough.

If you just need argument parsing and no commands then you can just use
modargs.args.parse directly.

Finally, the help documentation for your commands is just the __doc__
string of the function.
"""
import inspect, re, sys, traceback
S_IP_ADDRESS = lambda x, token: [
 'ip_address', token]
S_WORD = lambda x, token: ['word', token]
S_EMAIL_ADDR = lambda x, token: ['email', token]
S_OPTION = lambda x, token: ['option', token.split('-')[(-1)]]
S_INT = lambda x, token: ['int', int(token)]
S_BOOL = lambda x, token: ['bool', token in ('True', 'true', 'yes', 't', 'y')]
S_EMPTY = lambda x, token: ['empty', '']
S_STRING = lambda x, token: ['string', token]
S_TRAILING = lambda x, token: ['trailing', None]

class ArgumentError(Exception):
    """Thrown when modargs.args encounters a command line format error."""
    pass


SCANNER = re.Scanner([
 (
  '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}', S_EMAIL_ADDR),
 (
  '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]', S_IP_ADDRESS),
 (
  '-+[a-zA-Z0-9]+', S_OPTION),
 (
  '[0-9]+', S_INT),
 (
  '--', S_TRAILING),
 (
  '(True|False|true|false|yes|no|t|f|y|n)\\b', S_BOOL),
 (
  '[a-z\\-]+', S_WORD),
 (
  '\\s', S_EMPTY),
 (
  '.+', S_STRING)])

def match(tokens, of_type=None):
    """
    Responsible for taking a token off and processing it, ensuring it is 
    of the correct type.  If of_type is None (the default) then you are
    asking for anything.
    """
    if of_type:
        if not peek(tokens, of_type):
            if of_type == 'option':
                raise ArgumentError('Expecting an option, not a %s' % tokens[0][0])
            raise ArgumentError("Expecting '%s' type of argument not %s in tokens: %r.  Read the help." % (
             of_type, tokens[0][0], tokens))
    tok = tokens.pop(0)
    return tok[1]


def peek(tokens, of_type):
    """Returns true if the next token is of the type, false if not.  It does not
    modify the token stream the way match does."""
    if len(tokens) == 0:
        raise ArgumentError('This command expected more on the command line.  Not sure how you did that.')
    return tokens[0][0] == of_type


def trailing_production(data, tokens):
    """Parsing production that handles trailing arguments after a -- is given."""
    data['TRAILING'] = [ x[1] for x in tokens ]
    del tokens[:]


def option_production(data, tokens):
    """The Option production, used for -- or - options.  The number of - aren't 
    important.  It will handle either individual options, or paired options."""
    if peek(tokens, 'trailing'):
        match(tokens, 'trailing')
        trailing_production(data, tokens)
    else:
        opt = match(tokens, 'option')
        if not tokens:
            data[opt] = True
        elif peek(tokens, 'option') or peek(tokens, 'trailing'):
            data[opt] = True
        else:
            value = match(tokens)
            if opt in data:
                try:
                    data[opt].append(value)
                except AttributeError:
                    data[opt] = [
                     data[opt], value]

            else:
                data[opt] = value


def options_production(tokens):
    """List of options, optionally after the command has already been taken off."""
    data = {}
    while tokens:
        option_production(data, tokens)

    return data


def command_production(tokens):
    """The command production, just pulls off a word really."""
    return match(tokens, 'word')


def tokenize(argv):
    """Goes through the command line args and tokenizes each one, trying to match
    something in the scanner.  If any argument doesn't completely parse then it
    is considered a 'string' and returned raw."""
    tokens = []
    for arg in argv:
        toks, remainder = SCANNER.scan(arg)
        if remainder or len(toks) > 1:
            tokens.append(['string', arg])
        else:
            tokens += toks

    return tokens


def parse(argv):
    """
    Tokenizes and then parses the command line as wither a command style or
    plain options style argument list.  It determines this by simply if the
    first argument is a 'word' then it's a command.  If not then it still
    returns the first element of the tuple as None.  This means you can do::

        command, options = args.parse(sys.argv[1:])

    and if `command==None` then it was an option style, if not then it's a command 
    to deal with.
    """
    tokens = tokenize(argv)
    if not tokens:
        return (None, {})
    else:
        if peek(tokens, 'word'):
            return (
             command_production(tokens), options_production(tokens))
        else:
            return (
             None, options_production(tokens))

        return


def function_for(mod, command, ending='_command'):
    """
    Return a reference to the function for a given command.
    """
    return mod.__dict__[(command + ending)]


def determine_kwargs(function):
    """
    Uses the inspect module to figure out what the keyword arguments
    are and what they're defaults should be, then creates a dict with
    that setup.  The results of `determine_kwargs()` is typically handed
    to `ensure_defaults()`.
    """
    spec = inspect.getargspec(function)
    keys = spec[0]
    values = spec[(-1)]
    result = {}
    if not values:
        values = []
    for i in range(0, len(values)):
        keyindex = len(keys) - len(values) + i
        result[keys[keyindex]] = values[i]

    return result


def determine_kwdocs(function):
    """
    Retrieves docstrings written as comments in function definition.
    """
    keys = determine_kwargs(function).keys()
    kwdocs = dict([ (k, None) for k in keys ])
    source = inspect.getsourcelines(function)[0]
    for l in source:
        m = re.match('\\s*([a-z]+)\\s*=\\s*(.+),?\\s*#(.+)\\s*', l)
        if m:
            arg, value, doc = m.groups()
            if arg in keys:
                kwdocs[arg] = doc.strip()
        else:
            kwm = re.match('\\s*\\*\\*([a-z]+)\\s*#(.+)\\s*', l)
            if kwm:
                kwarg, doc = kwm.groups()
                kwdocs['kwargs'] = doc.strip()

    return kwdocs


def ensure_defaults(options, reqs):
    """
    Goes through the given options and the required ones and does the
    work of making sure they match.  It will raise an ArgumentError
    if any option is required.  It will also detect that required TRAILING
    arguments were not given and raise a separate error for that.
    """
    for key in reqs:
        if reqs[key] == None:
            if key not in options:
                if key == 'TRAILING':
                    raise ArgumentError('Additional arguments required after a -- on the command line.')
                else:
                    raise ArgumentError('Option -%s is required by this command.' % key)
        elif key not in options:
            options[key] = reqs[key]

    return


def command_module(mod, command, options, ending='_command', cli_options=None):
    """Takes a module, uses the command to run that function."""
    function = function_for(mod, command, ending)
    kwargs = determine_kwargs(function)
    ensure_defaults(options, kwargs)
    if '__cli_options' in kwargs.keys():
        options['__cli_options'] = cli_options
    try:
        function(**options)
    except TypeError as e:
        tb = traceback.format_exc()
        if 'function(**options)' not in tb.splitlines()[2] and len(tb.splitlines()) / 2 == len(tb.split('File')):
            print '//////////////////////////////////////////////////'
            print tb
            print '//////////////////////////////////////////////////'
            raise Exception('traceback did not have expected contents, modargs is confused, please save the traceback printed above and report this bug')
        if len(tb.splitlines()) == 4:
            print 'Modargs Argument Error: %s' % e.message
            sys.exit(1)
        else:
            print tb
            sys.exit(1)


def available_help(mod, ending='_command'):
    """Returns the dochelp from all functions in this module that have _command
    at the end."""
    help_text = []
    for key in mod.__dict__:
        if key.endswith(ending):
            name = key.split(ending)[0]
            docstring = mod.__dict__[key].__doc__
            if docstring:
                help_text.append(name + ':\n' + docstring)

    return help_text


def help_for_command(mod, command, ending='_command'):
    """
    Returns the help string for just this one command in the module.
    If that command doesn't exist then it will return None so you can
    print an error message.
    """
    if command in available_commands(mod):
        return trim_docstring(mod.__dict__[(command + ending)].__doc__)
    else:
        return
        return


def available_commands(mod, ending='_command'):
    """Just returns the available commands, rather than the whole long list."""
    commands = []
    for key in mod.__dict__:
        if key.endswith(ending):
            commands.append(key.split(ending)[0])

    commands.sort()
    return commands


def invalid_command_message(mod, exit_on_error):
    """Called when you give an invalid command to print what you can use."""
    print 'You must specify a valid command.  Try these: '
    print (', ').join(available_commands(mod))
    if exit_on_error:
        sys.exit(1)
    else:
        return False


def parse_and_run_command(argv, mod, default_command=None, exit_on_error=True, extra_options=None):
    """
    A one-shot function that parses the args, and then runs the command
    that the user specifies.  If you set a default_command, and they don't
    give one then it runs that command.  If you don't specify a command,
    and they fail to give one then it prints an error.

    On this error (failure to give a command) it will call `sys.exit(1)`.
    Set `exit_on_error=False` if you don't want this behavior, like if
    you're doing a unit test.
    """
    try:
        command, options = parse(argv)
        cli_options = options.copy()
        if extra_options:
            options.update(extra_options)
        if not command and default_command:
            command = default_command
        elif not command and not default_command:
            return invalid_command_message(mod, exit_on_error)
        if command not in available_commands(mod):
            return invalid_command_message(mod, exit_on_error)
        command_module(mod, command, options, cli_options=cli_options)
    except ArgumentError as exc:
        print 'ERROR: ', exc
        if exit_on_error:
            sys.exit(1)

    return True


def load_module(name):
    try:
        mod = __import__(name)
    except ImportError:
        return

    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod


def help_command(prog, mod, default_command=None, on=False):
    """Prints the help text generated by help_text."""
    print help_text(prog, mod, default_command, on),


def help_text(prog, mod, default_command=None, on=False):
    """Generates help text based on command docstrings and named arguments."""
    text = []
    leading_spaces = '   '
    if not on:
        text.append('Available commands for %s are:' % prog)
        for cmd in available_commands(mod):
            text.append('%s%s' % (leading_spaces, cmd))

        text.append("\nFor help on a particular command type, e.g., '%s help -on %s'" % (prog, cmd))
    else:
        command_help_text = help_for_command(mod, on)
        if on == default_command:
            prog_on = prog
        else:
            prog_on = '%s %s' % (prog, on)
        dec = '=' * (11 + len(prog_on))
        text.append(dec)
        text.append("Help for '%s'" % prog_on)
        text.append(dec)
        if command_help_text:
            for line in command_help_text.splitlines():
                text.append(leading_spaces + line)

            text.append('')
        fn = function_for(mod, on)
        kwargs = determine_kwargs(fn)
        kwdocs = determine_kwdocs(fn)
        if len(kwargs) > 0:
            text.append(leading_spaces + 'Arguments:')
        for k in sorted(kwargs.keys()):
            if k.startswith('_'):
                continue
            v = kwargs[k]
            doc = kwdocs[k]
            if doc:
                docs = '- %s' % doc
            else:
                docs = ''
            if v is None:
                arg_help_text = '%s%s %s,\n' % (leading_spaces * 2, k, docs)
                arg_help_text += "%s[required] e.g. '%s --%s <value>'\n" % (leading_spaces * 4, prog_on, k)
            else:
                arg_help_text = '%s%s %s\n' % (leading_spaces * 2, k, docs)
                arg_help_text += "%s[optional, defaults to '%s']" % (leading_spaces * 4, v)
                if len(str(v)) > 8:
                    arg_help_text += '\n' + leading_spaces * 4
                if ' ' in str(v):
                    v_str = '"%s"' % v
                else:
                    v_str = v
                arg_help_text += " e.g. '%s --%s %s'\n" % (prog_on, k, v_str)
            text.append(arg_help_text + '\n')

    if kwdocs.has_key('kwargs'):
        text.append('%sKeyword Arguments:\n' % leading_spaces)
        text.append('%s%s\n\n' % (leading_spaces * 2, kwdocs['kwargs']))
    return ('\n').join(text)


def trim_docstring(docstring):
    if not docstring:
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [
     lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return ('\n').join(trimmed)


def completion_command(prog, mod, default_command=None, on=False):
    print completion_text(prog, mod, default_command, on)


def completion_text(prog, mod, default_command=None, on=False):
    cmds = available_commands(mod)
    options_for_commands = []
    for cmd in cmds:
        fn = function_for(mod, cmd)
        kwargs = determine_kwargs(fn)
        keystring = (' ').join([ '-%s' % k for k in kwargs.keys() ])
        options_for_commands.append('       %s)' % cmd)
        options_for_commands.append('           local names="%s"' % keystring)
        options_for_commands.append('           COMPREPLY=( $(compgen -W "${names}" -- ${cur}) )')
        options_for_commands.append('           return 0')
        options_for_commands.append('             ;;')

    cmds_list = (' ').join(cmds)
    text_vars = {'prog': prog, 
       'cmds_list': cmds_list, 
       'options_for_commands_text': ('\n').join(options_for_commands)}
    text = '_%(prog)s()\n{\n    local cur prev cmds base\n    COMPREPLY=()\n    cur="${COMP_WORDS[COMP_CWORD]}"\n    prev="${COMP_WORDS[COMP_CWORD-1]}"\n\n    case "${prev}" in\n%(options_for_commands_text)s\n        *)\n            ;;\n    esac\n\n    cmds="%(cmds_list)s"\n\n    COMPREPLY=($(compgen -W "${cmds}" -- ${cur}))\n    return 0\n}\ncomplete -F _%(prog)s %(prog)s' % text_vars
    return text