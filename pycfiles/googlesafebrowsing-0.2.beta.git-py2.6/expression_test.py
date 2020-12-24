# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/expression_test.py
# Compiled at: 2010-12-12 06:18:47
"""Test for googlesafebrowsing.expression."""
import expression, logging, unittest

class CanonicalizationTest(unittest.TestCase):

    def testCanonicalizeIp(self):
        ips = [
         ('1.2.3.4', '1.2.3.4'),
         ('012.034.01.055', '10.28.1.45'),
         ('0x12.0x43.0x44.0x01', '18.67.68.1'),
         ('167838211', '10.1.2.3'),
         ('12.0x12.01234', '12.18.2.156'),
         ('0x10000000b', '0.0.0.11'),
         ('asdf.com', None),
         ('0x120x34', None),
         ('123.123.0.0.1', None),
         ('1.2.3.00x0', None),
         ('fake ip', None),
         ('123.123.0.0.1', None),
         ('255.0.0.1', '255.0.0.1'),
         ('12.0x12.01234', '12.18.2.156'),
         ('012.034.01.055', '10.28.1.45'),
         ('0x12.0x43.0x44.0x01', '18.67.68.1'),
         ('167838211', '10.1.2.3'),
         ('3279880203', '195.127.0.11'),
         ('4294967295', '255.255.255.255'),
         ('10.192.95.89 xy', '10.192.95.89'),
         ('1.2.3.00x0', None),
         ('012.0xA0.01.089', '12.160.1.89')]
        for (testip, expected) in ips:
            actual = expression.ExpressionGenerator.CanonicalizeIp(testip)
            self.assertEqual(actual, expected, 'test input: %s, actual: %s, expected: %s' % (testip,
             actual,
             expected))

        return

    def testCanonicalizeUrl(self):
        urls = [('http://google.com/', 'http://google.com/'),
         ('http://google.com:80/a/b', 'http://google.com/a/b'),
         ('http://google.com:80/a/b/c/', 'http://google.com/a/b/c/'),
         ('http://GOOgle.com', 'http://google.com/'),
         ('http://..google..com../', 'http://google.com/'),
         ('http://google.com/%25%34%31%25%31%46', 'http://google.com/A%1F'),
         ('http://google^.com/', 'http://google^.com/'),
         ('http://google.com/1/../2/././', 'http://google.com/2/'),
         ('http://google.com/1//2?3//4', 'http://google.com/1/2?3//4'),
         ('http://host.com/%25%32%35', 'http://host.com/%25'),
         ('http://host.com/%25%32%35%25%32%35', 'http://host.com/%25%25'),
         ('http://host.com/%2525252525252525', 'http://host.com/%25'),
         ('http://host.com/asdf%25%32%35asd', 'http://host.com/asdf%25asd'),
         ('http://host.com/%%%25%32%35asd%%', 'http://host.com/%25%25%25asd%25%25'),
         ('http://www.google.com/', 'http://www.google.com/'),
         ('http://%31%36%38%2e%31%38%38%2e%39%39%2e%32%36/%2E%73%65%63%75%72%65/%77%77%77%2E%65%62%61%79%2E%63%6F%6D/',
 'http://168.188.99.26/.secure/www.ebay.com/'),
         ('http://195.127.0.11/uploads/%20%20%20%20/.verify/.eBaysecure=updateuserdataxplimnbqmn-xplmvalidateinfoswqpcmlx=hgplmcx/',
 'http://195.127.0.11/uploads/%20%20%20%20/.verify/.eBaysecure=updateuserdataxplimnbqmn-xplmvalidateinfoswqpcmlx=hgplmcx/'),
         ('http://host%23.com/%257Ea%2521b%2540c%2523d%2524e%25f%255E00%252611%252A22%252833%252944_55%252B',
 'http://host%23.com/~a!b@c%23d$e%25f^00&11*22(33)44_55+'),
         ('http://3279880203/blah', 'http://195.127.0.11/blah'),
         ('http://www.google.com/blah/..', 'http://www.google.com/'),
         ('http://a.com/../b', 'http://a.com/b'),
         ('www.google.com/', 'http://www.google.com/'),
         ('www.google.com', 'http://www.google.com/'),
         ('http://www.evil.com/blah#frag', 'http://www.evil.com/blah'),
         ('http://www.GOOgle.com/', 'http://www.google.com/'),
         ('http://www.google.com.../', 'http://www.google.com/'),
         ('http://www.google.com/foo\tbar\rbaz\n2', 'http://www.google.com/foobarbaz2'),
         ('http://www.google.com/q?', 'http://www.google.com/q?'),
         ('http://www.google.com/q?r?', 'http://www.google.com/q?r?'),
         ('http://www.google.com/q?r?s', 'http://www.google.com/q?r?s'),
         ('http://evil.com/foo#bar#baz', 'http://evil.com/foo'),
         ('http://evil.com/foo;', 'http://evil.com/foo;'),
         ('http://evil.com/foo?bar;', 'http://evil.com/foo?bar;'),
         (b'http://\x01\x80.com/', 'http://%01%80.com/'),
         ('http://notrailingslash.com', 'http://notrailingslash.com/'),
         ('http://www.gotaport.com:1234/', 'http://www.gotaport.com:1234/'),
         ('http://www.google.com:443/', 'http://www.google.com:443/'),
         ('  http://www.google.com/  ', 'http://www.google.com/'),
         ('http:// leadingspace.com/', 'http://%20leadingspace.com/'),
         ('http://%20leadingspace.com/', 'http://%20leadingspace.com/'),
         ('%20leadingspace.com/', 'http://%20leadingspace.com/'),
         ('https://www.securesite.com:443/', 'https://www.securesite.com/'),
         ('ftp://ftp.myfiles.com:21/', 'ftp://ftp.myfiles.com/'),
         ('http://some%1Bhost.com/%1B', 'http://some%1Bhost.com/%1B'),
         ('http://test%00\x00.com/', 'http://test%00%00.com/'),
         ('http://user:password@google.com/', 'http://google.com/'),
         ('', None),
         (':', None),
         ('/blah', None),
         ('#ref', None),
         ('/blah#ref', None),
         ('?query#ref', None),
         ('/blah?query#ref', None),
         ('/blah;param', None),
         ('http://#ref', None),
         ('http:///blah#ref', None),
         ('http://?query#ref', None),
         ('http:///blah?query#ref', None),
         ('http:///blah;param', None),
         ('http:///blah;param?query#ref', None),
         ('mailto:bryner@google.com', None),
         ('myprotocol://site.com/', None),
         ('http://i.have.way.too.many.dots.com/', 'http://i.have.way.too.many.dots.com/'),
         ('http%3A%2F%2Fwackyurl.com:80/', 'http://wackyurl.com/'),
         ('http://W!eird<>Ho$^.com/', 'http://w!eird<>ho$^.com/'),
         ('ftp://host.com?q', 'ftp://host.com/?q')]
        for (testin, expected) in urls:
            actual = expression.ExpressionGenerator.CanonicalizeUrl(testin)
            self.assertEqual(actual, expected, 'test input: %s, actual: %s, expected: %s' % (
             testin, actual, expected))

        return


class ExprGenTest(unittest.TestCase):

    def CheckExpr(self, url, expected):
        gen = expression.ExpressionGenerator(url)
        exprs = list(gen.Expressions())
        self.assertEqual(len(exprs), len(expected), 'Length mismatch.\nExpected: %s\nActual:  %s' % (
         expected, exprs))
        for i in xrange(len(exprs)):
            self.assertEqual(exprs[i].Value(), expected[i], 'List mismatch.\nExpected: %s\nAactual:  %s' % (expected,
             exprs))

    def testExpressionGenerator(self):
        self.CheckExpr('http://12.0x12.01234/a/b/cde/f?g=foo&h=bar#quux', [
         '12.18.2.156/a/b/cde/f?g=foo&h=bar',
         '12.18.2.156/a/b/cde/f',
         '12.18.2.156/a/b/cde/',
         '12.18.2.156/a/b/',
         '12.18.2.156/a/',
         '12.18.2.156/'])
        self.CheckExpr('http://www.google.com/a/b/cde/f?g=foo&h=bar#quux', [
         'www.google.com/a/b/cde/f?g=foo&h=bar',
         'www.google.com/a/b/cde/f',
         'www.google.com/a/b/cde/',
         'www.google.com/a/b/',
         'www.google.com/a/',
         'www.google.com/',
         'google.com/a/b/cde/f?g=foo&h=bar',
         'google.com/a/b/cde/f',
         'google.com/a/b/cde/',
         'google.com/a/b/',
         'google.com/a/',
         'google.com/'])
        self.CheckExpr('http://a.b.c.d.e.f.g/h/i/j/k/l/m/n/o?p=foo&q=bar#quux', [
         'a.b.c.d.e.f.g/h/i/j/k/l/m/n/o?p=foo&q=bar',
         'a.b.c.d.e.f.g/h/i/j/k/l/m/n/o',
         'a.b.c.d.e.f.g/h/i/j/',
         'a.b.c.d.e.f.g/h/i/',
         'a.b.c.d.e.f.g/h/',
         'a.b.c.d.e.f.g/',
         'c.d.e.f.g/h/i/j/k/l/m/n/o?p=foo&q=bar',
         'c.d.e.f.g/h/i/j/k/l/m/n/o',
         'c.d.e.f.g/h/i/j/',
         'c.d.e.f.g/h/i/',
         'c.d.e.f.g/h/',
         'c.d.e.f.g/',
         'd.e.f.g/h/i/j/k/l/m/n/o?p=foo&q=bar',
         'd.e.f.g/h/i/j/k/l/m/n/o',
         'd.e.f.g/h/i/j/',
         'd.e.f.g/h/i/',
         'd.e.f.g/h/',
         'd.e.f.g/',
         'e.f.g/h/i/j/k/l/m/n/o?p=foo&q=bar',
         'e.f.g/h/i/j/k/l/m/n/o',
         'e.f.g/h/i/j/',
         'e.f.g/h/i/',
         'e.f.g/h/',
         'e.f.g/',
         'f.g/h/i/j/k/l/m/n/o?p=foo&q=bar',
         'f.g/h/i/j/k/l/m/n/o',
         'f.g/h/i/j/',
         'f.g/h/i/',
         'f.g/h/',
         'f.g/'])
        self.CheckExpr('http://www.phisher.co.uk/a/b', [
         'www.phisher.co.uk/a/b',
         'www.phisher.co.uk/a/',
         'www.phisher.co.uk/',
         'phisher.co.uk/a/b',
         'phisher.co.uk/a/',
         'phisher.co.uk/',
         'co.uk/a/b',
         'co.uk/a/',
         'co.uk/'])
        self.CheckExpr('http://a.b/?', ['a.b/'])
        self.CheckExpr('http://1.2.3.4/a/b', [
         '1.2.3.4/a/b', '1.2.3.4/a/', '1.2.3.4/'])
        self.CheckExpr('foo.com', ['foo.com/'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()