# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/gitinspector.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
import localization
localization.init()
import atexit, basedir, blame, changes, clone, config, extensions, filtering, format, help, interval, getopt, metrics, os, optval, outputable, responsibilities, sys, terminal, timeline, version

class Runner:

    def __init__(self):
        self.hard = False
        self.include_metrics = False
        self.list_file_types = False
        self.localize_output = False
        self.repo = b'.'
        self.responsibilities = False
        self.grading = False
        self.timeline = False
        self.useweeks = False

    def output(self):
        if not self.localize_output:
            localization.disable()
        terminal.skip_escapes(not sys.stdout.isatty())
        terminal.set_stdout_encoding()
        previous_directory = os.getcwd()
        os.chdir(self.repo)
        absolute_path = basedir.get_basedir_git()
        os.chdir(absolute_path)
        format.output_header()
        outputable.output(changes.ChangesOutput(self.hard))
        if changes.get(self.hard).get_commits():
            outputable.output(blame.BlameOutput(self.hard, self.useweeks))
            if self.timeline:
                outputable.output(timeline.Timeline(changes.get(self.hard), self.useweeks))
            if self.include_metrics:
                outputable.output(metrics.Metrics())
            if self.responsibilities:
                outputable.output(responsibilities.ResponsibilitiesOutput(self.hard, self.useweeks))
            outputable.output(filtering.Filtering())
            if self.list_file_types:
                outputable.output(extensions.Extensions())
        format.output_footer()
        os.chdir(previous_directory)


def __check_python_version__():
    if sys.version_info < (2, 6):
        python_version = str(sys.version_info[0]) + b'.' + str(sys.version_info[1])
        sys.exit(_(b'gitinspector requires at least Python 2.6 to run (version {0} was found).').format(python_version))


def main():
    terminal.check_terminal_encoding()
    terminal.set_stdin_encoding()
    argv = terminal.convert_command_line_to_utf8()
    __run__ = Runner()
    try:
        __opts__, __args__ = optval.gnu_getopt(argv[1:], b'f:F:hHlLmrTwx:', [b'exclude=', b'file-types=', b'format=',
         b'hard:true', b'help', b'list-file-types:true',
         b'localize-output:true', b'metrics:true', b'responsibilities:true',
         b'since=', b'grading:true', b'timeline:true', b'until=', b'version',
         b'weeks:true'])
        for arg in __args__:
            __run__.repo = arg

        __run__.repo = clone.create(__run__.repo)
        config.init(__run__)
        clear_x_on_next_pass = True
        for o, a in __opts__:
            if o in ('-h', '--help'):
                help.output()
                sys.exit(0)
            elif o in ('-f', '--file-types'):
                extensions.define(a)
            elif o in ('-F', '--format'):
                if not format.select(a):
                    raise format.InvalidFormatError(_(b'specified output format not supported.'))
            elif o == b'-H':
                __run__.hard = True
            elif o == b'--hard':
                __run__.hard = optval.get_boolean_argument(a)
            elif o == b'-l':
                __run__.list_file_types = True
            elif o == b'--list-file-types':
                __run__.list_file_types = optval.get_boolean_argument(a)
            elif o == b'-L':
                __run__.localize_output = True
            elif o == b'--localize-output':
                __run__.localize_output = optval.get_boolean_argument(a)
            elif o == b'-m':
                __run__.include_metrics = True
            elif o == b'--metrics':
                __run__.include_metrics = optval.get_boolean_argument(a)
            elif o == b'-r':
                __run__.responsibilities = True
            elif o == b'--responsibilities':
                __run__.responsibilities = optval.get_boolean_argument(a)
            elif o == b'--since':
                interval.set_since(a)
            elif o == b'--version':
                version.output()
                sys.exit(0)
            elif o == b'--grading':
                grading = optval.get_boolean_argument(a)
                __run__.include_metrics = grading
                __run__.list_file_types = grading
                __run__.responsibilities = grading
                __run__.grading = grading
                __run__.hard = grading
                __run__.timeline = grading
                __run__.useweeks = grading
            elif o == b'-T':
                __run__.timeline = True
            elif o == b'--timeline':
                __run__.timeline = optval.get_boolean_argument(a)
            elif o == b'--until':
                interval.set_until(a)
            elif o == b'-w':
                __run__.useweeks = True
            elif o == b'--weeks':
                __run__.useweeks = optval.get_boolean_argument(a)
            elif o in ('-x', '--exclude'):
                if clear_x_on_next_pass:
                    clear_x_on_next_pass = False
                    filtering.clear()
                filtering.add(a)

        __check_python_version__()
        __run__.output()
    except (filtering.InvalidRegExpError, format.InvalidFormatError, optval.InvalidOptionArgument, getopt.error) as exception:
        print(sys.argv[0], b'\x08:', exception.msg, file=sys.stderr)
        print(_(b"Try `{0} --help' for more information.").format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)


@atexit.register
def cleanup():
    clone.delete()


if __name__ == b'__main__':
    main()