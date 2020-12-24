# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnny/workspaces/lazerball/src/python3.4env/lib/python3.4/site-packages/htdataredirector/units/rfd21733/registry.py
# Compiled at: 2014-10-08 05:42:38
# Size of source mod 2**32: 404 bytes


class Registry:

    def all(self):
        """TODO: get this from a web service if we ever need this functionality later."""
        units = '\n4145dd1d\nd2a593fd\na6fb75a5\n0f29fb21\n92c85574\n07cf535f\n02590a8f\n83e7a9af\n67a9beea\nad2a5920\n91017f38\n7d80598c\na593f39d\n164fce20\n73d4df5e\n880bf969\n5903ca41\n9a593f26\naa593f26\n5a54b241\ne40f29fe\nc329ab35\n5b73e921\n29bedd42\n'
        return set(units.splitlines())