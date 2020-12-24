# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/renderer.py
# Compiled at: 2009-09-30 05:37:25
import zipfile, shutil, xml.sax, os, os.path, re
from UserDict import UserDict
import appy.pod
from appy.pod import PodError
from appy.shared.xml_parser import XmlElement
from appy.pod.pod_parser import PodParser, PodEnvironment, OdInsert
from appy.pod.converter import ODT_FILE_TYPES
from appy.pod.buffers import FileBuffer
from appy.pod.xhtml2odt import Xhtml2OdtConverter
from appy.pod.doc_importers import OdtImporter, ImageImporter, PdfImporter
from appy.pod.styles_manager import StylesManager
from appy.shared.utils import FolderDeleter
BAD_CONTEXT = 'Context must be either a dict, a UserDict or an instance.'
RESULT_FILE_EXISTS = 'Result file "%s" exists.'
CANT_WRITE_RESULT = 'I cannot write result file "%s". %s'
TEMP_FOLDER_EXISTS = 'I need to use a temp folder "%s" but this folder already exists.'
CANT_WRITE_TEMP_FOLDER = 'I cannot create temp folder "%s". %s'
NO_PY_PATH = 'Extension of result file is "%s". In order to perform conversion from ODT to this format we need to call OpenOffice. But the Python interpreter which runs the current script does not know UNO, the library that allows to connect to OpenOffice in server mode. If you can\'t install UNO in this Python interpreter, you can specify, in parameter "pythonWithUnoPath", the path to a UNO-enabled Python interpreter. One such interpreter may be found in <open_office_path>/program.'
PY_PATH_NOT_FILE = '"%s" is not a file. You must here specify the absolute path of a Python interpreter (.../python, .../python.sh, .../python.exe, .../python.bat...).'
BLANKS_IN_PATH = 'Blanks were found in path "%s". Please use the DOS-names (ie, "progra~1" instead of "Program files" or "docume~1" instead of "Documents and settings".'
BAD_RESULT_TYPE = 'Result "%s" has a wrong extension. Allowed extensions are: "%s".'
CONVERT_ERROR = 'An error occurred during the conversion. %s'
BAD_OO_PORT = 'Bad OpenOffice port "%s". Make sure it is an integer.'
XHTML_ERROR = 'An error occurred while rendering XHTML content.'
WARNING_INCOMPLETE_ODT = 'Warning: your ODT file may not be complete (ie imported documents may not be present). This is because we could not connect to OpenOffice in server mode: %s'
DOC_NOT_SPECIFIED = 'Please specify a document to import, either with a stream (parameter "content") or with a path (parameter "at")'
DOC_FORMAT_ERROR = 'POD was unable to deduce the document format. Please specify it through parameter named "format" (=odt, gif, png, ...).'
DOC_WRONG_FORMAT = 'Format "%s" is not supported.'
f = open('%s/styles.in.content.xml' % os.path.dirname(appy.pod.__file__))
CONTENT_POD_STYLES = f.read()
f.close()
CONTENT_POD_FONTS = '<@style@:font-face style:name="PodStarSymbol" @svg@:font-family="StarSymbol"/>'
f = file('%s/styles.in.styles.xml' % os.path.dirname(appy.pod.__file__))
STYLES_POD_STYLES = f.read()
f.close()
STYLES_POD_FONTS = '<@style@:font-face @style@:name="PodStarSymbol" @svg@:font-family="StarSymbol"/>'

class Renderer:
    __module__ = __name__

    def __init__(self, template, context, result, pythonWithUnoPath=None, ooPort=2002, stylesMapping={}, forceOoCall=False):
        """This Python Open Document Renderer (PodRenderer) loads a document
        template (p_template) which is a OpenDocument file with some elements
        written in Python. Based on this template and some Python objects
        defined in p_context, the renderer generates an OpenDocument file
        (p_result) that instantiates the p_template and fills it with objects
        from the p_context. If p_result does not end with .odt, the Renderer
        will call OpenOffice to perform a conversion. If p_forceOoCall is True,
        even if p_result ends with .odt, OpenOffice will be called, not for
        performing a conversion, but for updating some elements like indexes
        (table of contents, etc) and sections containing links to external
        files (which is the case, for example, if you use the default function
        "document"). If the Python interpreter which runs the current script
        is not UNO-enabled, this script will run, in another process, a
        UNO-enabled Python interpreter (whose path is p_pythonWithUnoPath)
        which will call OpenOffice. In both cases, we
        will try to connect to OpenOffice in server mode on port p_ooPort.
        If you plan to make "XHTML to OpenDocument" conversions, you may specify
        a styles mapping in p_stylesMapping."""
        self.template = template
        self.templateZip = zipfile.ZipFile(template)
        self.result = result
        self.contentXml = None
        self.stylesXml = None
        self.stylesManager = None
        self.tempFolder = None
        self.curdir = os.getcwd()
        self.env = None
        self.pyPath = pythonWithUnoPath
        self.ooPort = ooPort
        self.forceOoCall = forceOoCall
        self.prepareFolders()
        self.unzipFolder = os.path.join(self.tempFolder, 'unzip')
        os.mkdir(self.unzipFolder)
        for zippedFile in self.templateZip.namelist():
            fileName = os.path.basename(zippedFile)
            folderName = os.path.dirname(zippedFile)
            fullFolderName = self.unzipFolder
            if folderName:
                fullFolderName = os.path.join(fullFolderName, folderName)
                if not os.path.exists(fullFolderName):
                    os.makedirs(fullFolderName)
            if fileName:
                fullFileName = os.path.join(fullFolderName, fileName)
                f = open(fullFileName, 'wb')
                fileContent = self.templateZip.read(zippedFile)
                if fileName == 'content.xml':
                    self.contentXml = fileContent
                elif fileName == 'styles.xml':
                    self.stylesManager = StylesManager(fileContent)
                    self.stylesXml = fileContent
                f.write(fileContent)
                f.close()

        self.templateZip.close()
        pe = PodEnvironment
        contentInserts = (
         OdInsert(CONTENT_POD_FONTS, XmlElement('font-face-decls', nsUri=pe.NS_OFFICE), nsUris={'style': pe.NS_STYLE, 'svg': pe.NS_SVG}),
         OdInsert(CONTENT_POD_STYLES, XmlElement('automatic-styles', nsUri=pe.NS_OFFICE), nsUris={'style': pe.NS_STYLE, 'fo': pe.NS_FO, 'text': pe.NS_TEXT, 'table': pe.NS_TABLE}))
        self.contentParser = self.createPodParser('content.xml', context, contentInserts)
        stylesInserts = (
         OdInsert(STYLES_POD_FONTS, XmlElement('font-face-decls', nsUri=pe.NS_OFFICE), nsUris={'style': pe.NS_STYLE, 'svg': pe.NS_SVG}),
         OdInsert(STYLES_POD_STYLES, XmlElement('styles', nsUri=pe.NS_OFFICE), nsUris={'style': pe.NS_STYLE, 'fo': pe.NS_FO}))
        self.stylesParser = self.createPodParser('styles.xml', context, stylesInserts)
        self.setStylesMapping(stylesMapping)
        return

    def createPodParser(self, odtFile, context, inserts):
        """Creates the parser with its environment for parsing the given
           p_odtFile (content.xml or styles.xml). p_context is given by the pod
           user, while p_inserts depends on the ODT file we must parse."""
        evalContext = {'xhtml': self.renderXhtml, 'test': self.evalIfExpression, 'document': self.importDocument}
        if hasattr(context, '__dict__'):
            evalContext.update(context.__dict__)
        elif isinstance(context, dict) or isinstance(context, UserDict):
            evalContext.update(context)
        else:
            raise PodError(BAD_CONTEXT)
        env = PodEnvironment(evalContext, inserts)
        fileBuffer = FileBuffer(env, os.path.join(self.tempFolder, odtFile))
        env.currentBuffer = fileBuffer
        return PodParser(env, self)

    def renderXhtml(self, xhtmlString, encoding='utf-8', stylesMapping={}):
        """Method that can be used (under the name 'xhtml') into a pod template
           for converting a chunk of XHTML content (p_xhtmlString) into a chunk
           of ODT content."""
        stylesMapping = self.stylesManager.checkStylesMapping(stylesMapping)
        ns = self.currentParser.env.namespaces
        xhtmlContent = '<podXhtml>%s</podXhtml>' % xhtmlString
        return Xhtml2OdtConverter(xhtmlContent, encoding, self.stylesManager, stylesMapping, ns).run()

    def evalIfExpression(self, condition, ifTrue, ifFalse):
        """This method implements the method 'test' which is proposed in the
           default pod context. It represents an 'if' expression (as opposed to
           the 'if' statement): depending on p_condition, expression result is
           p_ifTrue or p_ifFalse."""
        if condition:
            return ifTrue
        return ifFalse

    imageFormats = ('png', 'jpeg', 'jpg', 'gif')
    mimeTypes = {'application/vnd.oasis.opendocument.text': 'odt', 'application/msword': 'doc', 'text/rtf': 'rtf', 'application/pdf': 'pdf', 'image/png': 'png', 'image/jpeg': 'jpg', 'image/gif': 'gif'}
    ooFormats = ('odt', )

    def importDocument(self, content=None, at=None, format=None, anchor='as-char'):
        """If p_at is not None, it represents a path or url allowing to find
           the document. If p_at is None, the content of the document is
           supposed to be in binary format in p_content. The document
           p_format may be: odt or any format in imageFormats. p_anchor is only
           relevant for images."""
        ns = self.currentParser.env.namespaces
        importer = None
        if not content:
            if not at:
                raise PodError(DOC_NOT_SPECIFIED)
            if not (format or at):
                raise PodError(DOC_FORMAT_ERROR)
            format = os.path.splitext(at)[1][1:]
        elif self.mimeTypes.has_key(format):
            format = self.mimeTypes[format]
        isImage = False
        if format in self.ooFormats:
            importer = OdtImporter
            self.forceOoCall = True
        elif format in self.imageFormats:
            importer = ImageImporter
            isImage = True
        elif format == 'pdf':
            importer = PdfImporter
        else:
            raise PodError(DOC_WRONG_FORMAT % format)
        imp = importer(content, at, format, self.tempFolder, ns)
        if isImage:
            imp.setAnchor(anchor)
        return imp.run()

    def prepareFolders(self):
        if os.path.exists(self.result):
            raise PodError(RESULT_FILE_EXISTS % self.result)
        try:
            f = open(self.result, 'w')
            f.write('Hello')
            f.close()
        except OSError, oe:
            raise PodError(CANT_WRITE_RESULT % (self.result, oe))
        except IOError, ie:
            raise PodError(CANT_WRITE_RESULT % (self.result, oe))

        self.result = os.path.abspath(self.result)
        os.remove(self.result)
        self.tempFolder = os.path.abspath(self.result) + '.temp'
        if os.path.exists(self.tempFolder):
            raise PodError(TEMP_FOLDER_EXISTS % self.tempFolder)
        try:
            os.mkdir(self.tempFolder)
        except OSError, oe:
            raise PodError(CANT_WRITE_TEMP_FOLDER % (self.result, oe))

    def run(self):
        """Renders the result."""
        self.currentParser = self.contentParser
        self.currentParser.parse(self.contentXml)
        self.currentParser = self.stylesParser
        self.currentParser.parse(self.stylesXml)
        self.finalize()

    def getStyles(self):
        """Returns a dict of the styles that are defined into the template."""
        return self.stylesManager.styles

    def setStylesMapping(self, stylesMapping):
        """Establishes a correspondance between, on one hand, CSS styles or
           XHTML tags that will be found inside XHTML content given to POD,
           and, on the other hand, ODT styles found into the template."""
        try:
            stylesMapping = self.stylesManager.checkStylesMapping(stylesMapping)
            self.stylesManager.stylesMapping = stylesMapping
        except PodError, po:
            if os.path.exists(self.tempFolder):
                FolderDeleter.delete(self.tempFolder)
            raise po

    def reportProblem(self, msg, resultType):
        """When trying to call OO in server mode for producing ODT
           (=forceOoCall=True), if an error occurs we still have an ODT to
           return to the user. So we produce a warning instead of raising an
           error."""
        if resultType == 'odt' and self.forceOoCall:
            print WARNING_INCOMPLETE_ODT % msg
        else:
            raise msg

    def callOpenOffice(self, resultOdtName, resultType):
        """Call Open Office in server mode to convert or update the ODT
           result."""
        try:
            if not isinstance(self.ooPort, int) and not isinstance(self.ooPort, long):
                raise PodError(BAD_OO_PORT % str(self.ooPort))
            try:
                from appy.pod.converter import Converter, ConverterError
                try:
                    Converter(resultOdtName, resultType, self.ooPort).run()
                except ConverterError, ce:
                    raise PodError(CONVERT_ERROR % str(ce))

            except ImportError:
                if not self.pyPath:
                    raise PodError(NO_PY_PATH % resultType)
                if self.pyPath.find(' ') != -1:
                    raise PodError(BLANKS_IN_PATH % self.pyPath)
                if not os.path.isfile(self.pyPath):
                    raise PodError(PY_PATH_NOT_FILE % self.pyPath)
                if resultOdtName.find(' ') != -1:
                    qResultOdtName = '"%s"' % resultOdtName
                else:
                    qResultOdtName = resultOdtName
                convScript = '%s/converter.py' % os.path.dirname(appy.pod.__file__)
                if convScript.find(' ') != -1:
                    convScript = '"%s"' % convScript
                cmd = '%s %s %s %s -p%d' % (self.pyPath, convScript, qResultOdtName, resultType, self.ooPort)
                prgPipes = os.popen3(cmd)
                convertOutput = prgPipes[2].read()
                for pipe in prgPipes:
                    pipe.close()

                if convertOutput:
                    errors = []
                    for error in convertOutput.split('\n'):
                        error = error.strip()
                        if not error:
                            continue
                        elif error.startswith('warning'):
                            pass
                        else:
                            errors.append(error)

                    if errors:
                        raise PodError(CONVERT_ERROR % ('\n').join(errors))

        except PodError, pe:
            if resultType == 'odt' and self.forceOoCall:
                print WARNING_INCOMPLETE_ODT % str(pe)
            else:
                raise pe

    def finalize(self):
        """Re-zip the result and potentially call OpenOffice if target format is
           not ODT or if forceOoCall is True."""
        for odtFile in ('content.xml', 'styles.xml'):
            shutil.copy(os.path.join(self.tempFolder, odtFile), os.path.join(self.unzipFolder, odtFile))

        resultOdtName = os.path.join(self.tempFolder, 'result.odt')
        resultOdt = zipfile.ZipFile(resultOdtName, 'w')
        os.chdir(self.unzipFolder)
        for (dir, dirnames, filenames) in os.walk('.'):
            for f in filenames:
                resultOdt.write(os.path.join(dir, f)[2:])

        resultOdt.close()
        resultType = os.path.splitext(self.result)[1]
        try:
            if resultType == '.odt' and not self.forceOoCall:
                os.rename(resultOdtName, self.result)
            else:
                if resultType.startswith('.'):
                    resultType = resultType[1:]
                if resultType not in ODT_FILE_TYPES.keys():
                    raise PodError(BAD_RESULT_TYPE % (self.result, ODT_FILE_TYPES.keys()))
                self.callOpenOffice(resultOdtName, resultType)
                resPrefix = os.path.splitext(resultOdtName)[0] + '.'
                if resultType == 'odt':
                    resultName = resPrefix + 'res.odt'
                    if not os.path.exists(resultName):
                        resultName = resultOdtName
                else:
                    resultName = resPrefix + resultType
                os.rename(resultName, self.result)
        finally:
            os.chdir(self.curdir)
            FolderDeleter.delete(self.tempFolder)