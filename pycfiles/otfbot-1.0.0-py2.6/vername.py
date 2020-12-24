# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/vername.py
# Compiled at: 2011-04-22 06:35:42
"""
    Calculate a pronounceable name from a git version
"""
vowels = list('aeiou')
consonants = 'abcdefghijklmnopqrstuvwxyz'
hex = '0123456789abcdef'
consonants = list(set(consonants) - set(vowels) - set('cqvxy'))
consonants.sort()
vowels.sort()
vowels2 = [ (x, y) for x in vowels for y in vowels ]
vowels2.sort()
assert len(consonants) == 16, 'consonants has len %d instead of 16' % len(consonants)
assert len(vowels) == 5, 'vowels has len %d instead of 5' % len(vowels)
assert len(vowels2) == 25, 'vowels2 has len %d instead of 25' % len(vowels2)

def ver2name(ver):
    """
        convert a 7-digit hex-number (git commit) to a pronounceable name

        @param ver: version, must have 7 digits
        @type ver: str
    """
    assert type(ver) == str
    assert len(ver) == 7
    name = ''
    for i in xrange(3):
        name += consonants[hex.index(ver[(i * 2)])]
        if i == 2:
            name += vowels[((hex.index(ver[(i * 2)]) + hex.index(ver[(i * 2 + 1)])) % 5)]
        else:
            name += vowels2[hex.index(ver[6])][i]
        name += consonants[hex.index(ver[(i * 2 + 1)])]

    name = name[0].upper() + name[1:]
    return name


def name2ver(name):
    """
        convert a versionname back to a git version

        @param name: must be a 9-digit string as produced by ver2name
        @type name: str
    """
    name = name.lower()
    assert len(name) == 9
    ver = ''
    for i in xrange(3):
        ver += hex[consonants.index(name[(3 * i)])]
        ver += hex[consonants.index(name[(3 * i + 2)])]

    ver += hex[vowels2.index((name[1], name[4]))]
    return ver


def validVername(name):
    """
        checks a name, if its a valid version name,
        which can be converted to a 7-digit git revision

        @param name: the name
        @type name: str
    """
    if not len(name) == 9:
        return False
    if not set([ name[i] for i in [1, 4, 7] ]).issubset(set(vowels)):
        return False
    if not set([ name[i] for i in [0, 2, 3, 5, 6, 8] ]).issubset(set(consonants)):
        return False
    if (
     name[1], name[4]) not in vowels2:
        return False
    if not vowels2.index((name[1], name[4])) < 16:
        return False
    return True


if __name__ == '__main__':
    import unittest, hashlib, random

    class Ver2NameTestCase(unittest.TestCase):

        def testRandom(self):
            ver = hashlib.md5(str(random.random())).hexdigest()[:7]
            name = ver2name(ver)
            self.assertEquals(ver, name2ver(name))

        def testStatic(self):
            self.assertEquals(ver2name('474c8b9'), 'Helhusmur')
            self.assertEquals(name2ver('Helhusmur'), '474c8b9')
            for i in 'aeiou':
                self.assertEquals(name2ver('Helhusm' + i + 'r'), '474c8b9')


    unittest.main()