# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/google/apputils/app.py
# Compiled at: 2015-02-20 20:25:16
"""Generic entry point for Google applications.

To use this module, simply define a 'main' function with a single
'argv' argument and add the following to the end of your source file:

if __name__ == '__main__':
  app.run()

TODO(user): Remove silly main-detection logic, and force all clients
of this module to check __name__ explicitly.  Fix all current clients
that don't check __name__.
"""
import errno, os, pdb, socket, stat, struct, sys, time, traceback, gflags as flags
FLAGS = flags.FLAGS
flags.DEFINE_boolean('run_with_pdb', 0, 'Set to true for PDB debug mode')
flags.DEFINE_boolean('pdb_post_mortem', 0, 'Set to true to handle uncaught exceptions with PDB post mortem.')
flags.DEFINE_boolean('run_with_profiling', 0, 'Set to true for profiling the script. Execution will be slower, and the output format might change over time.')
flags.DEFINE_string('profile_file', None, 'Dump profile information to a file (for python -m pstats). Implies --run_with_profiling.')
flags.DEFINE_boolean('use_cprofile_for_profiling', True, 'Use cProfile instead of the profile module for profiling. This has no effect unless --run_with_profiling is set.')
EXCEPTION_HANDLERS = []
help_text_wrap = False

class Error(Exception):
    pass


class UsageError(Error):
    """The arguments supplied by the user are invalid.

  Raise this when the arguments supplied are invalid from the point of
  view of the application. For example when two mutually exclusive
  flags have been supplied or when there are not enough non-flag
  arguments. It is distinct from flags.FlagsError which covers the lower
  level of parsing and validating individual flags.
  """

    def __init__(self, message, exitcode=1):
        Error.__init__(self, message)
        self.exitcode = exitcode


class HelpFlag(flags.BooleanFlag):
    """Special boolean flag that displays usage and raises SystemExit."""
    NAME = 'help'

    def __init__(self):
        flags.BooleanFlag.__init__(self, self.NAME, 0, 'show this help', short_name='?', allow_override=1)

    def Parse(self, arg):
        if arg:
            usage(shorthelp=1, writeto_stdout=1)
            print
            print 'Try --helpfull to get a list of all flags.'
            sys.exit(1)


class HelpshortFlag(HelpFlag):
    """--helpshort is an alias for --help."""
    NAME = 'helpshort'


class HelpfullFlag(flags.BooleanFlag):
    """Display help for flags in this module and all dependent modules."""

    def __init__(self):
        flags.BooleanFlag.__init__(self, 'helpfull', 0, 'show full help', allow_override=1)

    def Parse(self, arg):
        if arg:
            usage(writeto_stdout=1)
            sys.exit(1)


class HelpXMLFlag(flags.BooleanFlag):
    """Similar to HelpfullFlag, but generates output in XML format."""

    def __init__(self):
        flags.BooleanFlag.__init__(self, 'helpxml', False, 'like --helpfull, but generates XML output', allow_override=1)

    def Parse(self, arg):
        if arg:
            flags.FLAGS.WriteHelpInXMLFormat(sys.stdout)
            sys.exit(1)


class BuildDataFlag(flags.BooleanFlag):
    """Boolean flag that writes build data to stdout and exits."""

    def __init__(self):
        flags.BooleanFlag.__init__(self, 'show_build_data', 0, 'show build data and exit')

    def Parse(self, arg):
        if arg:
            sys.stdout.write(build_data.BuildData())
            sys.exit(0)


def parse_flags_with_usage(args):
    """Try parsing the flags, printing usage and exiting if unparseable."""
    try:
        argv = FLAGS(args)
        return argv
    except flags.FlagsError as error:
        sys.stderr.write('FATAL Flags parsing error: %s\n' % error)
        sys.stderr.write('Pass --helpshort or --helpfull to see help on flags.\n')
        sys.exit(1)


_define_help_flags_called = False

def DefineHelpFlags():
    """Register help flags. Idempotent."""
    global _define_help_flags_called
    if not _define_help_flags_called:
        flags.DEFINE_flag(HelpFlag())
        flags.DEFINE_flag(HelpshortFlag())
        flags.DEFINE_flag(HelpfullFlag())
        flags.DEFINE_flag(HelpXMLFlag())
        flags.DEFINE_flag(BuildDataFlag())
        _define_help_flags_called = True


def RegisterAndParseFlagsWithUsage():
    """Register help flags, parse arguments and show usage if appropriate.

  Returns:
    remaining arguments after flags parsing
  """
    DefineHelpFlags()
    argv = parse_flags_with_usage(sys.argv)
    return argv


def really_start(main=None):
    """Initializes flag values, and calls main with non-flag arguments.

  Only non-flag arguments are passed to main().  The return value of main() is
  used as the exit status.

  Args:
    main: Main function to run with the list of non-flag arguments, or None
      so that sys.modules['__main__'].main is to be used.
  """
    argv = RegisterAndParseFlagsWithUsage()
    if main is None:
        main = sys.modules['__main__'].main
    try:
        if FLAGS.run_with_pdb:
            sys.exit(pdb.runcall(main, argv))
        elif FLAGS.run_with_profiling or FLAGS.profile_file:
            import atexit
            if FLAGS.use_cprofile_for_profiling:
                import cProfile as profile
            else:
                import profile
            profiler = profile.Profile()
            if FLAGS.profile_file:
                atexit.register(profiler.dump_stats, FLAGS.profile_file)
            else:
                atexit.register(profiler.print_stats)
            retval = profiler.runcall(main, argv)
            sys.exit(retval)
        else:
            sys.exit(main(argv))
    except UsageError as error:
        usage(shorthelp=1, detailed_error=error, exitcode=error.exitcode)
    except:
        if FLAGS.pdb_post_mortem:
            traceback.print_exc()
            pdb.post_mortem()
        raise

    return


def run():
    """Begin executing the program.

  - Parses command line flags with the flag module.
  - If there are any errors, print usage().
  - Calls main() with the remaining arguments.
  - If main() raises a UsageError, print usage and the error message.
  """
    return _actual_start()


def _actual_start():
    """Another layer in the starting stack."""
    tb = None
    try:
        raise ZeroDivisionError('')
    except ZeroDivisionError:
        tb = sys.exc_info()[2]

    if not tb:
        raise AssertionError
        prev_prev_frame = tb.tb_frame.f_back.f_back
        return prev_prev_frame or None
    else:
        prev_prev_name = prev_prev_frame.f_globals.get('__name__', None)
        if prev_prev_name != '__main__' and not prev_prev_name.endswith('.appcommands'):
            return
        del tb
        if hasattr(sys, 'exc_clear'):
            sys.exc_clear()
        try:
            really_start()
        except SystemExit as e:
            raise
        except Exception as e:
            for handler in EXCEPTION_HANDLERS:
                try:
                    if handler.Wants(e):
                        handler.Handle(e)
                except:
                    sys.stderr.write(traceback.format_exc())
                    raise

            raise

        return


def usage(shorthelp=0, writeto_stdout=0, detailed_error=None, exitcode=None):
    """Write __main__'s docstring to stderr with some help text.

  Args:
    shorthelp: print only flags from this module, rather than all flags.
    writeto_stdout: write help message to stdout, rather than to stderr.
    detailed_error: additional detail about why usage info was presented.
    exitcode: if set, exit with this status code after writing help.
  """
    if writeto_stdout:
        stdfile = sys.stdout
    else:
        stdfile = sys.stderr
    doc = sys.modules['__main__'].__doc__
    if not doc:
        doc = '\nUSAGE: %s [flags]\n' % sys.argv[0]
        doc = flags.TextWrap(doc, indent='       ', firstline_indent='')
    else:
        num_specifiers = doc.count('%') - 2 * doc.count('%%')
        try:
            doc %= (sys.argv[0],) * num_specifiers
        except (OverflowError, TypeError, ValueError):
            pass

        if help_text_wrap:
            doc = flags.TextWrap(flags.DocToHelp(doc))
        if shorthelp:
            flag_str = FLAGS.MainModuleHelp()
        else:
            flag_str = str(FLAGS)
        try:
            stdfile.write(doc)
            if flag_str:
                stdfile.write('\nflags:\n')
                stdfile.write(flag_str)
            stdfile.write('\n')
            if detailed_error is not None:
                stdfile.write('\n%s\n' % detailed_error)
        except IOError as e:
            if e.errno != errno.EPIPE:
                raise

    if exitcode is not None:
        sys.exit(exitcode)
    return


class ExceptionHandler(object):
    """Base exception handler from which other may inherit."""

    def Wants(self, unused_exc):
        """Check if this exception handler want to handle this exception.

    Args:
      unused_exc: Exception, the current exception

    Returns:
      boolean

    This base handler wants to handle all exceptions, override this
    method if you want to be more selective.
    """
        return True

    def Handle(self, exc):
        """Do something with the current exception.

    Args:
      exc: Exception, the current exception

    This method must be overridden.
    """
        raise NotImplementedError()


def InstallExceptionHandler(handler):
    """Install an exception handler.

  Args:
    handler: an object conforming to the interface defined in ExceptionHandler

  Raises:
    TypeError: handler was not of the correct type

  All installed exception handlers will be called if main() exits via
  an abnormal exception, i.e. not one of SystemExit, KeyboardInterrupt,
  FlagsError or UsageError.
  """
    if not isinstance(handler, ExceptionHandler):
        raise TypeError('handler of type %s does not inherit from ExceptionHandler' % type(handler))
    EXCEPTION_HANDLERS.append(handler)