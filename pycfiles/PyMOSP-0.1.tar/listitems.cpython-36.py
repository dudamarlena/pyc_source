# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/commands/listitems.py
# Compiled at: 2019-03-26 15:56:51
# Size of source mod 2**32: 1579 bytes
__doc__ = 'Display all solvers, problems, and test problems'
from .basecomm import *
from inspect import getmembers, isclass, ismodule

class ListItems(BaseComm):
    """ListItems"""

    def run(self):
        """
        Print the list of solvers, problems, and testers that are
        included in PyMOSO.
        """
        probclasses = getmembers(problems, isclass)
        solvclasses = getmembers(solvers, isclass)
        testclasses = getmembers(testers, isclass)
        sstr = 'Solver'
        sstrund = '************************'
        descstr = 'Description'
        print(f"\n{sstr:30} {descstr:30}")
        print(f"{sstrund:30} {sstrund:30}")
        for s0, s1 in solvclasses:
            docstr = s1.__doc__.split('\n')[1].strip()
            print(f"{s0:30} {docstr:30}")

        pstr = 'Problems'
        tstr = 'Test Name (if available)'
        print(f"\n{pstr:30} {descstr:60} {tstr:30}")
        print(f"{sstrund:30} {sstrund:60} {sstrund:30}")
        for p0, p1 in probclasses:
            ctlist = [t[0] for t in testclasses if issubclass(t[1]().ranorc, p1)]
            p2 = ctlist[0] if ctlist else ''
            docstr = p1.__doc__.split('\n')[1].strip()
            print(f"{p0:30} {docstr:60} {p2:30}")