# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fdtool\modules\dbschema\dbschema.py
# Compiled at: 2018-06-19 13:38:40
import sys, re, string, math
from itertools import *
lowercase = string.lowercase + 'ßäöüçáéíóúàèìòùãẽĩõũâêîôûëï'
uppercase = string.uppercase + 'ÄÖÜÇÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛËÏ'
letters = lowercase + uppercase

def upcSplit(s):
    attr = None
    attrs = set()
    for c in s:
        if c in uppercase:
            if attr != None:
                attrs.add(attr)
            attr = c
        else:
            if attr == None:
                attr = ''
            attr += c

    if attr != None:
        attrs.add(attr)
    return attrs


def unionUpcSplit(s):
    return map(set, chain(*map(upcSplit, s)))


sep = re.compile('[ ]*[/, \r\n][ ]*')
intdepsep = re.compile(';')
allsep = re.compile('[ ]*[,; ][ ]*')
upcsplit = True

def ScanAttr(attrsastxt):
    global upcsplit
    findattr = attrsastxt == ''
    if upcsplit:
        attrs = set(chain(*map(upcSplit, allsep.split(attrsastxt))))
        for a in attrs:
            if len(a) == 0:
                raise NameError('empty string instead of attribute')
            if a[0] not in uppercase:
                raise NameError('attribute does not start with uppercase letters: ' + a)

    else:
        attrs = set(allsep.split(attrsastxt))
    return attrs


def ScanAbh(abhhastxt):
    abhh = {}
    for abhtx in sep.split(abhhastxt):
        if abhtx.strip() == '':
            continue
        try:
            li, re = abhtx.split('->', 1)
        except ValueError:
            raise ValueError("split by '->' did not succeed for rules: '%s' ('%s')" % (abhtx, abhhastxt))

        li = frozenset(intdepsep.split(li))
        re = set(intdepsep.split(re))
        if upcsplit:
            li = frozenset(chain(*map(upcSplit, li)))
            re = set(chain(*map(upcSplit, re)))
        if li in abhh:
            abhh[li] = abhh[li].union(re)
        else:
            abhh[li] = re

    return abhh


def ScanAttrAbh(attrstxt, abhtxt):
    return (
     ScanAttr(attrstxt), ScanAbh(abhtxt))


shouldsort = True

def attr2str(attrs, attrsep='' if upcsplit else ';'):
    attrs = list(attrs)
    if shouldsort:
        attrs.sort()
    return string.join(attrs, attrsep)


def abh2str(li, re):
    attrsep = '' if upcsplit else ';'
    li = list(li)
    re = list(re)
    if shouldsort:
        li.sort()
        re.sort()
    return string.join(li, attrsep) + '->' + string.join(re, attrsep)


def abhh2str(abhh, linesep='\n'):
    lii = list(abhh.keys())

    def setcmp(set1, set2):
        return cmp(string.join(set1, ''), string.join(set2, ''))

    if shouldsort:
        lii.sort(setcmp)
    result = ''
    for li in lii:
        result = result + abh2str(li, abhh[li]) + linesep

    if '\n' not in linesep and '\r' not in linesep:
        result = result[0:-len(linesep)]
    return result


def closure(attrs, abh):
    try:
        haschanged = True
        while haschanged:
            haschanged = False
            for li, re in abh.items():
                if li <= attrs and not re <= attrs:
                    attrs = attrs.union(re)
                    haschanged = True

    except Exception as ex:
        print >> sys.stderr, 'error in dependency: %s->%s' % (li, re)
        raise ex

    return attrs


def shuffle(lis, num):
    newlis = []
    positions = 1
    while positions <= len(lis):
        item = lis[(len(lis) - positions)]
        newlis.insert(num % positions, item)
        num = num / positions
        positions += 1

    return newlis


def mincoverage(abh, scramble=0, hints={}):
    traverse = []
    for key in abh.keys():
        if len(key) == 1:
            traverse = [key] + traverse
        else:
            traverse.append(key)

    traverse = shuffle(traverse, scramble)
    while len(traverse) > 0:
        li = traverse.pop()
        re = abh[li]
        redabh = abh.copy()
        del redabh[li]
        othersclosure = closure(li, redabh)
        newre = re.difference(othersclosure).difference(li)
        liset = set(li)
        precond = liset.union(re)
        newre_list = list(newre)
        if li in hints:
            firsttouch = newre.difference(hints[li])
            lasttouch = newre.difference(firsttouch)
            newre_list = list(firsttouch) + list(lasttouch)
        for r in newre_list:
            precond.remove(r)
            if r in closure(precond, redabh):
                newre.remove(r)
            else:
                precond.add(r)

        if len(newre) == 0:
            abh = redabh
        else:
            installed_newre = False
            if len(li) > 1:
                lired = liset
                for l in li:
                    tryred = lired.copy()
                    tryred.remove(l)
                    cls = closure(tryred, redabh)
                    if li <= cls:
                        lired = tryred

                if lired != li:
                    abh = redabh
                    lired = frozenset(lired)
                    if lired in abh:
                        abh[lired] = abh[lired].union(newre)
                    else:
                        abh[lired] = newre
                    installed_newre = True
            if not installed_newre:
                abh = redabh
                abh[li] = newre

    return abh


def keyBaseSets(attr, abh):
    attrch = dict([ (a, 0) for a in attr ])
    for li, re in abh.items():
        for l in li:
            attrch[l] = attrch[l] | 1

        for r in re:
            attrch[r] = attrch[r] | 2

    sets = (
     set(), set(), set(), set())
    for a, ch in attrch.items():
        sets[ch].add(a)

    return sets


def keysTreeAlg(attr, abh, verbty=None):
    verbty = verbosity if verbty == None else verbty
    ua, li, re, mi = keyBaseSets(attr, abh)
    subkey = frozenset(li.union(ua))
    if closure(subkey, abh) == attr:
        finalkey = subkey
        return (
         finalkey, {finalkey})
    else:
        keys = set()
        curlvl = dict()
        primattr = set()
        lvl = 1
        lpad = ''
        for m in mi:
            csk = subkey.union(frozenset(m))
            if closure(csk, abh) == attr:
                for p in csk:
                    primattr.add(p)

                keys.add(csk)
            else:
                curlvl[csk] = m

        while len(curlvl) > 0:
            prevlvl = curlvl
            curlvl = dict()
            lvl += 1
            lpad += ' '
            for subkey, maxm in prevlvl.items():
                missingattr = set()
                for a in mi:
                    if a > maxm and a not in subkey:
                        missingattr.add(a)

                for m in missingattr:
                    newattr = subkey.union(frozenset(m))
                    ispartofkey = False
                    for key in keys:
                        if key <= newattr:
                            ispartofkey = True
                            break

                    if not ispartofkey:
                        if closure(newattr, abh) == attr:
                            keys.add(newattr)
                            for p in newattr:
                                primattr.add(p)

                        else:
                            curlvl[newattr] = max(maxm, m)

        return (
         primattr, keys)