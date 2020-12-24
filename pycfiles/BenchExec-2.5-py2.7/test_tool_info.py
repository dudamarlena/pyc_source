# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_tool_info.py
# Compiled at: 2019-11-28 13:06:29
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse, contextlib, logging, inspect, os, sys
sys.dont_write_bytecode = True
import benchexec, benchexec.benchexec
from benchexec import model
import benchexec.tools.template
COLOR_RED = b'\x1b[31;1m'
COLOR_GREEN = b'\x1b[32;1m'
COLOR_ORANGE = b'\x1b[33;1m'
COLOR_MAGENTA = b'\x1b[35;1m'
COLOR_DEFAULT = b'\x1b[m'
COLOR_DESCRIPTION = COLOR_MAGENTA
COLOR_VALUE = COLOR_GREEN
COLOR_WARNING = COLOR_RED
if not sys.stdout.isatty():
    COLOR_DEFAULT = b''
    COLOR_DESCRIPTION = b''
    COLOR_VALUE = b''
    COLOR_WARNING = b''

def print_value(description, value, extra_line=False):
    print((b'{}{}{}:{}â\x80\x9c{}{}{}â\x80\x9d').format(COLOR_DESCRIPTION, description, COLOR_DEFAULT, b'\n\t' if extra_line else b' ', COLOR_VALUE, value, COLOR_DEFAULT), file=sys.stderr)


def print_list(description, value):
    print_value(description, list(value), extra_line=True)


def print_multiline_list(description, values):
    print((b'{}{}{}:').format(COLOR_DESCRIPTION, description, COLOR_DEFAULT), file=sys.stderr)
    for value in values:
        print((b'\tâ\x80\x9c{}{}{}â\x80\x9d').format(COLOR_VALUE, value, COLOR_DEFAULT), file=sys.stderr)


def print_multiline_text(description, value):
    if value is None:
        print((b'{}{}{}: {}None{}').format(COLOR_DESCRIPTION, description, COLOR_DEFAULT, COLOR_WARNING, COLOR_DEFAULT), file=sys.stderr)
    elif not value.strip():
        print((b'{}{}{}: {}â\x80\x9c{}â\x80\x9d{}').format(COLOR_DESCRIPTION, description, COLOR_DEFAULT, COLOR_WARNING, value, COLOR_DEFAULT), file=sys.stderr)
    else:
        print((b'{}{}{}:').format(COLOR_DESCRIPTION, description, COLOR_DEFAULT), file=sys.stderr)
        for line in value.splitlines():
            print((b'\t{}{}{}').format(COLOR_VALUE, line, COLOR_DEFAULT), file=sys.stderr)

    return


@contextlib.contextmanager
def log_if_unsupported(msg):
    """Catch any exception in block and log it with a message about an unsupported feature"""
    try:
        yield
    except BaseException as e:
        logging.warning(b'Tool-info module does not support %s: â\x80\x9c%sâ\x80\x9d', msg, e, exc_info=not isinstance(e, benchexec.tools.template.UnsupportedFeatureException))


def print_tool_info(tool):
    print_multiline_text(b'Documentation of tool module', inspect.getdoc(tool))
    print_value(b'Name of tool', tool.name())
    executable = tool.executable()
    print_value(b'Executable', executable)
    if not os.path.isabs(executable):
        print_value(b'Executable (absolute path)', os.path.abspath(executable))
    else:
        logging.warning(b'Path to executable is absolute, this might be problematic in scenarios where runs are distributed to other machines.')
    try:
        print_value(b'Version', tool.version(executable))
    except:
        logging.warning(b'Determining version failed:', exc_info=1)

    working_directory = tool.working_directory(executable)
    print_value(b'Working directory', working_directory)
    if not os.path.isabs(working_directory):
        print_value(b'Working directory (absolute path)', os.path.abspath(working_directory))
    program_files = list(tool.program_files(executable))
    if program_files:
        print_multiline_list(b'Program files', program_files)
        print_multiline_list(b'Program files (absolute paths)', map(os.path.abspath, program_files))
    else:
        logging.warning(b'Tool module specifies no program files.')
    environment = tool.environment(executable)
    new_environment = environment.pop(b'newEnv', {})
    if new_environment:
        print_multiline_list(b'Additional environment variables', ((b'{}={}').format(variable, value) for variable, value in new_environment.items()))
    append_environment = environment.pop(b'additionalEnv', {})
    if append_environment:
        print_multiline_list(b'Appended environment variables', ((b'{}=${{{}}}{}').format(variable, variable, value) for variable, value in append_environment.items()))
    if environment:
        logging.warning(b'Tool module returned invalid entries for environment, these will be ignored: â\x80\x9c%sâ\x80\x9d', environment)
    with log_if_unsupported(b'tasks without options, property file, and resource limits'):
        cmdline = model.cmdline_for_run(tool, executable, [], [b'INPUT.FILE'], None, {})
        print_list(b'Minimal command line', cmdline)
        if b'INPUT.FILE' not in (b' ').join(cmdline):
            logging.warning(b'Tool module ignores input file.')
    with log_if_unsupported(b'tasks with command-line options'):
        cmdline = model.cmdline_for_run(tool, executable, [b'-SOME_OPTION'], [b'INPUT.FILE'], None, {})
        print_list(b'Command line with parameter', cmdline)
        if b'-SOME_OPTION' not in cmdline:
            logging.warning(b'Tool module ignores command-line options.')
    with log_if_unsupported(b'tasks with property file'):
        cmdline = model.cmdline_for_run(tool, executable, [], [b'INPUT.FILE'], b'PROPERTY.PRP', {})
        print_list(b'Command line with property file', cmdline)
        if b'PROPERTY.PRP' not in (b' ').join(cmdline):
            logging.warning(b'Tool module ignores property file.')
    with log_if_unsupported(b'tasks with multiple input files'):
        cmdline = model.cmdline_for_run(tool, executable, [], [b'INPUT1.FILE', b'INPUT2.FILE'], None, {})
        print_list(b'Command line with multiple input files', cmdline)
        if b'INPUT1.FILE' in (b' ').join(cmdline) and b'INPUT2.FILE' not in (b' ').join(cmdline):
            logging.warning(b'Tool module ignores all but first input file.')
    with log_if_unsupported(b'tasks with CPU-time limit'):
        cmdline = model.cmdline_for_run(tool, executable, [], [b'INPUT.FILE'], None, {model.SOFTTIMELIMIT: 123})
        print_list(b'Command line CPU-time limit', cmdline)
    return tool


def analyze_tool_output(tool, file):
    try:
        output = file.readlines()
    except (IOError, UnicodeDecodeError) as e:
        logging.warning(b'Cannot read tool output from â\x80\x9c%sâ\x80\x9d: %s', file.name, e)
        return

    try:
        result = tool.determine_result(returncode=0, returnsignal=0, output=output, isTimeout=False)
        print_value(b'Result of analyzing tool output in â\x80\x9c' + file.name + b'â\x80\x9d', result, extra_line=True)
    except:
        logging.warning(b'Tool module failed to analyze result in â\x80\x9c%sâ\x80\x9d:', file.name, exc_info=1)


def main(argv=None):
    """
    A simple command-line interface to print information provided by a tool info.
    """
    if sys.version_info < (3, ):
        sys.exit(b'benchexec.test_tool_info needs Python 3 to run.')
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(fromfile_prefix_chars=b'@', description=b'Test a tool info for BenchExec and print out all relevant information this tool info provides.\n           Part of BenchExec: https://github.com/sosy-lab/benchexec/')
    parser.add_argument(b'tool', metavar=b'TOOL', help=b'name of tool info to test')
    parser.add_argument(b'--tool-output', metavar=b'OUTPUT_FILE', nargs=b'+', type=argparse.FileType(b'r'), help=b'optional names of text files with example outputs of a tool run')
    benchexec.benchexec.add_container_args(parser)
    options = parser.parse_args(argv[1:])
    logging.basicConfig(format=COLOR_WARNING + b'%(levelname)s: %(message)s' + COLOR_DEFAULT)
    print_value(b'Name of tool module', options.tool)
    try:
        tool_module, tool = model.load_tool_info(options.tool, options)
        try:
            print_value(b'Full name of tool module', tool_module)
            print_tool_info(tool)
            if options.tool_output:
                for file in options.tool_output:
                    analyze_tool_output(tool, file)

        finally:
            tool.close()

    except benchexec.BenchExecException as e:
        sys.exit(str(e))

    return


if __name__ == b'__main__':
    main()