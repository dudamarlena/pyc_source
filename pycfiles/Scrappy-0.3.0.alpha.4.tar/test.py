# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/louist/Documents/Python/Scrappy/tests/test.py
# Compiled at: 2013-01-19 07:25:32
import os, unittest, random, string, scrappy.core

def random_unicode(length=10):
    ru = lambda : unichr(random.randint(0, 1114111))
    return ('').join([ ru() for _ in xrange(length) ])


def random_ascii(length=10):
    ascii = string.printable + string.whitespace
    return ('').join([ random.choice(ascii) for _ in xrange(length) ])


def test_compare_strings():
    """Test normalized Levenshtein distance.
    """
    hamming = lambda s, ss: sum(ch1 != ch2 for ch1, ch2 in zip(s, ss))
    bigstrn = lambda slen, slen2: float(max(slen, slen2))
    for i in range(1000):
        s1 = random_unicode(random.randint(1, 50))
        s2 = random_unicode(random.randint(1, 50))
        ls1 = len(s1)
        ls2 = len(s2)
        diff = scrappy.compare_strings(s1, s2)
        assert diff >= 0 and diff <= 1
        assert diff >= (max(ls1, ls2) - min(ls1, ls2)) / bigstrn(ls1, ls2)
        if ls1 == ls2:
            assert diff == hamming(s1, s2) / bigstrn(ls1, ls2)
            assert diff == 0 and s1 == s2


def test_normalize():
    for i in xrange(1000):
        scrappy.normalize(random_ascii(i))

    for i in xrange(1000):
        scrappy.normalize(random_unicode(i))


class Test_Scrape(unittest.TestCase):

    def validate_output(self, scrp, id):
        self.assertTrue(scrp.map_episode_info())
        self.assertEqual(str(scrp.id), str(id))

    def test_basic(self):
        """Test simple scrape
        """
        s = scrappy.Scrape('its always sunny in philadelphia 1x2.mkv')
        self.validate_output(s, '75805')

    def test_glob(self):
        s = scrappy.Scrape('*phil*')
        self.validate_output(s, '75805')

    def test_list(self):
        s = scrappy.Scrape(['its always sunny i n philadelphia 101.mkv',
         'its always sunny in philadelphia 1x2.mkv',
         'its always sunny in phil s03e04.avi'])
        self.validate_output(s, '75805')

    def test_iter(self):
        s = scrappy.Scrape(f for f in os.listdir(os.getcwd()) if 'phil' in f)
        self.validate_output(s, '75805')

    def test_tvdbid(self):
        s = scrappy.Scrape('its always sunny i n philadelphia 101.mkv', tvdbid=75805)
        self.validate_output(s, '75805')

    def test_abstract(self):
        s = scrappy.Scrape(['its always sunny i n philadelphia 101.mkv',
         'its always sunny in philadelphia 1x2.mkv',
         'its always sunny in phil s03e04.avi'], interface=scrappy.AbstractMediaInterface)
        self.validate_output(s, '75805')