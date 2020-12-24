# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\sogettext\model.py
# Compiled at: 2011-06-28 13:57:33
from datetime import datetime
from sqlobject import SQLObject, ForeignKey, MultipleJoin, DateTimeCol, StringCol, UnicodeCol
from turbogears.database import PackageHub
hub = PackageHub('turbogears.i18n.sogettext')
__connection__ = hub

class TG_Domain(SQLObject):
    __module__ = __name__

    class sqlmeta:
        __module__ = __name__
        table = 'tg_i18n_domain'
        defaultOrder = 'name'

    name = StringCol(alternateID=True)
    messages = MultipleJoin('TG_Message')


class TG_Message(SQLObject):
    __module__ = __name__

    class sqlmeta:
        __module__ = __name__
        table = 'tg_i18n_message'
        defaultOrder = 'name'

    name = UnicodeCol()
    text = UnicodeCol(default='')
    domain = ForeignKey('TG_Domain')
    locale = StringCol(length=15)
    created = DateTimeCol(default=datetime.now)
    updated = DateTimeCol(default=None)

    def _set_text(self, text):
        self._SO_set_text(text)
        self.updated = datetime.now()