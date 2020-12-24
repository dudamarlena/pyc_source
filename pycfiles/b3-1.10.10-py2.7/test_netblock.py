# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\netblocker\netblock\test_netblock.py
# Compiled at: 2016-03-08 18:42:10
import unittest
from b3.plugins.netblocker.netblock import netblock

class basicTests(unittest.TestCase):
    knownIPRStrs = (
     (None, '<IPRanges: >'),
     ('127.0.0.1', '<IPRanges: 127.0.0.1>'),
     ('127.0.0.10-127.0.0.20', '<IPRanges: 127.0.0.10-127.0.0.20>'),
     ('127.0.0.0/24', '<IPRanges: 127.0.0.0-127.0.0.255>'),
     ('127.0.0.1/32', '<IPRanges: 127.0.0.1>'),
     ('127/32', '<IPRanges: 127.0.0.0>'),
     ('127/8', '<IPRanges: 127.0.0.0-127.255.255.255>'),
     ('0/0', '<IPRanges: 0.0.0.0-255.255.255.255>'),
     ('127.', '<IPRanges: 127.0.0.0-127.255.255.255>'),
     ('127.10.', '<IPRanges: 127.10.0.0-127.10.255.255>'),
     ('127.10.12.', '<IPRanges: 127.10.12.0-127.10.12.255>'))

    def testStrResults(self):
        """Test the result of str() of IPRanges on known values."""
        for i, res in self.knownIPRStrs:
            if i == None:
                r = netblock.IPRanges()
            else:
                r = netblock.IPRanges(i)
            self.assertEqual(str(r), res)
            if i != None:
                self.assertEqual(r.len() > 0, 1)
                r.remove(i)
                self.assertEqual(r.len(), 0)
                r.add(i)
                self.assertEqual(str(r), res)

        return

    def testInOperator(self):
        """Test the 'in' operator for IPRanges."""
        r = netblock.IPRanges('127/8')
        self.assertEqual('127.0.0.1' in r, 1)
        self.assertEqual('126.255.255.255' in r, 0)
        r = netblock.IPRanges('127.0.0.0/24')
        r.add('128.0.0.0/23')
        r.add('255.255.255.0/24')
        r.add('0.0.0.0/24')
        self.assertEqual(len(r), 1280)
        c = 0
        for e in r:
            self.assertEqual(e in r, 1)
            en = netblock.strtoip(e)
            self.assertEqual(en in r, 1)
            c += 1

        self.assertEqual(c, len(r))

    def testIterResult(self):
        """Test that iteration of a netblock results in IP addresses."""
        r = netblock.IPRanges('127.0.0.0-127.0.0.2')
        self.assertEqual(tuple(r), ('127.0.0.0', '127.0.0.1', '127.0.0.2'))

    knownCIDRValues = (
     (
      '127/8', ['127.0.0.0/8']),
     (
      '0/0', ['0.0.0.0/0']),
     (
      '127.0.0.0-127.0.0.127', ['127.0.0.0/25']),
     (
      '127.0.0.0-127.0.2.255', ['127.0.0.0/23', '127.0.2.0/24']),
     (
      '127.0.1.0-127.0.3.255', ['127.0.1.0/24', '127.0.2.0/23']),
     (
      '127.0.0.255-127.0.1.255', ['127.0.0.255', '127.0.1.0/24']),
     (
      '0.0.0.127-0.0.1.130',
      ['0.0.0.127', '0.0.0.128/25',
       '0.0.1.0/25', '0.0.1.128/31',
       '0.0.1.130']),
     (
      '250.250.250.250', ['250.250.250.250']),
     (
      '0.0.0.0-0.0.0.1', ['0.0.0.0/31']),
     (
      '255.255.255.255', ['255.255.255.255']),
     (
      '0.0.0.0', ['0.0.0.0']),
     (
      '127.255.255.255-128.0.0.0', ['127.255.255.255', '128.0.0.0']),
     (
      '126.0.0.0-129.255.255.255', ['126.0.0.0/7', '128.0.0.0/7']),
     (
      '126.0.0.0-129.0.0.255', ['126.0.0.0/7', '128.0.0.0/8', '129.0.0.0/24']))

    def testCIDROutput(self):
        """Test IPRanges.tocidr for correct operation on basic input."""
        for ival, res in self.knownCIDRValues:
            n = netblock.IPRanges(ival)
            self.assertEqual(n.tocidr(), res)
            n1 = netblock.IPRanges()
            for cidr in n.tocidr():
                n1.add(cidr)

            self.assertEqual(n1.tocidr(), res)

    def testAddoddcidr(self):
        """test that .addoddcidr() at least passes a basic test."""
        n = netblock.IPRanges()
        n.addoddcidr('127.0.0.1/24')
        self.assertEqual(str(n), '<IPRanges: 127.0.0.0-127.0.0.255>')

    def testRemoveoddcidr(self):
        """test that .removeoddcidr() at least passes a basic test."""
        n = netblock.IPRanges('127.0.0.0/23')
        n.removeoddcidr('127.0.0.1/24')
        self.assertEqual(str(n), '<IPRanges: 127.0.1.0-127.0.1.255>')


class failureTests(unittest.TestCase):
    knownBadInitArgs = ('127.0', '127.0./16', '.127/16', '.127/8', '127.0.0.0.5', '256.0.0.0',
                        '127.0.0.0/33', '127.0.0.0/-1', '127.0.0.1/24', '127.0.100.0-127.0.0.0',
                        '-127.0.0.0', '127.0.0.0-', '127..', '256.', '127.10.10.10.')

    def testKnownInitFailures(self):
        """Test that IPRanges fails to initialize in known situations."""
        for a in self.knownBadInitArgs:
            self.assertRaises(netblock.NBError, netblock.IPRanges, a)
            r = netblock.IPRanges()
            self.assertRaises(netblock.NBError, r.add, a)

    def testBadCIDRError(self):
        """Test that IPRanges properly indicates bogus CIDR errors."""
        self.assertRaises(netblock.BadCIDRError, netblock.IPRanges, '127.0.0.1/24')


if __name__ == '__main__':
    unittest.main()