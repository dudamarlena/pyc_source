# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/src/archdb/src/TaxID.py
# Compiled at: 2018-02-02 06:39:02
from SBI.databases import TaxID
tables = {'taxid': 'taxid', 'taxold': 'taxid_old'}

class TaxID(TaxID):

    def __init__(self, taxid=None, inline=None):
        super(TaxID, self).__init__(taxid=taxid, inline=inline)

    def toSQL(self):
        if not self.has_old:
            return ('INSERT INTO {0} VALUES ({1.taxid},"{1.name}",{1.parent},"{1.rank}");').format(tables['taxid'], self)
        else:
            if not self.has_new:
                return ('INSERT INTO {0} (oldid) VALUES ({1.taxid});').format(tables['taxold'], self)
            return ('INSERT INTO {0} VALUES ({1.taxid},{1.new});').format(tables['taxold'], self)