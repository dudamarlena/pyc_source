# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/parsing_utils.py
# Compiled at: 2014-05-19 10:07:56


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def hemineutral(s):
    lhind = s.lower().find('lh')
    rhind = s.lower().find('rh')
    if lhind > rhind:
        return rreplace(s, 'lh', '%s', 1)
    else:
        if rhind > lhind:
            return rreplace(s, 'rh', '%s', 1)
        return s


def mangle_hemi(s):
    return '%s_%s' % (s[-2:], s[:-3])


def demangle_hemi(s):
    return '%s-%s' % (s[3:], s[:2])


def same_hemi(s1, s2, char=None):
    if char is None:
        return s1[0] == s2[0]
    else:
        return s1[0] == s2[0] == char
        return


def str2intlist(s):
    import re
    return re.split(',| |;', s.strip('[]'))


def appendhemis(olddict, hemi):
    return dict(map(lambda (k, v): (k, '%s%s' % (hemi, str(v))), olddict.items()))


def eqfun(x):
    return lambda y: y == x