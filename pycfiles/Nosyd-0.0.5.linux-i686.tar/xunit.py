# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/nosyd/xunit.py
# Compiled at: 2009-10-06 05:43:16
import logging
logger = logging.getLogger('nosyd')

class XunitTestSuite:

    def __init__(self, name, tests, errors, failures, skip, testcases):
        self.name = name
        self.tests = tests
        self.errors = errors
        self.failures = failures
        self.skip = skip
        self.testcases = testcases

    def __add__(self, o):
        return XunitTestSuite('combined', self.tests + o.tests, self.errors + o.errors, self.failures + o.failures, self.skip + o.skip, self.testcases + o.testcases)

    def __str__(self):
        return 'XunitTestSuite: %s %s %s %s %s' % (self.name, self.tests, self.errors, self.failures, self.skip)

    def failed_testcase(self, tc):
        return tc.failed()

    def list_failure_names(self):
        failed_testcases = filter(self.failed_testcase, self.testcases)
        return [ el.name for el in failed_testcases ]


class TestCase:

    def __init__(self, classname, name, failure):
        self.classname = classname
        self.name = name
        self.failure = failure

    def failed(self):
        return self.failure != None


class Failure:

    def __init__(self, type, text):
        self.type = type
        self.text = text


def parse_xunit_results(filename, skip_attr_name='skip'):
    try:
        from xml.dom import minidom
        xmldoc = minidom.parse(filename)
        ts = xmldoc.firstChild
        tcs = ts.getElementsByTagName('testcase')
        testcases = []
        for tc in tcs:
            failure = None
            if len(tc.childNodes) > 0:
                failureNode = tc.childNodes[0]
                failure = Failure(attr_val(failureNode, 'type'), failureNode.childNodes[0].data)
            testcases.append(TestCase(attr_val(tc, 'classname'), attr_val(tc, 'name'), failure))

        return XunitTestSuite(attr_val(ts, 'name'), int(attr_val(ts, 'tests')), int(attr_val(ts, 'errors')), int(attr_val(ts, 'failures')), int(attr_val(ts, skip_attr_name)), testcases)
    except Exception, e:
        logger.debug("Couldn't parse file " + filename + ': ' + str(type(e)) + ' ' + str(e))
        return

    return


def parse_surefire_results(filename):
    return parse_xunit_results(filename, 'skipped')


def attr_val(node, attr_name):
    return node.attributes[attr_name].value