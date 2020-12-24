# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/helpers/xpath.py
# Compiled at: 2008-08-22 15:02:55
import golem
from lxml import etree
import sys

def permute(l):
    if len(l) <= 1:
        return [ [x] for x in l[0] ]
    return [ [x] + y for x in l[0] for y in permute(l[1:]) ]


def _getxpath(entry):
    try:
        return entry.gxpath.path
    except AttributeError:
        return

    return


def _fixpath(path):
    if path.startswith('/'):
        return path
    else:
        return '/' + path


def _xpathsingle(queryset, predicate):
    res = ''
    xpaths = [ _getxpath(entry) for entry in queryset ]
    if None in xpaths:
        return
    while len(xpaths) >= 2:
        if xpaths[1].startswith(xpaths[0]):
            xpaths.pop(0)
        else:
            path = xpaths.pop(0)
            res += _fixpath(path)

    res += _fixpath(xpaths[0])
    if predicate:
        res += predicate
    return res


def xpath(query, templates=False):
    perms = permute([ concept.getAllImplementations() for concept in query ])
    predicate = query.getpredicate()
    if templates:
        xpaths = []
        for p in perms:
            xpath = _xpathsingle(p, predicate)
            if xpath is not None:
                try:
                    template = p[(-1)].templates[('getvalue', 'pygolem_serialization')]
                    txml = etree.tostring(template)
                except KeyError:
                    txml = None
                else:
                    xpaths.append((xpath, txml))

    else:
        xpaths = filter(lambda x: x != None, [ _xpathsingle(l, predicate) for l in perms ])
    return xpaths


def __test():
    d = golem.Dictionary('/Users/adw27/Documents/workspace/golem/trunk/bin/ossiaDict.xml')
    e = d['{http://www.esc.cam.ac.uk/ossia}emin:finalModule']
    f = d['{http://www.esc.cam.ac.uk/ossia}OrderParameterSquared']
    print [e, f]
    print permute([e.getAllImplementations(), f.getAllImplementations()])
    print xpath(golem.db.conceptlist(*[e, f]), templates=True)


if __name__ == '__main__':
    __test()