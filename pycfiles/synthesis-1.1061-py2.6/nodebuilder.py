# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/nodebuilder.py
# Compiled at: 2010-12-12 18:24:12
from conf import settings
import clsexceptions, dbobjects
from selector import HUDHMIS30XMLTest, HUDHMIS28XMLTest, JFCSXMLTest, VendorXMLTest, SVCPOINT406XMLTest, SVCPOINT20XMLTest
from errcatalog import catalog
import os
from queryobject import QueryObject
from conf import outputConfiguration
import clspostprocessing, fileutils
from emailprocessor import XMLProcessorNotifier
from datetime import datetime
import iniutils
from hmisxml30writer import HMISXMLWriter
from hmisxml28writer import HMISXML28Writer
hmiscsv30writer_loaded = False
hmisxml28writer_loaded = False
hmisxml30writer_loaded = False
svcptxml20writer_loaded = False
svcptxml406writer_loaded = False
jfcsxmlwriter_loaded = False

class NodeBuilder(dbobjects.DatabaseObjects):

    def __init__(self, queryOptions):
        print 'initializing nodebuilder'
        dbobjects.DatabaseObjects()
        generateOutputformat = outputConfiguration.Configuration[queryOptions.configID]['outputFormat']
        self.transport = outputConfiguration.Configuration[queryOptions.configID]['transportConfiguration']
        self.queryOptions = queryOptions
        if generateOutputformat == 'svcpoint406':
            try:
                from svcpointxml_406_writer import SVCPOINTXMLWriter
                svcptxml406writer_loaded = True
                print 'import of Svcpt XML Writer, version 4.06 was successful'
            except:
                print 'import of Svcpt XML Writer, version 4.06 failed'
                svcptxml406writer_loaded = False
            else:
                self.writer = SVCPOINTXMLWriter(settings.OUTPUTFILES_PATH, queryOptions)
                self.validator = SVCPOINT406XMLTest()
        elif generateOutputformat == 'hmisxml28':
            try:
                from hmisxml28writer import HMISXML28Writer
                hmisxml28writer_loaded = True
            except:
                print 'import of HMISXMLWriter, version 2.8, failed'
                hmisxml28writer_loaded = False
            else:
                if settings.DEBUG:
                    print 'settings.OUTPUTFILES_PATH is ', settings.OUTPUTFILES_PATH
                self.writer = HMISXML28Writer(settings.OUTPUTFILES_PATH, queryOptions)
                self.validator = HUDHMIS28XMLTest()
        elif generateOutputformat == 'hmisxml30':
            try:
                from hmisxml30writer import HMISXMLWriter
                print 'import of HMISXMLWriter, version 3.0 occurred successfully'
                hmisxml30writer_loaded = True
            except Exception, e:
                print 'import of HMISXMLWriter, version 3.0, failed', e
                hmisxml30writer_loaded = False
            else:
                if settings.DEBUG:
                    print 'settings.OUTPUTFILES_PATH is ', settings.OUTPUTFILES_PATH
                self.writer = HMISXMLWriter(settings.OUTPUTFILES_PATH, queryOptions)
                self.validator = HUDHMIS30XMLTest()
        elif generateOutputformat == 'hmiscsv30':
            try:
                from hmiscsv30writer import HmisCsv30Writer
                hmiscsv30writer_loaded = True
            except:
                hmiscsv30writer_loaded = False
            else:
                self.writer = HmisCsv30Writer(settings.OUTPUTFILES_PATH, queryOptions, debug=True)
        elif generateOutputformat == 'jfcsxml':
            print 'Need to hook up the JFCSWriter in Nodebuilder'
        else:
            err = catalog.errorCatalog[1001]
            raise clsexceptions.UndefinedXMLWriter, (err[0], err[1], 'NodeBuilder.__init__() ' + generateOutputformat)
        self.pprocess = clspostprocessing.ClsPostProcessing(queryOptions.configID)

    def run(self):
        """This is the main method controlling this entire program."""
        if self.writer.write():
            filesToTransfer = fileutils.grabFiles(os.path.join(settings.OUTPUTFILES_PATH, '*.xml'))
            validFiles = []
            for eachFile in filesToTransfer:
                fs = open(eachFile, 'r')
                if self.validator.validate(fs):
                    validFiles.append(eachFile)
                    print 'oK'
                fs.close()

            if self.transport == '':
                print 'Output Complete...Please see output files: %s' % filesToTransfer
            if self.transport == 'sys.stdout':
                for eachFile in validFiles:
                    fs = open(eachFile, 'r')
                    lines = fs.readlines()
                    fs.close()
                    for line in lines:
                        print line

            if self.transport == 'sftp':
                self.pprocess.processFileSFTP(validFiles)
            elif self.transport == 'email':
                for eachFile in validFiles:
                    self.email = XMLProcessorNotifier('', eachFile)
                    msgBody = self.formatMsgBody()
                    self.email.sendDocumentAttachment('Your report results', msgBody, eachFile)

            elif self.transport == 'vpnftp':
                if len(validFiles) > 0:
                    pd = iniutils.LoadConfig('fileConverter.ini')
                    self.pprocess.setINI(pd)
                    self.pprocess.processFileVPN(validFiles)
            elif self.transport == 'vpncp':
                pass

    def formatMsgBody(self):
        msgBody = 'Your report was requested on %s. /r/nThe report criteria is: \r\n\t StartDate: %s /r/n \t EndDate: %s /r/n /t Previously Reported: %s /r/n /t Previously UnReported: %s' % (
         datetime.today(), self.queryOptions.startDate, self.queryOptions.endDate, self.queryOptions.reported, self.queryOptions.unreported)

    def selectNodes(self, start_date, end_date, nodename):
        pass

    def flagNodes(self):
        pass


if hmisxml30writer_loaded is True:

    class HmisXmlWriter(HMISXMLWriter):

        def __init__(self):
            self.xML = HMISXMLWriter(os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH))

        def write(self):
            pass


if hmisxml28writer_loaded is True:

    class HmisXmlWriter(HMISXML28Writer):

        def __init__(self):
            self.xML = HMISXML28Writer(os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH))

        def write(self):
            pass


if __name__ == '__main__':
    optParse = QueryObject()
    options = optParse.getOptions()
    if options != None:
        try:
            NODEBUILDER = NodeBuilder(options)
            RESULTS = NODEBUILDER.run()
        except clsexceptions.UndefinedXMLWriter:
            print 'Please specify a format for outputting your XML'
            raise

# global hmiscsv30writer_loaded ## Warning: Unused global
# global hmisxml28writer_loaded ## Warning: Unused global
# global hmisxml30writer_loaded ## Warning: Unused global
# global jfcsxmlwriter_loaded ## Warning: Unused global
# global svcptxml20writer_loaded ## Warning: Unused global
# global svcptxml406writer_loaded ## Warning: Unused global