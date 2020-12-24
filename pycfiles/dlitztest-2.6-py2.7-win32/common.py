# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\common.py
# Compiled at: 2013-03-13 13:15:35
"""Self-testing for PyCrypto hash modules"""
__revision__ = '$Id$'
import sys, unittest, binascii
from Crypto.Util.py3compat import *
if sys.hexversion < 33751040:

    def dict(**kwargs):
        return kwargs.copy()


else:
    dict = dict

class HashDigestSizeSelfTest(unittest.TestCase):

    def __init__(self, hashmod, description, expected):
        unittest.TestCase.__init__(self)
        self.hashmod = hashmod
        self.expected = expected
        self.description = description

    def shortDescription(self):
        return self.description

    def runTest(self):
        self.failUnless(hasattr(self.hashmod, 'digest_size'))
        self.assertEquals(self.hashmod.digest_size, self.expected)
        h = self.hashmod.new()
        self.failUnless(hasattr(h, 'digest_size'))
        self.assertEquals(h.digest_size, self.expected)


class HashSelfTest(unittest.TestCase):

    def __init__(self, hashmod, description, expected, input):
        unittest.TestCase.__init__(self)
        self.hashmod = hashmod
        self.expected = expected
        self.input = input
        self.description = description

    def shortDescription(self):
        return self.description

    def runTest(self):
        h = self.hashmod.new()
        h.update(self.input)
        out1 = binascii.b2a_hex(h.digest())
        out2 = h.hexdigest()
        h = self.hashmod.new(self.input)
        out3 = h.hexdigest()
        out4 = binascii.b2a_hex(h.digest())
        self.assertEqual(self.expected, out1)
        if sys.version_info[0] == 2:
            self.assertEqual(self.expected, out2)
            self.assertEqual(self.expected, out3)
        else:
            self.assertEqual(self.expected.decode(), out2)
            self.assertEqual(self.expected.decode(), out3)
        self.assertEqual(self.expected, out4)
        h2 = h.new()
        h2.update(self.input)
        out5 = binascii.b2a_hex(h2.digest())
        self.assertEqual(self.expected, out5)


class HashTestOID(unittest.TestCase):

    def __init__(self, hashmod, oid):
        unittest.TestCase.__init__(self)
        self.hashmod = hashmod
        self.oid = oid

    def runTest(self):
        h = self.hashmod.new()
        if self.oid == None:
            try:
                raised = 0
                a = h.oid
            except AttributeError:
                raised = 1

            self.assertEqual(raised, 1)
        else:
            self.assertEqual(h.oid, self.oid)
        return


class MACSelfTest(unittest.TestCase):

    def __init__(self, hashmod, description, expected_dict, input, key, hashmods):
        unittest.TestCase.__init__(self)
        self.hashmod = hashmod
        self.expected_dict = expected_dict
        self.input = input
        self.key = key
        self.hashmods = hashmods
        self.description = description

    def shortDescription(self):
        return self.description

    def runTest(self):
        for hashname in self.expected_dict.keys():
            hashmod = self.hashmods[hashname]
            key = binascii.a2b_hex(b(self.key))
            data = binascii.a2b_hex(b(self.input))
            expected = b(('').join(self.expected_dict[hashname].split()))
            h = self.hashmod.new(key, digestmod=hashmod)
            h.update(data)
            out1 = binascii.b2a_hex(h.digest())
            out2 = h.hexdigest()
            h = self.hashmod.new(key, data, hashmod)
            out3 = h.hexdigest()
            out4 = binascii.b2a_hex(h.digest())
            h2 = h.copy()
            h.update(b('blah blah blah'))
            out5 = binascii.b2a_hex(h2.digest())
            self.assertEqual(expected, out1)
            if sys.version_info[0] == 2:
                self.assertEqual(expected, out2)
                self.assertEqual(expected, out3)
            else:
                self.assertEqual(expected.decode(), out2)
                self.assertEqual(expected.decode(), out3)
            self.assertEqual(expected, out4)
            self.assertEqual(expected, out5)


def make_hash_tests(module, module_name, test_data, digest_size, oid=None):
    tests = []
    for i in range(len(test_data)):
        row = test_data[i]
        expected, input = map(b, row[0:2])
        if len(row) < 3:
            description = repr(input)
        else:
            description = row[2].encode('latin-1')
        name = '%s #%d: %s' % (module_name, i + 1, description)
        tests.append(HashSelfTest(module, name, expected, input))

    if oid is not None:
        oid = b(oid)
    name = '%s #%d: digest_size' % (module_name, i + 1)
    tests.append(HashDigestSizeSelfTest(module, name, digest_size))
    tests.append(HashTestOID(module, oid))
    return tests


def make_mac_tests(module, module_name, test_data, hashmods):
    tests = []
    for i in range(len(test_data)):
        row = test_data[i]
        key, data, results, description = row
        name = '%s #%d: %s' % (module_name, i + 1, description)
        tests.append(MACSelfTest(module, name, results, data, key, hashmods))

    return tests