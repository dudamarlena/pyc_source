# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/hmisxml30writer.py
# Compiled at: 2011-01-03 14:39:55
from clsexceptions import SoftwareCompatibilityError
import os.path, dbobjects, xmlutilities
from sys import version
from conf import settings
from datetime import datetime
from sqlalchemy import or_, and_, between
thisVersion = version[0:3]
if float(settings.MINPYVERSION) < float(thisVersion):
    try:
        import xml.etree.ElementTree as ET
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

class HMISXMLWriter(dbobjects.DatabaseObjects):
    hmis_namespace = 'http://www.hmis.info/schema/3_0/HUD_HMIS.xsd'
    airs_namespace = 'http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd'
    nsmap = {'hmis': hmis_namespace, 'airs': airs_namespace}

    def __init__(self, poutDirectory, processingOptions, debug=False):
        self.errorMsgs = []
        self.iDG = xmlutilities.IDGeneration()
        self.debug = debug
        self.outDirectory = poutDirectory
        self.mappedObjects = dbobjects.DatabaseObjects()
        self.options = processingOptions

    def write(self):
        self.startTransaction()
        self.processXML()
        self.prettify()
        xmlutilities.writeOutXML(self)
        return True

    def prettify(self):
        xmlutilities.indent(self.root_element)

    def startTransaction(self):
        self.session = self.mappedObjects.session(echo_uow=True)

    def createDoc(self):
        root_element = ET.Element('hmis:Sources')
        root_element.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        root_element.attrib['xmlns:airs'] = 'http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd'
        root_element.attrib['xmlns:hmis'] = 'http://www.hmis.info/schema/3_0/HUD_HMIS.xsd'
        root_element.attrib['xsi:schemaLocation'] = 'http://www.hmis.info/schema/3_0/HUD_HMIS.xsd http://www.hmis.info/schema/3_0/HUD_HMIS.xsd'
        root_element.attrib['hmis:version'] = '3.0'
        root_element.text = '\n'
        return root_element

    def createOtherNames(self, xml):
        othernames = ET.SubElement(xml, 'hmis:OtherNames')
        return othernames

    def customizeOtherNames(self, xml):
        attributes = []
        elements = [
         'OtherFirstName',
         'OtherMiddleName',
         'OtherLastName',
         'OtherSuffix']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def createPersonHistorical(self, xml):
        personhistorical = ET.SubElement(xml, 'hmis:PersonHistorical')
        return personhistorical

    def customizePersonHistorical(self, xml):
        attributes = []
        elements = [
         'PersonHistoricalID',
         'SiteServiceID',
         'ChildEnrollmentStatus',
         'ChronicHealthCondition',
         'CurrentlyInSchool',
         'ContactsMade',
         'Degree',
         'Destinations',
         'DisablingCondition',
         'DevelopmentalDisability',
         'DomesticViolence',
         'Employment',
         'EngagedDate',
         'HealthStatus',
         'HighestSchoolLevel',
         'HIVAIDSStatus',
         'HousingStatus',
         'HUDChronicHomeless',
         'HUDHomelessEpisodes',
         'IncomeLast30Days',
         'IncomeAndSources',
         'IncomeTotalMonthly',
         'LengthOfStayAtPriorResidence',
         'MentalHealthProblem',
         'NonCashBenefitsLast30Days',
         'NonCashBenefits',
         'PersonAddress',
         'PersonEmail',
         'PersonPhoneNumber',
         'PhysicalDisability',
         'Pregnancy',
         'PriorResidence',
         'SubstanceAbuseProblem',
         'Veteran',
         'VocationalTraining']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        se = theElements['IncomeAndSources']
        subElements = ['IncomeSourceCode', 'IncomeSourceOther']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'HIVAIDSStatus'
        se = theElements[elementName]
        subElements = ['HasHIVAIDS', 'ReceiveHIVAIDSServices']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'MentalHealthProblem'
        se = theElements[elementName]
        subElements = ['HasMentalHealthProblem', 'MentalHealthIndefinite', 'ReceiveMentalHealthServices']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'NonCashBenefits'
        se = theElements[elementName]
        NonCashBenefit = self.createSubElement(se, 'hmis', 'NonCashBenefit')
        subElements = [
         'NonCashBenefitID']
        self.customizeSubElements(NonCashBenefit, 'hmis', subElements, data=[])
        elementName = 'PersonAddress'
        se = theElements[elementName]
        subElements = ['AddressPeriod', 'PreAddressLine', 'Line1', 'Line2', 'City', 'County', 'State', 'ZIPCode', 'Country', 'IsLastPermanentZIP', 'ZIPQualityCode']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'PersonEmail'
        se = theElements[elementName]
        elementName = 'PersonEmail'
        se = theElements[elementName]
        elementName = 'PhysicalDisability'
        se = theElements[elementName]
        subElements = ['HasPhysicalDisability', 'ReceivePhysicalDisabilityServices']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'Pregnancy'
        se = theElements[elementName]
        subElements = ['PregnancyID', 'PregnancyStatus', 'DueDate']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'PriorResidence'
        se = theElements[elementName]
        subElements = ['PriorResidenceID', 'PriorResidenceCode', 'PriorResidenceOther']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'SubstanceAbuseProblem'
        se = theElements[elementName]
        subElements = ['HasSubstanceAbuseProblem', 'SubstanceAbuseIndefinite', 'ReceiveSubstanceAbuseServices']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'Veteran'
        se = theElements[elementName]
        subElements = ['MilitaryBranches', 'MilitaryServiceDuration', 'ServedInWarZone', 'ServiceEra', 'VeteranStatus', 'WarZonesServed']
        self.customizeSubElements(se, 'hmis', subElements, data=[])
        elementName = 'VocationalTraining'
        se = theElements[elementName]
        return xml

    def createRace(self, xml):
        race = ET.SubElement(xml, 'hmis:Race')
        return race

    def customizeRace(self, xml):
        pass

    def createReleaseOfInformation(self, xml):
        releaseofinformation = ET.SubElement(xml, 'hmis:ReleaseOfInformation')
        return releaseofinformation

    def customizeReleaseOfInformation(self, xml):
        attributes = []
        elements = [
         'ReleaseOfInformationID',
         'SiteServiceID',
         'Documentation',
         'EffectivePeriod',
         'ReleaseGranted']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def createServiceEvent(self, xml):
        serviceevent = ET.SubElement(xml, 'hmis:ServiceEvent')
        return serviceevent

    def customizeServiceEvent(self, xml):
        attributes = []
        elements = [
         'ServiceEventID',
         'SiteServiceID',
         'HouseholdID',
         'FundingSources',
         'IsReferral',
         'QuantityOfServiceEvent',
         'QuantityOfServiceEventUnit',
         'ServiceEventAIRSCode',
         'ServiceEventEffectivePeriod',
         'ServiceEventProvisionDate',
         'ServiceEventRecordedDate',
         'ServiceEventNotes',
         'ServiceEventIndFam']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def createSiteServiceParticipation(self, xml):
        siteserviceparticipation = ET.SubElement(xml, 'hmis:SiteServiceParticipation')
        return siteserviceparticipation

    def customizeSiteServiceParticipation(self, xml):
        attributes = []
        elements = [
         'SiteServiceParticipationID',
         'SiteServiceID',
         'HouseholdID',
         'Need',
         'ParticipationDates',
         'PersonHistorical',
         'ReasonsForLeaving',
         'ServiceEvent']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def createTaxonomy(self, xml):
        taxonomy = ET.SubElement(xml, 'hmis:Taxonomy')
        return taxonomy

    def customizeTaxonomy(self, xml, taxonomyData=[]):
        elementCounter = 0
        taxonomyElement = ET.SubElement(xml, 'airs:Taxonomy')
        for taxonomyRow in taxonomyData:
            if elementCounter == 2:
                elementCounter = 0
                taxonomyElement = ET.SubElement(xml, 'airs:Taxonomy')
            taxonomySubElement = ET.SubElement(taxonomyElement, 'airs:Code')
            taxonomySubElement.text = taxonomyRow.code
            elementCounter += 1

    def createPerson(self, records):
        person = ET.SubElement(records, 'hmis:Person')
        return person

    def customizePerson(self, xml):
        attributes = []
        elements = [
         'PersonID',
         'DateOfBirth',
         'Ethnicity',
         'Gender',
         'LegalFirstName',
         'LegalLastName',
         'LegalMiddleName',
         'LegalSuffix']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def customizePersonSSN(self, xml):
        pass

    def createHousehold(self, records):
        household = ET.SubElement(records, 'hmis:Household')
        return household

    def customizeHousehold(self, xml):
        attributes = []
        elements = [
         'HouseholdID',
         'HeadOfHouseholdID']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def generateElements(self, xml, namespaceString, elementDictionary):
        theElements = {}
        for element in elementDictionary:
            theElements[element] = ET.SubElement(xml, namespaceString + ':%s' % element)

        return theElements

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
        return member

    def customizeMember(self, member):
        client_id = ET.SubElement(member, 'client_id')
        date_entered = ET.SubElement(member, 'date_entered')
        date_ended = ET.SubElement(member, 'date_ended')
        head_of_household = ET.SubElement(member, 'head_of_household')
        relationship = ET.SubElement(member, 'relationship')
        xpRegion = 'hmis:Region'
        xpRegionIDIDNum = 'hmis:RegionID/hmis:IDNum'
        xpRegionIDIDStr = 'hmis:RegionID/hmis:IDStr'
        xpSiteServiceID = 'hmis:SiteServiceID'
        xpRegionType = 'hmis:RegionType'
        xpRegionTypeDateCollected = 'hmis:RegionType/@hmis:dateCollected'
        xpRegionTypeDateEffective = 'hmis:RegionType/@hmis:dateEffective'
        xpRegionTypeDataCollectionStage = 'hmis:RegionType/@hmis:dataCollectionStage'
        xpRegionDescription = 'hmis:RegionDescription'
        xpRegionDescriptionDateCollected = 'hmis:RegionDescription/@hmis:dateCollected'
        xpRegionDescriptionDateEffective = 'hmis:RegionDescription/@hmis:dateEffective'
        xpRegionDescriptionDataCollectionStage = 'hmis:RegionDescription/@hmis:dataCollectionStage'

    def createRegion(self, records):
        region = ET.SubElement(records, 'region')
        return region
        xpAgency = 'hmis:Agency'
        xpAgencyDelete = '@hmis:Delete'
        xpAgencyDeleteOccurredDate = '@hmis:DeleteOccurredDate'
        xpAgencyDeleteEffective = '@hmis:DeleteEffective'
        xpAirsKey = 'airs:Key'
        xpAirsName = 'airs:Name'
        xpAgencyDescription = 'airs:AgencyDescription'
        xpIRSStatus = 'airs:IRSStatus'
        xpSourceOfFunds = 'airs:SourceOfFunds'
        xpRecordOwner = '@hmis:RecordOwner'
        xpFEIN = '@hmis:FEIN'
        xpYearInc = '@hmis:YearInc'
        xpAnnualBudgetTotal = '@hmis:AnnualBudgetTotal'
        xpLegalStatus = '@hmis:LegalStatus'
        xpExcludeFromWebsite = '@hmis:ExcludeFromWebsite'
        xpExcludeFromDirectory = '@hmis:ExcludeFromDirectory'

    def createAgency_old2(self, records):
        agency = ET.SubElement(records, 'agency')
        return agency

    def createAgency_old(self, records):
        xpSite = 'airs:Site'
        xpSiteDeleteOccurredDate = '@airs:DeleteOccurredDate'
        xpSiteDeleteEffective = '@airs:DeleteEffective'
        xpSiteDelete = '@airs:Delete'
        xpKey = 'airs:Key'
        xpName = 'airs:Name'
        xpSiteDescription = 'airs:SiteDescription'
        xpPhysicalAddressPreAddressLine = 'airs:PhysicalAddress/airs:PreAddressLine'
        xpPhysicalAddressLine1 = 'airs:PhysicalAddress/airs:Line1'
        xpPhysicalAddressLine2 = 'airs:PhysicalAddress/airs:Line2'
        xpPhysicalAddressCity = 'airs:PhysicalAddress/airs:City'
        xpPhysicalAddressCounty = 'airs:PhysicalAddress/airs:County'
        xpPhysicalAddressState = 'airs:PhysicalAddress/airs:State'
        xpPhysicalAddressZipCode = 'airs:PhysicalAddress/airs:ZipCode'
        xpPhysicalAddressCountry = 'airs:PhysicalAddress/airs:Country'
        xpPhysicalAddressReasonWithheld = 'airs:PhysicalAddress/airs:ReasonWithheld'
        xpPhysicalAddressConfidential = 'airs:PhysicalAddress/@airs:Confidential'
        xpPhysicalAddressDescription = 'airs:PhysicalAddress/@airs:Description'
        xpMailingAddressPreAddressLine = 'airs:MailingAddress/airs:PreAddressLine'
        xpMailingAddressLine1 = 'airs:MailingAddress/airs:Line1'
        xpMailingAddressLine2 = 'airs:MailingAddress/airs:Line2'
        xpMailingAddressCity = 'airs:MailingAddress/airs:City'
        xpMailingAddressCounty = 'airs:MailingAddress/airs:County'
        xpMailingAddressState = 'airs:MailingAddress/airs:State'
        xpMailingAddressZipCode = 'airs:MailingAddress/airs:ZipCode'
        xpMailingAddressCountry = 'airs:MailingAddress/airs:Country'
        xpMailingAddressReasonWithheld = 'airs:MailingAddress/airs:ReasonWithheld'
        xpMailingAddressConfidential = 'airs:MailingAddress/@airs:Confidential'
        xpMailingAddressDescription = 'airs:MailingAddress/@airs:Description'
        xpNoPhysicalAddressDescription = 'airs:NoPhysicalAddress/airs:Description'
        xpNoPhysicalAddressExplanation = 'airs:NoPhysicalAddress/airs:Explanation'
        xpDisabilitiesAccess = 'airs:DisabilitiesAccess'
        xpPhysicalLocationDescription = 'airs:PhysicalLocationDescription'
        xpBusServiceAccess = 'airs:BusServiceAccess'
        xpPublicAccessToTransportation = 'airs:PublicAccessToTransportation'
        xpYearInc = 'airs:YearInc'
        xpAnnualBudgetTotal = 'airs:AnnualBudgetTotal'
        xpLegalStatus = 'airs:LegalStatus'
        xpExcludeFromWebsite = 'airs:ExcludeFromWebsite'
        xpExcludeFromDirectory = 'airs:ExcludeFromDirectory'
        xpAgencyKey = 'airs:AgencyKey'

    def createSite_AKA(self, xml):
        aka = ET.SubElement(xml, 'airs:AKA')
        return aka

    def customizeSite_AKA(self, xml):
        attributes = []
        elements = [
         'Name',
         'Confidential',
         'Description']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'airs', elements)
        return xml

    def createSite(self, xml):
        site = ET.SubElement(xml, 'hmis:Site')
        return site

    def customizeSite(self, xml):
        attributes = []
        elements = [
         'Key',
         'Name',
         'SiteDescription']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'airs', elements)
        return xml

    def customizeDOW(self, xml, data=[]):
        DsOW = [
         'Sunday',
         'Monday',
         'Tuesday',
         'Wednesday',
         'Thursday',
         'Friday',
         'Saturday']
        for DOW in DsOW:
            elementDOW = self.createSiteService_TimeOpen_DayOfWeek(xml, DOW)
            self.customizeSiteService_TimeOpen_DayOfWeek(elementDOW)

    def manageSiteService(self, export):
        siteservice = self.createSiteService(export)
        siteservice = self.customizeSiteService(siteservice, siteServiceData=None)
        phone = self.createSiteServicePhone(siteservice)
        phone = self.customizeSiteServicePhone(phone)
        timeopen = self.createSiteService_TimeOpen(siteservice)
        timeopen = self.customizeSiteService_TimeOpen(timeopen)
        self.customizeDOW(timeopen, data=[])
        elementnotes = self.createSiteService_TimeOpen_Notes(timeopen, 'Notes')
        seasonal = self.createSiteService_Seasonal(siteservice)
        seasonal = self.customizeSiteService_Seasonal(seasonal)
        taxonomy = self.createTaxonomy(siteservice)
        taxonomy = self.customizeTaxonomy(taxonomy, [])
        languages = self.createSubElement(siteservice, ns='airs', element='Languages')
        subElements = ['Name']
        languages = self.customizeSubElements(languages, 'airs', subElements, data=[])
        timeopen = self.createSiteService_TimeOpen(languages)
        self.customizeDOW(timeopen, data=[])
        elementnotes = self.createSiteService_TimeOpen_Notes(timeopen, 'Notes')
        return

    def createSubElement(self, xml, ns, element):
        subelement = ET.SubElement(xml, '%s:%s' % (ns, element))
        return subelement

    def customizeSubElements(self, xml, ns, subElements, data):
        attributes = []
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, ns, subElements)
        return xml

    def createSiteService_Seasonal(self, xml):
        ns = 'airs'
        element = 'Seasonal'
        seasonal = ET.SubElement(xml, '%s:%s' % (ns, element))
        return seasonal

    def customizeSiteService_Seasonal(self, xml):
        ns = 'airs'
        attributes = []
        elements = [
         'Description',
         'StartDate',
         'EndDate']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, ns, elements)
        return xml

    def createSiteService(self, xml):
        siteservice = ET.SubElement(xml, 'hmis:SiteService')
        return siteservice

    def customizeSiteService(self, xml):
        attributes = []
        elements = [
         'Name',
         'Key',
         'Description']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'airs', elements)
        return xml

    def createSiteService_TimeOpen(self, xml):
        timeopen = ET.SubElement(xml, 'airs:TimeOpen')
        return timeopen

    def createSiteService_TimeOpen_DayOfWeek(self, xml, dow):
        timeopen = ET.SubElement(xml, 'airs:%s' % dow)
        return timeopen

    def createSiteService_TimeOpen_Notes(self, xml, elementName):
        to_notes = ET.SubElement(xml, 'airs:%s' % elementName)
        return to_notes

    def customizeSiteService_TimeOpen_Notes(self, xml):
        pass

    def customizeSiteService_TimeOpen_DayOfWeek(self, xml):
        ns = 'airs'
        attributes = []
        elements = [
         'From',
         'To']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, ns, elements)
        return xml

    def customizeSiteService_TimeOpen(self, xml):
        ns = 'airs'
        attributes = []
        elements = []
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, ns, elements)
        return xml

    def createSiteServicePhone(self, xml):
        phone = ET.SubElement(xml, 'airs:Phone')
        return phone

    def customizeSiteServicePhone(self, xml):
        attributes = [
         'TollFree',
         'Confidential']
        elements = [
         'PhoneNumber',
         'ReasonWithheld',
         'Extension',
         'Description',
         'Type',
         'Function']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'airs', elements)
        return xml

    def createService(self, xml):
        service = ET.SubElement(xml, 'hmis:Service')
        service.text = '\n'
        service.tail = '\n'
        return service

    def customizeService(self, xml):
        attributes = []
        elements = [
         'COCCode',
         'Configuration',
         'DirectServiceCode',
         'FundingSources',
         'GranteeIdentifier',
         'IndividualFamilyCode',
         'Inventory',
         'ResidentialTrackingMethod',
         'ServiceType',
         'ServiceEffectivePeriod',
         'ServiceRecordedDate',
         'TargetPopulationA',
         'TargetPopulationB']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def createNeed(self, xml):
        need = ET.SubElement(xml, 'need')
        return need

    def customizeNeed(self, xml):
        attributes = []
        elements = [
         'NeedID',
         'SiteServiceID',
         'ServiceEventID',
         'NeedEffectivePeriod',
         'NeedRecordedDate',
         'NeedStatus']
        theAttributes = {}
        for attribute in attributes:
            xml.attrib[attribute] = ''

        theElements = {}
        theElements = self.generateElements(xml, 'hmis', elements)
        return xml

    def createSource(self, xml):
        source = ET.SubElement(xml, 'hmis:Source')
        return source

    def createExport(self, xml):
        export = ET.SubElement(xml, 'hmis:Export')
        return export

    def customizeExport(self, xml, exportData):
        exportID = ET.SubElement(xml, 'hmis:ExportID')
        self.processIDDeleteAttributes(exportID, exportData)
        IDStr = ET.SubElement(exportID, 'hmis:IDStr')
        if exportData.export_id_id_id_num == '' or exportData.export_id_id_id_num is None:
            IDStr.text = exportData.export_id_id_id_str
        else:
            IDStr.text = exportData.export_id_id_id_num
        fields = [
         'ExportDate',
         'ExportPeriod']
        theElements = {}
        for field in fields:
            theElements[field] = ET.SubElement(xml, 'hmis:%s' % field)

        theElements['ExportDate'].text = exportData.export_date.isoformat()
        startPeriod = ET.SubElement(theElements['ExportPeriod'], 'hmis:StartDate')
        startPeriod.text = exportData.export_period_start_date.isoformat()
        endPeriod = ET.SubElement(theElements['ExportPeriod'], 'hmis:EndDate')
        endPeriod.text = exportData.export_period_end_date.isoformat()
        return xml

    def processIDDeleteAttributes(self, xml, data):
        xml.attrib['hmis:delete'] = '1'
        xml.attrib['hmis:deleteOccurredDate'] = datetime.now().isoformat()
        xml.attrib['hmis:deleteEffective'] = datetime.now().isoformat()

    def customizeSource(self, xml, sourceData):
        sourceID = ET.SubElement(xml, 'hmis:SourceID')
        self.processIDDeleteAttributes(sourceID, sourceData)
        IDStr = ET.SubElement(sourceID, 'hmis:IDStr')
        if sourceData.source_id_id_id_num == '' or sourceData.source_id_id_id_num is None:
            IDStr.text = sourceData.source_id_id_id_str
        else:
            IDStr.text = sourceData.source_id_id_id_num
        fields = [
         'SoftwareVendor',
         'SoftwareVersion',
         'SourceContactEmail',
         'SourceContactExtension',
         'SourceContactFirst',
         'SourceContactLast',
         'SourceContactPhone',
         'SourceName']
        theElements = {}
        for field in fields:
            theElements[field] = ET.SubElement(xml, 'hmis:%s' % field)

        theElements['SoftwareVendor'].text = sourceData.software_vendor
        theElements['SoftwareVersion'].text = sourceData.software_version
        theElements['SourceContactEmail'].text = sourceData.source_contact_email
        theElements['SourceContactExtension'].text = sourceData.source_contact_extension
        theElements['SourceContactFirst'].text = sourceData.source_contact_first
        theElements['SourceContactLast'].text = sourceData.source_contact_last
        theElements['SourceContactPhone'].text = sourceData.source_contact_phone
        theElements['SourceName'].text = sourceData.source_name
        return xml

    def pullConfiguration(self, pExportID):
        source = self.session.query(dbobjects.Source).filter(dbobjects.Source.export_id == pExportID).one()
        self.configurationRec = self.session.query(dbobjects.SystemConfiguration).filter(and_(dbobjects.SystemConfiguration.source_id == source.source_id, dbobjects.SystemConfiguration.processing_mode == settings.MODE)).one()

    def createAgency(self, xml):
        agency = ET.SubElement(xml, 'hmis:Agency')
        return agency

    def queryTaxonomy(self, siteServiceID=None, needID=None):
        return self.session.query(dbobjects.Taxonomy).filter(and_(dbobjects.Taxonomy.site_service_index_id == siteServiceID, dbobjects.Taxonomy.need_index_id == needID)).all()

    def querySpatialLocation(self, siteID=None, agencyLocationID=None):
        return self.session.query(dbobjects.SpatialLocation).filter(and_(dbobjects.SpatialLocation.site_index_id == siteID, dbobjects.SpatialLocation.agency_location_index_id == agencyLocationID)).all()

    def querySiteService(self, exportID=None, reportID=None, siteID=None, agencyLocationID=None):
        return self.session.query(dbobjects.SiteService).filter(and_(dbobjects.SiteService.export_index_id == exportID, dbobjects.SiteService.report_index_id == reportID, dbobjects.SiteService.site_index_id == siteID, dbobjects.SiteService.agency_location_index_id == agencyLocationID)).all()

    def queryLanguages(self, siteID=None, siteServiceID=None, agencyLocationID=None):
        return self.session.query(dbobjects.Languages).filter(and_(dbobjects.Languages.site_index_id == siteID, dbobjects.Languages.site_service_index_id == siteServiceID, dbobjects.Languages.agency_location_index_id == agencyLocationID)).all()

    def queryCrossStreet(self, siteID=None):
        return self.session.query(dbobjects.CrossStreet).filter(and_(dbobjects.CrossStreet.site_index_id == siteID)).all()

    def queryAKA(self, agencyID=None, siteID=None, agencyLocationID=None):
        return self.session.query(dbobjects.Aka).filter(and_(dbobjects.Aka.site_index_id == siteID, dbobjects.Aka.agency_index_id == agencyID, dbobjects.Aka.agency_location_index_id == agencyLocationID)).all()

    def queryOtherAddress(self, siteID=None, agencyLocationID=None):
        return self.session.query(dbobjects.OtherAddress).filter(and_(dbobjects.OtherAddress.site_index_id == siteID, dbobjects.OtherAddress.agency_location_index_id == agencyLocationID)).all()

    def queryResourceInfo(self, agencyID=None, siteServiceID=None):
        return self.session.query(dbobjects.ResourceInfo).filter(and_(dbobjects.ResourceInfo.agency_index_id == agencyID, dbobjects.ResourceInfo.site_service_index_id == siteServiceID)).all()

    def querySite(self, exportID=None, reportID=None, agencyID=None):
        return self.session.query(dbobjects.Site).filter(and_(dbobjects.Site.agency_index_id == agencyID)).all()

    def queryService(self, agencyID=None):
        return self.session.query(dbobjects.Service).filter(and_(dbobjects.Service.agency_index_id == agencyID)).all()

    def queryServiceGroup(self, agencyID=None):
        return self.session.query(dbobjects.ServiceGroup).filter(and_(dbobjects.ServiceGroup.agency_index_id == agencyID)).all()

    def queryLicenseAccreditation(self, agencyID=None):
        return self.session.query(dbobjects.LicenseAccreditation).filter(and_(dbobjects.LicenseAccreditation.agency_index_id == agencyID)).all()

    def queryTimeOpen(self, siteID=None, languageID=None, siteServiceID=None, agencyLocationID=None):
        return self.session.query(dbobjects.TimeOpen).filter(and_(dbobjects.TimeOpen.site_index_id == siteID, dbobjects.TimeOpen.languages_index_id == languageID, dbobjects.TimeOpen.site_service_index_id == siteServiceID, dbobjects.TimeOpen.agency_location_index_id == agencyLocationID)).all()

    def queryContact(self, agencyID=None, resourceID=None, siteID=None, agencyLocationID=None):
        return self.session.query(dbobjects.Contact).filter(and_(dbobjects.Contact.agency_index_id == agencyID, dbobjects.Contact.resource_info_index_id == resourceID, dbobjects.Contact.site_index_id == siteID, dbobjects.Contact.agency_location_index_id == agencyLocationID)).all()

    def queryEmail(self, agencyID=None, contactID=None, resourceID=None, siteID=None, personHistoricalID=None):
        return self.session.query(dbobjects.Email).filter(and_(dbobjects.Email.agency_index_id == agencyID, dbobjects.Email.contact_index_id == contactID, dbobjects.Email.resource_info_index_id == resourceID, dbobjects.Email.site_index_id == siteID, dbobjects.Email.person_historical_index_id == personHistoricalID)).all()

    def queryAgencyLocationEmail(self, agencyID=None, agencyLocationID=None, contactID=None, resourceID=None, siteID=None, personHistoricalID=None):
        return self.session.query(dbobjects.Email).filter(and_(dbobjects.Email.agency_index_id == agencyID, dbobjects.Email.contact_index_id == contactID, dbobjects.Email.resource_info_index_id == resourceID, dbobjects.Email.site_index_id == siteID, dbobjects.Email.person_historical_index_id == personHistoricalID, dbobjects.Email.agency_location_index_id == agencyLocationID)).all()

    def queryAgencyURL(self, agencyID=None, siteID=None):
        filter_result = self.session.query(dbobjects.Url).filter(and_(dbobjects.Url.agency_index_id == agencyID, dbobjects.Url.site_index_id == siteID, dbobjects.Url.agency_location_index_id == None)).all()
        return filter_result

    def queryAgencyLocationURL(self, agencyLocationID=None, agencyID=None):
        result = self.session.query(dbobjects.Url).filter(and_(dbobjects.Url.agency_index_id == agencyID, dbobjects.Url.agency_location_index_id == agencyLocationID, agencyLocationID != None)).all()
        return result

    def queryAgencyLocation(self, agencyID=None):
        return self.session.query(dbobjects.AgencyLocation).filter(and_(dbobjects.AgencyLocation.agency_index_id == agencyID)).all()

    def queryPhone(self, agencyID=None, contactID=None, resourceID=None, siteID=None, siteServiceID=None, personHistoricalID=None, agencyLocationID=None):
        return self.session.query(dbobjects.Phone).filter(and_(dbobjects.Phone.agency_index_id == agencyID, dbobjects.Phone.contact_index_id == contactID, dbobjects.Phone.resource_info_index_id == resourceID, dbobjects.Phone.site_index_id == siteID, dbobjects.Phone.site_service_index_id == siteServiceID, dbobjects.Phone.person_historical_index_id == personHistoricalID, dbobjects.Phone.agency_location_index_id == agencyLocationID)).all()

    def customizeAgency(self, xml, agencyData, siteIndexID=None):
        xml.attrib['RecordOwner'] = agencyData.record_owner
        xml.attrib['FEIN'] = agencyData.fein
        xml.attrib['YearInc'] = agencyData.year_inc
        xml.attrib['AnnualBudgetTotal'] = agencyData.annual_budget_total
        xml.attrib['LegalStatus'] = agencyData.legal_status
        xml.attrib['ExcludeFromWebsite'] = agencyData.exclude_from_website
        xml.attrib['ExcludeFromDirectory'] = agencyData.exclude_from_directory
        elements = [
         'Key',
         'Name',
         'AgencyDescription',
         'AKA',
         'AgencyLocation',
         'Phone',
         'URL',
         'Email']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Key'].text = agencyData.airs_key
        theElements['Name'].text = agencyData.airs_name
        theElements['AgencyDescription'].text = agencyData.agency_description
        AKA = theElements['AKA']
        AKARows = self.queryAKA(agencyData.id)
        for AKARow in AKARows:
            akarow = self.customizeAgencyAKA(AKA, AKARow)

        AgencyLocationElement = theElements['AgencyLocation']
        AgencyLocationData = self.queryAgencyLocation(agencyID=agencyData.id)
        for agencylocationRows in AgencyLocationData:
            agencyLoc = self.customizeAgencyLocation(AgencyLocationElement, agencyData, agencylocationRows)

        PhoneElement = theElements['Phone']
        AgencyPhoneData = self.queryPhone(agencyID=agencyData.id)
        for phoneRow in AgencyPhoneData:
            phoneSubElement = self.customizeAgencyPhone(PhoneElement, phoneRow)

        urlElement = theElements['URL']
        AgencyURLData = self.queryAgencyURL(agencyID=agencyData.id)
        for urlRow in AgencyURLData:
            urlSubElement = self.addURL(urlElement, urlRow)

        EmailElement = theElements['Email']
        AgencyEmailData = self.queryEmail(agencyID=agencyData.id)
        for emailRow in AgencyEmailData:
            urlSubElement = self.customizeAgencyEmail(EmailElement, emailRow)

        AgencyContactData = self.queryContact(agencyID=agencyData.id)
        if AgencyContactData:
            ContactElement = ET.SubElement(xml, 'airs:Contact')
            for contactRow in AgencyContactData:
                contactSubElement = self.customizeAgencyContact(ContactElement, contactRow, agencyData)

        AgencyLicenseAccreditationData = self.queryLicenseAccreditation(agencyID=agencyData.id)
        for accreditationRow in AgencyLicenseAccreditationData:
            LicenseAccreditationElement = ET.SubElement(xml, 'airs:LicenseAccreditation')
            licenseAcreditationSubElement = self.customizeAgencyLicenseAccreditation(LicenseAccreditationElement, accreditationRow)

        elements = [
         'IRSStatus',
         'SourceOfFunds',
         'ServiceGroup',
         'Service',
         'Site',
         'ResourceInfo']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['IRSStatus'] = agencyData.irs_status
        theElements['SourceOfFunds'] = agencyData.source_of_funds
        ServiceGroupElement = theElements['ServiceGroup']
        AgencyServiceGroupData = self.queryServiceGroup(agencyID=agencyData.id)
        for serviceGroupRow in AgencyServiceGroupData:
            serviceGroupSubElement = self.customizeAgencyServiceGroup(ServiceGroupElement, serviceGroupRow)

        SiteElement = theElements['Site']
        AgencySiteData = self.querySite(agencyID=agencyData.id)
        for siteRow in AgencySiteData:
            serviceGroupSubElement = self.customizeAgencySite(SiteElement, agencyData, siteRow)

        ResourceInfoElement = theElements['ResourceInfo']
        resourceInfoData = self.queryResourceInfo(agencyID=agencyData.id)
        for resourceInfoRow in resourceInfoData:
            serviceGroupSubElement = self.customizeAgencyResourceInfo(ResourceInfoElement, resourceInfoRow)

        return xml

    def createAgencyAKA(self, xml):
        AKA = ET.SubElement(xml, 'airs:AKA')
        return AKA

    def customizeMailingAddress(self, xml, agencyLocationData):
        xml.attrib['Confidential'] = agencyLocationData.mailing_address_confidential
        xml.attrib['Description'] = agencyLocationData.mailing_address_description
        elements = [
         'PreAddressLine',
         'Line1',
         'Line2',
         'City',
         'County',
         'State',
         'ZipCode',
         'Country']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['PreAddressLine'].text = agencyLocationData.mailing_address_pre_address_line
        theElements['Line1'].text = agencyLocationData.mailing_address_line_1
        theElements['Line2'].text = agencyLocationData.mailing_address_line_2
        theElements['City'].text = agencyLocationData.mailing_address_city
        theElements['State'].text = agencyLocationData.mailing_address_state
        theElements['County'].text = agencyLocationData.mailing_address_county
        theElements['ZipCode'].text = agencyLocationData.mailing_address_zip_code
        theElements['Country'].text = agencyLocationData.mailing_address_country

    def customizeAgencyAKA(self, xml, AKAData):
        elements = [
         'Name',
         'Confidential',
         'Description']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Name'].text = AKAData.name
        theElements['Confidential'].text = AKAData.confidential
        theElements['Description'].text = AKAData.description

    def customizeAgencyLocation(self, xml, agencyData, agencyLocationData):
        xml.attrib['PublicAccessToTransportation'] = agencyLocationData.public_access_to_transportation
        xml.attrib['YearInc'] = agencyLocationData.year_inc
        xml.attrib['AnnualBudgetTotal'] = agencyLocationData.annual_budget_total
        xml.attrib['LegalStatus'] = agencyLocationData.legal_status
        xml.attrib['ExcludeFromWebsite'] = agencyLocationData.exclude_from_website
        xml.attrib['ExcludeFromDirectory'] = agencyLocationData.exclude_from_directory
        elements = [
         'Key',
         'Name',
         'SiteDescription',
         'AKA',
         'MailingAddress',
         'OtherAddress',
         'Phone',
         'URL',
         'Email',
         'Contact',
         'TimeOpen',
         'Languages',
         'DisabilitiesAccess',
         'PhysicalLocationDescription',
         'BusServiceAccess',
         'SiteService',
         'SpatialLocation']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Key'].text = agencyLocationData.key
        theElements['Name'].text = agencyLocationData.name
        theElements['SiteDescription'].text = agencyLocationData.site_description
        akaElement = theElements['AKA']
        AKARows = self.queryAKA(agencyID=agencyData.id, agencyLocationID=agencyLocationData.id)
        for AKARow in AKARows:
            akarow = self.customizeAgencyAKA(akaElement, AKARow)

        mailAddressElement = theElements['MailingAddress']
        self.customizeMailingAddress(mailAddressElement, agencyLocationData)
        otheraddressElement = theElements['OtherAddress']
        OtherAddressData = self.queryOtherAddress(siteID=None, agencyLocationID=agencyLocationData.id)
        for otheraddressRow in OtherAddressData:
            otherAddressSubElement = self.customizeSiteOtherAddress(otheraddressElement, otheraddressRow)

        crossStreetData = self.queryCrossStreet(agencyLocationData.id)
        for crossStreetRow in crossStreetData:
            crossStreetSubElement = ET.SubElement(xml, 'airs:CrossStreet')
            crossStreetSubElement.text = crossStreetRow.cross_street

        phoneElement = theElements['Phone']
        sitePhoneData = self.queryPhone(agencyID=agencyData.id, contactID=None, resourceID=None, agencyLocationID=agencyLocationData.id)
        for phoneRow in sitePhoneData:
            phoneSubElement = self.customizeAgencyPhone(phoneElement, phoneRow)

        urlElement = theElements['URL']
        SiteURLData = self.queryAgencyLocationURL(agencyLocationData.id, agencyData.id)
        for urlRow in SiteURLData:
            urlSubElement = self.addURL(urlElement, urlRow)

        emailElement = theElements['Email']
        SiteEmailData = self.queryAgencyLocationEmail(agencyData.id, agencyLocationData.id, siteID=None)
        for emailRow in SiteEmailData:
            emailSubElement = self.customizeAgencyEmail(emailElement, emailRow)

        contactElement = theElements['Contact']
        siteContactData = self.queryContact(agencyID=agencyData.id, siteID=None, agencyLocationID=agencyLocationData.id)
        for siteContactRow in siteContactData:
            contactSubElement = self.customizeAgencyContact(contactElement, siteContactRow, agencyData)

        timeopenElement = theElements['TimeOpen']
        timeOpenData = self.queryTimeOpen(siteID=None, languageID=None, siteServiceID=None, agencyLocationID=agencyLocationData.id)
        for timeOpenRow in timeOpenData:
            timeopenSubElement = self.customizeTimeOpen(timeopenElement, timeOpenRow)

        languagesElement = theElements['Languages']
        siteLanguageData = self.queryLanguages(agencyLocationID=agencyLocationData.id)
        for siteLanguageRow in siteLanguageData:
            languagesSubElement = self.customizeSiteLanguage(languagesElement, siteLanguageRow)

        theElements['DisabilitiesAccess'].text = agencyLocationData.disabilities_access
        theElements['PhysicalLocationDescription'].text = agencyLocationData.physical_location_description
        theElements['BusServiceAccess'].text = agencyLocationData.bus_service_access
        siteServiceElement = theElements['SiteService']
        siteServiceData = self.querySiteService(agencyLocationID=agencyLocationData.id)
        for siteServiceRow in siteServiceData:
            siteServiceSubElement = self.customizeSiteService(siteServiceElement, siteServiceRow)

        spatiallocationElement = theElements['SpatialLocation']
        siteSpatialLocationData = self.querySpatialLocation(agencyLocationID=agencyLocationData.id)
        for siteSpatialLocationRow in siteSpatialLocationData:
            languagesSubElement = self.customizeSpatialLocation(spatiallocationElement, siteSpatialLocationRow)

        return

    def customizeAgencyPhone(self, xml, phoneData):
        xml.attrib['TollFree'] = phoneData.toll_free
        xml.attrib['Confidential'] = phoneData.confidential
        elements = [
         'PhoneNumber',
         'Extension',
         'Description',
         'Type',
         'Function']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['PhoneNumber'].text = phoneData.phone_number
        if phoneData.extension is not None:
            theElements['Extension'].text = phoneData.extension
        if phoneData.description is not None:
            theElements['Description'].text = phoneData.description
        if phoneData.type is not None:
            theElements['Type'].text = phoneData.type
        if phoneData.function is not None:
            theElements['Function'].text = phoneData.function
        return

    def addURL(self, xml, URLData):
        elements = [
         'Address',
         'Note']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Address'].text = URLData.address
        theElements['Note'].text = URLData.note

    def customizeAgencyEmail(self, xml, EmailData):
        elements = [
         'Address',
         'Note']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Address'].text = EmailData.address
        theElements['Note'].text = EmailData.note

    def customizeSiteLanguage(self, xml, LanguagesData):
        elements = [
         'Name',
         'TimeOpen',
         'Notes']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Name'].text = LanguagesData.name
        theElements['Notes'].text = LanguagesData.notes

    def customizeSiteService(self, xml, siteServiceData):
        if siteServiceData is None:
            return xml
        else:
            xml.attrib['AreaFlexibility'] = siteServiceData.area_flexibility
            xml.attrib['ServiceNotAlwaysAvailable'] = siteServiceData.service_not_always_available
            xml.attrib['ServiceGroupKey'] = siteServiceData.service_group_key
            elements = [
             'Key']
            theElements = {}
            for element in elements:
                theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

            theElements['Key'].text = siteServiceData.key
            taxonomyData = self.queryTaxonomy(siteServiceID=siteServiceData.id)
            if len(taxonomyData) > 0:
                taxonomySubElement = self.customizeTaxonomy(xml, taxonomyData)
            return

    def customizeSpatialLocation(self, xml, spatialLocationData):
        elements = [
         'Description',
         'Datum',
         'Latitude',
         'Longitude']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Description'].text = spatialLocationData.description
        theElements['Datum'].text = spatialLocationData.datum
        theElements['Latitude'].text = spatialLocationData.latitude
        theElements['Longitude'].text = spatialLocationData.longitude

    def customizeTimeOpen(self, xml, TimeOpenData):
        pass

    def customizeAgencyContact(self, xml, ContactData, agencyData):
        xml.attrib['Type'] = ContactData.type
        if ContactData.title:
            title = ET.SubElement(xml, 'airs:Title')
            title.text = ContactData.title
        if ContactData.name:
            name = ET.SubElement(xml, 'airs:Name')
            name.text = ContactData.name
        AgencyEmailData = self.queryEmail(agencyData.id, ContactData.id)
        print 'agency contact email results:', AgencyEmailData
        if AgencyEmailData:
            email = ET.SubElement(xml, 'airs:Email')
            for emailRow in AgencyEmailData:
                urlSubElement = self.customizeAgencyEmail(email, emailRow)

        AgencyPhoneData = self.queryPhone(agencyData.id, ContactData.id)
        print 'agency contact phone results:', AgencyPhoneData
        if AgencyPhoneData:
            phone = ET.SubElement(xml, 'airs:Phone')
            for phoneRow in AgencyPhoneData:
                phoneSubElement = self.customizeAgencyPhone(phone, phoneRow)

    def customizeAgencyLicenseAccreditation(self, xml, AccreditationData):
        elements = ['License',
         'LicensedBy']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['License'].text = AccreditationData.license
        theElements['LicensedBy'].text = AccreditationData.licensed_by

    def customizeAgencyServiceGroup(self, xml, serviceGroupData):
        elements = [
         'Key',
         'Name',
         'ProgramName']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Key'].text = serviceGroupData.key
        theElements['Name'].text = serviceGroupData.name
        theElements['ProgramName'].text = serviceGroupData.program_name

    def customizeSiteOtherAddress(self, xml, siteOtherAddress):
        xml.attrib['Confidential'] = siteOtherAddress.confidential
        xml.attrib['Description'] = siteOtherAddress.description
        elements = [
         'Line1',
         'Line2',
         'City',
         'State',
         'ZipCode',
         'Country']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Line1'].text = siteOtherAddress.line_1
        theElements['Line2'].text = siteOtherAddress.line_2
        theElements['City'].text = siteOtherAddress.city
        theElements['State'].text = siteOtherAddress.state
        theElements['ZipCode'].text = siteOtherAddress.zip_code
        theElements['Country'].text = siteOtherAddress.country

    def customizeAgencyResourceInfo(self, xml, agencyData):
        xml.attrib['AvailableForDirectory'] = agencyData.available_for_directory
        xml.attrib['AvailableForReferral'] = agencyData.available_for_referral
        xml.attrib['AvailableForResearch'] = agencyData.available_for_research
        xml.attrib['DateAdded'] = agencyData.date_added.isoformat()
        xml.attrib['DateLastVerified'] = agencyData.date_last_verified.isoformat()
        xml.attrib['DateOfLastAction'] = agencyData.date_of_last_action.isoformat()
        xml.attrib['LastActionType'] = agencyData.last_action_type
        elements = [
         'Contact']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        contactElement = theElements['Contact']
        siteContactData = self.queryContact(agencyID=agencyData.id, siteID=None)
        for siteContactRow in siteContactData:
            contactSubElement = self.customizeAgencyContact(contactElement, siteContactRow, agencyData)

        return

    def customizeAgencySite(self, xml, agencyData, siteData):
        xml.attrib['PublicAccessToTransportation'] = siteData.public_access_to_transportation
        xml.attrib['YearInc'] = siteData.year_inc
        xml.attrib['AnnualBudgetTotal'] = siteData.annual_budget_total
        xml.attrib['LegalStatus'] = siteData.legal_status
        xml.attrib['ExcludeFromWebsite'] = siteData.exclude_from_website
        xml.attrib['ExcludeFromDirectory'] = siteData.exclude_from_directory
        elements = [
         'Key',
         'Name',
         'SiteDescription',
         'AKA',
         'OtherAddress',
         'Phone',
         'URL',
         'Email',
         'Contact',
         'TimeOpen',
         'Languages',
         'DisabilitiesAccess',
         'PhysicalLocationDescription',
         'BusServiceAccess',
         'SpatialLocation']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Key'].text = siteData.airs_key
        theElements['Name'].text = siteData.airs_name
        theElements['SiteDescription'].text = siteData.site_description
        akaElement = theElements['AKA']
        AKARows = self.queryAKA(agencyID=agencyData.id, siteID=siteData.id)
        for AKARow in AKARows:
            akarow = self.customizeAgencyAKA(akaElement, AKARow)

        otheraddressElement = theElements['OtherAddress']
        OtherAddressData = self.queryOtherAddress(siteData.id)
        for otheraddressRow in OtherAddressData:
            otherAddressSubElement = self.customizeSiteOtherAddress(otheraddressElement, otheraddressRow)

        crossStreetData = self.queryCrossStreet(siteData.id)
        for crossStreetRow in crossStreetData:
            crossStreetSubElement = ET.SubElement(xml, 'airs:CrossStreet')
            crossStreetSubElement.text = crossStreetRow.cross_street

        phoneElement = theElements['Phone']
        sitePhoneData = self.queryPhone(agencyID=agencyData.id, contactID=None, resourceID=None, siteID=siteData.id)
        for phoneRow in sitePhoneData:
            phoneSubElement = self.customizeAgencyPhone(phoneElement, phoneRow)

        urlElement = theElements['URL']
        SiteURLData = self.queryAgencyURL(agencyID=agencyData.id, siteID=siteData.id)
        for urlRow in SiteURLData:
            urlSubElement = self.addURL(urlElement, urlRow)

        emailElement = theElements['Email']
        SiteEmailData = self.queryEmail(agencyData.id, siteID=siteData.id)
        for emailRow in SiteEmailData:
            emailSubElement = self.customizeAgencyEmail(emailElement, emailRow)

        contactElement = theElements['Contact']
        siteContactData = self.queryContact(agencyID=agencyData.id, siteID=siteData.id)
        for siteContactRow in siteContactData:
            contactSubElement = self.customizeAgencyContact(contactElement, siteContactRow, agencyData)

        timeopenElement = theElements['TimeOpen']
        languagesElement = theElements['Languages']
        siteLanguageData = self.queryLanguages(siteID=siteData.id)
        for siteLanguageRow in siteLanguageData:
            languagesSubElement = self.customizeSiteLanguage(languagesElement, siteLanguageRow)

        theElements['DisabilitiesAccess'].text = siteData.disabilities_access
        theElements['PhysicalLocationDescription'].text = siteData.physical_location_description
        theElements['BusServiceAccess'].text = siteData.bus_service_access
        spatiallocationElement = theElements['SpatialLocation']
        siteSpatialLocationData = self.querySpatialLocation(siteID=siteData.id)
        for siteSpatialLocationRow in siteSpatialLocationData:
            languagesSubElement = self.customizeSpatialLocation(spatiallocationElement, siteSpatialLocationRow)

        return

    def customizeAgencyService(self):
        elements = [
         'Name',
         'Confidential',
         'Description']
        theElements = {}
        for element in elements:
            theElements[element] = ET.SubElement(xml, 'airs:%s' % element)

        theElements['Name'].text = AKAData.name
        theElements['Confidential'].text = AKAData.confidential
        theElements['Description'].text = AKAData.description

    def processXML(self):
        self.root_element = self.createDoc()
        if self.options.reported == True:
            Sources = self.session.query(dbobjects.Source)
        elif self.options.unreported == True:
            Sources = self.session.query(dbobjects.Source)
        elif self.options.reported == None:
            Sources = self.session.query(dbobjects.Source)
        for sourceData in Sources:
            source = self.createSource(self.root_element)
            source = self.customizeSource(source, sourceData)
            link = self.session.query(dbobjects.SourceExportLink).filter(dbobjects.SourceExportLink.source_index_id == sourceData.id).one()
            export_rec_id = link.export_index_id
            exportRecs = self.session.query(dbobjects.Export).filter(dbobjects.Export.export_id == export_rec_id).all()
            for exportData in exportRecs:
                export = self.createExport(source)
                export = self.customizeExport(export, exportData)
                agency = self.createAgency(export)
                agencyRecs = self.session.query(dbobjects.Agency).filter(dbobjects.Agency.export_index_id == export_rec_id).all()
                for agencyData in agencyRecs:
                    agency = self.customizeAgency(agency, agencyData)

                houseHold = self.createHousehold(export)
                houseHold = self.customizeHousehold(houseHold)
                person = self.createPerson(export)

            person = self.customizePerson(person)
            need = self.createNeed(person)
            need = self.customizeNeed(need)
            taxonomy = self.createTaxonomy(need)
            taxonomy = self.customizeTaxonomy(taxonomy, [])
            othernames = self.createOtherNames(person)
            othernames = self.customizeOtherNames(othernames)
            personhistorical = self.createPersonHistorical(person)
            personhistorical = self.customizePersonHistorical(personhistorical)
            race = self.createRace(person)
            race = self.customizeRace(race)
            releaseofinformation = self.createReleaseOfInformation(person)
            releaseofinformation = self.customizeReleaseOfInformation(releaseofinformation)
            serviceevent = self.createServiceEvent(person)
            serviceevent = self.customizeServiceEvent(serviceevent)
            siteserviceparticipation = self.createSiteServiceParticipation(person)
            siteserviceparticipation = self.customizeSiteServiceParticipation(siteserviceparticipation)
            person = self.customizePersonSSN(person)
            service = self.createService(export)
            service = self.customizeService(service)
            site = self.createSite(export)
            site = self.customizeSite(site)
            aka = self.createSite_AKA(site)
            aka = self.customizeSite_AKA(aka)
            self.manageSiteService(export)

        return


if __name__ == '__main__':
    from queryobject import QueryObject
    optParse = QueryObject()
    options = optParse.getOptions()
    if options != None:
        try:
            vld = HMISXMLWriter('.', options)
            vld.write()
        except clsexceptions.UndefinedXMLWriter:
            print 'Please specify a format for outputting your XML'
            raise