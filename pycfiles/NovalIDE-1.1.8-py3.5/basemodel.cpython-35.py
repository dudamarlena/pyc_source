# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/project/basemodel.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 22838 bytes
import copy, os, os.path, noval.util.xmlutils as xmlutils, noval.util.logger as logger, noval.util.apputils as sysutilslib
from noval.consts import PROJECT_NAMESPACE_URL
import noval.python.parser.utils as parserutils, noval.util.utils as utils
PROJECT_VERSION_050730 = '10'
PROJECT_VERSION_050826 = '11'
PROJECT_VERSION_190719 = '12'

class BaseProject(object):
    __xmlname__ = 'project'
    __xmlexclude__ = ('fileName', '_projectDir', '_getDocCallback', '_cacheEnabled',
                      '_startupfile')
    __xmlattributes__ = ('_homeDir', 'version', 'name', 'id')
    __xmlrename__ = {'_homeDir': 'homeDir', '_appInfo': 'appInfo'}
    __xmlflattensequence__ = {'_files': ('file', )}
    __xmldefaultnamespace__ = xmlutils.AG_NS_URL
    __xmlattrnamespaces__ = {PROJECT_NAMESPACE_URL: ['version', '_homeDir']}

    def __init__(self):
        self.__xmlnamespaces__ = {PROJECT_NAMESPACE_URL: xmlutils.AG_NS_URL}
        self.version = PROJECT_VERSION_190719
        self._files = []
        self._projectDir = None
        self._homeDir = None
        self._cacheEnabled = 0
        self.name = ''
        self.id = ''
        self._startupfile = None
        self._properties = ProjectProperty(self)
        self._runinfo = RunInfo(self)

    def GetPropertiPages(self):
        return self._properties._pages

    @property
    def RunInfo(self):
        return self._runinfo

    @property
    def StartupFile(self):
        return self._startupfile

    @StartupFile.setter
    def StartupFile(self, startupfile):
        if self._startupfile is not None:
            self._startupfile.IsStartup = False
        self._startupfile = startupfile
        if self._startupfile is not None:
            self._startupfile.IsStartup = True
            self._runinfo.StartupFile = self.GetRelativePath(self._startupfile)

    @property
    def Id(self):
        return self.id

    @Id.setter
    def Id(self, project_id):
        self.id = project_id

    @property
    def Name(self):
        return self.name

    @Name.setter
    def Name(self, name):
        self.name = name

    def initialize(self):
        for file in self._files:
            file._parentProj = self

    def __copy__(self):
        clone = Project()
        clone._files = [copy.copy(file) for file in self._files]
        clone._projectDir = self._projectDir
        clone._homeDir = self._homeDir
        if not ACTIVEGRID_BASE_IDE:
            clone._appInfo = copy.copy(self._appInfo)
        return clone

    def GetAppInfo(self):
        return self._appInfo

    def AddFile(self, filePath=None, logicalFolder=None, type=None, name=None, file=None):
        """ Usage: self.AddFile(filePath, logicalFolder, type, name)  # used for initial generation of object
                   self.AddFile(file=xyzFile)  # normally used for redo/undo
            Add newly created file object using filePath and logicalFolder or given file object
        """
        if file:
            self._files.append(file)
        else:
            self._files.append(ProjectFile(self, filePath, logicalFolder, type, name, getDocCallback=None))

    def RemoveFile(self, file):
        if file.IsStartup:
            self.StartupFile = None
        self._files.remove(file)

    def FindFile(self, filePath):
        if filePath:
            for file in self._files:
                if parserutils.ComparePath(file.filePath, filePath):
                    return file

    def GetRelativePath(self, pj_file):
        if isinstance(pj_file, ProjectFile):
            filepath = pj_file.filePath
        else:
            filepath = pj_file
        return filepath.replace(self.homeDir, '').lstrip(os.sep)

    def _GetFilePaths(self):
        return [file.filePath for file in self._files]

    filePaths = property(_GetFilePaths)

    def _GetProjectFiles(self):
        return self._files

    projectFiles = property(_GetProjectFiles)

    def _GetLogicalFolders(self):
        folders = []
        for file in self._files:
            if file.logicalFolder and file.logicalFolder not in folders:
                folders.append(file.logicalFolder)

        return folders

    logicalFolders = property(_GetLogicalFolders)

    def _GetPhysicalFolders(self):
        physicalFolders = []
        for file in self._files:
            physicalFolder = file.physicalFolder
            if physicalFolder and physicalFolder not in physicalFolders:
                physicalFolders.append(physicalFolder)

        return physicalFolders

    physicalFolders = property(_GetPhysicalFolders)

    def _GetHomeDir(self):
        if self._homeDir:
            return self._homeDir
        else:
            return self._projectDir

    def _SetHomeDir(self, parentPath):
        self._homeDir = parentPath

    def _IsDefaultHomeDir(self):
        return self._homeDir == None

    isDefaultHomeDir = property(_IsDefaultHomeDir)
    homeDir = property(_GetHomeDir, _SetHomeDir)

    def GetRelativeFolders(self):
        relativeFolders = []
        for file in self._files:
            relFolder = file.GetRelativeFolder(self.homeDir)
            if relFolder and relFolder not in relativeFolders:
                relativeFolders.append(relFolder)

        return relativeFolders

    def AbsToRelativePath(self):
        for file in self._files:
            file.AbsToRelativePath(self.homeDir)

    def RelativeToAbsPath(self):
        for file in self._files:
            file.RelativeToAbsPath(self.homeDir)

    def _SetCache(self, enable):
        """
            Only turn this on if your operation assumes files on disk won't change.
            Once your operation is done, turn this back off.
            Nested enables are allowed, only the last disable will disable the cache.
            
            This bypasses the IsDocumentModificationDateCorrect call because the modification date check is too costly, it hits the disk and takes too long.
        """
        if enable:
            if self._cacheEnabled == 0:
                for file in self._files:
                    file.ClearCache()

            self._cacheEnabled += 1
        else:
            self._cacheEnabled -= 1

    def _GetCache(self):
        return self._cacheEnabled > 0

    cacheEnabled = property(_GetCache, _SetCache)

    def fullPath(self, fileName):
        if os.path.isabs(fileName):
            absPath = fileName
        else:
            if self.homeDir:
                absPath = os.path.join(self.homeDir, fileName)
            else:
                absPath = os.path.abspath(fileName)
        return os.path.normpath(absPath)

    def documentRefFactory(self, name, fileType, filePath):
        return ProjectFile(self, filePath=self.fullPath(filePath), type=fileType, name=name, getDocCallback=self._getDocCallback)

    def findAllRefs(self):
        return self._files

    def GetXFormsDirectory(self):
        forms = self.findRefsByFileType(basedocmgr.FILE_TYPE_XFORM)
        filePaths = map(lambda form: form.filePath, forms)
        xformdir = os.path.commonprefix(filePaths)
        if not xformdir:
            xformdir = self.homeDir
        return xformdir

    def setRefs(self, files):
        self._files = files

    def findRefsByFileType(self, fileType):
        fileList = []
        for file in self._files:
            if fileType == file.type:
                fileList.append(file)

        return fileList

    def GenerateServiceRefPath(self, wsdlFilePath):
        import wx
        from WsdlAgEditor import WsdlAgDocument
        ext = WsdlAgDocument.WSDL_AG_EXT
        for template in wx.GetApp().GetDocumentManager().GetTemplates():
            if template.GetDocumentType() == WsdlAgDocument:
                ext = template.GetDefaultExtension()
                break

        wsdlAgFilePath = os.path.splitext(wsdlFilePath)[0] + ext
        return wsdlAgFilePath

    def SetDocCallback(self, getDocCallback):
        self._getDocCallback = getDocCallback
        for file in self._files:
            file._getDocCallback = getDocCallback


class Project(BaseProject):
    pass


class ProjectFile(object):
    __xmlname__ = 'file'
    __xmlexclude__ = ('_parentProj', '_getDocCallback', '_docCallbackCacheReturnValue',
                      '_docModelCallbackCacheReturnValue', '_doc', 'isStartup')
    __xmlattributes__ = ['filePath', 'logicalFolder', 'type', 'name']
    __xmldefaultnamespace__ = xmlutils.AG_NS_URL

    def __init__(self, parent=None, filePath=None, logicalFolder=None, type=None, name=None, getDocCallback=None):
        self._parentProj = parent
        self.filePath = filePath
        self.logicalFolder = logicalFolder
        self.type = type
        self.name = name
        self._getDocCallback = getDocCallback
        self._docCallbackCacheReturnValue = None
        self._docModelCallbackCacheReturnValue = None
        self._doc = None
        self.isStartup = False

    @property
    def IsStartup(self):
        if type(self.isStartup) == str:
            return False
        return self.isStartup

    @IsStartup.setter
    def IsStartup(self, is_startup):
        self.isStartup = is_startup

    def _GetDocumentModel(self):
        if self._docCallbackCacheReturnValue and (self._parentProj.cacheEnabled or self._docCallbackCacheReturnValue.IsDocumentModificationDateCorrect()):
            return self._docModelCallbackCacheReturnValue
        if self._getDocCallback:
            self._docCallbackCacheReturnValue, self._docModelCallbackCacheReturnValue = self._getDocCallback(self.filePath)
            return self._docModelCallbackCacheReturnValue

    document = property(_GetDocumentModel)

    def _GetDocument(self):
        if self._docCallbackCacheReturnValue and (self._parentProj.cacheEnabled or self._docCallbackCacheReturnValue.IsDocumentModificationDateCorrect()):
            return self._docCallbackCacheReturnValue
        if self._getDocCallback:
            self._docCallbackCacheReturnValue, self._docModelCallbackCacheReturnValue = self._getDocCallback(self.filePath)
            return self._docCallbackCacheReturnValue

    ideDocument = property(_GetDocument)

    def ClearCache(self):
        self._docCallbackCacheReturnValue = None
        self._docModelCallbackCacheReturnValue = None

    def _typeEnumeration(self):
        return basedocmgr.FILE_TYPE_LIST

    def _GetPhysicalFolder(self):
        dir = None
        if self.filePath:
            dir = os.path.dirname(self.filePath)
            if os.sep != '/':
                dir = dir.replace(os.sep, '/')
        return dir

    physicalFolder = property(_GetPhysicalFolder)

    def GetRelativeFolder(self, parentPath):
        parentPathLen = len(parentPath)
        dir = None
        if self.filePath:
            dir = os.path.dirname(self.filePath)
            if dir.startswith(parentPath + os.sep):
                dir = '.' + dir[parentPathLen:]
            if os.sep != '/':
                dir = dir.replace(os.sep, '/')
        return dir

    def AbsToRelativePath(self, parentPath):
        """ Used to convert path to relative path for saving (disk format) """
        parentPathLen = len(parentPath)
        if self.filePath.startswith(parentPath + os.sep):
            self.filePath = '.' + self.filePath[parentPathLen:]
            if os.sep != '/':
                self.filePath = self.filePath.replace(os.sep, '/')

    def RelativeToAbsPath(self, parentPath):
        """ Used to convert path to absolute path (for any necessary disk access) """
        if self.filePath.startswith('./'):
            self.filePath = os.path.normpath(os.path.join(parentPath, self.filePath))

    def _GetDoc(self):
        import wx, wx.lib.docview
        if not self._doc:
            docMgr = wx.GetApp().GetDocumentManager()
            try:
                doc = docMgr.CreateDocument(self.filePath, docMgr.GetFlags() | wx.lib.docview.DOC_SILENT | wx.lib.docview.DOC_OPEN_ONCE | wx.lib.docview.DOC_NO_VIEW)
                if doc == None:
                    docs = docMgr.GetDocuments()
                    for d in docs:
                        if d.GetFilename() == self.filePath:
                            doc = d
                            break

                self._doc = doc
            except Exception as e:
                logger.reportException(e, stacktrace=True)

        return self._doc

    def _GetLocalServiceProcessName(self):
        doc = self._GetDoc()
        if doc:
            return doc.GetModel().processName
        else:
            return

    processName = property(_GetLocalServiceProcessName)

    def _GetStateful(self):
        return self._GetDoc().GetModel().stateful

    def _SetStateful(self, stateful):
        self._GetDoc().GetModel().stateful = stateful

    stateful = property(_GetStateful, _SetStateful)

    def _GetLocalServiceCodeFile(self):
        return self._GetDoc().GetModel().localServiceCodeFile

    def _SetLocalServiceCodeFile(self, codefile):
        self._GetDoc().GetModel().localServiceCodeFile = codefile

    localServiceCodeFile = property(_GetLocalServiceCodeFile, _SetLocalServiceCodeFile)

    def _GetLocalServiceClassName(self):
        return self._GetDoc().GetModel().localServiceClassName

    def _SetLocalServiceClassName(self, className):
        self._GetDoc().GetModel().localServiceClassName = className

    localServiceClassName = property(_GetLocalServiceClassName, _SetLocalServiceClassName)

    def getServiceParameter(self, message, part):
        return self._GetDoc().GetModel().getServiceParameter(message, part)

    def _GetServiceRefServiceType(self):
        doc = self._GetDoc()
        if not doc:
            return
        else:
            model = doc.GetModel()
            if hasattr(model, 'serviceType'):
                return model.serviceType
            return

    def _SetServiceRefServiceType(self, serviceType):
        self._GetDoc().GetModel().serviceType = serviceType

    serviceType = property(_GetServiceRefServiceType, _SetServiceRefServiceType)

    def getExternalPackage(self):
        import activegrid.model.projectmodel as projectmodel, wx, ProjectEditor
        appInfo = self._GetDoc().GetAppInfo()
        if appInfo.language == None:
            language = wx.ConfigBase_Get().Read(ProjectEditor.APP_LAST_LANGUAGE, projectmodel.LANGUAGE_DEFAULT)
        else:
            language = appInfo.language
        if language == projectmodel.LANGUAGE_PYTHON:
            suffix = '.py'
        elif language == projectmodel.LANGUAGE_PHP:
            suffix = '.php'
        pyFilename = self.name + suffix
        return self._GetDoc().GetAppDocMgr().fullPath(pyFilename)


class ProjectProperty(object):
    __xmlexclude__ = ('_parentProj', )
    __xmlname__ = 'property'
    __xmlflattensequence__ = {'_pages': ('page', )}
    __xmlattributes__ = []
    __xmldefaultnamespace__ = xmlutils.AG_NS_URL

    def __init__(self, parent=None):
        self._parentProj = parent
        self._pages = []

    def AddPage(self, name, item, objclass):
        page = PropertyPage(name, item, objclass, self)
        self._pages.append(page)


class PropertyPage(object):
    __xmlexclude__ = ('_parentProj', )
    __xmlname__ = 'page'
    __xmlattributes__ = ['name', 'item', 'objclass']
    __xmldefaultnamespace__ = xmlutils.AG_NS_URL

    def __init__(self, name=None, item=None, objclass=None, parent=None):
        self._parentProj = parent
        self.name = name
        self.item = item
        self.objclass = objclass


class RunInfo(object):
    __xmlexclude__ = ('_parentProj', )
    __xmlname__ = 'runInfo'
    __xmldefaultnamespace__ = xmlutils.AG_NS_URL

    def __init__(self, parent=None):
        self._parentProj = parent
        self.RunConfig = None
        self.StartupFile = None
        self.DocumentTemplate = None


class Project_10:
    __doc__ = ' Version 1.0, kept for upgrading to latest version.  Over time, this should be deprecated. '
    __xmlname__ = 'project'
    __xmlrename__ = {'_files': 'files'}
    __xmlexclude__ = ('fileName', )
    __xmlattributes__ = ['version']

    def __init__(self):
        self.version = PROJECT_VERSION_050730
        self._files = []

    def initialize(self):
        """ Required method for xmlmarshaller """
        pass

    def upgradeVersion(self):
        currModel = Project()
        for file in self._files:
            currModel._files.append(ProjectFile(currModel, file))

        return currModel


def load(fileObject):
    version = xmlutils.getAgVersion(fileObject.name)
    if version >= PROJECT_VERSION_050826:
        fileObject.seek(0)
        project = xmlutils.load(fileObject.name, knownTypes=KNOWNTYPES, knownNamespaces=xmlutils.KNOWN_NAMESPACES, createGenerics=True)
    else:
        if version == PROJECT_VERSION_050730:
            fileObject.seek(0)
            project = xmlutils.load(fileObject.name, knownTypes={'project': Project_10}, createGenerics=True)
            project = project.upgradeVersion()
        else:
            fileObject.seek(0)
            project = xmlutils.load(fileObject.name, knownTypes={'project': Project_10}, createGenerics=True)
            if project:
                project = project.upgradeVersion()
            else:
                return
    if project:
        project._projectDir = os.path.dirname(fileObject.name)
        project.RelativeToAbsPath()
    return project


def save(fileObject, project, productionDeployment=False):
    if not project._projectDir:
        project._projectDir = os.path.dirname(fileObject.name)
    if isinstance(project._projectDir, str) and utils.is_py2():
        project._projectDir = project._projectDir.decode('utf-8')
    project.AbsToRelativePath()
    savedHomeDir = project.homeDir
    if productionDeployment:
        project.homeDir = None
    xmlutils.save(fileObject.name, project, prettyPrint=True, knownTypes=KNOWNTYPES, knownNamespaces=xmlutils.KNOWN_NAMESPACES)
    if productionDeployment:
        project.homeDir = savedHomeDir
    project.RelativeToAbsPath()