# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commandline/commandline.py
# Compiled at: 2009-06-13 10:52:59
__doc__ = 'This is a helper module for making intuitive command line programs with \nzero effort. It takes a function signature like:\n example_function(string1, string2=\'something\', string3=\'something else\')\nand turns it into a simple command-line app with usage:\n example_program string1 [string2 [string3]]\n\nAll you have to do is:\n if __name__ == "__main__":\n    import commandline\n    commandline.run_as_main(example_function)\n\nLimitations\n============\n\nNote that it currently can\'t print help information for arguments other than \ntheir default values, but it will print your docstring for you if that\'s of \nany use.\nHelp for arguments will probably come with python3000\'s function annotations. \nhttp://www.python.org/dev/peps/pep-3107/\n\nArgument types are inferred from the default arguments. \nCurrently supported are: int, float, bool, str, commandline.Choice\nIf things don\'t have a default argument, I can\'t infer the type so assume str.\n\n\n'
CHANGELOG = '\nFor more changelog stuff, try reading my bzr log.\n\n#Things passed in as positional arguments will currently be passed in as strings, \n#and override things passed in as options. I really need to migrate to some \n#optparse-like library that understands positional arguments.\nfixed 20090612 fo 0.1.2\n\n#Currently, only a single function can be exposed per executable. \n#Eventually, I want to be able to do subcommands, like how bzr does\nFixed 2009, with expose_subcommands, but still a bit messy/bad at handling errors\nI think that defining some kind of @subcommand(\'progname\') decorator might be better.\nand then use run(\'progname\') to run it. Guess we\'ll see.\n\n# All arguments are currently treated as strings. If you want them passed in as \n# something else, use map:\n#  def distance(x, y, z):\n#      x, y, z = map(float, [x, y, z])\n#      print sqrt(x**2 + y**2 + z**2)\n# I might make a decorator for this kind of thing at some point, but in reality,\n# I think it would be better done using annotations.\nFIXED 2009: Types of arguments are now inferred from their default values.\nBoolean options are translated into a --argname and a --no_argname flag.\n\ncurrently, you can\'t run [bound] class methods as main, because of a limitation in the "inspect" module.\n#FIXED 20090221\n\nI need to think about how to create a "choice" data type which doesn\'t screw up the API\ndef example(name=choice(\'Fred\', \'Bill\')):\n    print name \nname must quack like \'Fred\': I will have to inheret from string, but have an "alternatives" member variable, which can be used by commandline.\n#Done 20090221\n\n\n'
__all__ = [
 'run_as_main', 'run_if_main', 'run_as_subcommand', 'choice']
import sys, types
from optparse import OptionParser
from inspect_convenience import get_usage, get_compulsary_args, get_args_with_defaults, get_argnames, no_of_compulsary_args, get_doc

class Choice(str):
    """This is just so that we can add members to string objects."""


def choice(*choices):
    """
    returns something which behaves like a string, but provides api docs
    which can be read by the commandline interface translator, telling
    the user which strings are valid options.

    Usage:
    def which_door(door=choice('a','b','c')):
        print 'you chose door', door
    """
    ret = Choice(choices[0])
    ret.choices = choices
    return ret


def _add_to_parser(parser, argname, default=None):
    """An internal helper function to wrap around optparse."""
    assert argname == argname.strip('_'), 'Limitation caused by optparse.'
    if default is None:
        parser.add_option('--' + argname, type='str', dest=argname, help='This must be specified as an option or argument.')
    elif isinstance(default, bool):
        parser.add_option('--' + argname, action='store_true', default=default, dest=argname, help='default="%default"')
        parser.add_option('--no' + argname, action='store_false', default=default, dest=argname, help='opposite of"')
    elif isinstance(default, Choice):
        parser.add_option('--' + argname, type='choice', default=default, dest=argname, choices=default.choices, help='default="%default"')
    elif isinstance(default, int):
        parser.add_option('--' + argname, type='int', default=default, dest=argname, help='default=%default')
    elif isinstance(default, float):
        parser.add_option('--' + argname, type='float', default=default, dest=argname, help='default=%default')
    elif isinstance(default, complex):
        parser.add_option('--' + argname, type='complex', default=default, dest=argname, help='default=%default')
    elif isinstance(default, str):
        parser.add_option('--' + argname, type='str', default=default, dest=argname, help='default="%default"')
    else:
        raise TypeError("Sorry. You can't have default arguments of type %s" % type(default))
    return


def expose_subcommands(name):
    """See expose_module_subcommands"""
    expose_module_subcommands(name)


def expose_module_subcommands(name):
    """Only exposes functions defined within the file named.
    This function is likely to be depricated, as it uses a lot of magic."""
    if name == '__main__':
        module = sys.modules[name]
        subcommands = get_subcommand_names(module)
        try:
            subcommand = sys.argv[1]
        except KeyError:
            print_usage(subcommands)
            exit(1)
            return
        else:
            if subcommand in subcommands:
                func = getattr(module, sys.argv[1])
                run_as_subcommand(func, sys.argv[2:])
            else:
                print subcommand, 'is not a valid subcommand.'
                print_usage(subcommands)


def print_usage(subcommands):
    """This is the usage message for a script with subcommands."""
    print 'Usage:', sys.argv[0], 'command [args] [options]'
    print 'commands are:'
    for subcommand in subcommands:
        print subcommand


def get_subcommand_names(module):
    """An internal function for inspecting modules looking for subcommands.
    Lists all functions defined within the module (no imported functions or 
    methods)"""
    subcommands = []
    for obj_name in dir(module):
        if obj_name == obj_name.strip('_'):
            obj = getattr(module, obj_name)
            if isinstance(obj, types.FunctionType):
                if obj.__module__ == module.__name__:
                    subcommands.append(obj_name)

    return subcommands


def run_if_main(name):
    """ A convenience function. At the bottom of your file, put:
     import commandline
     commandline.run_if_main(__name__)

    which is equivalent to:
     if __name__ == "__main__":
         import commandline
         commandline.run_as_main(main)
    
    I might delete this function in the future.
    """
    if name == '__main__':
        run_as_main(sys.modules[name].main)


def run_as_main(func, args=sys.argv[1:], name=sys.argv[0]):
    """ At the bottom of your file, put:
    if __name__ == "__main__":
        import commandline
        commandline.run_as_main(main)
    and suddenly, you have yourself a command line program.
    
    >>> import commandline
    >>> def test1(arg1, arg2=2, arg3=3):
    ...     print arg1, arg2, arg3
    ...
    >>> commandline.run_as_main(test1, ['hi'])
    hi 2 3
    """
    return run_as_subcommand(func, args, name)


def create_parser(func, command_name):
    """Creates an OptParse.OptionParser, and populates it using the arguments
    to func.
    """
    usage = get_usage(func, command_name)
    parser = OptionParser(usage=usage, epilog=get_doc(func))
    for (argname, default) in get_args_with_defaults(func):
        _add_to_parser(parser, argname, default)

    for argname in get_compulsary_args(func):
        _add_to_parser(parser, argname)

    return parser


def fudge_args(args, argnames):
    """Basically add positional argument support to optparse"""
    for i in range(min(len(args), len(argnames))):
        if not args[i].startswith('-'):
            args[i] = '--%s=%s' % (argnames[i], args[i])
        else:
            break

    return args


def run_as_subcommand(func, args=sys.argv[2:], command_name=None):
    """An internal function for enabling subcommands."""
    if command_name is None:
        command_name = func.func_name
    kwargs = get_kwargs(func, args, command_name)
    if kwargs is not None:
        return func(**kwargs)
    else:
        exit(1)
        return


def get_kwargs(func, args, command_name=None):
    """Creates a parser for the commandline args, and turns them into a form 
    that can be passed into func as kwargs. It also does some fudging, so that
    positional arguments get parsed by optparse correctly.
    
    returns kwargs, or None if there are errors (might make it raise in future.
    """
    if command_name is None:
        command_name = func.func_name
    argnames = get_argnames(func)
    args = fudge_args(args, argnames)
    parser = create_parser(func, command_name)
    (options, leftover_args) = parser.parse_args(args)
    kwargs = dict([ (key, value) for (key, value) in options.__dict__.items() if key == key.strip('_')
                  ])
    num_compulsary = no_of_compulsary_args(func)
    argnames = get_argnames(func)
    missingnames = [ name for name in argnames if kwargs[name] is None ]
    if missingnames:
        parser.print_usage()
        print 'The following compulsory arguments are missing:',
        print (', ').join(missingnames)
    elif leftover_args:
        parser.print_usage()
        print '(Please put options last, and no more args than shown.)'
        print 'Unexpected argument(s):', (', ').join(leftover_args)
    else:
        return kwargs
    return


TESTMODE = False

def exit(status):
    """Set TESTMODE to True to allow doctests to work. 
    Otherwise we get screwed by SystemExit exceptions."""
    if TESTMODE:
        pass
    else:
        sys.exit(status)


if __name__ == '__main__':

    def example_function(string1, string2='something', int1=1):
        """This is just an example. You should really try writing your own
        commandline programs."""
        print string1, string2, int1


    run_as_main(example_function)