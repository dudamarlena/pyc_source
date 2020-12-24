# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/catwalk/tg2/test/controllers/root.py
# Compiled at: 2009-01-11 14:12:53
from tg.controllers import TGController
from catwalk.tg2 import Catwalk
from catwalk.tg2.test.model import DBSession, metadata

class RootController(TGController):
    catwalk = Catwalk(DBSession, metadata)