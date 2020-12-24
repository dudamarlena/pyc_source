# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/db1/c.py
# Compiled at: 2009-11-11 15:21:14
from elixir import Entity, ManyToMany

class C(Entity):
    cs = ManyToMany('.b.B')
    as_ = ManyToMany('..db2.a.A')