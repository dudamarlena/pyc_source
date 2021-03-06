# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\envs\Test\lib\arelle\ModelManager.py
# Compiled at: 2018-03-15 06:25:35
# Size of source mod 2**32: 10990 bytes
__doc__ = '\nCreated on Oct 3, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import gc, sys, traceback, logging
from arelle import ModelXbrl, Validate, DisclosureSystem, PackageManager
from arelle.PluginManager import pluginClassMethods

def initialize(cntlr):
    modelManager = ModelManager(cntlr)
    modelManager.modelXbrl = None
    return modelManager


class ModelManager:
    """ModelManager"""

    def __init__(self, cntlr):
        self.cntlr = cntlr
        self.validateDisclosureSystem = False
        self.disclosureSystem = DisclosureSystem.DisclosureSystem(self)
        self.validateCalcLB = False
        self.validateInferDecimals = True
        self.validateDedupCalcs = False
        self.validateInfoset = False
        self.validateUtr = False
        self.skipDTS = False
        self.skipLoading = None
        self.abortOnMajorError = False
        self.collectProfileStats = False
        self.loadedModelXbrls = []
        from arelle import Locale
        self.locale = Locale.getUserLocale(cntlr.config.get('userInterfaceLocaleOverride', ''))
        self.defaultLang = Locale.getLanguageCode()
        self.customTransforms = None

    def shutdown(self):
        self.status = 'shutdown'

    def addToLog(self, message, messageCode='', file='', refs=[], level=logging.INFO):
        """Add a simple info message to the default logger
           
        :param message: Text of message to add to log.
        :type message: str
        :param messageCode: Message code (e.g., a prefix:id of a standard error)
        :param messageCode: str
        :param file: File name (and optional line numbers) pertaining to message
        :param refs: [{"href":file,"sourceLine":lineno},...] pertaining to message
        :type file: str
        """
        self.cntlr.addToLog(message, messageCode=messageCode, file=file, refs=refs, level=level)

    def showStatus(self, message, clearAfter=None):
        """Provide user feedback on status line of GUI or web page according to type of controller.
        
        :param message: Message to display on status widget.
        :type message: str
        :param clearAfter: Time, in ms., after which to clear the message (e.g., 5000 for 5 sec.)
        :type clearAfter: int
        """
        self.cntlr.showStatus(message, clearAfter)

    def viewModelObject(self, modelXbrl, objectId):
        """Notify any active views to show and highlight selected object.  Generally used
        to scroll list control to object and highlight it, or if tree control, to find the object
        and open tree branches as needed for visibility, scroll to and highlight the object.
           
        :param modelXbrl: ModelXbrl (DTS) whose views are to be notified
        :type modelXbrl: ModelXbrl
        :param objectId: Selected object id (string format corresponding to ModelObject.objectId() )
        :type objectId: str
        """
        self.cntlr.viewModelObject(modelXbrl, objectId)

    def reloadViews(self, modelXbrl):
        """Notify all active views to reload and redisplay their entire contents.  May be used
        when loaded model is changed significantly, or when individual object change notifications
        (by viewModelObject) would be difficult to identify or too numerous.
           
        :param modelXbrl: ModelXbrl (DTS) whose views are to be reloaded
        :type modelXbrl: ModelXbrl
        """
        self.cntlr.reloadViews(modelXbrl)

    def load(self, filesource, nextaction=None, taxonomyPackages=None, **kwargs):
        """Load an entry point modelDocument object(s), which in turn load documents they discover 
        (for the case of instance, taxonomies, and versioning reports), but defer loading instances 
        for test case and RSS feeds.  
        
        The modelXbrl that is loaded is 'stacked', by this class, so that any modelXbrl operations such as validate, 
        and close, operate on the most recently loaded modelXbrl, and compareDTSes operates on the two 
        most recently loaded modelXbrl's.
        
        :param filesource: may be a FileSource object, with the entry point selected, or string file name (or web URL). 
        :type filesource: FileSource or str
        :param nextAction: status line text string, if any, to show upon completion
        :type nextAction: str
        :param taxonomyPackages: array of URLs of taxonomy packages required for load operation
        """
        if taxonomyPackages:
            resetPackageMappings = False
            for pkgUrl in taxonomyPackages:
                if PackageManager.addPackage(self.cntlr, pkgUrl):
                    resetPackageMappings = True

            if resetPackageMappings:
                PackageManager.rebuildRemappings(self.cntlr)
        try:
            if filesource.url.startswith('urn:uuid:'):
                for modelXbrl in self.loadedModelXbrls:
                    if not modelXbrl.isClosed:
                        if modelXbrl.uuid == filesource.url:
                            return modelXbrl

                raise IOError(_('Open file handle is not open: {0}').format(filesource.url))
        except AttributeError:
            pass

        self.filesource = filesource
        modelXbrl = None
        for customLoader in pluginClassMethods('ModelManager.Load'):
            modelXbrl = customLoader(self, filesource)
            if modelXbrl is not None:
                break

        if modelXbrl is None:
            modelXbrl = (ModelXbrl.load)(self, filesource, nextaction, **kwargs)
        self.modelXbrl = modelXbrl
        self.loadedModelXbrls.append(self.modelXbrl)
        return self.modelXbrl

    def saveDTSpackage(self, allDTSes=False):
        if allDTSes:
            for modelXbrl in self.loadedModelXbrls:
                modelXbrl.saveDTSpackage()

        elif self.modelXbrl is not None:
            self.modelXbrl.saveDTSpackage()

    def create(self, newDocumentType=None, url=None, schemaRefs=None, createModelDocument=True, isEntry=False, errorCaptureLevel=None, initialXml=None, base=None):
        self.modelXbrl = ModelXbrl.create(self, newDocumentType=newDocumentType, url=url, schemaRefs=schemaRefs, createModelDocument=createModelDocument, isEntry=isEntry,
          errorCaptureLevel=errorCaptureLevel,
          initialXml=initialXml,
          base=base)
        self.loadedModelXbrls.append(self.modelXbrl)
        return self.modelXbrl

    def validate(self):
        """Validates the most recently loaded modelXbrl (according to validation properties).
        
        Results of validation will be in log.
        """
        try:
            if self.modelXbrl:
                Validate.validate(self.modelXbrl)
        except Exception as err:
            self.addToLog(_('[exception] Validation exception: {0} at {1}').format(err, traceback.format_tb(sys.exc_info()[2])))

    def compareDTSes(self, versReportFile, writeReportFile=True):
        """Compare two most recently loaded DTSes, saving versioning report in to the file name provided.
        
        :param versReportFile: file name in which to save XBRL Versioning Report
        :type versReportFile: str
        :param writeReportFile: False to prevent writing XBRL Versioning Report file
        :type writeReportFile: bool
        """
        from arelle.ModelVersReport import ModelVersReport
        if len(self.loadedModelXbrls) >= 2:
            fromDTS = self.loadedModelXbrls[(-2)]
            toDTS = self.loadedModelXbrls[(-1)]
            from arelle.ModelDocument import Type
            modelVersReport = self.create(newDocumentType=(Type.VERSIONINGREPORT), url=versReportFile,
              createModelDocument=False)
            ModelVersReport(modelVersReport).diffDTSes(versReportFile, fromDTS, toDTS)
            return modelVersReport

    def close(self, modelXbrl=None):
        """Closes the specified or most recently loaded modelXbrl
        
        :param modelXbrl: Specific ModelXbrl to be closed (defaults to last opened ModelXbrl)
        :type modelXbrl: ModelXbrl
        """
        if modelXbrl is None:
            modelXbrl = self.modelXbrl
        if modelXbrl:
            while modelXbrl in self.loadedModelXbrls:
                self.loadedModelXbrls.remove(modelXbrl)

            if modelXbrl == self.modelXbrl:
                if len(self.loadedModelXbrls) > 0:
                    self.modelXbrl = self.loadedModelXbrls[0]
                else:
                    self.modelXbrl = None
            modelXbrl.close()
            gc.collect()

    def loadCustomTransforms(self):
        if self.customTransforms is None:
            self.customTransforms = {}
            for pluginMethod in pluginClassMethods('ModelManager.LoadCustomTransforms'):
                pluginMethod(self.customTransforms)