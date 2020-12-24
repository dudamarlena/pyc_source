# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/catwalk/tg2/test/controllers/root.py
# Compiled at: 2009-01-11 14:12:53
from tg.controllers import TGController
from catwalk.tg2 import Catwalk
from catwalk.tg2.test.model import DBSession, metadata

class RootController(TGController):
    catwalk = Catwalk(DBSession, metadata)