# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/utils.py
# Compiled at: 2010-04-14 23:21:46
"""
Some handy facility script.
"""
import re
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'
REVISION_PATTERN = '(r([0-9]+))'

def revision2Link(description, linkBase):
    """
    convert the reversion number to SVN web view changeset.
    """
    revisions = re.findall(REVISION_PATTERN, description)
    newDesc = description
    for (rNumber, number) in revisions:
        link = "<a href='%s?view=rev&revision=%s'>%s</a>" % (linkBase, number, rNumber)
        newDesc = newDesc.replace(rNumber, link)

    return newDesc