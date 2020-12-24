# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/addRelated.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 695 bytes
"""
Entry point for getting related files.
@author: jimk
@date 2018-IX-27
A typical input was cut -f1 -d'|' Github://drs-deposit/output/outlines/

"""
from DBApps.relatedAdder import AddRelatedParser, RelatedAdder

def AddRelated():
    """
    Entry point for getting Related files, either outlines or print masters
    :return:
    """
    arp = AddRelatedParser(description='Adds list of works to either outlines or printmasters',
      usage=' sourceFile: list of workNames')
    addArgs = arp.parsedArgs
    ar = RelatedAdder(addArgs)
    ar.Add(sproc=f"Add{ar.TypeString}", sourceFile=(addArgs.sourceFile))


if __name__ == '__main__':
    AddRelated()