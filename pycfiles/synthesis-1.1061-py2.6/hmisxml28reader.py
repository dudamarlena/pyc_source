# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/hmisxml28reader.py
# Compiled at: 2010-12-12 18:24:12
"""reads an HMIS XML Document into memory and parses its contents

storing them into a postgresql database.  This is a log database, so it holds 
everything and doesn't worry about deduplication.  The only thing it enforces 
are exportids, which must be unique."""
import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
from sqlalchemy.exceptions import IntegrityError
import dateutil.parser
from conf import settings
import clsexceptions, dbobjects, fileutils
from errcatalog import catalog

class HMISXML28Reader(dbobjects.DatabaseObjects):
    """Implements reader interface."""
    implements(Reader)
    hmis_namespace = 'http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd'
    airs_namespace = 'http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd'
    nsmap = {'hmis': hmis_namespace, 'airs': airs_namespace}

    def __init__(self, xml_file):
        self.xml_file = xml_file
        dbo = dbobjects.DatabaseObjects()
        self.session = dbo.Session()

    def read(self):
        """Takes an XML instance file and reads it into 

        memory as a node tree."""
        tree = etree.parse(self.xml_file)
        return tree

    def process_data(self, tree):
        """Shreds the XML document into the database."""
        root_element = tree.getroot()
        try:
            self.parse_export(root_element)
        except IntegrityError:
            fileutils.makeBlock('CAUGHT INTEGRITY ERROR')
            err = catalog.errorCatalog[1002]
            raise clsexceptions.DuplicateXMLDocumentError, (err[0], err[1], 'process_data()')

    def parse_source(self, root_element):
        """Look for a DatabaseID and related fields in the XML and persists it."""
        xpSourceID = '/hmis:SourceDatabase/hmis:DatabaseID'
        xpSourceIDIDNum = 'hmis:IDNum'
        xpSourceIDIDStr = 'hmis:IDStr'
        xpExportIDIDNum = '../hmis:Export/hmis:ExportID/hmis:IDNum'
        xpExportIDIDStr = '../hmis:Export/hmis:ExportID/hmis:IDStr'
        xpIDNumdateCollected = 'hmis:IDNum/@hmis:dateCollected'
        xpIDStrdateCollected = 'hmis:IDStr/@hmis:dateCollected'
        xpSourceContactEmail = '../hmis:DatabaseContactEmail'
        xpSourceContactEmaildateCollected = '../hmis:DatabaseContactEmail/@hmis:dateCollected'
        xpSourceContactExtension = '../hmis:DatabaseContactExtension'
        xpSourceContactExtensiondateCollected = '../hmis:DatabaseContactExtension/@hmis:dateCollected'
        xpSourceContactFirst = '../hmis:DatabaseContactFirst'
        xpSourceContactFirstdateCollected = '../hmis:DatabaseContactFirst/@hmis:dateCollected'
        xpSourceContactLast = '../hmis:DatabaseContactLast'
        xpSourceContactLastdateCollected = '../hmis:DatabaseContactLast/@hmis:dateCollected'
        xpSourceContactPhone = '../hmis:DatabaseContactPhone'
        xpSourceContactPhonedateCollected = '../hmis:DatabaseContactPhone/@hmis:dateCollected'
        xpSourceName = '../hmis:DatabaseName'
        xpSourceNamedateCollected = '../hmis:DatabaseName/@hmis:dateCollected'
        database_id_tag = root_element.xpath(xpSourceID, namespaces={'hmis': self.hmis_namespace})[0]
        database_id_tag = [
         database_id_tag]
        if database_id_tag is not None:
            for item in database_id_tag:
                self.parse_dict = {}
                database_id_val = item.xpath(xpSourceIDIDNum, namespaces={'hmis': self.hmis_namespace})
                if len(database_id_val) is 0:
                    database_id_val = item.xpath(xpSourceIDIDStr, namespaces={'hmis': self.hmis_namespace})
                    self.parse_dict.__setitem__('source_id', database_id_val[0].text)
                    self.existence_test_and_add('source_id_date_collected', item.xpath(xpIDStrdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                else:
                    self.parse_dict.__setitem__('source_id', database_id_val[0].text)
                    self.existence_test_and_add('source_id_date_collected', item.xpath(xpIDNumdateCollected, namespaces={'hmis': self.hmis_namespace})[0], 'attribute_date')
                test = item.xpath(xpExportIDIDNum, namespaces={'hmis': self.hmis_namespace})
                if len(test) is 0:
                    self.existence_test_and_add('export_id', item.xpath(xpExportIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                else:
                    self.existence_test_and_add('export_id', test, 'text')
                self.existence_test_and_add('source_email', item.xpath(xpSourceContactEmail, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_email_date_collected', item.xpath(xpSourceContactEmaildateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('source_contact_extension', item.xpath(xpSourceContactExtension, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_extension_date_collected', item.xpath(xpSourceContactExtensiondateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('source_contact_first', item.xpath(xpSourceContactFirst, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_first_date_collected', item.xpath(xpSourceContactFirstdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('source_contact_last', item.xpath(xpSourceContactLast, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_last_date_collected', item.xpath(xpSourceContactLastdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('source_contact_phone', item.xpath(xpSourceContactPhone, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_phone_date_collected', item.xpath(xpSourceContactPhonedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('source_name', item.xpath(xpSourceName, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_name_date_collected', item.xpath(xpSourceNamedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.Source)
                self.parse_person(root_element)
                self.parse_household(root_element)

            return
        else:
            return

    def parse_export(self, root_element):
        """Looks for an ExportID and related fields in the XML and persists it."""
        xpExport = 'hmis:Export'
        xpExportIDIDNum = 'hmis:ExportID/hmis:IDNum'
        xpExportIDIDStr = 'hmis:ExportID/hmis:IDStr'
        xpIDNumdateCollected = 'hmis:ExportID/hmis:IDNum/@hmis:dateCollected'
        xpIDStrdateCollected = 'hmis:ExportID/hmis:IDStr/@hmis:dateCollected'
        xpExportExportDate = 'hmis:ExportDate'
        xpExportExportDatedateCollected = 'hmis:ExportDate/@hmis:dateCollected'
        xpExportPeriodStartDate = 'hmis:ExportPeriod/hmis:StartDate'
        xpExportPeriodStartDatedateCollected = 'hmis:ExportPeriod/hmis:StartDate/@hmis:dateCollected'
        xpExportPeriodEndDate = 'hmis:ExportPeriod/hmis:EndDate'
        xpExportPeriodEndDatedateCollected = 'hmis:ExportPeriod/hmis:EndDate/@hmis:dateCollected'
        xpExportSoftwareVendor = 'hmis:SoftwareVendor'
        xpExportSoftwareVendordateCollected = 'hmis:SoftwareVendor/@hmis:dateCollected'
        xpExportSoftwareVendor = 'hmis:SoftwareVendor'
        xpExportSoftwareVendordateCollected = 'hmis:SoftwareVendor/@hmis:dateCollected'
        xpExportSoftwareVersion = 'hmis:SoftwareVersion'
        xpExportSoftwareVersiondateCollected = 'hmis:SoftwareVersion/@hmis:dateCollected'
        export = root_element.xpath(xpExport, namespaces={'hmis': self.hmis_namespace})[0]
        export = [
         export]
        if export is not None:
            for item in export:
                self.parse_dict = {}
                test = item.xpath(xpExportIDIDNum, namespaces={'hmis': self.hmis_namespace})
                if len(test) is 0:
                    test = item.xpath(xpExportIDIDStr, namespaces={'hmis': self.hmis_namespace})
                    self.export_id = test
                    value = self.existence_test_and_add('export_id', test, 'text')
                    self.existence_test_and_add('export_id_date_collected', item.xpath(xpIDStrdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                else:
                    self.export_id = test
                    self.existence_test_and_add('export_id', test, 'text')
                    self.existence_test_and_add('export_id_date_collected', item.xpath(xpIDNumdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_date', item.xpath(xpExportExportDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                self.existence_test_and_add('export_date_date_collected', item.xpath(xpExportExportDatedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_period_start_date', item.xpath(xpExportPeriodStartDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                self.existence_test_and_add('export_period_start_date_date_collected', item.xpath(xpExportPeriodStartDatedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_period_end_date', item.xpath(xpExportPeriodEndDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                self.existence_test_and_add('export_period_end_date_date_collected', item.xpath(xpExportPeriodEndDatedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_software_vendor', item.xpath(xpExportSoftwareVendor, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('export_software_vendor_date_collected', item.xpath(xpExportSoftwareVendordateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_software_version', item.xpath(xpExportSoftwareVersion, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('export_software_version_date_collected', item.xpath(xpExportSoftwareVersiondateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.Export)
                self.parse_source(root_element)

        else:
            self.shred(self.parse_dict, dbobjects.Export)
            return
        return

    def parse_other_names(self, person_tag):
        """Looks for an OtherNames tag and related fields in the XML and persists it."""
        xpOtherNames = 'hmis:OtherNames'
        xpOtherFirstNameUnhashed = 'hmis:OtherFirstName/hmis:Unhashed'
        xpOtherFirstNameHashed = 'hmis:OtherFirstName/hmis:Hashed'
        xpOtherFirstNameDateCollectedUnhashed = 'hmis:OtherFirstName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherFirstNameDateCollectedHashed = 'hmis:OtherFirstName/hmis:Hashed/@hmis:dateCollected'
        xpOtherLastNameUnhashed = 'hmis:OtherLastName/hmis:Unhashed'
        xpOtherLastNameHashed = 'hmis:OtherLastName/hmis:Hashed'
        xpOtherLastNameDateCollectedUnhashed = 'hmis:OtherLastName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherLastNameDateCollectedHashed = 'hmis:OtherLastName/hmis:Hashed/@hmis:dateCollected'
        xpOtherMiddleNameUnhashed = 'hmis:OtherMiddleName/hmis:Unhashed'
        xpOtherMiddleNameHashed = 'hmis:OtherMiddleName/hmis:Hashed'
        xpOtherMiddleNameDateCollectedUnhashed = 'hmis:OtherMiddleName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherMiddleNameDateCollectedHashed = 'hmis:OtherMiddleName/hmis:Hashed/@hmis:dateCollected'
        xpOtherSuffixUnhashed = 'hmis:OtherSuffix/hmis:Unhashed'
        xpOtherSuffixHashed = 'hmis:OtherSuffix/hmis:Hashed'
        xpOtherSuffixDateCollectedUnhashed = 'hmis:OtherSuffix/hmis:Unhashed/@hmis:dateCollected'
        xpOtherSuffixDateCollectedHashed = 'hmis:OtherSuffix/hmis:Hashed/@hmis:dateCollected'
        other_names = person_tag.xpath(xpOtherNames, namespaces={'hmis': self.hmis_namespace})
        if other_names is not None:
            for item in other_names:
                self.parse_dict = {}
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                test = self.existence_test_and_add('other_first_name_unhashed', item.xpath(xpOtherFirstNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('other_first_name_date_collected', item.xpath(xpOtherFirstNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    test = self.existence_test_and_add('other_first_name_hashed', item.xpath(xpOtherFirstNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('other_first_name_date_collected', item.xpath(xpOtherFirstNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('other_last_name_unhashed', item.xpath(xpOtherLastNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('other_last_name_date_collected', item.xpath(xpOtherLastNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('other_last_name_hashed', item.xpath(xpOtherLastNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('other_last_name_date_collected', item.xpath(xpOtherLastNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('other_middle_name_unhashed', item.xpath(xpOtherMiddleNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('other_middle_name_date_collected', item.xpath(xpOtherMiddleNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('other_middle_name_hashed', item.xpath(xpOtherMiddleNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('other_middle_name_date_collected', item.xpath(xpOtherMiddleNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('other_suffix_unhashed', item.xpath(xpOtherSuffixUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('other_suffix_date_collected', item.xpath(xpOtherSuffixDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('other_suffix_hashed', item.xpath(xpOtherSuffixHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('other_suffix_date_collected', item.xpath(xpOtherSuffixDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.OtherNames)

        else:
            self.shred(self.parse_dict, dbobjects.OtherNames)
            return
        return

    def parse_hud_homeless_episodes(self, element):
        xpHudHomelessEpisodes = 'hmis:HUDHomelessEpisodes'
        xpStartDate = 'hmis:StartDate'
        xpStartDateDateCollected = 'hmis:StartDate/@hmis:dateCollected'
        xpEndDate = 'hmis:EndDate'
        xpEndDateDateCollected = 'hmis:EndDate/@hmis:dateCollected'
        itemElements = element.xpath(xpHudHomelessEpisodes, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                fldName = 'start_date'
                self.existence_test_and_add(fldName, item.xpath(xpStartDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'start_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'end_date'
                self.existence_test_and_add(fldName, item.xpath(xpEndDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'end_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                self.shred(self.parse_dict, dbobjects.HUDHomelessEpisodes)

        return

    def parse_veteran(self, element):
        xpVeteran = 'hmis:Veteran'
        xpServiceEra = 'hmis:ServiceEra'
        xpServiceEraDateCollected = 'hmis:ServiceEra/@hmis:dateCollected'
        xpMilitaryServiceDuration = 'hmis:MilitaryServiceDuration'
        xpMilitaryServiceDurationDateCollected = 'hmis:MilitaryServiceDuration/@hmis:dateCollected'
        xpServedInWarZone = 'hmis:ServedInWarZone'
        xpServedInWarZoneDateCollected = 'hmis:ServedInWarZone/@hmis:dateCollected'
        xpWarZone = 'hmis:WarZone'
        xpWarZoneDateCollected = 'hmis:WarZone/@hmis:dateCollected'
        xpWarZoneOther = 'hmis:WarZoneOther'
        xpWarZoneOtherDateCollected = 'hmis:WarZoneOther/@hmis:dateCollected'
        xpMonthsInWarZone = 'hmis:MonthsInWarZone'
        xpMonthsInWarZoneDateCollected = 'hmis:MonthsInWarZone/@hmis:dateCollected'
        xpReceivedFire = 'hmis:ReceivedFire'
        xpReceivedFireDateCollected = 'hmis:ReceivedFire/@hmis:dateCollected'
        xpMilitaryBranch = 'hmis:MilitaryBranch'
        xpMilitaryBranchDateCollected = 'hmis:MilitaryBranch/@hmis:dateCollected'
        xpMilitaryBranchOther = 'hmis:MilitaryBranchOther'
        xpMilitaryBranchOtherDateCollected = 'hmis:MilitaryBranchOther/@hmis:dateCollected'
        xpDischargeStatus = 'hmis:DischargeStatus'
        xpDischargeStatusDateCollected = 'hmis:DischargeStatus/@hmis:dateCollected'
        xpDischargeStatusOther = 'hmis:DischargeStatusOther'
        xpDischargeStatusOtherDateCollected = 'hmis:DischargeStatusOther/@hmis:dateCollected'
        itemElements = element.xpath(xpVeteran, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                fldName = 'service_era'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEra, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_era_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEraDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'military_service_duration'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryServiceDuration, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'military_service_duration_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryServiceDurationDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'served_in_war_zone'
                self.existence_test_and_add(fldName, item.xpath(xpServedInWarZone, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'served_in_war_zone_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServedInWarZoneDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'war_zone'
                self.existence_test_and_add(fldName, item.xpath(xpWarZone, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'war_zone_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpWarZoneDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'war_zone_other'
                self.existence_test_and_add(fldName, item.xpath(xpWarZoneOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'war_zone_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpWarZoneOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'months_in_war_zone'
                self.existence_test_and_add(fldName, item.xpath(xpMonthsInWarZone, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'months_in_war_zone_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMonthsInWarZoneDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'received_fire'
                self.existence_test_and_add(fldName, item.xpath(xpReceivedFire, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'received_fire_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReceivedFireDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'military_branch'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranch, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'military_branch_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranchDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'military_branch_other'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranchOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'military_branch_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranchOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'discharge_status'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'discharge_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'discharge_status_other'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatusOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'discharge_status_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatusOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                self.shred(self.parse_dict, dbobjects.Veteran)

        return

    def parse_person_address(self, element):
        xpPersonAddress = 'hmis:PersonAddress'
        xpAddressPeriodStartDate = 'hmis:AddressPeriod/hmis:StartDate'
        xpAddressPeriodStartDateDateCollected = 'hmis:AddressPeriod/hmis:StartDate/@hmis:dateCollected'
        xpAddressPeriodEndDate = 'hmis:AddressPeriod/hmis:EndDate'
        xpAddressPeriodEndDateDateCollected = 'hmis:AddressPeriod/hmis:EndDate/@hmis:dateCollected'
        xpPreAddressLine = 'hmis:PreAddressLine'
        xpPreAddressLineDateCollected = 'hmis:PreAddressLine/@hmis:dateCollected'
        xpLine1 = 'hmis:Line1'
        xpLine1DateCollected = 'hmis:Line1/@hmis:dateCollected'
        xpLine2 = 'hmis:Line2'
        xpLine2DateCollected = 'hmis:Line2/@hmis:dateCollected'
        xpCity = 'hmis:City'
        xpCityDateCollected = 'hmis:City/@hmis:dateCollected'
        xpCounty = 'hmis:County'
        xpCountyDateCollected = 'hmis:County/@hmis:dateCollected'
        xpState = 'hmis:State'
        xpStateDateCollected = 'hmis:State/@hmis:dateCollected'
        xpZIPCode = 'hmis:ZIPCode'
        xpZIPCodeDateCollected = 'hmis:ZIPCode/@hmis:dateCollected'
        xpCountry = 'hmis:Country'
        xpCountryDateCollected = 'hmis:Country/@hmis:dateCollected'
        xpIsLastPermanentZip = 'hmis:IsLastPermanentZIP'
        xpIsLastPermanentZipDateCollected = 'hmis:IsLastPermanentZIP/@hmis:dateCollected'
        xpZipQualityCode = 'hmis:ZIPQualityCode'
        xpZipQualityCodeDateCollected = 'hmis:ZIPQualityCode/@hmis:dateCollected'
        itemElements = element.xpath(xpPersonAddress, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                test = item.xpath(xpAddressPeriodStartDate, namespaces={'hmis': self.hmis_namespace})
                if len(test) > 0:
                    fldName = 'address_period_start_date'
                    self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodStartDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                    fldName = 'line2_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = item.xpath(xpAddressPeriodEndDate, namespaces={'hmis': self.hmis_namespace})
                if len(test) > 0:
                    fldName = 'address_period_end_date'
                    self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodEndDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                    fldName = 'address_period_end_date_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'pre_address_line'
                self.existence_test_and_add(fldName, item.xpath(xpPreAddressLine, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'pre_address_line_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPreAddressLineDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'line1'
                self.existence_test_and_add(fldName, item.xpath(xpLine1, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'line1_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpLine1DateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'line2'
                self.existence_test_and_add(fldName, item.xpath(xpLine2, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'line2_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpLine2DateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'city'
                self.existence_test_and_add(fldName, item.xpath(xpCity, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'city_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpCityDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'county'
                self.existence_test_and_add(fldName, item.xpath(xpCounty, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'county_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpCountyDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'state'
                self.existence_test_and_add(fldName, item.xpath(xpState, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'state_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpStateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'zip_code'
                self.existence_test_and_add(fldName, item.xpath(xpZIPCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'zip_code_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpZIPCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'country'
                self.existence_test_and_add(fldName, item.xpath(xpCountry, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'country_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpCountryDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'is_last_permanent_zip'
                self.existence_test_and_add(fldName, item.xpath(xpIsLastPermanentZip, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'is_last_permanent_zip_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpIsLastPermanentZipDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'zip_quality_code'
                self.existence_test_and_add(fldName, item.xpath(xpZipQualityCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'zip_quality_code_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpZipQualityCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                self.shred(self.parse_dict, dbobjects.PersonAddress)

        return

    def parse_income_and_sources(self, item):
        xpIncomeAndSources = 'hmis:IncomeAndSources'
        xpAmount = 'hmis:Amount'
        xpAmountDateCollected = 'hmis:Amount/@hmis:dateCollected'
        xpIncomeSourceCode = 'hmis:IncomeSourceCode'
        xpIncomeSourceCodeDateCollected = 'hmis:IncomeSourceCode/@hmis:dateCollected'
        xpIncomeSourceOther = 'hmis:IncomeSourceOther'
        xpIncomeSourceOtherDateCollected = 'hmis:IncomeSourceOther/@hmis:dateCollected'
        incomeSources = item.xpath(xpIncomeAndSources, namespaces={'hmis': self.hmis_namespace})
        if incomeSources is not None:
            for income in incomeSources:
                fldName = 'amount'
                self.existence_test_and_add(fldName, income.xpath(xpAmount, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'amount_date_collected'
                self.existence_test_and_add(fldName, income.xpath(xpAmountDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'income_source_code'
                self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'income_source_code_date_collected'
                self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'income_source_other'
                self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'income_source_other_date_collected'
                self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                self.shred(self.parse_dict, dbobjects.IncomeAndSources)

        return

    def parse_person_historical(self, person_tag):
        """Looks for an PersonHistorical tag and related fields in the XML and persists it."""
        xpSvcParticipationPersonHistorical = 'hmis:SiteServiceParticipation/hmis:PersonHistorical'
        xpPersonHistorical = 'hmis:PersonHistorical'
        xpPersonHistoricalIDIDNum = 'hmis:PersonHistoricalID/hmis:IDNum'
        xpPersonHistoricalIDIDNumDateCollected = 'hmis:PersonHistoricalID/hmis:IDNum/@hmis:dateCollected'
        xpPersonHistoricalIDIDStr = 'hmis:PersonHistoricalID/hmis:IDStr'
        xpPersonHistoricalIDIDStrDateCollected = 'hmis:PersonHistoricalID/hmis:IDStr/@hmis:dateCollected'
        xpBarrierCode = 'hmis:BarrierCode'
        xpBarrierCodeDateCollected = 'hmis:BarrierCode/@hmis:dateCollected'
        xpBarrierOther = 'hmis:BarrierOther'
        xpBarrierOtherDateCollected = 'hmis:BarrierOther/@hmis:dateCollected'
        xpChildCurrentlyEnrolledInSchool = 'hmis:ChildCurrentlyEnrolledInSchool'
        xpChildCurrentlyEnrolledInSchoolDateCollected = 'hmis:ChildCurrentlyEnrolledInSchool/@hmis:dateCollected'
        xpCurrentlyEmployed = 'hmis:CurrentlyEmployed'
        xpCurrentlyEmployedDateCollected = 'hmis:CurrentlyEmployed/@hmis:dateCollected'
        xpCurrentlyInSchool = 'hmis:CurrentlyInSchool'
        xpCurrentlyInSchoolDateCollected = 'hmis:CurrentlyInSchool/@hmis:dateCollected'
        xpDegreeCode = 'hmis:DegreeCode'
        xpDegreeCodeDateCollected = 'hmis:DegreeCode/@hmis:dateCollected'
        xpDegreeOther = 'hmis:DegreeOther'
        xpDegreeOtherDateCollected = 'hmis:DegreeOther/@hmis:dateCollected'
        xpDevelopmentalDisability = 'hmis:DevelopmentalDisability'
        xpDevelopmentalDisabilityDateCollected = 'hmis:DevelopmentalDisability/@hmis:dateCollected'
        xpDomesticViolence = 'hmis:DomesticViolence'
        xpDomesticViolenceDateCollected = 'hmis:DomesticViolence/@hmis:dateCollected'
        xpDomesticViolenceHowLong = 'hmis:DomesticViolenceHowLong'
        xpDomesticViolenceHowLongDateCollected = 'hmis:DomesticViolenceHowLong/@hmis:dateCollected'
        xpDueDate = 'hmis:DueDate'
        xpDueDateDateCollected = 'hmis:DueDate/@hmis:dateCollected'
        xpEmploymentTenure = 'hmis:EmploymentTenure'
        xpEmploymentTenureDateCollected = 'hmis:EmploymentTenure/@hmis:dateCollected'
        xpHealthStatus = 'hmis:HealthStatus'
        xpHealthStatusDateCollected = 'hmis:HealthStatus/@hmis:dateCollected'
        xpHighestSchoolLevel = 'hmis:HighestSchoolLevel'
        xpHighestSchoolLevelDateCollected = 'hmis:HighestSchoolLevel/@hmis:dateCollected'
        xpHIVAIDSStatus = 'hmis:HIVAIDSStatus'
        xpHIVAIDSStatusDateCollected = 'hmis:HIVAIDSStatus/@hmis:dateCollected'
        xpHoursWorkedLastWeek = 'hmis:HoursWorkedLastWeek'
        xpHoursWorkedLastWeekDateCollected = 'hmis:HoursWorkedLastWeek/@hmis:dateCollected'
        xpHUDChronicHomeless = 'hmis:HUDChronicHomeless'
        xpHUDChronicHomelessDateCollected = 'hmis:HUDChronicHomeless/@hmis:dateCollected'
        xpHUDHomeless = 'hmis:HUDHomeless'
        xpHUDHomelessDateCollected = 'hmis:HUDHomeless/@hmis:dateCollected'
        xpLengthOfStayAtPriorResidence = 'hmis:LengthOfStayAtPriorResidence'
        xpLengthOfStayAtPriorResidenceDateCollected = 'hmis:LengthOfStayAtPriorResidence/@hmis:dateCollected'
        xpLookingForWork = 'hmis:LookingForWork'
        xpLookingForWorkDateCollected = 'hmis:LookingForWork/@hmis:dateCollected'
        xpMentalHealthIndefinite = 'hmis:MentalHealthIndefinite'
        xpMentalHealthIndefiniteDateCollected = 'hmis:MentalHealthIndefinite/@hmis:dateCollected'
        xpMentalHealthProblem = 'hmis:MentalHealthProblem'
        xpMentalHealthProblemDateCollected = 'hmis:MentalHealthProblem/@hmis:dateCollected'
        xpNonCashSourceCode = 'hmis:NonCashSourceCode'
        xpNonCashSourceCodeDateCollected = 'hmis:NonCashSourceCode/@hmis:dateCollected'
        xpNonCashSourceOther = 'hmis:NonCashSourceOther'
        xpNonCashSourceOtherDateCollected = 'hmis:NonCashSourceOther/@hmis:dateCollected'
        xpPersonEmail = 'hmis:PersonEmail'
        xpPersonEmailDateCollected = 'hmis:PersonEmail/@hmis:dateCollected'
        xpPersonPhoneNumber = 'hmis:PersonPhoneNumber'
        xpPersonPhoneNumberDateCollected = 'hmis:PersonPhoneNumber/@hmis:dateCollected'
        xpPhysicalDisability = 'hmis:PhysicalDisability'
        xpPhysicalDisabilityDateCollected = 'hmis:PhysicalDisability/@hmis:dateCollected'
        xpPregnancyStatus = 'hmis:PregnancyStatus'
        xpPregnancyStatusDateCollected = 'hmis:PregnancyStatus/@hmis:dateCollected'
        xpPriorResidence = 'hmis:PriorResidence'
        xpPriorResidenceDateCollected = 'hmis:PriorResidence/@hmis:dateCollected'
        xpPriorResidenceOther = 'hmis:PriorResidenceOther'
        xpPriorResidenceOtherDateCollected = 'hmis:PriorResidenceOther/@hmis:dateCollected'
        xpReasonForLeaving = 'hmis:ReasonForLeaving'
        xpReasonForLeavingDateCollected = 'hmis:ReasonForLeaving/@hmis:dateCollected'
        xpReasonForLeavingOther = 'hmis:ReasonForLeavingOther'
        xpReasonForLeavingOtherDateCollected = 'hmis:ReasonForLeavingOther/@hmis:dateCollected'
        xpSchoolLastEnrolledDate = 'hmis:SchoolLastEnrolledDate'
        xpSchoolLastEnrolledDateDateCollected = 'hmis:SchoolLastEnrolledDate/@hmis:dateCollected'
        xpSchoolName = 'hmis:SchoolName'
        xpSchoolNameDateCollected = 'hmis:SchoolName/@hmis:dateCollected'
        xpSchoolType = 'hmis:SchoolType'
        xpSchoolTypeDateCollected = 'hmis:SchoolType/@hmis:dateCollected'
        xpSubsidyOther = 'hmis:SubsidyOther'
        xpSubsidyOtherDateCollected = 'hmis:SubsidyOther/@hmis:dateCollected'
        xpSubsidyType = 'hmis:SubsidyType'
        xpSubsidyTypeDateCollected = 'hmis:SubsidyType/@hmis:dateCollected'
        xpSubstanceAbuseIndefinite = 'hmis:SubstanceAbuseIndefinite'
        xpSubstanceAbuseIndefiniteDateCollected = 'hmis:SubstanceAbuseIndefinite/@hmis:dateCollected'
        xpSubstanceAbuseProblem = 'hmis:SubstanceAbuseProblem'
        xpSubstanceAbuseProblemDateCollected = 'hmis:SubstanceAbuseProblem/@hmis:dateCollected'
        xpTotalIncome = 'hmis:TotalIncome'
        xpTotalIncomeDateCollected = 'hmis:TotalIncome/@hmis:dateCollected'
        xpVocationalTraining = 'hmis:VocationalTraining'
        xpVocationalTrainingDateCollected = 'hmis:VocationalTraining/@hmis:dateCollected'
        person_historical = person_tag.xpath(xpPersonHistorical, namespaces={'hmis': self.hmis_namespace})
        if len(person_historical) == 0:
            person_historical = person_tag.xpath(xpSvcParticipationPersonHistorical, namespaces={'hmis': self.hmis_namespace})
        if person_historical is not None and len(person_historical) > 0:
            for item in person_historical:
                self.parse_dict = {}
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                fldName = 'person_historical_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'person_historical_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'person_historical_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'person_historical_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'barrier_code'
                self.existence_test_and_add(fldName, item.xpath(xpBarrierCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'barrier_code_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpBarrierCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'barrier_other'
                self.existence_test_and_add(fldName, item.xpath(xpBarrierOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'barrier_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpBarrierOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'child_currently_enrolled_in_school'
                self.existence_test_and_add(fldName, item.xpath(xpChildCurrentlyEnrolledInSchool, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'child_currently_enrolled_in_school_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpChildCurrentlyEnrolledInSchoolDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'currently_employed'
                self.existence_test_and_add(fldName, item.xpath(xpCurrentlyEmployed, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'currently_employed_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpCurrentlyEmployedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'currently_in_school'
                self.existence_test_and_add(fldName, item.xpath(xpCurrentlyInSchool, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'currently_in_school_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpCurrentlyInSchoolDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'degree_code'
                self.existence_test_and_add(fldName, item.xpath(xpDegreeCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'degree_code_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDegreeCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'degree_other'
                self.existence_test_and_add(fldName, item.xpath(xpDegreeOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'degree_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDegreeOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'developmental_disability'
                self.existence_test_and_add(fldName, item.xpath(xpDevelopmentalDisability, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'developmental_disability_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDevelopmentalDisabilityDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'domestic_violence'
                self.existence_test_and_add(fldName, item.xpath(xpDomesticViolence, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'domestic_violence_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDomesticViolenceDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'domestic_violence_how_long'
                self.existence_test_and_add(fldName, item.xpath(xpDomesticViolenceHowLong, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'domestic_violence_how_long_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDomesticViolenceHowLongDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'due_date'
                self.existence_test_and_add(fldName, item.xpath(xpDueDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'due_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDueDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'employment_tenure'
                self.existence_test_and_add(fldName, item.xpath(xpEmploymentTenure, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'employment_tenure_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpEmploymentTenureDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'health_status'
                self.existence_test_and_add(fldName, item.xpath(xpHealthStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'health_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHealthStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'highest_school_level'
                self.existence_test_and_add(fldName, item.xpath(xpHighestSchoolLevel, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'highest_school_level_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHighestSchoolLevelDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'hivaids_status'
                self.existence_test_and_add(fldName, item.xpath(xpHIVAIDSStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'hivaids_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHIVAIDSStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'hours_worked_last_week'
                self.existence_test_and_add(fldName, item.xpath(xpHoursWorkedLastWeek, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'hours_worked_last_week_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHoursWorkedLastWeekDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'hud_chronic_homeless'
                self.existence_test_and_add(fldName, item.xpath(xpHUDChronicHomeless, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'hud_chronic_homeless_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHUDChronicHomelessDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'hud_homeless'
                self.existence_test_and_add(fldName, item.xpath(xpHUDHomeless, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'hud_homeless_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHUDHomelessDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'length_of_stay_at_prior_residence'
                self.existence_test_and_add(fldName, item.xpath(xpLengthOfStayAtPriorResidence, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'length_of_stay_at_prior_residence_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpLengthOfStayAtPriorResidenceDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'looking_for_work'
                self.existence_test_and_add(fldName, item.xpath(xpLookingForWork, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'looking_for_work_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpLookingForWorkDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'mental_health_indefinite'
                self.existence_test_and_add(fldName, item.xpath(xpMentalHealthIndefinite, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'mental_health_indefinite_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMentalHealthIndefiniteDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'mental_health_problem'
                self.existence_test_and_add(fldName, item.xpath(xpMentalHealthProblem, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'mental_health_problem_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMentalHealthProblemDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'non_cash_source_code'
                self.existence_test_and_add(fldName, item.xpath(xpNonCashSourceCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'non_cash_source_code_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpNonCashSourceCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'non_cash_source_other'
                self.existence_test_and_add(fldName, item.xpath(xpNonCashSourceOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'non_cash_source_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpNonCashSourceOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'person_email'
                self.existence_test_and_add(fldName, item.xpath(xpPersonEmail, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'person_email_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPersonEmailDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'person_phone_number'
                self.existence_test_and_add(fldName, item.xpath(xpPersonPhoneNumber, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'person_phone_number_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPersonPhoneNumberDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'physical_disability'
                self.existence_test_and_add(fldName, item.xpath(xpPhysicalDisability, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'physical_disability_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPhysicalDisabilityDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'pregnancy_status'
                self.existence_test_and_add(fldName, item.xpath(xpPregnancyStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'pregnancy_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPregnancyStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'prior_residence'
                self.existence_test_and_add(fldName, item.xpath(xpPriorResidence, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'prior_residence_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPriorResidenceDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'prior_residence_other'
                self.existence_test_and_add(fldName, item.xpath(xpPriorResidenceOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'prior_residence_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPriorResidenceOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'reason_for_leaving'
                self.existence_test_and_add(fldName, item.xpath(xpReasonForLeaving, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'reason_for_leaving_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReasonForLeavingDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'reason_for_leaving_other'
                self.existence_test_and_add(fldName, item.xpath(xpReasonForLeavingOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'reason_for_leaving_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReasonForLeavingOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'school_last_enrolled_date'
                self.existence_test_and_add(fldName, item.xpath(xpSchoolLastEnrolledDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'school_last_enrolled_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSchoolLastEnrolledDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'school_name'
                self.existence_test_and_add(fldName, item.xpath(xpSchoolName, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'school_name_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSchoolNameDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'school_type'
                self.existence_test_and_add(fldName, item.xpath(xpSchoolType, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'school_type_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSchoolTypeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'subsidy_other'
                self.existence_test_and_add(fldName, item.xpath(xpSubsidyOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'subsidy_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSubsidyOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'subsidy_type'
                self.existence_test_and_add(fldName, item.xpath(xpSubsidyType, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'subsidy_type_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSubsidyTypeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'substance_abuse_indefinite'
                self.existence_test_and_add(fldName, item.xpath(xpSubstanceAbuseIndefinite, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'substance_abuse_indefinite_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSubstanceAbuseIndefiniteDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'substance_abuse_problem'
                self.existence_test_and_add(fldName, item.xpath(xpSubstanceAbuseProblem, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'substance_abuse_problem_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSubstanceAbuseProblemDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'total_income'
                self.existence_test_and_add(fldName, item.xpath(xpTotalIncome, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'total_income_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpTotalIncomeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'vocational_training'
                self.existence_test_and_add(fldName, item.xpath(xpVocationalTraining, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'vocational_training_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpVocationalTrainingDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.PersonHistorical)
                self.parse_hud_homeless_episodes(item)
                self.parse_income_and_sources(item)
                self.parse_person_address(item)
                self.parse_veteran(item)

        else:
            self.shred(self.parse_dict, dbobjects.PersonHistorical)
            return
        return

    def parse_person(self, root_element):
        """Looks for a Person tag and related fields in the XML and persists 

        it.  This code allows for multiple persons per file"""
        xpPerson = 'hmis:Person'
        xpExportID = '../hmis:Export/hmis:ExportID/hmis:IDNum'
        xpPersonIDHashed = 'hmis:PersonID/hmis:Hashed'
        xpPersonIDUnhashed = 'hmis:PersonID/hmis:Unhashed'
        xpPersonIDDateCollectedHashed = 'hmis:PersonID/hmis:Hashed/@hmis:dateCollected'
        xpPersonIDDateCollectedUnhashed = 'hmis:PersonID/hmis:Unhashed/@hmis:dateCollected'
        xpPersonDateOfBirthHashed = 'hmis:DateOfBirth/hmis:Hashed'
        xpPersonDateOfBirthUnhashed = 'hmis:DateOfBirth/hmis:Unhashed'
        xpPersonDateOfBirthDateCollectedHashed = 'hmis:DateOfBirth/hmis:Hashed/@hmis:dateCollected'
        xpPersonDateOfBirthDateCollectedUnhashed = 'hmis:DateOfBirth/hmis:Unhashed/@hmis:dateCollected'
        xpPersonEthnicityHashed = 'hmis:Ethnicity/hmis:Hashed'
        xpPersonEthnicityUnhashed = 'hmis:Ethnicity/hmis:Unhashed'
        xpPersonEthnicityDateCollectedHashed = 'hmis:Ethnicity/hmis:Hashed/@hmis:dateCollected'
        xpPersonEthnicityDateCollectedUnhashed = 'hmis:Ethnicity/hmis:Unhashed/@hmis:dateCollected'
        xpPersonGenderHashed = 'hmis:Gender/hmis:Hashed'
        xpPersonGenderUnhashed = 'hmis:Gender/hmis:Unhashed'
        xpPersonGenderDateCollectedHashed = 'hmis:Gender/hmis:Hashed/@hmis:dateCollected'
        xpPersonGenderDateCollectedUnhashed = 'hmis:Gender/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalFirstNameHashed = 'hmis:LegalFirstName/hmis:Hashed'
        xpPersonLegalFirstNameUnhashed = 'hmis:LegalFirstName/hmis:Unhashed'
        xpPersonLegalFirstNameDateCollectedHashed = 'hmis:LegalFirstName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalFirstNameDateCollectedUnhashed = 'hmis:LegalFirstName/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalLastNameHashed = 'hmis:LegalLastName/hmis:Hashed'
        xpPersonLegalLastNameUnhashed = 'hmis:LegalLastName/hmis:Unhashed'
        xpPersonLegalLastNameDateCollectedHashed = 'hmis:LegalLastName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalLastNameDateCollectedUnhashed = 'hmis:LegalLastName/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalMiddleNameHashed = 'hmis:LegalMiddleName/hmis:Hashed'
        xpPersonLegalMiddleNameUnhashed = 'hmis:LegalMiddleName/hmis:Unhashed'
        xpPersonLegalMiddleNameDateCollectedHashed = 'hmis:LegalMiddleName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalMiddleNameDateCollectedUnhashed = 'hmis:LegalMiddleName/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalSuffixHashed = 'hmis:LegalSuffix/hmis:Hashed'
        xpPersonLegalSuffixUnhashed = 'hmis:LegalSuffix/hmis:Unhashed'
        xpPersonLegalSuffixDateCollectedHashed = 'hmis:LegalSuffix/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalSuffixDateCollectedUnhashed = 'hmis:LegalSuffix/hmis:Unhashed/@hmis:dateCollected'
        xpPersonSocialSecurityNumberHashed = 'hmis:SocialSecurityNumber/hmis:Hashed'
        xpPersonSocialSecurityNumberUnhashed = 'hmis:SocialSecurityNumber/hmis:Unhashed'
        xpPersonSocialSecurityNumberDateCollectedHashed = 'hmis:SocialSecurityNumber/hmis:Hashed/@hmis:dateCollected'
        xpPersonSocialSecurityNumberDateCollectedUnhashed = 'hmis:SocialSecurityNumber/hmis:Unhashed/@hmis:dateCollected'
        xpPersonSocialSecNumberQualityCode = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode'
        xpPersonSocialSecNumberQualityCodeDateCollected = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:dateCollected'
        person = root_element.xpath(xpPerson, namespaces={'hmis': self.hmis_namespace})
        if person is not None:
            for item in person:
                self.parse_dict = {}
                test = self.existence_test_and_add('person_id_unhashed', item.xpath(xpPersonIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_id_date_collected', item.xpath(xpPersonIDDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_id_hashed', item.xpath(xpPersonIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_id_date_collected', item.xpath(xpPersonIDDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_id', self.export_id, 'text')
                test = self.existence_test_and_add('person_date_of_birth_unhashed', item.xpath(xpPersonDateOfBirthUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_date_of_birth_date_collected', item.xpath(xpPersonDateOfBirthDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_date_of_birth_hashed', item.xpath(xpPersonDateOfBirthHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_date_of_birth_date_collected', item.xpath(xpPersonDateOfBirthDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_ethnicity_unhashed', item.xpath(xpPersonEthnicityUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_ethnicity_date_collected', item.xpath(xpPersonEthnicityDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_ethnicity_hashed', item.xpath(xpPersonEthnicityHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_ethnicity_date_collected', item.xpath(xpPersonEthnicityDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_gender_unhashed', item.xpath(xpPersonGenderUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_gender_date_collected', item.xpath(xpPersonGenderDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_gender_hashed', item.xpath(xpPersonGenderHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_gender_date_collected', item.xpath(xpPersonGenderDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_first_name_unhashed', item.xpath(xpPersonLegalFirstNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_first_name_date_collected', item.xpath(xpPersonLegalFirstNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_first_name_hashed', item.xpath(xpPersonLegalFirstNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_first_name_date_collected', item.xpath(xpPersonLegalFirstNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_last_name_unhashed', item.xpath(xpPersonLegalLastNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_last_name_date_collected', item.xpath(xpPersonLegalLastNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_last_name_hashed', item.xpath(xpPersonLegalLastNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_last_name_date_collected', item.xpath(xpPersonLegalLastNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_middle_name_unhashed', item.xpath(xpPersonLegalMiddleNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_middle_name_date_collected', item.xpath(xpPersonLegalMiddleNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_middle_name_hashed', item.xpath(xpPersonLegalMiddleNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_middle_name_date_collected', item.xpath(xpPersonLegalMiddleNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_suffix_unhashed', item.xpath(xpPersonLegalSuffixUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_suffix_date_collected', item.xpath(xpPersonLegalSuffixDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_suffix_hashed', item.xpath(xpPersonLegalSuffixHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_suffix_date_collected', item.xpath(xpPersonLegalSuffixDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_social_security_number_unhashed', item.xpath(xpPersonSocialSecurityNumberUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_social_security_number_date_collected', item.xpath(xpPersonSocialSecurityNumberDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_social_security_number_hashed', item.xpath(xpPersonSocialSecurityNumberHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_social_security_number_date_collected', item.xpath(xpPersonSocialSecurityNumberDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('person_social_sec_number_quality_code', item.xpath(xpPersonSocialSecNumberQualityCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('person_social_sec_number_quality_code_date_collected', item.xpath(xpPersonSocialSecNumberQualityCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.Person)
                self.parse_person_historical(item)
                self.parse_other_names(item)
                self.parse_races(item)
                self.parse_release_of_information(item)
                self.parse_site_service_participation(item)

            return
        else:
            self.shred(self.parse_dict, dbobjects.Person)
            return
            return

    def parse_races(self, person_tag):
        """Looks for a Race tag and related fields in the XML and persists it."""
        xpRaces = 'hmis:Race'
        xpRaceUnhashed = 'hmis:Unhashed'
        xpRaceHashed = 'hmis:Hashed'
        xpRaceDateCollectedUnhashed = 'hmis:Unhashed/@hmis:dateCollected'
        xpRaceDateCollectedHashed = 'hmis:Hashed/@hmis:dateCollected'
        races = person_tag.xpath(xpRaces, namespaces={'hmis': self.hmis_namespace})
        if races is not None:
            for item in races:
                self.parse_dict = {}
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                test = self.existence_test_and_add('race_unhashed', item.xpath(xpRaceUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('race_date_collected', item.xpath(xpRaceDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('race_hashed', item.xpath(xpRaceHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('race_date_collected', item.xpath(xpRaceDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.Races)

        else:
            self.shred(self.parse_dict, dbobjects.Races)
            return
        return

    def parse_household(self, element):
        xpHousehold = 'hmis:Household'
        xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDNumDateCollected = 'hmis:HouseholdIDIDNum/@hmis:dateCollected'
        xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
        xpHouseholdIDIDStrDateCollected = 'hmis:HouseholdID/hmis:IDStr/@hmis:dateCollected'
        xpHeadOfHouseholdIDUnhashed = 'hmis:HeadOfHouseholdID/hmis:Unhashed'
        xpHeadOfHouseholdIDUnhashedDateCollected = 'hmis:HeadOfHouseholdID/hmis:Unhashed/@hmis:dateCollected'
        xpHeadOfHouseholdIDHashed = 'hmis:HeadOfHouseholdID/hmis:Hashed'
        xpHeadOfHouseholdIDHashedDateCollected = 'hmis:HeadOfHouseholdID/hmis:Hashed/@hmis:dateCollected'
        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                self.existence_test_and_add('export_id', self.export_id, 'text')
                fldName = 'household_id_num'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'household_id_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'household_id_str'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'household_id_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'head_of_household_id_unhashed'
                self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'head_of_household_id_unhashed_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDUnhashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'head_of_household_id_hashed'
                self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'head_of_household_id_hashed_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDHashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.Household)
                self.parse_members(item)

        return

    def parse_members(self, element):
        xpMembers = 'hmis:Members'
        xpMember = 'hmis:Member'
        xpPersonIDUnhashed = 'hmis:PersonID/hmis:Unhashed'
        xpPersonIDUnhashedDateCollected = 'hmis:PersonID/hmis:Unhashed/@hmis:dateCollected'
        xpPersonIDHashed = 'hmis:PersonID/hmis:Hashed'
        xpPersonIDHashedDateCollected = 'hmis:PersonID/hmis:Hashed/@hmis:dateCollected'
        xpRelationshipToHeadOfHousehold = 'hmis:RelationshipToHeadOfHousehold'
        xpRelationshipToHeadOfHouseholdDateCollected = 'hmis:RelationshipToHeadOfHousehold/@hmis:dateCollected'
        test = element.xpath(xpMembers, namespaces={'hmis': self.hmis_namespace})
        if len(test) > 0:
            itemElements = test[0].xpath(xpMember, namespaces={'hmis': self.hmis_namespace})
            if itemElements is not None:
                for item in itemElements:
                    self.parse_dict = {}
                    fldName = 'person_id_unhashed'
                    self.existence_test_and_add(fldName, item.xpath(xpPersonIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName = 'person_id_unhashed_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpPersonIDUnhashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    fldName = 'person_id_hashed'
                    self.existence_test_and_add(fldName, item.xpath(xpPersonIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName = 'person_id_hashed_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpPersonIDHashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    fldName = 'relationship_to_head_of_household'
                    self.existence_test_and_add(fldName, item.xpath(xpRelationshipToHeadOfHousehold, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName = 'relationship_to_head_of_household_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpRelationshipToHeadOfHouseholdDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    self.existence_test_and_add('household_index_id', self.household_index_id, 'no_handling')
                    self.shred(self.parse_dict, dbobjects.Members)

        return

    def parse_release_of_information(self, element):
        xpReleaseOfInformation = 'hmis:ReleaseOfInformation'
        xpReleaseOfInformationIDIDNum = 'hmis:ReleaseOfInformationID/hmis:IDNum'
        xpReleaseOfInformationIDIDNumDateCollected = 'hmis:ReleaseOfInformationID/hmis:IDNum/@hmis:dateCollected'
        xpReleaseOfInformationIDIDStr = 'hmis:ReleaseOfInformationID/hmis:IDStr'
        xpReleaseOfInformationIDIDStrDateCollected = 'hmis:ReleaseOfInformationID/hmis:IDStr/@hmis:dateCollected'
        xpSiteServiceIDIDNum = 'hmis:SiteServiceID/hmis:IDNum'
        xpSiteServiceIDIDNumDateCollected = 'hmis:SiteServiceID/hmis:IDNum/@hmis:dateCollected'
        xpSiteServiceIDIDStr = 'hmis:SiteServiceID/hmis:IDStr'
        xpSiteServiceIDIDStrDateCollected = 'hmis:SiteServiceID/hmis:IDStr/@hmis:dateCollected'
        xpDocumentation = 'hmis:Documentation'
        xpDocumentationDateCollected = 'hmis:Documentation/@hmis:dateCollected'
        xpStartDate = 'hmis:EffectivePeriod/hmis:StartDate'
        xpStartDateDateCollected = 'hmis:EffectivePeriod/hmis:StartDate/@hmis:dateCollected'
        xpEndDate = 'hmis:EffectivePeriod/hmis:EndDate'
        xpEndDateDateCollected = 'hmis:EffectivePeriod/hmis:EndDate/@hmis:dateCollected'
        xpReleaseGranted = 'hmis:ReleaseGranted'
        xpReleaseGrantedDateCollected = 'hmis:ReleaseGranted/@hmis:dateCollected'
        itemElements = element.xpath(xpReleaseOfInformation, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                fldName = 'release_of_information_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'release_of_information_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'release_of_information_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'release_of_information_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'documentation'
                self.existence_test_and_add(fldName, item.xpath(xpDocumentation, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'documentation_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDocumentationDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'start_date'
                self.existence_test_and_add(fldName, item.xpath(xpStartDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'start_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'end_date'
                self.existence_test_and_add(fldName, item.xpath(xpEndDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'end_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'release_granted'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseGranted, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'release_granted_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseGrantedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.ReleaseOfInformation)

        return

    def parse_need(self, element):
        xpNeed = 'hmis:Need'
        xpNeedIDIDNum = 'hmis:NeedID/hmis:IDNum'
        xpNeedIDIDNumDateCollected = 'hmis:NeedID/hmis:IDNum/@hmis:dateCollected'
        xpNeedIDIDStr = 'hmis:NeedIDIDStr'
        xpNeedIDIDStrDateCollected = 'hmis:NeedID/hmis:IDStr/@hmis:dateCollected'
        xpSiteServiceIDIDNum = 'hmis:SiteServiceID/hmis:IDNum'
        xpSiteServiceIDIDNumDateCollected = 'hmis:SiteServiceID/hmis:IDNum/@hmis:dateCollected'
        xpSiteServiceIDIDStr = 'hmis:SiteServiceID/hmis:IDStr'
        xpSiteServiceIDIDStrDateCollected = 'hmis:SiteServiceIDIDStr/@hmis:dateCollected'
        xpServiceEventIDIDNum = 'hmis:ServiceEventID/hmis:IDNum'
        xpServiceEventIDIDNumDateCollected = 'hmis:ServiceEventIDIDNum/@hmis:dateCollected'
        xpServiceEventIDIDStr = 'hmis:ServiceEventID/hmis:IDStr'
        xpServiceEventIDIDStrDateCollected = 'hmis:ServiceEventID/hmis:IDStr/@hmis:dateCollected'
        xpNeedStatus = 'hmis:NeedStatus'
        xpNeedStatusDateCollected = 'hmis:NeedStatus/@hmis:dateCollected'
        xpTaxonomy = 'hmis:Taxonomy/airs:Code'
        xpTaxonomyDateCollected = 'hmis:Taxonomy/airs:Code/@hmis:dateCollected'
        itemElements = element.xpath(xpNeed, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                fldName = 'need_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpNeedIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'need_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpNeedIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'need_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpNeedIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'need_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpNeedIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_event_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_event_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_event_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_event_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'need_status'
                self.existence_test_and_add(fldName, item.xpath(xpNeedStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'need_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpNeedStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'taxonomy'
                self.existence_test_and_add(fldName, item.xpath(xpTaxonomy, namespaces=self.nsmap), 'text')
                self.shred(self.parse_dict, dbobjects.Need)

        return

    def parse_site_service_participation(self, element):
        xpSiteServiceParticipation = 'hmis:SiteServiceParticipation'
        xpSiteServiceParticipationIDIDNum = 'hmis:SiteServiceParticipationID/hmis:IDNum'
        xpSiteServiceParticipationIDIDNumDateCollected = 'hmis:SiteServiceParticipationID/hmis:IDNum/@hmis:dateCollected'
        xpSiteServiceParticipationIDIDStr = 'hmis:SiteServiceParticipationID/hmis:IDStr'
        xpSiteServiceParticipationIDIDStrDateCollected = 'hmis:SiteServiceParticipationID/hmis:IDStr/@hmis:dateCollected'
        xpSiteServiceIDIDNum = 'hmis:SiteServiceID/hmis:IDNum'
        xpSiteServiceIDIDNumDateCollected = 'hmis:SiteServiceID/hmis:IDNum/@hmis:dateCollected'
        xpSiteServiceIDIDStr = 'hmis:SiteServiceID/hmis:IDStr'
        xpSiteServiceIDIDStrDateCollected = 'hmis:SiteServiceID/hmis:IDStr/@hmis:dateCollected'
        xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDNumDateCollected = 'hmis:HouseholdID/hmis:IDNum/@hmis:dateCollected'
        xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
        xpHouseholdIDIDStrDateCollected = 'hmis:HouseholdID/hmis:IDStr/@hmis:dateCollected'
        xpDestination = 'hmis:Destination'
        xpDestinationDateCollected = 'hmis:Destination/@hmis:dateCollected'
        xpDestinationOther = 'hmis:DestinationOther'
        xpDestinationOtherDateCollected = 'hmis:DestinationOther/@hmis:dateCollected'
        xpDestinationTenure = 'hmis:DestinationTenure'
        xpDestinationTenureDateCollected = 'hmis:DestinationTenure/@hmis:dateCollected'
        xpDisablingCondition = 'hmis:DisablingCondition'
        xpDisablingConditionDateCollected = 'hmis:DisablingCondition/@hmis:dateCollected'
        xpStartDate = 'hmis:ParticipationDates/hmis:StartDate'
        xpStartDateDateCollected = 'hmis:ParticipationDates/hmis:StartDate/@hmis:dateCollected'
        xpEndDate = 'hmis:ParticipationDates/hmis:EndDate'
        xpEndDateDateCollected = 'hmis:ParticipationDates/hmis:EndDate/@hmis:dateCollected'
        xpVeteranStatus = 'hmis:VeteranStatus'
        xpVeteranStatusDateCollected = 'hmis:VeteranStatus/@hmis:dateCollected'
        itemElements = element.xpath(xpSiteServiceParticipation, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                fldName = 'site_service_participation_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceParticipationIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_participation_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceParticipationIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_participation_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceParticipationIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_participation_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceParticipationIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'site_service_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'site_service_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'household_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'household_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'household_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'household_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'destination'
                self.existence_test_and_add(fldName, item.xpath(xpDestination, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'destination_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDestinationDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'destination_other'
                self.existence_test_and_add(fldName, item.xpath(xpDestinationOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'destination_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDestinationOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'destination_tenure'
                self.existence_test_and_add(fldName, item.xpath(xpDestinationTenure, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'destination_tenure_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDestinationTenureDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'disabling_condition'
                self.existence_test_and_add(fldName, item.xpath(xpDisablingCondition, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'disabling_condition_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDisablingConditionDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'participation_dates_start_date'
                self.existence_test_and_add(fldName, item.xpath(xpStartDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'participation_dates_start_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'participation_dates_end_date'
                self.existence_test_and_add(fldName, item.xpath(xpEndDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'participation_dates_end_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'veteran_status'
                self.existence_test_and_add(fldName, item.xpath(xpVeteranStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'veteran_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpVeteranStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.SiteServiceParticipation)
                self.parse_need(item)
                self.parse_service_event(item)

        return

    def parse_service_event(self, element):
        xpServiceEvent = 'hmis:ServiceEvent'
        xpServiceEventIDIDNum = 'hmis:ServiceEventID/hmis:IDNum'
        xpServiceEventIDIDNumDateCollected = 'hmis:ServiceEventID/hmis:IDNum/@hmis:dateCollected'
        xpServiceEventIDIDStr = 'hmis:ServiceEventID/hmis:IDStr'
        xpServiceEventIDIDStrDateCollected = 'hmis:ServiceEventID/hmis:IDStr/@hmis:dateCollected'
        xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDNumDateCollected = 'hmis:HouseholdID/hmis:IDNum/@hmis:dateCollected'
        xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
        xpHouseholdIDIDStrDateCollected = 'hmis:HouseholdIDIDStr/@hmis:dateCollected'
        xpIsReferral = 'hmis:IsReferral'
        xpIsReferralDateCollected = 'hmis:IsReferral/@hmis:dateCollected'
        xpQuantityOfService = 'hmis:QuantityOfService'
        xpQuantityOfServiceDateCollected = 'hmis:QuantityOfService/@hmis:dateCollected'
        xpQuantityOfServiceMeasure = 'hmis:QuantityOfServiceMeasure'
        xpQuantityOfServiceMeasureDateCollected = 'hmis:QuantityOfServiceMeasure/@hmis:dateCollected'
        xpServiceAIRSCode = 'hmis:ServiceAIRSCode'
        xpServiceAIRSCodeDateCollected = 'hmis:ServiceAIRSCode/@hmis:dateCollected'
        xpServicePeriodStartDate = 'hmis:ServicePeriod/hmis:StartDate'
        xpServicePeriodStartDateDateCollected = 'hmis:ServicePeriod/hmis:StartDate/@hmis:dateCollected'
        xpServicePeriodEndDate = 'hmis:ServicePeriod/hmis:EndDate'
        xpServicePeriodEndDateDateCollected = 'hmis:ServicePeriod/hmis:EndDate/@hmis:dateCollected'
        xpServiceUnit = 'hmis:ServiceUnit'
        xpServiceUnitDateCollected = 'hmis:ServiceUnit/@hmis:dateCollected'
        xpTypeOfService = 'hmis:TypeOfService'
        xpTypeOfServiceDateCollected = 'hmis:TypeOfService/@hmis:dateCollected'
        xpTypeOfServiceOther = 'hmis:TypeOfServiceOther'
        xpTypeOfServiceOtherDateCollected = 'hmis:TypeOfServiceOther/@hmis:dateCollected'
        itemElements = element.xpath(xpServiceEvent, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                fldName = 'service_event_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_event_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_event_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_event_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEventIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'household_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'household_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'household_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'household_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'is_referral'
                self.existence_test_and_add(fldName, item.xpath(xpIsReferral, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'is_referral_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpIsReferralDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'quantity_of_service'
                self.existence_test_and_add(fldName, item.xpath(xpQuantityOfService, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'quantity_of_service_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpQuantityOfServiceDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'quantity_of_service_measure'
                self.existence_test_and_add(fldName, item.xpath(xpQuantityOfServiceMeasure, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'quantity_of_service_measure_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpQuantityOfServiceMeasureDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_airs_code'
                self.existence_test_and_add(fldName, item.xpath(xpServiceAIRSCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_airs_code_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceAIRSCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_period_start_date'
                self.existence_test_and_add(fldName, item.xpath(xpServicePeriodStartDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_period_start_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServicePeriodStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_period_end_date'
                self.existence_test_and_add(fldName, item.xpath(xpServicePeriodEndDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_period_end_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServicePeriodEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'service_unit'
                self.existence_test_and_add(fldName, item.xpath(xpServiceUnit, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'service_unit_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceUnitDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'type_of_service'
                self.existence_test_and_add(fldName, item.xpath(xpTypeOfService, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'type_of_service_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpTypeOfServiceDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                fldName = 'type_of_service_other'
                self.existence_test_and_add(fldName, item.xpath(xpTypeOfServiceOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName = 'type_of_service_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpTypeOfServiceOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, dbobjects.ServiceEvent)

        return

    def shred(self, parse_dict, mapping):
        """Commits the record set to the database"""
        mapped = mapping(parse_dict)
        if mapping.__name__ == 'Household':
            self.household_index_id = mapped.id
        if mapping.__name__ == 'PersonHistorical':
            self.person_historical_index_id = mapped.id
        if mapping.__name__ == 'Person':
            self.person_index_id = mapped.id
            self.site_service_index_id = None
        if mapping.__name__ == 'SiteServiceParticipation':
            self.site_service_index_id = mapped.id
        self.session.commit()
        return

    def existence_test_and_add(self, db_column, query_string, handling):
        """checks that the query actually has a result and adds to dict"""
        if handling == 'no_handling':
            self.persist(db_column, query_string=query_string)
            return True
        else:
            if len(query_string) is not 0 or None:
                if handling == 'attribute_text':
                    self.persist(db_column, query_string[0])
                    return True
                else:
                    if handling == 'text':
                        self.persist(db_column, query_string=query_string[0].text)
                        return True
                    if handling == 'attribute_date':
                        self.persist(db_column, query_string=dateutil.parser.parse(query_string[0]))
                        return True
                    if handling == 'element_date':
                        self.persist(db_column, query_string=dateutil.parser.parse(query_string[0].text))
                        return True
                    print 'need to specify the handling'
                    return False
            else:
                return False
            return

    def persist(self, db_column, query_string):
        self.parse_dict.__setitem__(db_column, query_string)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    return


if __name__ == '__main__':
    sys.exit(main())