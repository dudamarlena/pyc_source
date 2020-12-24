# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/generic/container.py
# Compiled at: 2011-11-29 11:31:38


class Container(dict):
    """return the items as pseudo members
       >>> a = Container()
       >>> a['otto'] = 2
       >>> a.otto
       2
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]