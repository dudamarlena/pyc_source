# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\flatten.py
# Compiled at: 2013-01-14 06:47:43
"""
Flatten a nested list structure.

Source:
http://wiki.python.org/moin/ProblemSets/99%20Prolog%20Problems%20Solutions#Problem7.3AFlattenanestedliststructure
"""

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