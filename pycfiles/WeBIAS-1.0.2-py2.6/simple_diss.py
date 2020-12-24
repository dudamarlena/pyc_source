# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/validity/simple_diss.py
# Compiled at: 2015-04-13 16:10:50
from gnosis.xml.validity import *

class figure(EMPTY):
    pass


class _mixedpara(Or):
    _disjoins = (PCDATA, figure)


class paragraph(Some):
    _type = _mixedpara


class title(PCDATA):
    pass


class _paras(Some):
    _type = paragraph


class chapter(Seq):
    _order = (title, _paras)


class dissertation(Some):
    _type = chapter