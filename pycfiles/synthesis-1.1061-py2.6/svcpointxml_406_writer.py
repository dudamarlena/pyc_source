# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/svcpointxml_406_writer.py
# Compiled at: 2010-12-12 18:24:12
import os.path
from interpretpicklist import Interpretpicklist
import dateutils
from datetime import timedelta, date, datetime
from time import strptime, time
import xmlutilities, logger
from sys import version
from conf import settings
import clsexceptions, dbobjects, fileutils
from writer import Writer
from zope.interface import implements
from sqlalchemy import or_, and_, between
thisVersion = version[0:3]
if float(settings.MINPYVERSION) < float(version[0:3]):
    try:
        import xml.etree.cElementTree as ET
        from xml.etree.ElementTree import Element, SubElement, dump
    except ImportError:
        import xml.etree.ElementTree as ET
        from xml.etree.ElementTree import Element, SubElement

elif thisVersion == '2.4':
    try:
        import cElementTree as ET
        from elementtree.ElementTree import Element, SubElement, dump
    except ImportError:
        import elementtree.ElementTree as ET
        from elementtree.ElementTree import Element, SubElement

else:
    print 'Sorry, please see the minimum requirements to run this Application'
    theError = (1100, 'This application requires Python 2.4 or higher.  You are current using version: %s' % thisVersion, 'import Error XMLDumper.py')
    raise SoftwareCompatibilityError, theError

def buildWorkhistoryAttributes(element):
    element.attrib['date_added'] = datetime.now().isoformat()
    element.attrib['date_effective'] = datetime.now().isoformat()


class SVCPOINTXMLWriter(dbobjects.DatabaseObjects):
    implements(Writer)
    hmis_namespace = 'http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd'
    airs_namespace = 'http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd'
    nsmap = {'hmis': hmis_namespace, 'airs': airs_namespace}
    svcpt_version = '4.06'

    def __init__(self, poutDirectory, processingOptions, debugMessages=None):
        if settings.DEBUG:
            print 'XML File to be dumped to: %s' % poutDirectory
            self.log = logger.Logger(configFile='logging.ini', loglevel=40)
        self.outDirectory = poutDirectory
        self.pickList = Interpretpicklist()
        self.options = processingOptions
        self.errorMsgs = []
        self.iDG = xmlutilities.IDGeneration()
        self.mappedObjects = dbobjects.DatabaseObjects()

    def write(self):
        self.startTransaction()
        self.processXML()
        self.prettify()
        xmlutilities.writeOutXML()
        return True

    def updateReported(self, currentObject):
        try:
            if settings.DEBUG:
                print 'Updating reporting for object: %s' % currentObject.__class__
            currentObject.reported = True
            self.commitTransaction()
        except:
            print "Exception occurred during update the 'reported' flag"

    def prettify(self):
        FileUtilities.indent(self.root_element)

    def dumpErrors(self):
        print 'Error Reporting'
        print '-' * 80
        for row in range(len(self.errorMsgs)):
            print '%s %s' % (row, self.errorMsgs[row])

    def setSysID(self, pSysID):
        self.sysID = pSysID

    def commitTransaction(self):
        self.session.commit()

    def startTransaction(self):
        self.session = self.mappedObjects.session(echo_uow=True)

    def pullConfiguration(self, pExportID):
        source = self.session.query(dbobjects.Source).filter(dbobjects.Source.export_id == pExportID).one()
        self.configurationRec = self.session.query(dbobjects.SystemConfiguration).filter(and_(dbobjects.SystemConfiguration.source_id == source.source_id, dbobjects.SystemConfiguration.processing_mode == settings.MODE)).one()

    def processXML(self):
        if settings.DEBUG:
            print 'Appending XML to Base Record'
        self.SystemID = self.iDG.generateSystemID('system')
        self.root_element = self.createDoc()
        clients = self.createClients(self.root_element)
        if self.options.reported == True:
            Persons = self.session.query(dbobjects.Person).filter(dbobjects.Person.reported == True)
        elif self.options.unreported == True:
            Persons = self.session.query(dbobjects.Person).filter(or_(dbobjects.Person.reported == False, dbobjects.Person.reported == None))
        elif self.options.reported == None:
            Persons = self.session.query(dbobjects.Person)
        Persons = Persons.filter(between(dbobjects.Person.person_id_date_collected, self.options.startDate, self.options.endDate))
        for self.person in Persons:
            export = self.person.fk_person_to_export
            self.pullConfiguration(export.export_id)
            self.updateReported(self.person)
            self.ph = self.person.fk_person_to_person_historical
            self.race = self.person.fk_person_to_races
            self.site_service_part = self.person.fk_person_to_site_svc_part
            information_releases = self.person.fk_person_to_release_of_information
            self.iDG.initializeSystemID(self.person.id)
            self.sysID = self.person.id
            if self.person:
                self.client = self.createClient(clients)
                self.customizeClient(self.client)
                self.customizeClientPersonalIdentifiers(self.client, self.person)
                dynamic_content = self.createDynamicContent(self.client)
                self.customizeDynamicContent(dynamic_content)
            for ssp in self.site_service_part:
                needData = None
                if not ssp == None:
                    Needs = ssp.fk_participation_to_need
                    if Needs:
                        for needRecord in Needs:
                            self.updateReported(needRecord)
                            needs = self.createNeeds(self.client)
                            need = self.createNeed(needs, needRecord)
                            self.customizeNeed(need, needRecord)
                            ServiceEvents = self.session.query(dbobjects.ServiceEvent).filter(dbobjects.ServiceEvent.service_event_idid_num == needRecord.service_event_idid_num)
                            if ServiceEvents:
                                services = self.createServices(need)
                                for serviceRecord in ServiceEvents:
                                    self.updateReported(serviceRecord)
                                    service = self.createService(serviceRecord, services)
                                    self.customizeService(serviceRecord, service)

            if len(information_releases) > 0:
                info_releases = self.createInfo_releases(self.client)
                for self.IR in information_releases:
                    self.updateReported(self.IR)
                    info_release = self.createInfo_release(info_releases)
                    self.customizeInfo_release(info_release)

        if self.options.reported == True:
            site_service_part = self.session.query(dbobjects.SiteServiceParticipation).filter(dbobjects.SiteServiceParticipation.reported == True)
        elif self.options.unreported == True:
            site_service_part = self.session.query(dbobjects.SiteServiceParticipation).filter(or_(dbobjects.SiteServiceParticipation.reported == False, dbobjects.SiteServiceParticipation.reported == None))
        elif self.options.reported == None:
            site_service_part = self.session.query(dbobjects.SiteServiceParticipation)
        site_service_part = site_service_part.filter(between(dbobjects.SiteServiceParticipation.site_service_participation_idid_num_date_collected, self.options.startDate, self.options.endDate))
        entry_exits = self.createEntryExits(self.root_element)
        for EE in site_service_part:
            person = EE.fk_participation_to_person
            export = person.fk_person_to_export
            self.pullConfiguration(export.export_id)
            self.updateReported(EE)
            self.sysID = EE.id
            entry_exit = self.createEntryExit(entry_exits, EE)

        if self.options.reported == True:
            Household = self.session.query(dbobjects.Household).filter(dbobjects.Household.reported == True)
        elif self.options.unreported == True:
            Household = self.session.query(dbobjects.Household).filter(or_(dbobjects.Household.reported == False, dbobjects.Household.reported == None))
        elif self.options.reported == None:
            Household = self.session.query(dbobjects.Household)
        Household = Household.filter(between(dbobjects.Household.household_id_num_date_collected, self.options.startDate, self.options.endDate))
        if Household != None and Household.count() > 0:
            households = self.createHouseholds(self.root_element)
            for self.eachHouse in Household:
                self.updateReported(self.eachHouse)
                Members = self.eachHouse.fk_household_to_members
                household = self.createHousehold(households)
                self.customizeHousehold(household)
                if len(Members) > 0:
                    members = self.createMembers(household)
                    for eachMember in Members:
                        self.updateReported(eachMember)
                        member = self.createMember(members)
                        self.customizeMember(member, eachMember)

        return

    def createDoc(self):
        root_element = ET.Element('records')
        root_element.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        root_element.attrib['xsi:noNamespaceSchemaLocation'] = 'sp.xsd'
        root_element.attrib['schema_revision'] = '300_108'
        root_element.text = '\n'
        return root_element

    def createClients(self, root_element):
        clients = ET.SubElement(root_element, 'clients')
        return clients

    def createClient(self, clients):
        client = ET.SubElement(clients, 'client')
        return client

    def createEntryExits(self, root_element):
        entry_exits = ET.SubElement(root_element, 'entry_exits')
        return entry_exits

    def customizeClient(self, client):
        keyval = 'client'
        sysID = self.iDG.generateSysID2(keyval, self.sysID)
        recID = self.iDG.generateRecID(keyval)
        client.attrib['record_id'] = recID
        client.attrib['odbid'] = '%s' % self.configurationRec.odbid
        client.attrib['system_id'] = self.person.person_id_unhashed
        client.attrib['date_added'] = datetime.now().isoformat()
        client.attrib['date_updated'] = datetime.now().isoformat()

    def customizeClientForEntryExit(self, client):
        keyval = 'client'
        sysID = self.iDG.generateSysID2(keyval, self.sysID)
        recID = self.iDG.generateRecID(keyval)
        client.attrib['record_id'] = recID
        client.attrib['odbid'] = '%s' % self.configurationRec.odbid
        client.attrib['system_id'] = sysID
        client.attrib['date_added'] = datetime.now().isoformat()
        client.attrib['date_updated'] = datetime.now().isoformat()
        client.tail = '\n'

    def customizeClientPersonalIdentifiers(self, client, recordset):
        if recordset.person_legal_first_name_unhashed != '' and recordset.person_legal_first_name_unhashed != None:
            first_name = ET.SubElement(client, 'first_name')
            first_name.text = recordset.person_legal_first_name_unhashed
        if recordset.person_legal_last_name_unhashed != '' and recordset.person_legal_last_name_unhashed != None:
            last_name = ET.SubElement(client, 'last_name')
            last_name.text = recordset.person_legal_last_name_unhashed
        if recordset.person_legal_middle_name_unhashed != '' and recordset.person_legal_middle_name_unhashed != None:
            mi_initial = ET.SubElement(client, 'mi_initial')
            mi_initial.text = self.fixMiddleInitial(recordset.person_legal_middle_name_unhashed)
        fixedSSN = self.fixSSN(recordset.person_SSN_unhashed)
        if fixedSSN != '' and fixedSSN != None:
            soc_sec_no = ET.SubElement(client, 'soc_sec_no')
            soc_sec_no.text = fixedSSN
            ssn_data_quality = ET.SubElement(client, 'ssn_data_quality')
            ssn_data_quality.text = 'full ssn reported (hud)'
        return

    def customizeClientPersonalIdentifiersForEntryExit(self, client, recordset):
        first_name = ET.SubElement(client, 'first_name')
        first_name.text = recordset['First Name']
        last_name = ET.SubElement(client, 'last_name')
        last_name.text = recordset['Last Name']
        if recordset['MI'] != '':
            mi_initial = ET.SubElement(client, 'mi_initial')
            mi_initial.text = self.fixMiddleInitial(recordset['MI'])
        fixedSSN = self.fixSSN(recordset['SSN'])
        if fixedSSN != '':
            soc_sec_no = ET.SubElement(client, 'soc_sec_no')
            soc_sec_no.text = fixedSSN

    def createAddress_1(self, dynamiccontent):
        address_1 = ET.SubElement(dynamiccontent, 'address_1')
        address_1.attrib['date_added'] = datetime.now().isoformat()
        return address_1

    def createEmergencyContacts(self, dynamiccontent):
        emergencycontacts = ET.SubElement(dynamiccontent, 'emergencycontacts')
        emergencycontacts.attrib['date_added'] = datetime.now().isoformat()
        return emergencycontacts

    def customizeEmergencyContacts(self, emergencycontacts):
        contactsaddress = ET.SubElement(emergencycontacts, 'contactsaddress')
        contactsaddress.attrib['date_added'] = datetime.now().isoformat()
        contactsaddress.attrib['date_effective'] = dateutils.fixDate(self.intakes['IntakeDate'])
        contactsaddress.text = self.intakes['Emergency Address']
        contactscity = ET.SubElement(emergencycontacts, 'contactscity')
        contactscity.attrib['date_added'] = datetime.now().isoformat()
        contactscity.attrib['date_effective'] = dateutils.fixDate(self.intakes['IntakeDate'])
        contactscity.text = self.intakes['Emergency City']
        contactsname = ET.SubElement(emergencycontacts, 'contactsname')
        contactsname.attrib['date_added'] = datetime.now().isoformat()
        contactsname.attrib['date_effective'] = dateutils.fixDate(self.intakes['IntakeDate'])
        contactsname.text = self.intakes['Emergency Contact Name']
        contactsstate = ET.SubElement(emergencycontacts, 'contactsstate')
        contactsstate.attrib['date_added'] = datetime.now().isoformat()
        contactsstate.attrib['date_effective'] = dateutils.fixDate(self.intakes['IntakeDate'])
        contactsstate.text = self.intakes['Emergency State']

    def customizeAddress_1(self, address_1, dbo_address):
        clientscity = ET.SubElement(address_1, 'clientscity')
        clientscity.attrib['date_added'] = datetime.now().isoformat()
        clientscity.attrib['date_effective'] = dateutils.fixDate(dbo_address.city_date_collected)
        clientscity.text = dbo_address.city
        clientsstate = ET.SubElement(address_1, 'clientsstate')
        clientsstate.attrib['date_added'] = datetime.now().isoformat()
        clientsstate.attrib['date_effective'] = dateutils.fixDate(dbo_address.state_date_collected)
        clientsstate.text = dbo_address.state
        clientszip_1 = ET.SubElement(address_1, 'clientszip_1')
        clientszip_1.attrib['date_added'] = datetime.now().isoformat()
        clientszip_1.attrib['date_effective'] = dateutils.fixDate(dbo_address.zipcode_date_collected)
        clientszip_1.text = dbo_address.zipcode

    def createGroupedNeeds(self, base):
        return ET.SubElement(base, 'grouped_needs')

    def createNeeds(self, client):
        needs = ET.SubElement(client, 'needs')
        return needs

    def createNeed(self, needs, needData):
        keyval = 'need'
        sysID = self.iDG.generateSysID(keyval)
        date_for_need_id = needData.need_idid_num
        date_object_format = dateutils.fixDate(needData.need_idid_num_date_collected)
        sysID = sysID + str(date_object_format)
        recID = self.iDG.generateRecID(keyval)
        need = ET.SubElement(needs, 'need')
        need.attrib['record_id'] = recID
        need.attrib['system_id'] = sysID
        need.attrib['date_added'] = datetime.now().isoformat()
        need.attrib['date_updated'] = datetime.now().isoformat()
        return need

    def customizeNeed(self, need, needData):
        global converted_status
        provider_id = ET.SubElement(need, 'provider_id')
        provider_id.text = '%s' % self.configurationRec.providerid
        status = ET.SubElement(need, 'status')
        converted_status = None
        if needData.need_status is not None:
            if needData.need_status == '1':
                converted_status = 'identified'
            elif needData.need_status == '2':
                converted_status = 'closed'
            elif needData.need_status == '3':
                converted_status = 'closed'
            else:
                converted_status = None
        if converted_status is not None:
            status.text = converted_status
        code = ET.SubElement(need, 'code')
        code.attrib['type'] = 'airs taxonomy'
        code.text = needData.taxonomy
        date_set = ET.SubElement(need, 'date_set')
        date_set.text = dateutils.fixDate(needData.need_status_date_collected)
        amount = ET.SubElement(need, 'amount')
        amount.text = '0.00'
        outcome = ET.SubElement(need, 'outcome')
        converted_outcome = None
        if needData.need_status is not None:
            if needData.need_status == '1':
                converted_outcome = 'service pending'
            elif needData.need_status == '2':
                converted_outcome = 'not met'
            elif needData.need_status == '3':
                converted_outcome = 'fully met'
            else:
                converted_outcome = None
        if converted_status is not None:
            outcome.text = converted_outcome
        return

    def customizeNeedClients(self, need_clients):
        need_client = ET.SubElement(need_clients, 'need_client')
        need_client.attrib['system_id'] = '%s' % self.person_need.person_id_unhashed

    def createServices(self, need):
        services = ET.SubElement(need, 'services')
        return services

    def createService(self, serviceRecord, services):
        keyval = 'service'
        recID = self.iDG.generateRecID(keyval)
        service = ET.SubElement(services, 'service')
        service.attrib['record_id'] = recID
        service.attrib['system_id'] = serviceRecord.service_event_idid_num
        service.attrib['date_added'] = datetime.now().isoformat()
        service.attrib['date_updated'] = datetime.now().isoformat()
        return service

    def customizeService(self, serviceRecord, serviceElement):
        code = ET.SubElement(serviceElement, 'code')
        code.attrib['type'] = 'airs taxonomy'
        code.text = serviceRecord.service_airs_code
        service_provided = ET.SubElement(serviceElement, 'service_provided')
        service_provided.text = 'true'
        provide_provider_id = ET.SubElement(serviceElement, 'provide_provider_id')
        provide_provider_id.text = '14'
        provide_start_date = ET.SubElement(serviceElement, 'provide_start_date')
        service_period_start_date = dateutils.fixDate(serviceRecord.service_period_start_date)
        provide_start_date.text = service_period_start_date
        provide_end_date = ET.SubElement(serviceElement, 'provide_end_date')
        service_period_end_date = dateutils.fixDate(serviceRecord.service_period_end_date)
        provide_end_date.text = service_period_end_date
        provider_specific_service_code = ET.SubElement(serviceElement, 'provider_specific_service_code')
        provider_specific_service_code.text = serviceRecord.type_of_service

    def createGoals(self, client):
        goals = ET.SubElement(client, 'goals')
        return goals

    def createGoal(self, goals):
        keyval = 'goal'
        sysID = self.iDG.generateSysID(keyval)
        recID = self.iDG.generateRecID(keyval)
        goal = ET.SubElement(goals, 'goal')
        goal.attrib['record_id'] = recID
        goal.attrib['system_id'] = sysID
        goal.attrib['date_added'] = datetime.now().isoformat()
        goal.attrib['date_updated'] = datetime.now().isoformat()
        return goal

    def customizeGoal(self, goal):
        provider_id = ET.SubElement(goal, 'provider_id')
        date_set = ET.SubElement(goal, 'date_set')
        classification = ET.SubElement(goal, 'classification')
        Type = ET.SubElement(goal, 'type')
        Type.text = 'goaltypePickOption'
        status = ET.SubElement(goal, 'status')
        target_date = ET.SubElement(goal, 'target_date')
        outcome = ET.SubElement(goal, 'outcome')
        outcome_date = ET.SubElement(goal, 'outcome_date')
        projected_followup_date = ET.SubElement(goal, 'projected_followup_date')
        followup_made = ET.SubElement(goal, 'followup_made')
        actual_followup_date = ET.SubElement(goal, 'actual_followup_date')
        followup_outcome = ET.SubElement(goal, 'followup_outcome')

    def createAction_steps(self, goal):
        action_steps = ET.SubElement(goal, 'action_steps')
        return action_steps

    def createAction_step(self, action_steps):
        keyval = 'action_step'
        sysID = self.iDG.generateSysID(keyval)
        recID = self.iDG.generateRecID(keyval)
        action_step = ET.SubElement(action_steps, 'action_step')
        action_step.attrib['record_id'] = recID
        action_step.attrib['system_id'] = sysID
        action_step.attrib['date_added'] = datetime.now().isoformat()
        action_step.attrib['date_updated'] = datetime.now().isoformat()
        return action_step

    def customizeAction_step(self, action_step):
        provider_id = ET.SubElement(action_step, 'provider_id')
        provider_id.text = '%s' % self.configurationRec.providerid
        date_set = ET.SubElement(action_step, 'date_set')
        description = ET.SubElement(action_step, 'description')
        description.text = 'Will take 4k of text (4096 chars). Formatting is preserved.'
        status = ET.SubElement(action_step, 'status')
        target_date = ET.SubElement(action_step, 'target_date')
        outcome = ET.SubElement(action_step, 'outcome')
        outcome_date = ET.SubElement(action_step, 'outcome_date')
        projected_followup_date = ET.SubElement(action_step, 'projected_followup_date')
        followup_made = ET.SubElement(action_step, 'followup_made')
        followup_made.text = 'true'
        actual_followup_date = ET.SubElement(action_step, 'actual_followup_date')
        followup_outcome = ET.SubElement(action_step, 'followup_outcome')

    def customizeHousehold(self, household):
        Type = ET.SubElement(household, 'type')
        Type.text = 'other'
        name = ET.SubElement(household, 'name')
        name.text = 'tok100Type'

    def createEntryExit(self, entry_exits, EE):
        keyval = 'entry_exit'
        sysID = self.iDG.generateSysID(keyval)
        date_for_entry_exit_id = EE.participation_dates_start_date
        entry_exit_date_object_format = dateutils.fixDate(date_for_entry_exit_id)
        sysID = sysID + str(entry_exit_date_object_format)
        recID = self.iDG.generateRecID(keyval)
        entry_exit = ET.SubElement(entry_exits, 'entry_exit')
        entry_exit.attrib['record_id'] = recID
        entry_exit.attrib['system_id'] = sysID
        entry_exit.attrib['odbid'] = '%s' % self.configurationRec.odbid
        entry_exit.attrib['date_added'] = datetime.now().isoformat()
        entry_exit.attrib['date_updated'] = datetime.now().isoformat()
        self.customizeEntryExit(entry_exit, EE)
        return entry_exit

    def createEntryExitMember(self, entry_exit):
        keyval = 'member'
        sysID = self.iDG.generateSysID2(keyval, self.sysID)
        recID = self.iDG.generateRecID(keyval)
        members = ET.SubElement(entry_exit, 'members')
        member = ET.SubElement(members, 'member')
        member.attrib['record_id'] = recID
        member.attrib['system_id'] = sysID
        member.attrib['date_added'] = datetime.now().isoformat()
        member.attrib['date_updated'] = datetime.now().isoformat()
        client_id = ET.SubElement(member, 'client_id')
        keyval = 'client'
        client_id.text = self.iDG.generateSysID2(keyval, self.sysID)
        if dateutils.fixDate(self.outcom['Exit Date']) is not None:
            exit_date = ET.SubElement(member, 'exit_date')
            exit_date.text = dateutils.fixDate(self.outcom['Exit Date'])
        if self.pickList.getValue('EeDestinationPick', str.rstrip(self.outcom['Service Point Destnation Parse'])) != '':
            destination = ET.SubElement(member, 'destination')
            destination.text = self.pickList.getValue('EeDestinationPick', str.rstrip(self.outcom['Service Point Destnation Parse']))
        if self.outcom['Address'] != '' and self.outcom['Client ID'] != '' and self.outcom['Education'] != '' and self.outcom['Partner'] != '':
            notes = ET.SubElement(member, 'notes')
            notes.text = self.formatNotesField(notes.text, 'Address', self.outcom['Address'])
            if settings.DEBUG:
                notes.text = self.formatNotesField(notes.text, 'Client ID:', self.outcom['Client ID'])
            notes.text = self.formatNotesField(notes.text, 'Education', self.outcom['Education'])
            notes.text = self.formatNotesField(notes.text, 'Partner', self.outcom['Partner'])
        return

    def customizeEntryExit(self, entry_exit, EE):
        type = ET.SubElement(entry_exit, 'type')
        type.text = 'hud-40118'
        provider_id = ET.SubElement(entry_exit, 'provider_id')
        provider_id.text = '%s' % self.configurationRec.providerid
        if EE.participation_dates_start_date != '' and EE.participation_dates_start_date != None:
            entry_date = ET.SubElement(entry_exit, 'entry_date')
            entry_date.text = dateutils.fixDate(EE.participation_dates_start_date)
            EEperson = EE.fk_site_svc_part_to_person
            mbrs = self.createMembers(entry_exit)
            if EEperson.person_id_unhashed != None:
                mbr = self.createMemberEE(mbrs)
                self.customizeMemberEE(mbr, EE, EEperson)
        return

    def createInfo_releases(self, client):
        info_releases = ET.SubElement(client, 'info_releases')
        return info_releases

    def createInfo_release(self, info_releases):
        keyval = 'info_release'
        sysID = self.iDG.generateSysID(keyval)
        recID = self.iDG.generateRecID(keyval)
        info_release = ET.SubElement(info_releases, 'info_release')
        info_release.attrib['record_id'] = recID
        info_release.attrib['system_id'] = sysID
        info_release.attrib['date_added'] = datetime.now().isoformat()
        info_release.attrib['date_updated'] = datetime.now().isoformat()
        return info_release

    def customizeInfo_release(self, info_release):
        provider_id = ET.SubElement(info_release, 'provider_id')
        provider_id.text = '%s' % self.configurationRec.providerid
        date_started = ET.SubElement(info_release, 'date_started')
        date_started.text = self.IR.start_date
        date_ended = ET.SubElement(info_release, 'date_ended')
        date_ended.text = self.IR.end_date
        permission = ET.SubElement(info_release, 'permission')
        permission.text = self.IR.release_granted
        documentation = ET.SubElement(info_release, 'documentation')
        documentation.text = self.pickList.getValue('ROIDocumentationPickOption', str(self.IR.documentation))
        witness = ET.SubElement(info_release, 'witness')
        witness.text = 'tok50Type'

    def createDynamicContent(self, client):
        dynamic_content = ET.SubElement(client, 'dynamic_content')
        return dynamic_content

    def customizeDynamicContent(self, dynamiccontent):
        for ph in self.ph:
            self.updateReported(ph)
            dbo_address = ph.fk_person_historical_to_person_address
            dbo_veteran = ph.fk_person_historical_to_veteran
            if ph.hud_homeless != '' and ph.hud_homeless != None:
                isclienthomeless = ET.SubElement(dynamiccontent, 'isclienthomeless')
                isclienthomeless.attrib['date_added'] = datetime.now().isoformat()
                isclienthomeless.attrib['date_effective'] = dateutils.fixDate(ph.hud_homeless_date_collected)
                if ph.hud_homeless == '1':
                    isclienthomeless.text = 'true'
                if ph.hud_homeless == '' or ph.hud_homeless == None:
                    isclienthomeless.text = 'false'
            if ph.physical_disability != '' and ph.physical_disability != None:
                hud_disablingcondition = ET.SubElement(dynamiccontent, 'hud_disablingcondition')
                hud_disablingcondition.attrib['date_added'] = datetime.now().isoformat()
                hud_disablingcondition.attrib['date_effective'] = dateutils.fixDate(ph.physical_disability_date_collected)
                hud_disablingcondition.text = self.pickList.getValue('ENHANCEDYESNOPickOption', str.strip(ph.physical_disability.upper()))
            if ph.hours_worked_last_week != '' and ph.hours_worked_last_week != None:
                hud_hrsworkedlastweek = ET.SubElement(dynamiccontent, 'hud_hrsworkedlastweek')
                hud_hrsworkedlastweek.attrib['date_added'] = datetime.now().isoformat()
                hud_hrsworkedlastweek.attrib['date_effective'] = dateutils.fixDate(ph.hours_worked_last_week_date_collected)
                hud_hrsworkedlastweek.text = str.strip(ph.hours_worked_last_week)
            zipcode = ''
            if len(dbo_address) > 0:
                if dbo_address[0].zip_quality_code == 1:
                    zipcode = dbo_address[0].zipcode
                    if zipcode != '':
                        if zipcode != None:
                            hud_zipcodelastpermaddr = ET.SubElement(dynamiccontent, 'hud_zipcodelastpermaddr')
                            hud_zipcodelastpermaddr.attrib['date_added'] = datetime.now().isoformat()
                            hud_zipcodelastpermaddr.attrib['date_effective'] = dateutils.fixDate(dbo_address[0].zipcode_date_collected)
                            hud_zipcodelastpermaddr.text = zipcode
                if len(dbo_address) > 0:
                    if dbo_address[0].line1 != '':
                        self.updateReported(dbo_address[0])
                        address_2 = ET.SubElement(dynamiccontent, 'address_2')
                        address_2.attrib['date_added'] = datetime.now().isoformat()
                        address_2.attrib['date_effective'] = dateutils.fixDate(dbo_address[0].line1_date_collected)
                        address_2.text = dbo_address[0].line1
                if str(ph.substance_abuse_problem) != '' and ph.substance_abuse_problem != None:
                    usealcoholordrugs = ET.SubElement(dynamiccontent, 'usealcoholordrugs')
                    usealcoholordrugs.attrib['date_added'] = datetime.now().isoformat()
                    usealcoholordrugs.attrib['date_effective'] = dateutils.fixDate(ph.substance_abuse_problem_date_collected)
                    usealcoholordrugs.text = 'true'
                if len(self.site_service_part) > 0:
                    for ssp in self.site_service_part:
                        self.updateReported(ssp)
                        vet = ssp.veteran_status
                        if vet != '' and vet != None:
                            veteran = ET.SubElement(dynamiccontent, 'veteran')
                            veteran.text = self.pickList.getValue('ENHANCEDYESNOPickOption', str(vet))
                            veteran.attrib['date_added'] = datetime.now().isoformat()
                            veteran.attrib['date_effective'] = dateutils.fixDate(ssp.veteran_status_date_collected)
                            break

                if len(dbo_veteran) > 0:
                    hud_militarybranchinfo = None
                    for dbv in dbo_veteran:
                        self.updateReported(dbv)
                        branch = dbv.military_branch
                        if str(branch) != '' and dbv.military_branch != None:
                            if hud_militarybranchinfo == None:
                                hud_militarybranchinfo = ET.SubElement(dynamiccontent, 'hud_militarybranchinfo')
                                hud_militarybranchinfo.attrib['date_added'] = datetime.now().isoformat()
                        militarybranch = ET.SubElement(hud_militarybranchinfo, 'militarybranch')
                        militarybranch.attrib['date_added'] = datetime.now().isoformat()
                        militarybranch.attrib['date_effective'] = dateutils.fixDate(dbv.military_branch_date_collected)
                        militarybranch.text = self.pickList.getValue('MILITARYBRANCHPickOption', str(branch))

                homelessPickOption = []
                lookups = [
                 'Addiction',
                 'Divorce',
                 'Domestic Violence',
                 'Evicted within past week',
                 'Family-Personal Illness',
                 'Jail/Prison',
                 'Moved to seek work',
                 'Physical-Mental Disability',
                 'Unable to pay rent-mortgage',
                 'Other']
                if str(ph.hud_homeless) != '' and ph.hud_homeless != None:
                    primaryreasonforhomle = ET.SubElement(dynamiccontent, 'primaryreasonforhomle')
                    primaryreasonforhomle.attrib['date_added'] = datetime.now().isoformat()
                    primaryreasonforhomle.attrib['date_effective'] = dateutils.fixDate(ph.hud_homeless_date_collected)
                    primaryreasonforhomle.text = 'Other'
            elif len(dbo_address) > 0:
                if dbo_address[0].line1 != '':
                    address_1 = self.createAddress_1(dynamiccontent)
                    self.customizeAddress_1(address_1, dbo_address[0])
                if str(dbo_address[0].zipcode) != '' and not dbo_address[0].zipcode == None:
                    address_1 = self.createAddress_1(dynamiccontent)
                    self.customizeAddress_1(address_1, dbo_address[0])

        if str(ph.currently_employed) != '' and not ph.currently_employed == None:
            unemployed = ET.SubElement(dynamiccontent, 'unemployed')
            unemployed.attrib['date_added'] = datetime.now().isoformat()
            unemployed.attrib['date_effective'] = dateutils.fixDate(ph.currently_employed_date_collected)
            if ph.currently_employed == 1:
                unemployed.text = 'true'
            else:
                unemployed.text = 'false'
            if str(ph.total_income) != '' and not ph.total_income == None:
                monthlyincome = ET.SubElement(dynamiccontent, 'hud_totalmonthlyincome')
                monthlyincome.attrib['date_added'] = datetime.now().isoformat()
                monthlyincome.attrib['date_effective'] = dateutils.fixDate(ph.total_income_date_collected)
                monthlyincome.text = ph.total_income
            if str(ph.physical_disability) != '' and not ph.physical_disability == None:
                disabilities_1 = ET.SubElement(dynamiccontent, 'disabilities_1')
                disabilities_1.attrib['date_added'] = datetime.now().isoformat()
                self.customizeDisabilities_1(disabilities_1, ph)
        if self.person.person_gender_unhashed != '' and self.person.person_gender_unhashed != None:
            svpprofgender = ET.SubElement(dynamiccontent, 'svpprofgender')
            svpprofgender.attrib['date_added'] = datetime.now().isoformat()
            svpprofgender.attrib['date_effective'] = dateutils.fixDate(self.person.person_gender_date_collected)
            svpprofgender.text = self.pickList.getValue('SexPick', self.person.person_gender_unhashed)
        if self.person.person_date_of_birth_unhashed != '' and self.person.person_date_of_birth_unhashed != None:
            svpprofdob = ET.SubElement(dynamiccontent, 'svpprofdob')
            svpprofdob.attrib['date_added'] = datetime.now().isoformat()
            svpprofdob.attrib['date_effective'] = dateutils.fixDate(self.person.person_date_of_birth_date_collected)
            svpprofdob.text = dateutils.fixDate(self.person.person_date_of_birth_unhashed)
        if len(self.race) > 0:
            race = self.race[0].race_unhashed
            self.updateReported(self.race[0])
            if race != '' and race != None:
                if self.pickList.getValue('RacePick', str(race)) != '':
                    svpprofrace = ET.SubElement(dynamiccontent, 'svpprofrace')
                    svpprofrace.attrib['date_added'] = datetime.now().isoformat()
                    svpprofrace.attrib['date_effective'] = dateutils.fixDate(self.race[0].race_date_collected)
                    svpprofrace.text = self.pickList.getValue('RacePick', str(race))
        ethnicity = self.person.person_ethnicity_unhashed
        if ethnicity != '' and ethnicity != None:
            svpprofeth = ET.SubElement(dynamiccontent, 'svpprofeth')
            svpprofeth.attrib['date_added'] = datetime.now().isoformat()
            svpprofeth.attrib['date_effective'] = dateutils.fixDate(self.person.person_ethnicity_date_collected)
            svpprofeth.text = self.pickList.getValue('EthnicityPick', str(ethnicity))
        priorresidence = ph.prior_residence
        if priorresidence != '' and priorresidence != None:
            typeoflivingsituation = ET.SubElement(dynamiccontent, 'typeoflivingsituation')
            typeoflivingsituation.attrib['date_added'] = datetime.now().isoformat()
            typeoflivingsituation.attrib['date_effective'] = dateutils.fixDate(ph.prior_residence_date_collected)
            typeoflivingsituation.text = self.pickList.getValue('LIVINGSITTYPESPickOption', str(priorresidence))
        return

    def customizeDisabilities_1(self, disabilities_1, ph):
        noteondisability = ET.SubElement(disabilities_1, 'noteondisability')
        noteondisability.attrib['date_added'] = datetime.now().isoformat()
        noteondisability.attrib['date_effective'] = dateutils.fixDate(ph.physical_disability_date_collected)
        noteondisability.text = ph.physical_disability

    def createWorkhistory(self, dynamiccontent):
        workhistory = ET.SubElement(dynamiccontent, 'workhistory')
        workhistory.attrib['date_added'] = datetime.now().isoformat()
        return workhistory

    def customizeWorkhistory(self, workhistory):
        if self.intakes['EmployerName'] != '':
            employername = ET.SubElement(workhistory, 'employername')
            buildWorkhistoryAttributes(employername)
            employername.text = self.intakes['EmployerName']

    def createHouseholds(self, records):
        households = ET.SubElement(records, 'households')
        return households

    def createHousehold(self, households):
        keyval = 'household'
        sysID = self.iDG.generateSysID(keyval)
        recID = self.iDG.generateRecID(keyval)
        household = ET.SubElement(households, 'household')
        household.attrib['record_id'] = recID
        household.attrib['system_id'] = sysID
        household.attrib['date_added'] = datetime.now().isoformat()
        household.attrib['date_updated'] = datetime.now().isoformat()
        return household

    def createMembers(self, household):
        members = ET.SubElement(household, 'members')
        return members

    def createMember(self, members):
        keyval = 'member'
        recID = self.iDG.generateRecID(keyval)
        member = ET.SubElement(members, 'member')
        member.attrib['record_id'] = recID
        member.attrib['date_added'] = datetime.now().isoformat()
        member.attrib['date_updated'] = datetime.now().isoformat()
        member.attrib['system_id'] = self.iDG.generateSysID2('service', self.sysID)
        return member

    def createMemberEE(self, members):
        member = ET.SubElement(members, 'member')
        keyval = 'member'
        recID = self.iDG.generateRecID(keyval)
        member.attrib['record_id'] = recID
        member.attrib['date_added'] = datetime.now().isoformat()
        member.attrib['date_updated'] = datetime.now().isoformat()
        member.attrib['system_id'] = self.iDG.generateSysID2('service', self.sysID)
        return member

    def customizeMember(self, member_element, member):
        client_id = ET.SubElement(member_element, 'client_id')
        if member.person_id_unhashed != '':
            client_id.text = member.person_id_unhashed
            date_entered = ET.SubElement(member_element, 'date_entered')
            date_entered.text = dateutils.fixDate(member.person_id_unhashed_date_collected)
        else:
            client_id.text = member.person_id_hashed
            date_entered = ET.SubElement(member_element, 'date_entered')
            date_entered.text = dateutils.fixDate(member.person_id_hashed_date_collected)
        if member.relationship_to_head_of_household == '':
            head_of_household = ET.SubElement(member_element, 'head_of_household')
            head_of_household.text = 'true'
        else:
            relationship = ET.SubElement(member_element, 'relationship')
            relationship.text = self.pickList.getValue('RelationshipToHeadOfHousehold', str(member.relationship_to_head_of_household))

    def customizeMemberEE(self, EEMember_element, site_service_participation, member):
        client_id = ET.SubElement(EEMember_element, 'client_id')
        if member.person_id_unhashed != '':
            client_id.text = member.person_id_unhashed
        else:
            client_id.text = member.person_id_hashed
        entry_date = ET.SubElement(EEMember_element, 'entry_date')
        entry_date.text = dateutils.fixDate(site_service_participation.participation_dates_start_date)
        exit_date = ET.SubElement(EEMember_element, 'exit_date')
        exit_date.text = dateutils.fixDate(site_service_participation.participation_dates_end_date)
        reason_leaving = ET.SubElement(EEMember_element, 'reason_leaving')
        reason_leaving.text = ''
        reason_leaving_other = ET.SubElement(EEMember_element, 'reason_leaving_other')
        reason_leaving_other.text = ''
        destination = ET.SubElement(EEMember_element, 'destination')
        destination.text = site_service_participation.destination
        destination_other = ET.SubElement(EEMember_element, 'destination_other')
        destination_other.text = site_service_participation.destination_other
        notes = ET.SubElement(EEMember_element, 'notes')
        notes.text = ''
        tenure = ET.SubElement(EEMember_element, 'tenure')
        tenure.text = site_service_participation.destination_tenure
        subsidy = ET.SubElement(EEMember_element, 'subsidy')
        subsidy.text = ''

        def current_picture(node):
            """ Internal function.  Debugging aid for the export module."""
            if settings.DEBUG:
                print 'Current XML Picture is'
                print '======================\n' * 2
                dump(node)
                print '======================\n' * 2

    def formatNotesField(self, existingNotesData, formatName, newNotesData):
        if existingNotesData == None:
            existingNotesData = ''
            formatData = ''
        else:
            formatData = '\r\n'
        if newNotesData != 'None':
            newData = '%s %s [%s] %s' % (existingNotesData, formatData, formatName, newNotesData)
        else:
            newData = existingNotesData
        return newData

    def calcHourlyWage(self, monthlyWage):
        if monthlyWage != '':
            if monthlyWage.strip().isdigit():
                if float(monthlyWage) > 5000.0:
                    hourlyWage = float(monthlyWage) / 160.0
                else:
                    hourlyWage = float(monthlyWage)
            else:
                hourlyWage = 0.0
        else:
            hourlyWage = 0.0
        if settings.DEBUG:
            print str(round(hourlyWage, 2))
        return str(round(hourlyWage, 2))

    def fixMiddleInitial(self, middle_initial):
        fixed_middle_initial = str.lstrip(str.upper(middle_initial))[0]
        return fixed_middle_initial

    def fixSSN(self, incomingSSN):
        originalSSN = incomingSSN
        if incomingSSN == '' or incomingSSN == None:
            return incomingSSN
        else:
            dashCount = incomingSSN.count('-')
            if dashCount > 0:
                if dashCount == 2:
                    if settings.DEBUG:
                        self.debugMessages.log('incoming SSN is correctly formatted: %s\n' % incomingSSN)
                    return incomingSSN
                incomingSSN = string.replace(incomingSSN, '-', '')
                if len(incomingSSN) < 9:
                    theError = (1020, 'Data format error discovered in trying to cleanup incoming SSN: %s, original SSN: %s' % (incomingSSN, originalSSN))
                    if settings.DEBUG:
                        self.debugMessages.log('>>>> Incoming SSN is INcorrectly formatted.  Original SSN from input file is: %s and Attempted cleaned up SSN is: %s\n' % (originalSSN, incomingSSN))
                    raise dataFormatError, theError
            if settings.DEBUG:
                self.debugMessages.log('incoming SSN is INcorrectly formatted: %s.  Reformatting to: %s\n' % (incomingSSN, '%s-%s-%s' % (incomingSSN[0:3], incomingSSN[3:5], incomingSSN[5:10])))
            return '%s-%s-%s' % (incomingSSN[0:3], incomingSSN[3:5], incomingSSN[5:10])


if __name__ == '__main__':
    vld = SVCPOINTXMLWriter('.')
    vld.write()