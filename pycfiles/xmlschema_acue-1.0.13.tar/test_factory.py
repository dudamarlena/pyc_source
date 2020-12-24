# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/xmlschema_acue/components/xmlschema_acue/tests/xmlschema_acue_tests/testtools/test_factory.py
# Compiled at: 2019-05-19 13:21:22
"""
Test factory for creating test cases from lists of paths to XSD or XML files.

The list of cases can be defined within files named "testfiles". These are text files
that contain a list of relative paths to XSD or XML files, that are used to dinamically
build a set of test classes. Each path is followed by a list of options that defines a
custom setting for each test.
"""
import sys, re, os, fileinput, argparse, logging
from xmlschema_acue.validators import XMLSchema10, XMLSchema11
from tests.xmlschema_acue_tests.testtools.schema_observers import ObservedXMLSchema10, ObservedXMLSchema11
from testdata.xmlschema_acue_testdata import testdata_dir
logger = logging.getLogger(__file__)
TEST_FACTORY_OPTIONS = {'extra_cases': '-x' in sys.argv or '--extra' in sys.argv, 
   'check_with_lxml': '-l' in sys.argv or '--lxml' in sys.argv}
RUN_W3C_TEST_SUITE = '-w' in sys.argv or '--w3c' in sys.argv
sys.argv = [ a for a in sys.argv if a not in {'-x', '--extra', '-l', '--lxml'} ]

def get_test_args(args_line):
    """Returns the list of arguments from provided text line."""
    try:
        args_line, _ = args_line.split('#', 1)
    except ValueError:
        pass

    return re.split('(?<!\\\\) ', args_line.strip())


def create_test_line_args_parser():
    """Creates an arguments parser for uncommented on not blank "testfiles" lines."""

    def xsd_version_number(value):
        if value not in ('1.0', '1.1'):
            msg = '%r is not an XSD version.' % value
            raise argparse.ArgumentTypeError(msg)
        return value

    def defuse_data(value):
        if value not in ('always', 'remote', 'never'):
            msg = '%r is not a valid value.' % value
            raise argparse.ArgumentTypeError(msg)
        return value

    parser = argparse.ArgumentParser(add_help=True)
    parser.usage = "TEST_FILE [OPTIONS]\nTry 'TEST_FILE --help' for more information."
    parser.add_argument('filename', metavar='TEST_FILE', type=str, help='Test filename (relative path).')
    parser.add_argument('-L', dest='locations', nargs=2, type=str, default=None, action='append', metavar='URI-URL', help='Schema location hint overrides.')
    parser.add_argument('--version', dest='version', metavar='VERSION', type=xsd_version_number, default='1.0', help='XSD schema version to use for the test case (default is 1.0).')
    parser.add_argument('--errors', type=int, default=0, metavar='NUM', help='Number of errors expected (default=0).')
    parser.add_argument('--warnings', type=int, default=0, metavar='NUM', help='Number of warnings expected (default=0).')
    parser.add_argument('--inspect', action='store_true', default=False, help='Inspect using an observed custom schema class.')
    parser.add_argument('--defuse', metavar='(always, remote, never)', type=defuse_data, default='remote', help='Define when to use the defused XML data loaders.')
    parser.add_argument('--timeout', type=int, default=300, metavar='SEC', help='Timeout for fetching resources (default=300).')
    parser.add_argument('--defaults', action='store_true', default=False, help='Test data uses default or fixed values (skip strict encoding checks).')
    parser.add_argument('--skip', action='store_true', default=False, help='Skip strict encoding checks (for cases where test data uses default or fixed values or some test data are skipped by wildcards processContents).')
    parser.add_argument('--debug', action='store_true', default=False, help='Activate the debug mode (only the cases with --debug are executed).')
    return parser


test_line_parser = create_test_line_args_parser()

def tests_factory(test_class_builder, suffix='xml'):
    """
    Factory function for file based schema/validation cases.

    :param test_class_builder: the test class builder function.
    :param suffix: the suffix ('xml' or 'xsd') to consider for cases.
    :return: a list of test classes.
    """
    test_classes = {}
    test_num = 0
    debug_mode = False
    line_buffer = []
    test_file = os.path.normpath(testdata_dir + 'testfiles')
    testfiles = [test_file]
    if TEST_FACTORY_OPTIONS['extra_cases']:
        testfiles.extend(os.path.join(os.getcwd(), 'testfiles'))
    for line in fileinput.input(testfiles):
        line = line.strip()
        if not line or line[0] == '#':
            if not line_buffer:
                continue
            else:
                raise SyntaxError('Empty continuation at line %d!' % fileinput.filelineno())
        elif '#' in line:
            line = line.split('#', 1)[0].rstrip()
        if line[(-1)] == '\\':
            line_buffer.append(line[:-1].strip())
            continue
        elif line_buffer:
            line_buffer.append(line)
            line = (' ').join(line_buffer)
            del line_buffer[:]
        test_args = test_line_parser.parse_args(get_test_args(line))
        if test_args.locations is not None:
            test_args.locations = {k.strip('\'"'):v for k, v in test_args.locations}
        test_file = os.path.join(os.path.dirname(fileinput.filename()), test_args.filename)
        if os.path.isdir(test_file):
            logger.debug('Skip %s: is a directory.', test_file)
            continue
        elif os.path.splitext(test_file)[1].lower() != '.%s' % suffix:
            logger.debug('Skip %s: wrong suffix.', test_file)
            continue
        elif not os.path.isfile(test_file):
            logger.error('Skip %s: is not a file.', test_file)
            continue
        test_num += 1
        if debug_mode:
            if not test_args.debug:
                continue
        elif test_args.debug:
            debug_mode = True
            logger.debug('Debug mode activated: discard previous %r test classes.', len(test_classes))
            test_classes.clear()
        if test_args.version == '1.0':
            schema_class = ObservedXMLSchema10 if test_args.inspect else XMLSchema10
            check_with_lxml = TEST_FACTORY_OPTIONS['check_with_lxml']
        else:
            schema_class = ObservedXMLSchema11 if test_args.inspect else XMLSchema11
            check_with_lxml = False
        test_class = test_class_builder(test_file, test_args, test_num, schema_class, check_with_lxml)
        test_classes[test_class.__name__] = test_class
        logger.debug('Add XSD %s test class %r.', test_args.version, test_class.__name__)

    if line_buffer:
        raise ValueError('Not completed line continuation at the end!')
    return test_classes