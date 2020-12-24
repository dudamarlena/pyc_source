# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/selector.py
# Compiled at: 2011-01-23 15:52:21
r"""Figures out what type of data format we are dealing with, using validation \                                                                                                                             
or whatever we can use to test, so the appropriate reader correct implementation can be used."""
import os
from synthesis import fileutils
import sys, time
from synthesis.fileinputwatcher import FileInputWatcher
from synthesis.hmisxml28reader import HMISXML28Reader
from synthesis.hmisxml30reader import HMISXML30Reader
from synthesis.jfcsxmlreader import JFCSXMLReader
from synthesis.occhmisxml30reader import OCCHUDHMISXML30Reader
from lxml import etree
import Queue
from conf import settings
from synthesis.emailprocessor import XMLProcessorNotifier
from synthesis.filerouter import router
from os import path
import traceback, copy
from synthesis.clssocketcomm import serviceController

class FileHandler:
    """Sets up the watch on the directory, and handles the file once one comes in"""

    def __init__(self):
        dir_to_watch = settings.INPUTFILES_PATH
        self.queue = Queue.Queue(0)
        self.file_input_watcher = FileInputWatcher(dir_to_watch, self.queue)
        self.selector = Selector()
        if settings.GUI:
            if settings.DEBUG:
                print 'Now running the GUI serviceController code'
                sc = serviceController(True)
                sc.listen()
        else:
            if settings.DEBUG:
                print 'Now running FileHandler.nonGUIRun()'
            self.nonGUIRun()
            print 'returned to FileHandler.__init__ from nonGUIRun'
            print 'calling sys.exit'
            sys.exit()

    def setProcessingOptions(self, docName):
        """ ProcessingOptions is a dictionary on a per file/sender basis.
        Dictionary contains settings like does the sender use encryption etc.
        self.ProcessingOptions = 
            {
                'SMTPTOADDRESS': ['someone@domain.com,],
                'SMTPTOADDRESSCC': [],
                'SMTPTOADDRESSBCC': [],
                'FINGERPRINT':'',
                'USES_ENCRYPTION':True
            }
        """
        folderName = path.split(docName)[0]
        if settings.DEBUG:
            print 'folder name to email is', folderName
        if os.path.isdir(folderName):
            try:
                self.ProcessingOptions = settings.SMTPRECIPIENTS[folderName]
            except:
                raise

        else:
            print 'folder', folderName, 'is not a directory'

    def processFiles(self, new_file_loc):
        global valid
        self.setProcessingOptions(new_file_loc)
        self.email = XMLProcessorNotifier(new_file_loc)
        self.router = router()
        valid = False
        print 'The settings indicate that, for this folder, encryption is:', self.ProcessingOptions['USES_ENCRYPTION']
        if self.ProcessingOptions['USES_ENCRYPTION']:
            fileStream = self.crypto.decryptFile2Stream(new_file_loc)
            print 'stream', fileStream
        elif settings.DEBUG:
            print 'No encryption, so just opening the file', new_file_loc
        if settings.DEBUG:
            print 'attempting validation tests on', new_file_loc
        if os.path.isfile(new_file_loc):
            results = self.selector.validate(new_file_loc)
            for item in results:
                if item == True:
                    valid = True
                    try:
                        self.email.notifyValidationSuccess()
                    except:
                        print traceback.print_exc(file=sys.stdout)

                    if settings.DEBUG:
                        print 'moving to used_files',
                    self.router.moveUsed(new_file_loc)
                    return True

        if valid == False:
            if settings.DEBUG:
                print 'We did not have any successful validations'
            self.email.notifyValidationFailure()
            if settings.DEBUG:
                print 'moving to Failed'
            if os.path.isfile(new_file_loc):
                self.router.moveFailed(new_file_loc)
            elif settings.DEBUG:
                print "Can't move because file doesn't exist.  Shouldn't be trying to move anything to Failed if isn't there."
            return False

    def processExisting(self):
        """ this function churns through the input path(s) and processes files that are already there.
        iNotify only fires events since program was started so existing files don't get processed
        """
        listOfFiles = list()
        for folder in settings.INPUTFILES_PATH:
            listOfFiles.extend(fileutils.grabFiles(path.join(folder, '*')))
            if settings.DEBUG:
                print 'list of files grabbed in processExisting is', listOfFiles
            for inputFile in listOfFiles:
                self.processFiles(inputFile)

    def nonGUIPOSIXRun(self):
        if settings.DEBUG:
            print 'First, looking for preexisting files in input location.'
        self.processExisting()
        if settings.DEBUG:
            print 'monitoring starting ...'
        new_files = self.monitor()
        if settings.DEBUG:
            print 'monitoring done ...'
            print 'new_files is', new_files
        if not new_files:
            print 'No new files, returning'
            return
        for new_file in new_files:
            if settings.DEBUG:
                print 'Processing: %s' % new_file
            self.processFiles(new_file)

    def nonGUIWindowsRun(self):
        BASE_PATH = os.getcwd()
        path_to_watch = os.path.join(BASE_PATH, 'InputFiles')
        before = dict([ (f, None) for f in os.listdir(path_to_watch) ])
        try:
            while 1:
                time.sleep(10)
                after = dict([ (f, None) for f in os.listdir(path_to_watch) ])
                added = [ f for f in after if f not in before ]
                removed = [ f for f in before if f not in after ]
                if added:
                    print 'Added: ', (', ').join(added)
                    self.processExisting()
                if removed:
                    print 'Removed: ', (', ').join(removed)
                before = after

        except KeyboardInterrupt:
            return

        return

    def nonGUIRun(self):
        """looks for and handles files, if there is no gui controlling the daemon, as specified by the GUI option in settings.py."""
        if os.name == 'nt':
            if settings.DEBUG:
                print 'We have a Windows system, as determined by nonGUIRun.  So handing off to nonGUIWindowsRun()'
            self.nonGUIWindowsRun()
        else:
            if settings.DEBUG:
                print 'We have a POSIX system, as determined by nonGUIRun().  So handing off to nonGUIPOSIXRun()'
            self.nonGUIPOSIXRun()
            print 'back to nonGUIRun, so returning'

    def monitor(self):
        """function to start and stop the monitor"""
        try:
            self.file_input_watcher.monitor()
            if settings.DEBUG:
                print 'waiting for new input...'
            files = list()
            _QTO = 5
            while 1:
                try:
                    file_found_path = self.queue.get(block='true', timeout=_QTO)
                    if settings.DEBUG:
                        print 'found a new file: %s' % file_found_path
                    _QTO = 5
                    if file_found_path != None:
                        if settings.DEBUG:
                            print 'appending files'
                        files.append(file_found_path)
                    if settings.DEBUG:
                        print 'files found so far in while loop are ', files
                    continue
                except Queue.Empty:
                    if not files:
                        continue
                    files.reverse()
                    while files:
                        if settings.DEBUG:
                            print 'Queue.Empty exception, but files list is not empty, so files to process are', files
                        filepathitem = files.pop()
                        print 'processing ', filepathitem
                        self.processFiles(filepathitem)

                    continue
                except KeyboardInterrupt:
                    print 'KeyboardInterrupt caught in selector.monitor() while loop'
                    self.file_input_watcher.stop_monitoring()
                    break

        except KeyboardInterrupt:
            print 'KeyboardInterrupt caught in selector.monitor() main section'
            self.file_input_watcher.stop_monitoring()
        except:
            print 'General Exception'
            self.file_input_watcher.stop_monitoring()
            raise

        return


class Selector:
    """Figures out which data format is being received."""

    def __init__(self):
        if settings.DEBUG:
            print 'selector instantiated and figuring out what schema are available'
            for item in settings.SCHEMA_DOCS:
                print 'schema to potentially load: ' + settings.SCHEMA_DOCS[item]

    def validate(self, instance_file_loc, shred=True):
        """Validates against the various available schema and csv records.        If not specified in the configs, it keeps trying each available         test to find the first which successfully validates.  You just         pass it a test, and the xml instance data."""
        global results
        tests = [
         HUDHMIS30XMLTest, HUDHMIS28XMLTest, OCCHUDHMIS30XMLTest, JFCSXMLTest]
        if settings.DEBUG:
            print 'tests are', tests
        readers = {HUDHMIS30XMLTest: HUDHMIS30XMLInputReader, HUDHMIS28XMLTest: HUDHMIS28XMLInputReader, OCCHUDHMIS30XMLTest: OCCHUDHMIS30XMLInputReader, JFCSXMLTest: JFCSXMLInputReader}
        if settings.SKIP_VALIDATION_TEST is True:
            print 'skipping tests battery for debugging'
            print 'just shredding with JFCSXMLReader service_event schema'
            JFCSXMLInputReader.data_type = 'service_event'
            readers[JFCSXMLTest](instance_file_loc).shred()
            return
        if settings.DEBUG:
            print 'readers are', readers
        results = []
        for test in tests:
            test_instance = test()
            result = test_instance.validate(instance_file_loc)
            results.append(result)
            if settings.DEBUG:
                print 'validation return result is', result
                print 'results are cumulatively', results
            if True in results:
                loc_true = results.index(True)
                length_list = len(results)
                if loc_true == length_list - 1:
                    if settings.DEBUG:
                        print "we haven't had a positive validation until now, so go ahead and shred/move it"
                    if result:
                        if settings.DEBUG:
                            print 'shredding...'
                        if shred:
                            if settings.DEBUG:
                                print 'readers[test] is: ', readers[test]
                                print 'instance_file_loc: ', instance_file_loc
                            readers[test](instance_file_loc).shred()

        if not results:
            print 'results empty'
        return results


class VendorXMLTest:
    """Stub for any specific vendor's non-standardized XML format."""

    def __init__(self):
        self.name = 'Vendor XML'
        print 'running the', self.name, 'test'

    def validate(self, instance_filename):
        """implementation of interface's validate method"""
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to validate', instance_filename
        return False


class HUDHMIS28XMLTest:
    """Load in the HUD HMIS Schema, version 2.8."""

    def __init__(self):
        self.name = 'HUDHMIS28XML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['hud_hmis_xml_2_8']

    def validate(self, instance_stream):
        """This specific data format's validation process."""
        schema = open(self.schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid(instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results

            if results == None:
                print "The validator erred and couldn't determine if the xml                 was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error

        return


class HUDHMIS30XMLTest:
    """Load in the HUD HMIS Schema, version 3.0."""

    def __init__(self):
        self.name = 'HUDHMIS30XML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['hud_hmis_xml_3_0']
        print "settings.SCHEMA_DOCS['hud_hmis_xml_3_0'] is: ", settings.SCHEMA_DOCS['hud_hmis_xml_3_0']

    def validate(self, instance_stream):
        """This specific data format's validation process."""
        schema = open(self.schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid(instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results

            if results == None:
                print "The validator erred and couldn't determine if the xml                 was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error

        return


class OCCHUDHMIS30XMLTest:
    """Load in the HUD HMIS Schema, version 3.0."""

    def __init__(self):
        self.name = 'OCCHUDHMIS30XML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0']
        print "settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0'] is: ", settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0']

    def validate(self, instance_stream):
        """This specific data format's validation process."""
        schema = open(self.schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid(instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results

            if results == None:
                print "The validator erred and couldn't determine if the xml                 was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error

        return


class SVCPOINT20XMLTest:
    """Load in the SVCPoint Schema, version 2.0."""

    def __init__(self):
        self.name = 'Svcpt 2.0 XML'
        print 'running the Svcpt 2.0 XML test'
        self.schema_filename = settings.SCHEMA_DOCS['svcpoint_2_0_xml']

    def validate(self, instance_stream):
        """This specific data format's validation process."""
        schema = open(self.schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid(instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results

            if results == None:
                print "The validator erred and couldn't determine if the xml                 was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ',
            print error
            raise

        return


class SVCPOINT406XMLTest:
    """Load in the SVCPoint Schema, version 4.06"""

    def __init__(self):
        self.name = 'Svc406 XML'
        print 'running the Svcpt 4.06 XML test'
        self.schema_filename = settings.SCHEMA_DOCS['svcpoint_4_0_6_xml']

    def validate(self, instance_stream):
        """This specific data format's validation process."""
        schema = open(self.schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid(instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results

            if results == None:
                print "The validator erred and couldn't determine if the xml                 was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ',
            print error
            raise

        return


class JFCSXMLTest:
    """ Tests for JFCS data 
        * There are 2 possible data source types ('service_event' or 'client')
        Steps: (will stop and return True on first success)
            1 - Attempt to validate against 'service_event' schema: 'JFCS_SERVICE.xsd'
            2 - Attempt to validate against 'client' schema: 'JFCS_CLIENT.xsd'
            3 - Check for known 'service_event' elements anywhere in the tree
            4 - Check for known 'client' elements anywhere in the tree
    """

    def __init__(self):
        self.name = 'JFCS'
        print 'running the', self.name, 'test'
        self.service_event_schema_filename = settings.SCHEMA_DOCS['jfcs_service_event_xml']
        self.client_schema_filename = settings.SCHEMA_DOCS['jfcs_client_xml']
        self.service_event_elements = ['c4clientid', 'qprogram', 'serv_code', 'trdate', 'end_date', 'cunits']
        self.client_elements = ['aprgcode', 'a_date', 't_date', 'family_id', 'c4clientid', 'c4dob', 'hispanic', 'c4sex', 'c4firstname', 'c4lastname', 'c4mi', 'ethnicity', 'c4ssno', 'c4last_s01']

    def validate(self, instance_filename):
        """JFCS data format validation process"""
        copy_instance_stream = copy.copy(instance_filename)
        results = self.schemaTest(copy_instance_stream, self.service_event_schema_filename)
        if results == True:
            fileutils.makeBlock('JFCS service event XML data found.  Determined by service event schema.')
            JFCSXMLInputReader.data_type = 'service_event'
            return results
        results = self.schemaTest(copy_instance_stream, self.client_schema_filename)
        if results == True:
            fileutils.makeBlock('JFCS client XML data found.  Determined by client schema.')
            JFCSXMLInputReader.data_type = 'client'
            return results
        try:
            results = self.elementTest(copy_instance_stream, self.service_elements)
            if results == True:
                fileutils.makeBlock('JFCS service event XML data found.  Determined by service event elements.')
                JFCSXMLInputReader.data_type = 'service_event'
                return results
            results = self.elementTest(copy_instance_stream, self.client_elements)
            if results == True:
                fileutils.makeBlock('JFCS client XML data found.  Determined by client elements.')
                JFCSXMLInputReader.data_type = 'client'
                return results
        except Exception, exception:
            print 'XML Syntax Error.  There appears to be malformed XML.    ', exception

        return False

    def schemaTest(self, copy_instance_stream, schema_filename):
        """Attempt to validate input file against specific schema"""
        schema = open(schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(copy_instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.    ', error

        return False

    def elementTest(self, copy_instance_stream, elements):
        """Attempt to find elements in the input file by searching the tree"""
        xml_doc = etree.parse(copy_instance_stream)
        for e in elements:
            search_term = './/' + e
            if xml_doc.find(search_term) is None:
                return False

        return True


class PARXMLTest:
    """Load in the HUD HMIS Extended Schema for Operation PAR"""

    def __init__(self):
        self.name = 'PARXML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['operation_par_xml']

    def find_elements_by_type(self, schema_doc, type_content):
        element_names = schema_doc.xpath('//xsd:element[@type != $n]/@name', namespaces={'xsd': 'http://www.w3.org/2001/XMLSchema', 'ext': 'http://xsd.alexandriaconsulting.com/cgi-bin/trac.cgi/export/344/trunk/synthesis/xsd/Operation_PAR_Extend_HUD_HMIS_2_8.xsd', 'hmis': 'http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd'}, n=type_content)
        return element_names

    def validate(self, instance_stream):
        """This specific data format's validation process."""
        schema = open(self.schema_filename, 'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        copy_instance_stream = copy.copy(instance_stream)
        xml_doc = etree.parse(copy_instance_stream)
        ext_namespace_check = xml_doc.xpath('/ext:SourceDatabase', namespaces={'ext': 'http://xsd.alexandriaconsulting.com/cgi-bin/trac.cgi/export/344/trunk/synthesis/xsd/Operation_PAR_Extend_HUD_HMIS_2_8.xsd'})
        if len(ext_namespace_check) != 1:
            return False
        else:
            try:
                instance_parsed = etree.parse(copy_instance_stream)
                results = schema_parsed_xsd.validate(instance_parsed)
                if results == True:
                    schema_hudhmis_filename = settings.SCHEMA_DOCS['hud_hmis_2_8_xml']
                    schema_hudhmis_raw = open(schema_hudhmis_filename, 'r')
                    schema_hudhmis_parsed = etree.parse(schema_hudhmis_raw)
                    elements_string50 = self.find_elements_by_type(schema_parsed, 'hmis:string50')
                    elements_string50_ns = []
                    for e in elements_string50:
                        elem_with_ns = '{http://xsd.alexandriaconsulting.com/cgi-bin/trac.cgi/export/344/trunk/synthesis/xsd/Operation_PAR_Extend_HUD_HMIS_2_8.xsd}' + e
                        elements_string50_ns.append(elem_with_ns)

                    elements_string50 = self.find_elements_by_type(schema_hudhmis_parsed, 'hmis:string50')
                    for e in elements_string50:
                        elem_with_ns = '{http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd}' + e
                        elements_string50_ns.append(elem_with_ns)

                    elements_maxlength = elements_string50_ns
                    xml_root = xml_doc.getroot()
                    for e in xml_root.iter():
                        if str(e.tag) in elements_maxlength:
                            if len(e.text) > 32:
                                print 'XML Error.  Value %s exceeds database field length.' % str(e.tag)
                                return False

                    fileutils.makeBlock('The Operation PAR XML successfully validated.')
                    return results
                if results == False:
                    print 'The xml did not successfully validate against                 Operation PAR XML.'
                    try:
                        detailed_results = schema_parsed_xsd.assertValid(instance_parsed)
                        print detailed_results
                        return results
                    except etree.DocumentInvalid, error:
                        print 'Document Invalid Exception.  Here is the detail:'
                        print error
                        return results

                if results == None:
                    print "The validator erred and couldn't determine if the xml                 was either valid or invalid."
                    return results
            except etree.XMLSyntaxError, error:
                print 'XML Syntax Error.  There appears to be malformed XML.  ',
                print error
                raise

            return


class HUDHMIS28XMLInputReader(HMISXML28Reader):

    def __init__(self, instance_filename):
        self.reader = HMISXML28Reader(instance_filename)

    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree)
        except:
            raise


class HUDHMIS30XMLInputReader(HMISXML30Reader):

    def __init__(self, instance_filename):
        self.reader = HMISXML30Reader(instance_filename)

    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree)
        except:
            raise


class OCCHUDHMIS30XMLInputReader(OCCHUDHMISXML30Reader):

    def __init__(self, instance_filename):
        self.reader = OCCHUDHMISXML30Reader(instance_filename)
        if settings.DEBUG:
            print 'self.reader to be read is: ', self.reader

    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree)
        except:
            raise


class JFCSXMLInputReader(JFCSXMLReader):

    def __init__(self, instance_filename):
        self.reader = JFCSXMLReader(instance_filename)

    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree, self.data_type)
        except:
            raise


class VendorXMLInputReader:

    def __init__(self, xml_instance_file):
        self.name = 'Vendor XML'

    def shred(self):
        """implementation of interface's shred method"""
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to shred the XML Document: %s' % self.instance_filename
        return False