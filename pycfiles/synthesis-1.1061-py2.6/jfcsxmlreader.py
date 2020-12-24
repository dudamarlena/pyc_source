# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/jfcsxmlreader.py
# Compiled at: 2011-01-19 19:20:51
import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
import dateutil.parser, dbobjects
from conf import settings
from datetime import datetime

class JFCSXMLReader(dbobjects.DatabaseObjects):
    """ Synthesis import plugin for JFCS XML 
        JFCS provides 2 simple XML files
        - 1 for service data
        - 1 for client data
        This module parses the XML, maps the
        elements to database fields and 
        commits data to the database
    """
    implements(Reader)

    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.dbo = dbobjects.DatabaseObjects()
        self.session = self.dbo.Session()

    def read(self):
        """ suck in raw xml file and build etree object """
        tree = etree.parse(self.xml_file)
        return tree

    def process_data(self, tree, data_type):
        self.data_type = data_type
        self.source_id = str(settings.JFCS_SOURCE_ID)
        self.agency_airs_key = settings.JFCS_AGENCY_ID
        self.service_airs_key = settings.JFCS_SERVICE_ID
        self.source_email = 'kwright@jfcs-cares.org'
        if self.data_type == 'service_event':
            self.parse_service_event_xml(tree)
        elif self.data_type == 'client':
            self.parse_client_xml(tree)

    def parse_service_event_xml(self, tree):
        """ iterate through JFCS service simple xml calling appropriate parsers """
        lookup_or_add_source_id(self, self.source_id)
        for row_element in tree.getiterator(tag='row'):
            self.row_dict = {}
            for child in row_element:
                if child.text is not None:
                    if child.tag == 'c4clientid':
                        self.row_dict.__setitem__('c4clientid', child.text)
                    if child.tag == 'qprogram':
                        self.row_dict.__setitem__('qprogram', child.text)
                    if child.tag == 'serv_code':
                        self.row_dict.__setitem__('serv_code', child.text)
                    if child.tag == 'trdate':
                        self.row_dict.__setitem__('trdate', child.text)
                    if child.tag == 'end_date':
                        self.row_dict.__setitem__('end_date', child.text)
                    if child.tag == 'cunits':
                        self.row_dict.__setitem__('cunits', child.text)

            if self.row_dict.has_key('qprogram'):
                lookup_or_add_site_service_id(self, self.row_dict.__getitem__('qprogram'))
            self.parse_service_event()

        return

    def parse_client_xml(self, tree):
        """ iterate through JFCS service simple xml calling appropriate parsers """
        lookup_or_add_source_id(self, self.source_id)
        for row_element in tree.getiterator(tag='row'):
            self.row_dict = {}
            for child in row_element:
                if child.text is not None:
                    if child.tag == 'c4clientid':
                        self.row_dict.__setitem__('c4clientid', child.text)
                    if child.tag == 'c4dob':
                        self.row_dict.__setitem__('c4dob', child.text)
                    if child.tag == 'c4sex':
                        self.row_dict.__setitem__('c4sex', child.text)
                    if child.tag == 'c4firstname':
                        self.row_dict.__setitem__('c4firstname', child.text)
                    if child.tag == 'c4lastname':
                        self.row_dict.__setitem__('c4lastname', child.text)
                    if child.tag == 'c4mi':
                        self.row_dict.__setitem__('c4mi', child.text)
                    if child.tag == 'hispanic':
                        self.row_dict.__setitem__('hispanic', child.text)
                    if child.tag == 'c4ssno':
                        self.row_dict.__setitem__('c4ssno', child.text)
                    if child.tag == 'c4last_s01':
                        self.row_dict.__setitem__('c4last_s01', child.text)
                    if child.tag == 'ethnicity':
                        self.row_dict.__setitem__('ethnicity', child.text)
                    if child.tag == 'aprgcode':
                        self.row_dict.__setitem__('aprgcode', child.text)
                    if child.tag == 'a_date':
                        self.row_dict.__setitem__('a_date', child.text)
                    if child.tag == 't_date':
                        self.row_dict.__setitem__('t_date', child.text)
                    if child.tag == 'family_id':
                        self.row_dict.__setitem__('family_id', child.text)

            self.parse_person()

        return

    def parse_service_event(self):
        """ parse data for service_event table """
        self.parse_dict = {}
        self.person_index_id = ''
        self.lookup_or_add_person_index_id()
        if self.person_index_id is None:
            if settings.DEBUG:
                print 'Error: no person index id found!'
        else:
            self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
        try:
            self.site_service_participation_index_id
            if self.site_service_participation_index_id != None:
                self.existence_test_and_add('site_service_participation_index_id', self.site_service_participation_index_id, 'no_handling')
        except AttributeError:
            pass

        if self.row_dict.has_key('serv_code'):
            self.existence_test_and_add('jfcs_type_of_service', self.row_dict.__getitem__('serv_code'), 'text')
        if self.row_dict.has_key('end_date'):
            test = self.normalize_date(self.row_dict.__getitem__('end_date'))
            if test == True:
                self.existence_test_and_add('service_period_end_date', self.row_dict.__getitem__('end_date'), 'element_date')
        if self.row_dict.has_key('cunits'):
            self.existence_test_and_add('quantity_of_service', self.row_dict.__getitem__('cunits'), 'text')
        self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
        self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
        thetimenow = str(datetime.now())
        self.existence_test_and_add('site_service_recorded_date', thetimenow, 'element_date')
        self.shred(self.parse_dict, dbobjects.ServiceEvent)
        return

    def parse_person(self):
        """ parse data for person table """
        self.parse_dict = {}
        if self.row_dict.has_key('c4clientid'):
            self.existence_test_and_add('person_id_unhashed', self.row_dict.__getitem__('c4clientid'), 'text')
        if self.row_dict.has_key('c4dob'):
            self.existence_test_and_add('person_date_of_birth_unhashed', self.row_dict.__getitem__('c4dob'), 'text')
        if self.row_dict.has_key('c4sex'):
            if self.row_dict.__getitem__('c4sex').upper() == 'F':
                gender = '0'
            elif self.row_dict.__getitem__('c4sex').upper() == 'M':
                gender = '1'
            if gender is not None:
                self.existence_test_and_add('person_gender_unhashed', gender, 'text')
        if self.row_dict.has_key('c4firstname'):
            self.existence_test_and_add('person_legal_first_name_unhashed', self.row_dict.__getitem__('c4firstname'), 'text')
        if self.row_dict.has_key('c4lastname'):
            self.existence_test_and_add('person_legal_last_name_unhashed', self.row_dict.__getitem__('c4lastname'), 'text')
        if self.row_dict.has_key('c4mi'):
            self.existence_test_and_add('person_legal_middle_name_unhashed', self.row_dict.__getitem__('c4mi'), 'text')
        if self.row_dict.has_key('hispanic'):
            if self.row_dict.__getitem__('hispanic').upper() == 'N':
                ethnicity = '0'
            elif self.row_dict.__getitem__('hispanic').upper() == 'Y':
                ethnicity = '1'
            if ethnicity is not None:
                self.existence_test_and_add('person_ethnicity_unhashed', ethnicity, 'text')
        if self.row_dict.has_key('c4ssno'):
            self.existence_test_and_add('person_social_security_number_unhashed', self.row_dict.__getitem__('c4ssno').replace('-', ''), 'text')
        self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
        self.shred(self.parse_dict, dbobjects.Person)
        self.parse_other_names()
        self.parse_races()
        self.parse_site_service_participation()
        self.parse_household()
        return

    def parse_other_names(self):
        """ parse data for other_names table """
        self.parse_dict = {}
        if self.row_dict.has_key('c4last_s01') & self.row_dict.has_key('c4lastname'):
            if self.row_dict.__getitem__('c4lastname').lower() != self.row_dict.__getitem__('c4last_s01').lower():
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                self.existence_test_and_add('other_last_name_unhashed', self.row_dict.__getitem__('c4last_s01'), 'text')
                self.shred(self.parse_dict, dbobjects.OtherNames)

    def parse_races(self):
        """ parse data for races table """
        self.parse_dict = {}
        if self.row_dict.has_key('ethnicity'):
            if self.row_dict.__getitem__('ethnicity').upper() == 'M':
                race = '5'
            elif self.row_dict.__getitem__('ethnicity').upper() == 'H':
                race = '5'
            elif self.row_dict.__getitem__('ethnicity').upper() == 'W':
                race = '5'
            elif self.row_dict.__getitem__('ethnicity').upper() == 'B':
                race = '3'
            if race is not None:
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                self.existence_test_and_add('race_unhashed', race, 'text')
                self.shred(self.parse_dict, dbobjects.Races)
        return

    def parse_site_service_participation(self):
        """ parse data for site_service_participation table """
        self.parse_dict = {}
        self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
        self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
        try:
            self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
        except AttributeError:
            pass

        if self.row_dict.has_key('aprgcode'):
            self.existence_test_and_add('site_service_idid_num', self.row_dict.__getitem__('aprgcode'), 'text')
        if self.row_dict.has_key('a_date'):
            test = self.normalize_date(self.row_dict.__getitem__('a_date'))
            if test == True:
                self.existence_test_and_add('participation_dates_start_date', self.row_dict.__getitem__('a_date'), 'element_date')
        if self.row_dict.has_key('t_date'):
            test = self.normalize_date(self.row_dict.__getitem__('t_date'))
            if test == True:
                self.existence_test_and_add('participation_dates_end_date', self.row_dict.__getitem__('t_date'), 'element_date')
        self.shred(self.parse_dict, dbobjects.SiteServiceParticipation)

    def parse_household(self):
        """ parse data for household table """
        self.parse_dict = {}
        if self.row_dict.has_key('family_id'):
            famid = self.row_dict.__getitem__('family_id')
            household = self.session.query(dbobjects.Household).filter(dbobjects.Household.household_id_num == famid).first()
            if household is None:
                self.existence_test_and_add('household_id_num', famid, 'text')
                self.shred(self.parse_dict, dbobjects.Household)
                self.parse_members()
            elif settings.DEBUG:
                print 'Household ID ', famid, 'is already in the database; not adding.'
        return

    def parse_members(self):
        """ parse data for members table """
        self.parse_dict = {}
        if self.row_dict.has_key('c4clientid'):
            clientid = self.row_dict.__getitem__('c4clientid')
            householdmemberships = self.session.query(dbobjects.Members).filter(dbobjects.Members.household_index_id == self.household_index_id and dbobjects.Members.person_index_id == clientid).first()
            if householdmemberships is None:
                self.existence_test_and_add('household_index_id', self.household_index_id, 'no_handling')
                personrecord = self.session.query(dbobjects.Person).filter(dbobjects.Person.person_id_unhashed == clientid).first()
                self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
                self.existence_test_and_add('person_index_id', personrecord.id, 'no_handling')
                self.existence_test_and_add('household_index_id', self.household_index_id, 'no_handling')
                self.shred(self.parse_dict, dbobjects.Members)
            elif settings.DEBUG:
                print 'Household ID ', self.household_index_id, ' is already in the database with member id', clientid, '; not adding.'
        return

    def shred(self, parse_dict, mapping):
        """Commits the record set to the database"""
        mapped = mapping(parse_dict)
        self.session.add(mapped)
        self.session.commit()
        if mapping.__name__ == 'Export':
            self.export_index_id = mapped.id
        if mapping.__name__ == 'Household':
            self.household_index_id = mapped.id
        if mapping.__name__ == 'PersonHistorical':
            self.person_historical_index_id = mapped.id
        if mapping.__name__ == 'Person':
            self.person_index_id = mapped.id
        if mapping.__name__ == 'Service':
            self.service_index_id = mapped.id
        if mapping.__name__ == 'ServiceEvent':
            self.service_event_index_id = mapped.id
        if mapping.__name__ == 'Site':
            self.site_index_id = mapped.id
        if mapping.__name__ == 'SiteService':
            self.site_service_index_id = mapped.id
        if mapping.__name__ == 'SiteServiceParticipation':
            self.site_service_participation_index_id = mapped.id
        if mapping.__name__ == 'Source':
            self.source_index_id = mapped.id

    def existence_test_and_add(self, db_column, query_string, handling):
        """checks that the query actually has a result and adds to dict"""
        if handling == 'no_handling':
            self.persist(db_column, query_string=query_string)
            return True
        else:
            if len(query_string) is not 0 or None:
                if handling == 'attribute_text':
                    self.persist(db_column, query_string)
                    return True
                else:
                    if handling == 'text':
                        self.persist(db_column, query_string)
                        return True
                    if handling == 'attribute_date':
                        self.persist(db_column, query_string=dateutil.parser.parse(query_string))
                        return True
                    if handling == 'element_date':
                        self.persist(db_column, query_string=dateutil.parser.parse(query_string))
                        return True
                    print 'need to specify the handling'
                    return False
            else:
                return False
            return

    def persist(self, db_column, query_string):
        """ build dictionary of db_column:data """
        self.parse_dict.__setitem__(db_column, query_string)

    def normalize_date(self, raw_date):
        if raw_date.replace(' ', '') == '--':
            return False
        else:
            if raw_date.replace(' ', '') == '':
                return False
            return True

    def lookup_or_add_person_index_id(self):
        clientid = self.row_dict.__getitem__('c4clientid')
        person = self.session.query(dbobjects.Person).filter(dbobjects.Person.person_id_unhashed == clientid).first()
        if person is not None:
            self.person_index_id = person.id
            self.lookup_site_service_participation_index_id()
        else:
            self.parse_person()
        return

    def lookup_site_service_participation_index_id(self):
        """ lookup site_service_participation_index_id from site_service_participation table """
        site_service_participations = self.session.query(dbobjects.SiteServiceParticipation).filter(dbobjects.SiteServiceParticipation.person_index_id == self.person_index_id)
        for site_service_participation in site_service_participations:
            self.service_index_id = site_service_participation.id


def lookup_or_add_site_service_id(self, proposed_site_service_id):
    """the jfcs xml has the qprogram code in it, which is 'service' in AIRS parlance"""
    self.parse_dict = {}
    site_service_id = self.session.query(dbobjects.SiteService).filter(dbobjects.SiteService.site_service_id == proposed_site_service_id).first()
    if not site_service_id:
        self.existence_test_and_add('site_service_id', proposed_site_service_id, 'no_handling')
        self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
        thetimenow = str(datetime.now())
        self.existence_test_and_add('site_service_recorded_date', thetimenow, 'element_date')
        self.shred(self.parse_dict, dbobjects.SiteService)
    siteserviceid = self.session.query(dbobjects.SiteService.id).filter(dbobjects.SiteService.site_service_id == proposed_site_service_id).first()
    self.site_service_index_id = siteserviceid


def lookup_or_add_source_id(self, proposed_source_id):
    """check to see if  JFCS has a source_id assigned.  If it does, retrieve it.  If it doesn't, create one."""
    self.parse_dict = {}
    source_id = self.session.query(dbobjects.Source).filter(dbobjects.Source.source_id == proposed_source_id).first()
    if not source_id:
        self.existence_test_and_add('source_id', proposed_source_id, 'no_handling')
        self.existence_test_and_add('source_contact_email', self.source_email, 'text')
        self.existence_test_and_add('source_name', 'JFCS', 'text')
        self.shred(self.parse_dict, dbobjects.Source)
    sourceid = self.session.query(dbobjects.Source.id).filter(dbobjects.Source.source_id == proposed_source_id).first()
    self.source_index_id = sourceid
    lookup_or_add_source_export_link(self, sourceid)


def lookup_or_add_source_export_link(self, sourceprimarykey):
    self.parse_dict = {}
    create_source_export_link(self)


def create_source_export_link(self):
    """To create the source export link record, first add a new export record to the export table."""
    thetimenow = str(datetime.now())
    self.existence_test_and_add('export_date', thetimenow, 'element_date')
    self.shred(self.parse_dict, dbobjects.Export)
    self.parse_dict = {}
    self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
    self.existence_test_and_add('source_index_id', self.source_index_id, 'no_handling')
    self.shred(self.parse_dict, dbobjects.SourceExportLink)


def main(argv=None):
    """ Test the JFCSXMLReader class """
    if argv is None:
        argv = sys.argv
    inputFile = '/mnt/laptop01/Projects/Alexandria/DATA/StagingFiles/CRG.xml'
    data_type = 'service'
    if os.path.isfile(inputFile) is True:
        try:
            xml_file = open(inputFile, 'r')
        except:
            print 'Error opening input file'
        else:
            reader = JFCSXMLReader(xml_file)
            tree = reader.read()
            reader.process_data(tree, data_type)
            xml_file.close()
    return


if __name__ == '__main__':
    sys.exit(main())