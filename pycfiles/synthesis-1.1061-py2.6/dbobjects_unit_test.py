# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/dbobjects_unit_test.py
# Compiled at: 2011-01-03 14:39:55
"""Unit-tests various XML/CSV validation scenarios (called tests also) in 
selector.py."""
import dbobjects, unittest

class SelectorTestCase(unittest.TestCase):
    """see if the return value is a file path"""

    def test_get_export(self):
        """Tests if you can pull the export record from the database that have been imported/shredded."""
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        theExport = mappedObjects.queryDB(dbobjects.Export)[0]
        if settings.DEBUG:
            print theExport.export_software_vendor
        self.assertEqual(theExport.export_software_vendor, "HMIS_'R_Us")

    def test_get_export_children(self):
        """Tests if you can pull the exports related records from the database that have been imported/shredded.
        mapper(Export, export_table, properties={'fk_export_to_person': relation(Person), 'fk_export_to_database': relation(Database)})
        """
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        theExports = mappedObjects.queryDB(dbobjects.Export)
        for export in theExports:
            child = export.fk_export_to_person[0]

        if settings.DEBUG:
            print child.person_legal_first_name_unhashed
        self.assertTrue(child.person_social_security_number_unhashed == '111111111' and child.person_legal_first_name_unhashed == 'George')

    def test_get_exports_children_backref(self):
        """Tests if you can pull the exports related records from the database that have been imported/shredded.
        mapper(Export, export_table, properties={'fk_export_to_person': relation(Person), 'fk_export_to_database': relation(Database)})
        """
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        theExports = mappedObjects.queryDB(dbobjects.Export).first()
        if settings.DEBUG:
            print 'Software Vendor: %s' % theExports.export_software_vendor
        dbo = theExports.fk_export_to_database[0]
        print 'type: %s' % type(dbo)
        if settings.DEBUG:
            print 'dbo.database_contact_phone=%s' % dbo.database_contact_phone
        self.assertTrue(dbo.database_email == 'test@test.com')

    def test_get_person_historical(self):
        """Test if you can pull person_historical records from the database that have been imported/shredded
        """
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        ph = mappedObjects.queryDB(dbobjects.PersonHistorical).all()
        for historical in ph:
            if settings.DEBUG:
                print 'historical.person_historical_id_num=%s' % historical.person_historical_id_num

        self.assertEqual(len(ph), 6)

    def test_get_person_historicals_children_backref(self):
        """Tests if you can pull the children (IncomeAndSources) of person historical and get back to the person record for all records who earned $100
        mapper(PersonHistorical, person_historical_table, properties={'fk_income_and_sources': relation(IncomeAndSources), 'fk_veteran': relation(Veteran),'fk_hud_homeless_episodes': relation(HUDHomelessEpisodes),'fk_person_address': relation(PersonAddress)})
        """
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        ias = mappedObjects.queryDB(dbobjects.IncomeAndSources).filter_by(amount=100).all()
        for ia in ias:
            if settings.DEBUG:
                print 'IncomeAndSources.person_historical_id_num=%s' % ia.income_source_code

        p = ias[0].fk_income_and_sources_to_person_historical.fk_person_historical_to_person
        self.assertEqual(p.person_social_security_number_unhashed, '111111111')

    def test_get_other_names(self):
        """Tests that there are 0 'othername' records in the database
        """
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        cnt_other_names = mappedObjects.queryDB(dbobjects.OtherNames).count()
        self.assertEqual(cnt_other_names, 0)

    def test_number_of_persons_who_live_in_anytown_florida(self):
        """Query database for count of people who live in anytown Florida
        """
        settings.DEBUG_ALCHEMY = True
        mappedObjects = dbobjects.DatabaseObjects(pg_db)
        veteranCnt = mappedObjects.queryDB(dbobjects.Person).join([
         'fk_person_to_person_historical', 'fk_person_historical_to_person_address']).filter_by(city='Anytown', state='Florida').count()
        if settings.DEBUG:
            people = mappedObjects.queryDB(dbobjects.Person).join([
             'fk_person_to_person_historical', 'fk_person_historical_to_person_address']).filter_by(city='Anytown', state='Florida').all()
            for person in people:
                print '%s is from AnyTown, FL' % person.person_legal_first_name_unhashed

        self.assertEqual(veteranCnt, 1)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from conf import settings
    print 'Settings _debug val: %s' % settings.DEBUG
    if settings.DB_PASSWD == '':
        settings.DB_PASSWD = raw_input('Please enter your password: ')
    pg_db = create_engine('postgresql://%s:%s@localhost:5432/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_DATABASE), echo=settings.DEBUG_ALCHEMY)
    unittest.main()