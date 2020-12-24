# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/utils.py
# Compiled at: 2016-08-21 10:33:44
# Size of source mod 2**32: 8253 bytes
"""
Misc utils and setup calls.
"""
import sys, os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import bprc.cli, logging, json
from urllib.parse import urlencode
import collections, re
from pygments import highlight, lexers, formatters
from json import JSONDecoder
from json import JSONDecodeError
httpstatuscodes = {'100': 'Continue', 
 '101': 'Switching Protocols', 
 '200': 'OK', 
 '201': 'Created', 
 '202': 'Accepted', 
 '203': 'Non-Authoritative Information', 
 '204': 'No Content', 
 '205': 'Reset Content', 
 '206': 'Partial Content', 
 '300': 'Multiple Choices', 
 '301': 'Moved Permanently', 
 '302': 'Found', 
 '303': 'See Other', 
 '304': 'Not Modified', 
 '305': 'Use Proxy', 
 '307': 'Temporary Redirect', 
 '400': 'Bad Request', 
 '401': 'Unauthorized', 
 '402': 'Payment Required', 
 '403': 'Forbidden', 
 '404': 'Not Found', 
 '405': 'Method Not Allowed', 
 '406': 'Not Acceptable', 
 '407': 'Proxy Authentication Required', 
 '408': 'Request Time-out', 
 '409': 'Conflict', 
 '410': 'Gone', 
 '411': 'Length Required', 
 '412': 'Precondition Failed', 
 '413': 'Request Entity Too Large', 
 '414': 'Request-URI Too Large', 
 '415': 'Unsupported Media Type', 
 '416': 'Requested range not satisfiable', 
 '417': 'Expectation Failed', 
 '500': 'Internal Server Error', 
 '501': 'Not Implemented', 
 '502': 'Bad Gateway', 
 '503': 'Service Unavailable', 
 '504': 'Gateway Time-out', 
 '505': 'HTTP Version not supported'}

def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if bprc.cli.args.debug:
        debug_hook(exception_type, exception, traceback)
    else:
        print('{}: {}'.format(exception_type.__name__, exception))


sys.excepthook = exceptionHandler
logleveldict = {'none': 100, 
 'debug': logging.DEBUG, 
 'info': logging.INFO, 
 'warning': logging.WARNING, 
 'error': logging.ERROR, 
 'critical': logging.CRITICAL}

def vprint(arg):
    print(arg, file=sys.stderr)


verboseprint = vprint if bprc.cli.args.verbose else (lambda *a**a: None)

def vlog(msg):
    verboseprint(msg)
    logging.info(msg)


def errlog(msg, e):
    logging.error(msg)
    try:
        try:
            raise RuntimeError(msg) from e
        except Exception as er:
            sys.stderr.write('ERROR: ' + str(er) + '\n')

    finally:
        raise e


def printstepcolophon(step, *, file, id):
    """Prints out the heading of the step to the output file"""
    print('--- ' + step.name + ' ---', file=file)


def printhttprequest(step, *, file, id, colourful):
    """Prints out the heading of the step to the output file"""
    if colourful:
        if step.request.querystring == {}:
            print(step.httpmethod + ' ' + step.URL + '?' + urlencode(step.request.querystring), file=file)
        else:
            print(step.httpmethod + ' ' + step.URL + '?' + urlencode(step.request.querystring), file=file)
    else:
        if step.request.querystring == {}:
            print(step.httpmethod + ' ' + step.URL, file=file)
        else:
            print(step.httpmethod + ' ' + step.URL + '?' + urlencode(step.request.querystring), file=file)


def printhttpresponse(step, *, file, id, colourful):
    if colourful:
        print('HTTP/' + str(step.response.httpversion / 10) + ' ' + str(step.response.code) + ' ' + httpstatuscodes[str(step.response.code)].upper(), file=file)
    else:
        print('HTTP/' + str(step.response.httpversion / 10) + ' ' + str(step.response.code) + ' ' + httpstatuscodes[str(step.response.code)].upper(), file=file)


def printheaders(step, *, file, id, http_part, colourful):
    """Prints out the heading of the step to the output file"""
    logging.debug('in printheaders() http_part=' + http_part)
    od = collections.OrderedDict(sorted(eval('step.' + http_part + '.headers.items()')))
    for key, val in od.items():
        if colourful:
            print(key + ': ' + val, file=file)
        else:
            print(key + ': ' + val, file=file)


def printbody(step, *, file, id, http_part, colourful):
    if http_part == 'response':
        try:
            printoutput = json.dumps(step.response.body, indent=4, sort_keys=True)
            isJsonPayload = True
        except JSONDecodeError as e:
            printoutput = step.response.body
            colourful = False
            isJsonPayload = False

    else:
        try:
            printoutput = json.dumps(step.request.body, indent=4, sort_keys=True)
            isJsonPayload = True
        except JSONDecodeError as e:
            printoutput = step.request.body
            colourful = False
            isJsonPayload = False

        if colourful and isJsonPayload:
            print(highlight(printoutput, lexers.JsonLexer(), formatters.TerminalFormatter()), file=file)
        else:
            print(printoutput, file=file)


php_sub_pattern = re.compile('<%=(\\S+?)%>')
var_sub_pattern = re.compile('<%!(\\S+?)%>')
file_sub_pattern = re.compile('<%f(\\S+?)%>')

def _insert_file_param(m, *, recipe, variables):
    """used by the re.subn call below - takes an re.match object -returns a string"""
    try:
        with open(str(m.group(1)), 'rb') as (f):
            data = f.read()
            text = data.decode('utf-8')
            vlog('Found file-like pattern: <$f' + m.group(1) + '%>... substituting with contents of ' + m.group(1))
    except Exception as e:
        errlog('Could not open ' + m.group(1) + ' in the rest of the recipe. Aborting.', e)

    return text


def _insert_php_param(m, *, recipe, variables):
    """used by the re.subn call below - takes an re.match object -returns a string"""
    try:
        vlog('Found php-like pattern: <$=' + str(m.group(1)) + '%>... substituting with ' + str(eval('recipe.' + m.group(1))))
    except KeyError as ke:
        errlog('Could not find ' + m.group(1) + ' in the rest of the recipe. Aborting.', ke)

    return str(eval('recipe.' + m.group(1)))


def _insert_var(m, *, recipe, variables):
    """used by the re.subn call below - takes an re.match object -returns a string """
    try:
        vlog('Found variable pattern: <$!' + str(m.group(1)) + '%>... substituting with ' + str(eval('variables["' + m.group(1) + '"]')))
    except KeyError as ke:
        errlog('Could not find ' + m.group(1) + ' in the variables. Aborting.', ke)

    return str(eval('variables["' + m.group(1) + '"]'))