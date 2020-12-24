# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyrg.py
# Compiled at: 2010-11-08 11:24:11
"""pyrg - colorized Python's UnitTest Result Tool"""
from ConfigParser import ConfigParser
from subprocess import Popen, PIPE
from select import poll, POLLIN
from optparse import OptionParser
import sys, re, os, pwd
__version__ = '0.2.6'
__author__ = 'Hideo Hattroi <hhatto.jp@gmail.com>'
__license__ = 'NewBSDLicense'
__all__ = [
 'get_color', 'parse_unittest_result_verbose',
 'parse_unittest_result', 'set_configuration']
DEFAULT_CONFIG_PATH = '/home/%s/.pyrgrc' % pwd.getpwuid(os.getuid())[0]
PRINT_COLOR_SET_DEFAULT = {'ok': 'green', 
   'fail': 'red', 
   'error': 'yellow', 
   'function': 'cyan'}
PRINT_COLOR_SET = PRINT_COLOR_SET_DEFAULT.copy()
COLOR_MAP = {'black': '\x1b[30m%s\x1b[0m', 
   'gray': '\x1b[1;30m%s\x1b[0m', 
   'red': '\x1b[31m%s\x1b[0m', 
   'pink': '\x1b[1;31m%s\x1b[0m', 
   'darkred': '\x1b[2;31m%s\x1b[0m', 
   'green': '\x1b[32m%s\x1b[0m', 
   'yellowgreen': '\x1b[1;32m%s\x1b[0m', 
   'darkgreen': '\x1b[2;32m%s\x1b[0m', 
   'brown': '\x1b[33m%s\x1b[0m', 
   'yellow': '\x1b[1;33m%s\x1b[0m', 
   'gold': '\x1b[2;33m%s\x1b[0m', 
   'blue': '\x1b[34m%s\x1b[0m', 
   'lightblue': '\x1b[1;34m%s\x1b[0m', 
   'darkblue': '\x1b[2;34m%s\x1b[0m', 
   'magenta': '\x1b[35m%s\x1b[0m', 
   'lightmagenta': '\x1b[1;35m%s\x1b[0m', 
   'darkmagenta': '\x1b[2;35m%s\x1b[0m', 
   'cyan': '\x1b[36m%s\x1b[0m', 
   'lightcyan': '\x1b[1;36m%s\x1b[0m', 
   'darkcyan': '\x1b[2;36m%s\x1b[0m', 
   'silver': '\x1b[37m%s\x1b[0m', 
   'white': '\x1b[1;37m%s\x1b[0m', 
   'darksilver': '\x1b[2;37m%s\x1b[0m'}

def get_color(key):
    """color name get from COLOR_MAP dict."""
    global PRINT_COLOR_SET
    return COLOR_MAP[PRINT_COLOR_SET[key]]


def parse_result_line(line):
    """parse to test result when fail tests"""
    err = False
    fail = False
    if 'errors' in line:
        err = True
    if 'failures' in line:
        fail = True
    if err and fail:
        f = line.split('=')[1].split(',')[0]
        e = line.split('=')[2].split(')')[0]
        result = '(%s=%s, ' % (get_color('fail') % 'failures',
         get_color('fail') % f)
        result += '%s=%s)' % (get_color('error') % 'errors',
         get_color('error') % e)
    elif fail and not err:
        l = line.split('=')[1].split(')')[0]
        result = '(%s=%s)' % (get_color('fail') % 'failures',
         get_color('fail') % l)
    elif err and not fail:
        l = line.split('=')[1].split(')')[0]
        result = '(%s=%s)' % (get_color('error') % 'errors',
         get_color('error') % l)
    return get_color('fail') % 'FAILED' + ' %s' % result


def parse_lineone(line):
    """parse to test result line1"""
    results = []
    line = line.strip()
    for char in line:
        if '.' == char:
            results.append(get_color('ok') % '.')
        elif 'E' == char:
            results.append(get_color('error') % 'E')
        elif 'F' == char:
            results.append(get_color('fail') % 'F')
        else:
            results.append(char)

    return ('').join(results)


def coloring_method(line):
    """colorized method line"""
    return get_color('function') % line


def parse_unittest_result(lines):
    """parse test result"""
    results = []
    err_verbose = re.compile('ERROR:')
    fail_verbose = re.compile('FAIL:')
    unittests_ok = re.compile('OK')
    unittests_failed = re.compile('FAILED')
    if not lines:
        return ''
    results.append(parse_lineone(lines[0]) + '\n')
    for line in lines[1:]:
        if unittests_ok.match(line):
            result = get_color('ok') % 'OK'
        elif unittests_failed.match(line):
            result = parse_result_line(line)
        elif fail_verbose.match(line):
            result = '%s: %s\n' % (get_color('fail') % 'FAIL',
             coloring_method(line[6:-1]))
        elif err_verbose.match(line):
            result = '%s: %s\n' % (get_color('error') % 'ERROR',
             coloring_method(line[7:-1]))
        else:
            result = line
        results.append(result)

    return ('').join(results)


def parse_unittest_result_verbose(lines):
    """parse test result, verbose print mode."""
    ok = re.compile('ok$')
    fail = re.compile('FAIL$')
    err = re.compile('ERROR$')
    fail_verbose = re.compile('FAIL:')
    err_verbose = re.compile('ERROR:')
    unittests_ok = re.compile('OK')
    unittests_failed = re.compile('FAILED')
    results = []
    for line in lines:
        if ok.search(line):
            tmp = ok.split(line)
            result = tmp[0] + get_color('ok') % 'ok' + '\n'
        elif fail.search(line):
            tmp = fail.split(line)
            result = tmp[0] + get_color('fail') % 'FAIL' + '\n'
        elif err.search(line):
            tmp = err.split(line)
            result = tmp[0] + get_color('error') % 'ERROR' + '\n'
        elif fail_verbose.match(line):
            result = '%s: %s\n' % (get_color('fail') % 'FAIL',
             coloring_method(line[6:-1]))
        elif err_verbose.match(line):
            result = '%s: %s\n' % (get_color('error') % 'ERROR',
             coloring_method(line[7:-1]))
        elif unittests_ok.match(line):
            result = get_color('ok') % 'OK'
        elif unittests_failed.match(line):
            result = parse_result_line(line)
        else:
            result = line
        results.append(result)

    return ('').join(results)


def set_configuration(filename):
    """setting to printing color map"""
    ret = PRINT_COLOR_SET_DEFAULT.copy()
    if not os.path.exists(filename):
        return ret
    configure = ConfigParser()
    configure.read(filename)
    for (setkey, color) in configure.items('color'):
        if setkey not in PRINT_COLOR_SET:
            continue
        if color in COLOR_MAP:
            ret[setkey] = color
        else:
            ret[setkey] = PRINT_COLOR_SET_DEFAULT[setkey]

    return ret


def get_optionparser():
    """return to optparse's OptionParser object."""
    parser = OptionParser(version='pyrg: %s' % __version__, description=__doc__, usage='Usage: pyrg [options] TEST_SCRIPT.py\n     : python TEST_SCRIPT.py |& pyrg')
    parser.add_option('-v', '--verbose', action='store_true', dest='mode_verbose', help='print to verbose result for unittest.')
    parser.add_option('-d', '--default-color', action='store_true', dest='mode_defaultcolor', help='used to default color setting.')
    parser.add_option('-f', '--config-file', dest='config_filename', help='configuration file path')
    return parser


def check_verbose(line):
    verbose = re.compile('(ok$|ERROR$|FAIL$)')
    return verbose.search(line)


def main():
    """execute command line tool"""
    global PRINT_COLOR_SET
    parser = get_optionparser()
    (opts, args) = parser.parse_args()
    if not opts.mode_defaultcolor:
        if opts.config_filename:
            PRINT_COLOR_SET = set_configuration(opts.config_filename)
        else:
            PRINT_COLOR_SET = set_configuration(DEFAULT_CONFIG_PATH)
    if len(args):
        if opts.mode_verbose:
            cmdline = [
             'python', args[0], '-v']
            if len(args) >= 2:
                cmdline += [ i for i in args[1:] ]
            proc = Popen(cmdline, stdout=PIPE, stderr=PIPE)
            result = proc.communicate()[1]
            print parse_unittest_result_verbose(result.splitlines(1))
        else:
            cmdline = [
             'python']
            cmdline += [ i for i in args ]
            proc = Popen(cmdline, stdout=PIPE, stderr=PIPE)
            result = proc.communicate()[1]
            print parse_unittest_result(result.splitlines(1))
    else:
        poller = poll()
        poller.register(sys.stdin, POLLIN)
        pollret = poller.poll(1)
        if len(pollret) == 1 and pollret[0][1] & POLLIN:
            lines = sys.stdin.readlines()
            if check_verbose(lines[0]):
                print parse_unittest_result_verbose(lines)
            else:
                print parse_unittest_result(lines)
        else:
            parser.print_help()


if __name__ == '__main__':
    sys.exit(main())