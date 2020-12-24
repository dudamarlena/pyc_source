# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/test/test_db.py
# Compiled at: 2016-10-03 09:39:22
from bauble.test import BaubleTestCase
import bauble.plugins.plants.genus, bauble.plugins.garden.accession
from bauble import db
from bauble import prefs
prefs.testing = True
db.sqlalchemy_debug(True)

class GlobalFunctionsTests(BaubleTestCase):

    def test_get_next_code_first_this_year(self):
        self.assertEquals(db.class_of_object('genus'), bauble.plugins.plants.genus.Genus)
        self.assertEquals(db.class_of_object('accession_note'), bauble.plugins.garden.accession.AccessionNote)
        self.assertEquals(db.class_of_object('not_existing'), None)
        return