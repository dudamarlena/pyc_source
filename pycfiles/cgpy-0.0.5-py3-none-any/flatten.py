# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\utils\flatten.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = '\nFlatten a nested list structure.\n\nSource:\nhttp://wiki.python.org/moin/ProblemSets/99%20Prolog%20Problems%20Solutions#Problem7.3AFlattenanestedliststructure\n'

def flatten(nestedList):
    """Flatten a nested list structure."""

    def aux(listOrItem):
        """Generator to recursively yield items."""
        if isinstance(listOrItem, list):
            for elem in listOrItem:
                for item in aux(elem):
                    yield item

        else:
            yield listOrItem

    return list(aux(nestedList))