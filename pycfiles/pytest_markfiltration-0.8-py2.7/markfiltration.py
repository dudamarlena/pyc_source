# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/markfiltration/markfiltration.py
# Compiled at: 2011-11-07 21:14:37
import copy, pytest, py
from _pytest.mark import MarkInfo

def pytest_addoption(parser):
    group = parser.getgroup('general')
    group._addoption('-f', action='append', dest='filter', default=[], metavar='FILTEREXPR', help="only run tests which have marks that match givenkeyword expression.  An expression consists of space-separated terms. Each term must match. Precede a term with '-' to negate.")


def pytest_collection_modifyitems(items, config):
    if len(config.option.filter) == 1:
        config.option.keyword = config.option.filter[0].strip()
    else:
        config.option.keyword = (', ').join([ i.strip() for i in config.option.filter ])
    filterlist = config.option.filter
    if not filterlist:
        return
    remaining = []
    deselected = []
    for filtr in filterlist:
        dirty_items = copy.copy(items)
        for item in dirty_items:
            if filtr[:1] != '-' and skipbykeyword(item, filtr):
                deselected.append(item)
            elif filtr[:1] == '-' and skipbykeyword(item, filtr):
                deselected.append(item)
                if item in remaining:
                    del remaining[remaining.index(item)]
            else:
                remaining.append(item)

    deselected = [ i for i in set(deselected) ]
    remaining = [ i for i in set(remaining) ]
    if deselected:
        config.hook.pytest_deselected(items=list(set(deselected) - set(remaining)))
        items[:] = remaining


def skipbykeyword(colitem, keywordexpr):
    """ return True if they given keyword expression means to
        skip this collector/item.
    """
    if not keywordexpr:
        return
    else:
        itemkeywords = getkeywords(colitem)
        for key in filter(None, keywordexpr.split()):
            eor = key[:1] == '-'
            if eor:
                key = key[1:]
            if not eor ^ matchonekeyword(key, itemkeywords):
                return True

        return


def getkeywords(node):
    keywords = {}
    while node is not None:
        for keyword in node.keywords:
            if isinstance(node.keywords[keyword], MarkInfo):
                keywords[keyword] = node.keywords[keyword]

        node = node.parent

    return keywords


def matchonekeyword(key, itemkeywords):
    for elem in key.split('.'):
        for kw in itemkeywords:
            if elem == kw:
                break
        else:
            return False

    return True


class MarkFiltration(object):
    pass