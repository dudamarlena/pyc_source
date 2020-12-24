# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/opendocument.py
# Compiled at: 2020-01-18 11:47:38
"""Use OpenDocument to generate your documents."""
import zipfile, time, uuid, sys, mimetypes, copy, os.path
sys.path.append(os.path.dirname(__file__))
from io import StringIO, BytesIO
from odf.namespaces import *
import odf.manifest as manifest, odf.meta as meta
from odf.office import *
import odf.element as element
from odf.attrconverters import make_NCName
from xml.sax.xmlreader import InputSource
from odf.odfmanifest import manifestlist
import codecs
if sys.version_info[0] == 3:
    unicode = str
__version__ = TOOLSVERSION
_XMLPROLOGUE = "<?xml version='1.0' encoding='UTF-8'?>\n"
UNIXPERMS = 2175008768
IS_FILENAME = 0
IS_IMAGE = 1
assert sys.version_info[0] >= 2 and sys.version_info[1] >= 2
odmimetypes = {'application/vnd.oasis.opendocument.text': '.odt', 
   'application/vnd.oasis.opendocument.text-template': '.ott', 
   'application/vnd.oasis.opendocument.graphics': '.odg', 
   'application/vnd.oasis.opendocument.graphics-template': '.otg', 
   'application/vnd.oasis.opendocument.presentation': '.odp', 
   'application/vnd.oasis.opendocument.presentation-template': '.otp', 
   'application/vnd.oasis.opendocument.spreadsheet': '.ods', 
   'application/vnd.oasis.opendocument.spreadsheet-template': '.ots', 
   'application/vnd.oasis.opendocument.chart': '.odc', 
   'application/vnd.oasis.opendocument.chart-template': '.otc', 
   'application/vnd.oasis.opendocument.image': '.odi', 
   'application/vnd.oasis.opendocument.image-template': '.oti', 
   'application/vnd.oasis.opendocument.formula': '.odf', 
   'application/vnd.oasis.opendocument.formula-template': '.otf', 
   'application/vnd.oasis.opendocument.text-master': '.odm', 
   'application/vnd.oasis.opendocument.text-web': '.oth'}

class OpaqueObject():
    """
    just a record to bear a filename, a mediatype and a bytes content
    """

    def __init__(self, filename, mediatype, content=None):
        """
        the constructor
        @param filename a unicode string
        @param mediatype a unicode string
        @param content a byte string or None
        """
        assert type(filename) == type('')
        assert type(mediatype) == type('')
        assert type(content) == type('') or content == None
        self.mediatype = mediatype
        self.filename = filename
        self.content = content
        return


class OpenDocument():
    """
    A class to hold the content of an OpenDocument document
    Use the xml method to write the XML
    source to the screen or to a file.
    Example of use: d = OpenDocument(mimetype); fd.write(d.xml())
    """
    thumbnail = None

    def __init__(self, mimetype, add_generator=True):
        """
        the constructor
        @param mimetype a unicode string
        @param add_generator a boolean
        """
        assert type(mimetype) == type('')
        assert isinstance(add_generator, True.__class__)
        self.mimetype = mimetype
        self.childobjects = []
        self._extra = []
        self.folder = ''
        self.topnode = Document(mimetype=self.mimetype)
        self.topnode.ownerDocument = self
        self.clear_caches()
        self.Pictures = {}
        self.meta = Meta()
        self.topnode.addElement(self.meta)
        if add_generator:
            self.meta.addElement(meta.Generator(text=TOOLSVERSION))
        self.scripts = Scripts()
        self.topnode.addElement(self.scripts)
        self.fontfacedecls = FontFaceDecls()
        self.topnode.addElement(self.fontfacedecls)
        self.settings = Settings()
        self.topnode.addElement(self.settings)
        self.styles = Styles()
        self.topnode.addElement(self.styles)
        self.automaticstyles = AutomaticStyles()
        self.topnode.addElement(self.automaticstyles)
        self.masterstyles = MasterStyles()
        self.topnode.addElement(self.masterstyles)
        self.body = Body()
        self.topnode.addElement(self.body)

    def rebuild_caches(self, node=None):
        if node is None:
            node = self.topnode
        self.build_caches(node)
        for e in node.childNodes:
            if e.nodeType == element.Node.ELEMENT_NODE:
                self.rebuild_caches(e)

        return

    def clear_caches(self):
        """
        Clears internal caches
        """
        self.element_dict = {}
        self._styles_dict = {}
        self._styles_ooo_fix = {}

    def build_caches(self, elt):
        """
        Builds internal caches; called from element.py
        @param elt an element.Element instance
        """
        import odf.element
        assert isinstance(elt, element.Element) or isinstance(elt, odf.element.Element)
        if elt.qname not in self.element_dict:
            self.element_dict[elt.qname] = []
        self.element_dict[elt.qname].append(elt)
        if elt.qname == (STYLENS, 'style'):
            self.__register_stylename(elt)
        styleref = elt.getAttrNS(TEXTNS, 'style-name')
        if styleref is not None and styleref in self._styles_ooo_fix:
            elt.setAttrNS(TEXTNS, 'style-name', self._styles_ooo_fix[styleref])
        return

    def remove_from_caches(self, elt):
        """
        Updates internal caches when an element has been removed
        @param elt an element.Element instance
        """
        import odf.element
        assert isinstance(elt, element.Element) or isinstance(elt, odf.element.Element)
        self.element_dict[elt.qname].remove(elt)
        for e in elt.childNodes:
            if e.nodeType == element.Node.ELEMENT_NODE:
                self.remove_from_caches(e)

        if elt.qname == (STYLENS, 'style'):
            del self._styles_dict[elt.getAttrNS(STYLENS, 'name')]

    def __register_stylename(self, elt):
        """
        Register a style. But there are three style dictionaries:
        office:styles, office:automatic-styles and office:master-styles
        Chapter 14.
        @param elt an element.Element instance
        """
        assert isinstance(elt, element.Element)
        name = elt.getAttrNS(STYLENS, 'name')
        if name is None:
            return
        else:
            if elt.parentNode.qname in ((OFFICENS, 'styles'), (OFFICENS, 'automatic-styles')):
                if name in self._styles_dict:
                    newname = 'M' + name
                    self._styles_ooo_fix[name] = newname
                    name = newname
                    elt.setAttrNS(STYLENS, 'name', name)
                self._styles_dict[name] = elt
            return

    def toXml(self, filename=''):
        """
        converts the document to a valid Xml format.
        @param filename unicode string: the name of a file, defaults to
        an empty string.
        @return if filename is not empty, the XML code will be written into it
        and the method returns None; otherwise the method returns a StringIO
        containing valid XML.
        Then a ".getvalue()" should return a unicode string.
        """
        if not type(filename) == type(''):
            raise AssertionError
            result = None
            xml = StringIO()
            if sys.version_info[0] == 2:
                xml.write(_XMLPROLOGUE)
            else:
                xml.write(_XMLPROLOGUE)
            self.body.toXml(0, xml)
            result = filename or xml.getvalue()
        else:
            f = codecs.open(filename, 'w', encoding='utf-8')
            f.write(xml.getvalue())
            f.close()
        return result

    def xml(self):
        """
        Generates the full document as an XML "file"
        @return a bytestream in UTF-8 encoding
        """
        self.__replaceGenerator()
        xml = StringIO()
        if sys.version_info[0] == 2:
            xml.write(_XMLPROLOGUE)
        else:
            xml.write(_XMLPROLOGUE)
        self.topnode.toXml(0, xml)
        return xml.getvalue().encode('utf-8')

    def contentxml(self):
        """
        Generates the content.xml file
        @return a bytestream in UTF-8 encoding
        """
        xml = StringIO()
        xml.write(_XMLPROLOGUE)
        x = DocumentContent()
        x.write_open_tag(0, xml)
        if self.scripts.hasChildNodes():
            self.scripts.toXml(1, xml)
        if self.fontfacedecls.hasChildNodes():
            self.fontfacedecls.toXml(1, xml)
        a = AutomaticStyles()
        stylelist = self._used_auto_styles([self.styles, self.automaticstyles, self.body])
        if len(stylelist) > 0:
            a.write_open_tag(1, xml)
            for s in stylelist:
                s.toXml(2, xml)

            a.write_close_tag(1, xml)
        else:
            a.toXml(1, xml)
        self.body.toXml(1, xml)
        x.write_close_tag(0, xml)
        return xml.getvalue().encode('utf-8')

    def __manifestxml(self):
        """
        Generates the manifest.xml file;
        The self.manifest isn't avaible unless the document is being saved
        @return a unicode string
        """
        xml = StringIO()
        xml.write(_XMLPROLOGUE)
        self.manifest.toXml(0, xml)
        result = xml.getvalue()
        assert type(result) == type('')
        return result

    def metaxml(self):
        """
        Generates the meta.xml file
        @return a unicode string
        """
        self.__replaceGenerator()
        x = DocumentMeta()
        x.addElement(self.meta)
        xml = StringIO()
        xml.write(_XMLPROLOGUE)
        x.toXml(0, xml)
        result = xml.getvalue()
        assert type(result) == type('')
        return result

    def settingsxml(self):
        """
        Generates the settings.xml file
        @return a unicode string
        """
        x = DocumentSettings()
        x.addElement(self.settings)
        xml = StringIO()
        if sys.version_info[0] == 2:
            xml.write(_XMLPROLOGUE)
        else:
            xml.write(_XMLPROLOGUE)
        x.toXml(0, xml)
        result = xml.getvalue()
        assert type(result) == type('')
        return result

    def _parseoneelement(self, top, stylenamelist):
        """
        Finds references to style objects in master-styles
        and add the style name to the style list if not already there.
        Recursive
        @return the list of style names as unicode strings
        """
        for e in top.childNodes:
            if e.nodeType == element.Node.ELEMENT_NODE:
                for styleref in ((CHARTNS, 'style-name'),
                 (
                  DRAWNS, 'style-name'),
                 (
                  DRAWNS, 'text-style-name'),
                 (
                  PRESENTATIONNS, 'style-name'),
                 (
                  STYLENS, 'data-style-name'),
                 (
                  STYLENS, 'list-style-name'),
                 (
                  STYLENS, 'page-layout-name'),
                 (
                  STYLENS, 'style-name'),
                 (
                  TABLENS, 'default-cell-style-name'),
                 (
                  TABLENS, 'style-name'),
                 (
                  TEXTNS, 'style-name')):
                    if e.getAttrNS(styleref[0], styleref[1]):
                        stylename = e.getAttrNS(styleref[0], styleref[1])
                        if stylename not in stylenamelist:
                            stylenamelist.append(unicode(stylename))

                stylenamelist = self._parseoneelement(e, stylenamelist)

        return stylenamelist

    def _used_auto_styles(self, segments):
        """
        Loop through the masterstyles elements, and find the automatic
        styles that are used. These will be added to the automatic-styles
        element in styles.xml
        @return a list of element.Element instances
        """
        stylenamelist = []
        for top in segments:
            stylenamelist = self._parseoneelement(top, stylenamelist)

        stylelist = []
        for e in self.automaticstyles.childNodes:
            if isinstance(e, element.Element) and e.getAttrNS(STYLENS, 'name') in stylenamelist:
                stylelist.append(e)

        ok = True
        for e in stylelist:
            ok = ok and isinstance(e, element.Element)

        assert ok
        return stylelist

    def stylesxml(self):
        """
        Generates the styles.xml file
        @return valid XML code as a unicode string
        """
        xml = StringIO()
        xml.write(_XMLPROLOGUE)
        x = DocumentStyles()
        x.write_open_tag(0, xml)
        if self.fontfacedecls.hasChildNodes():
            self.fontfacedecls.toXml(1, xml)
        self.styles.toXml(1, xml)
        a = AutomaticStyles()
        a.write_open_tag(1, xml)
        for s in self._used_auto_styles([self.masterstyles]):
            s.toXml(2, xml)

        a.write_close_tag(1, xml)
        if self.masterstyles.hasChildNodes():
            self.masterstyles.toXml(1, xml)
        x.write_close_tag(0, xml)
        result = xml.getvalue()
        assert type(result) == type('')
        return result

    def addPicture(self, filename, mediatype=None, content=None):
        """
        Add a picture
        It uses the same convention as OOo, in that it saves the picture in
        the zipfile in the subdirectory 'Pictures'
        If passed a file ptr, mediatype must be set
        @param filename unicode string: name of a file for Pictures
        @param mediatype unicode string: name of a media, None by default
        @param content bytes: content of media, None by default
        @return a unicode string: the file name of the media, eventually
        created on the fly
        """
        if content is None:
            if mediatype is None:
                mediatype, encoding = mimetypes.guess_type(filename)
            if mediatype is None:
                mediatype = ''
                try:
                    ext = filename[filename.rindex('.'):]
                except:
                    ext = ''

            else:
                ext = mimetypes.guess_extension(mediatype)
            manifestfn = 'Pictures/%s%s' % (uuid.uuid4().hex.upper(), ext)
            self.Pictures[manifestfn] = (IS_FILENAME, filename, mediatype)
            content = ''
            filename = ''
        else:
            manifestfn = filename
            self.Pictures[manifestfn] = (IS_IMAGE, content, mediatype)
        assert type(filename) == type('')
        assert type(content) == type('')
        return manifestfn

    def addPictureFromFile(self, filename, mediatype=None):
        """
        Add a picture
        It uses the same convention as OOo, in that it saves the picture in
        the zipfile in the subdirectory 'Pictures'.
        If mediatype is not given, it will be guessed from the filename
        extension.
        @param filesname unicode string: name of an image file
        @param mediatype unicode string: type of media, dfaults to None
        @return a unicode string, the name of the created file
        """
        if mediatype is None:
            mediatype, encoding = mimetypes.guess_type(filename)
        if mediatype is None:
            mediatype = ''
            try:
                ext = filename[filename.rindex('.'):]
            except ValueError:
                ext = ''

        else:
            ext = mimetypes.guess_extension(mediatype)
        manifestfn = 'Pictures/%s%s' % (uuid.uuid4().hex.upper(), ext)
        self.Pictures[manifestfn] = (IS_FILENAME, filename, mediatype)
        assert type(filename) == type('')
        assert type(mediatype) == type('')
        return manifestfn

    def addPictureFromString(self, content, mediatype):
        """
        Add a picture from contents given as a Byte string.
        It uses the same convention as OOo, in that it saves the picture in
        the zipfile in the subdirectory 'Pictures'. The content variable
        is a string that contains the binary image data. The mediatype
        indicates the image format.
        @param content bytes: content of media
        @param mediatype unicode string: name of a media
        @return a unicode string, the name of the created file
        """
        assert type(content) == type('')
        assert type(mediatype) == type('')
        ext = mimetypes.guess_extension(mediatype)
        manifestfn = 'Pictures/%s%s' % (uuid.uuid4().hex.upper(), ext)
        self.Pictures[manifestfn] = (IS_IMAGE, content, mediatype)
        return manifestfn

    def addThumbnail(self, filecontent=None):
        """
        Add a fixed thumbnail
        The thumbnail in the library is big, so this is pretty useless.
        @param filecontent bytes: the content of a file; defaults to None
        """
        assert type(filecontent) == type('')
        if filecontent is None:
            import thumbnail
            self.thumbnail = thumbnail.thumbnail()
        else:
            self.thumbnail = filecontent
        return

    def addObject(self, document, objectname=None):
        """
        Adds an object (subdocument). The object must be an OpenDocument class
        @param document OpenDocument instance
        @param objectname unicode string: the name of an object to add
        @return a unicode string: the folder name in the zipfile the object is
        stored in.
        """
        assert isinstance(document, OpenDocument)
        assert type(objectname) == type('') or objectname == None
        self.childobjects.append(document)
        if objectname is None:
            document.folder = '%s/Object %d' % (self.folder, len(self.childobjects))
        else:
            document.folder = objectname
        return '.%s' % document.folder

    def _savePictures(self, anObject, folder):
        """
        saves pictures contained in an object
        @param anObject instance of OpenDocument containing pictures
        @param folder unicode string: place to save pictures
        """
        assert isinstance(anObject, OpenDocument)
        assert type(folder) == type('')
        hasPictures = False
        for arcname, picturerec in anObject.Pictures.items():
            what_it_is, fileobj, mediatype = picturerec
            self.manifest.addElement(manifest.FileEntry(fullpath='%s%s' % (folder, arcname), mediatype=mediatype))
            hasPictures = True
            if what_it_is == IS_FILENAME:
                self._z.write(fileobj, folder + arcname, zipfile.ZIP_STORED)
            else:
                zi = zipfile.ZipInfo(str(arcname), self._now)
                zi.compress_type = zipfile.ZIP_STORED
                zi.external_attr = UNIXPERMS
                self._z.writestr(zi, fileobj)

        subobjectnum = 1
        for subobject in anObject.childobjects:
            self._savePictures(subobject, '%sObject %d/' % (folder, subobjectnum))
            subobjectnum += 1

    def __replaceGenerator(self):
        """
        Removes a previous 'generator' stance and declares TOOLSVERSION
        as the new generator.
        Section 3.1.1: The application MUST NOT export the original identifier
        belonging to the application that created the document.
        """
        for m in self.meta.childNodes[:]:
            if m.qname == (METANS, 'generator'):
                self.meta.removeChild(m)

        self.meta.addElement(meta.Generator(text=TOOLSVERSION))

    def save(self, outputfile, addsuffix=False):
        """
        Save the document under the filename.
        If the filename is '-' then save to stdout
        @param outputfile unicode string: the special name '-' is for stdout;
        as an alternative, it can be an io.ByteIO instance which contains
        the ZIP content.
        @param addsuffix boolean: whether to add a suffix or not; defaults to False
        """
        if outputfile == '-':
            outputfp = zipfile.ZipFile(sys.stdout, 'w')
        else:
            if addsuffix:
                outputfile = outputfile + odmimetypes.get(self.mimetype, '.xxx')
            outputfp = zipfile.ZipFile(outputfile, 'w')
        self.__zipwrite(outputfp)
        outputfp.close()

    def write(self, outputfp):
        """
        User API to write the ODF file to an open file descriptor
        Writes the ZIP format
        @param outputfp open file descriptor
        """
        zipoutputfp = zipfile.ZipFile(outputfp, 'w')
        self.__zipwrite(zipoutputfp)

    def __zipwrite(self, outputfp):
        """
        Write the document to an open file pointer
        This is where the real work is done
        @param outputfp instance of zipfile.ZipFile
        """
        assert isinstance(outputfp, zipfile.ZipFile)
        self._z = outputfp
        self._now = time.localtime()[:6]
        self.manifest = manifest.Manifest()
        zi = zipfile.ZipInfo('mimetype', self._now)
        zi.compress_type = zipfile.ZIP_STORED
        zi.external_attr = UNIXPERMS
        self._z.writestr(zi, self.mimetype.encode('utf-8'))
        self._saveXmlObjects(self, '')
        self._savePictures(self, '')
        if self.thumbnail is not None:
            self.manifest.addElement(manifest.FileEntry(fullpath='Thumbnails/', mediatype=''))
            self.manifest.addElement(manifest.FileEntry(fullpath='Thumbnails/thumbnail.png', mediatype=''))
            zi = zipfile.ZipInfo('Thumbnails/thumbnail.png', self._now)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = UNIXPERMS
            self._z.writestr(zi, self.thumbnail)
        for op in self._extra:
            if op.filename == 'META-INF/documentsignatures.xml':
                continue
            self.manifest.addElement(manifest.FileEntry(fullpath=op.filename, mediatype=op.mediatype))
            if sys.version_info[0] == 3:
                zi = zipfile.ZipInfo(op.filename, self._now)
            else:
                zi = zipfile.ZipInfo(op.filename.encode('utf-8'), self._now)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = UNIXPERMS
            if op.content is not None:
                self._z.writestr(zi, op.content)

        zi = zipfile.ZipInfo('META-INF/manifest.xml', self._now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = UNIXPERMS
        self._z.writestr(zi, self.__manifestxml())
        del self._z
        del self._now
        del self.manifest
        return

    def _saveXmlObjects(self, anObject, folder):
        """
        save xml objects of an opendocument to some folder
        @param anObject instance of OpenDocument
        @param folder unicode string place to save xml objects
        """
        assert isinstance(anObject, OpenDocument)
        assert type(folder) == type('')
        if self == anObject:
            self.manifest.addElement(manifest.FileEntry(fullpath='/', mediatype=anObject.mimetype))
        else:
            self.manifest.addElement(manifest.FileEntry(fullpath=folder, mediatype=anObject.mimetype))
        self.manifest.addElement(manifest.FileEntry(fullpath='%sstyles.xml' % folder, mediatype='text/xml'))
        zi = zipfile.ZipInfo('%sstyles.xml' % folder, self._now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = UNIXPERMS
        self._z.writestr(zi, anObject.stylesxml().encode('utf-8'))
        self.manifest.addElement(manifest.FileEntry(fullpath='%scontent.xml' % folder, mediatype='text/xml'))
        zi = zipfile.ZipInfo('%scontent.xml' % folder, self._now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = UNIXPERMS
        self._z.writestr(zi, anObject.contentxml())
        if anObject.settings.hasChildNodes():
            self.manifest.addElement(manifest.FileEntry(fullpath='%ssettings.xml' % folder, mediatype='text/xml'))
            zi = zipfile.ZipInfo('%ssettings.xml' % folder, self._now)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = UNIXPERMS
            self._z.writestr(zi, anObject.settingsxml().encode('utf-8'))
        if self == anObject:
            self.manifest.addElement(manifest.FileEntry(fullpath='meta.xml', mediatype='text/xml'))
            zi = zipfile.ZipInfo('meta.xml', self._now)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = UNIXPERMS
            self._z.writestr(zi, anObject.metaxml().encode('utf-8'))
        subobjectnum = 1
        for subobject in anObject.childobjects:
            self._saveXmlObjects(subobject, '%sObject %d/' % (folder, subobjectnum))
            subobjectnum += 1

    def createElement(self, elt):
        """
        Inconvenient interface to create an element, but follows XML-DOM.
        Does not allow attributes as argument, therefore can't check grammar.
        @param elt element.Element instance
        @return an element.Element instance whose grammar is not checked
        """
        assert isinstance(elt, element.Element)
        return elt(check_grammar=False)

    def createTextNode(self, data):
        """
        Method to create a text node
        @param data unicode string to include in the Text element
        @return an instance of element.Text
        """
        assert type(data) == type('')
        return element.Text(data)

    def createCDATASection(self, data):
        """
        Method to create a CDATA section
        @param data unicode string to include in the CDATA element
        @return an instance of element.CDATASection
        """
        assert type(data) == type('')
        return element.CDATASection(cdata)

    def getMediaType(self):
        """
        Returns the media type
        @result a unicode string
        """
        assert type(self.mimetype) == type('')
        return self.mimetype

    def getStyleByName(self, name):
        """
        Finds a style object based on the name
        @param name unicode string the name of style to search
        @return a syle as an element.Element instance
        """
        assert type(name) == type('')
        ncname = make_NCName(name)
        if self._styles_dict == {}:
            self.rebuild_caches()
        result = self._styles_dict.get(ncname, None)
        assert isinstance(result, element.Element)
        return result

    def getElementsByType(self, elt):
        """
        Gets elements based on the type, which is function from
        text.py, draw.py etc.
        @param elt instance of a function which returns an element.Element
        @return a list of istances of element.Element
        """
        import types
        assert isinstance(elt, types.FunctionType)
        obj = elt(check_grammar=False)
        assert isinstance(obj, element.Element)
        if self.element_dict == {}:
            self.rebuild_caches()
        result = self.element_dict.get(obj.qname, [])
        ok = True
        for e in result:
            ok = ok and isinstance(e, element.Element)

        assert ok
        return result


def OpenDocumentChart():
    """
    Creates a chart document
    @return an OpenDocument instance with chart mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.chart')
    doc.chart = Chart()
    doc.body.addElement(doc.chart)
    return doc


def OpenDocumentDrawing():
    """
    Creates a drawing document
    @return an OpenDocument instance with drawing mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.graphics')
    doc.drawing = Drawing()
    doc.body.addElement(doc.drawing)
    return doc


def OpenDocumentImage():
    """
    Creates an image document
    @return an OpenDocument instance with image mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.image')
    doc.image = Image()
    doc.body.addElement(doc.image)
    return doc


def OpenDocumentPresentation():
    """
    Creates a presentation document
    @return an OpenDocument instance with presentation mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.presentation')
    doc.presentation = Presentation()
    doc.body.addElement(doc.presentation)
    return doc


def OpenDocumentSpreadsheet():
    """
    Creates a spreadsheet document
    @return an OpenDocument instance with spreadsheet mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.spreadsheet')
    doc.spreadsheet = Spreadsheet()
    doc.body.addElement(doc.spreadsheet)
    return doc


def OpenDocumentText():
    """
    Creates a text document
    @return an OpenDocument instance with text mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.text')
    doc.text = Text()
    doc.body.addElement(doc.text)
    return doc


def OpenDocumentTextMaster():
    """
    Creates a text master document
    @return an OpenDocument instance with master mimetype
    """
    doc = OpenDocument('application/vnd.oasis.opendocument.text-master')
    doc.text = Text()
    doc.body.addElement(doc.text)
    return doc


def __loadxmlparts(z, manifest, doc, objectpath):
    """
    Parses a document from its zipfile
    @param z an instance of zipfile.ZipFile
    @param manifest Manifest data structured in a dictionary
    @param doc instance of OpenDocument to feed in
    @param objectpath unicode string: path to an object
    """
    assert isinstance(z, zipfile.ZipFile)
    assert type(manifest) == type(dict())
    assert isinstance(doc, OpenDocument)
    assert type(objectpath) == type('')
    from odf.load import LoadParser
    from defusedxml.sax import make_parser
    from xml.sax import handler
    for xmlfile in (objectpath + 'settings.xml', objectpath + 'meta.xml', objectpath + 'content.xml', objectpath + 'styles.xml'):
        if xmlfile not in manifest:
            continue
        from xml.sax._exceptions import SAXParseException
        try:
            xmlpart = z.read(xmlfile).decode('utf-8')
            doc._parsing = xmlfile
            parser = make_parser()
            parser.setFeature(handler.feature_namespaces, 1)
            parser.setFeature(handler.feature_external_ges, 0)
            parser.setContentHandler(LoadParser(doc))
            parser.setErrorHandler(handler.ErrorHandler())
            inpsrc = InputSource()
            xmlpart = __fixXmlPart(xmlpart)
            inpsrc.setByteStream(BytesIO(xmlpart.encode('utf-8')))
            parser.parse(inpsrc)
            del doc._parsing
        except KeyError as v:
            pass
        except SAXParseException:
            print (
             '====== SAX FAILED TO PARSE ==========\n', xmlpart)


def __fixXmlPart(xmlpart):
    """
    fixes an xml code when it does not contain a set of requested
    "xmlns:whatever" declarations.
    added by G.K. on 2014/10/21
    @param xmlpart unicode string: some XML code
    @return fixed XML code
    """
    result = xmlpart
    requestedPrefixes = ('meta', 'config', 'dc', 'style', 'svg', 'fo', 'draw', 'table',
                         'form')
    for prefix in requestedPrefixes:
        if (' xmlns:{prefix}').format(prefix=prefix) not in xmlpart:
            try:
                pos = result.index(' xmlns:')
                toInsert = (' xmlns:{prefix}="urn:oasis:names:tc:opendocument:xmlns:{prefix}:1.0"').format(prefix=prefix)
                result = result[:pos] + toInsert + result[pos:]
            except:
                pass

    return result


def __detectmimetype(zipfd, odffile):
    """
    detects the mime-type of an ODF file
    @param zipfd an open zipfile.ZipFile instance
    @param odffile this parameter is not used
    @return a mime-type as a unicode string
    """
    assert isinstance(zipfd, zipfile.ZipFile)
    try:
        mimetype = zipfd.read('mimetype').decode('utf-8')
        return mimetype
    except:
        pass

    manifestpart = zipfd.read('META-INF/manifest.xml')
    manifest = manifestlist(manifestpart)
    for mentry, mvalue in manifest.items():
        if mentry == '/':
            if not type(mvalue['media-type']) == type(''):
                raise AssertionError
                return mvalue['media-type']

    return 'application/vnd.oasis.opendocument.text'


def load(odffile):
    """
    Load an ODF file into memory
    @param odffile unicode string: name of a file, or as an alternative,
    an open readable stream
    @return a reference to the structure (an OpenDocument instance)
    """
    z = zipfile.ZipFile(odffile)
    mimetype = __detectmimetype(z, odffile)
    doc = OpenDocument(mimetype, add_generator=False)
    manifestpart = z.read('META-INF/manifest.xml')
    manifest = manifestlist(manifestpart)
    __loadxmlparts(z, manifest, doc, '')
    for mentry, mvalue in manifest.items():
        if mentry[:9] == 'Pictures/' and len(mentry) > 9:
            doc.addPicture(mvalue['full-path'], mvalue['media-type'], z.read(mentry))
        elif mentry == 'Thumbnails/thumbnail.png':
            doc.addThumbnail(z.read(mentry))
        elif mentry in ('settings.xml', 'meta.xml', 'content.xml', 'styles.xml'):
            pass
        elif mentry[:7] == 'Object ' and len(mentry) < 11 and mentry[(-1)] == '/':
            subdoc = OpenDocument(mvalue['media-type'], add_generator=False)
            doc.addObject(subdoc, '/' + mentry[:-1])
            __loadxmlparts(z, manifest, subdoc, mentry)
        elif mentry[:7] == 'Object ':
            pass
        elif mvalue['full-path'][(-1)] == '/':
            doc._extra.append(OpaqueObject(mvalue['full-path'], mvalue['media-type'], None))
        else:
            doc._extra.append(OpaqueObject(mvalue['full-path'], mvalue['media-type'], z.read(mentry)))

    z.close()
    b = doc.getElementsByType(Body)
    if mimetype[:39] == 'application/vnd.oasis.opendocument.text':
        doc.text = b[0].firstChild
    elif mimetype[:43] == 'application/vnd.oasis.opendocument.graphics':
        doc.graphics = b[0].firstChild
    elif mimetype[:47] == 'application/vnd.oasis.opendocument.presentation':
        doc.presentation = b[0].firstChild
    elif mimetype[:46] == 'application/vnd.oasis.opendocument.spreadsheet':
        doc.spreadsheet = b[0].firstChild
    elif mimetype[:40] == 'application/vnd.oasis.opendocument.chart':
        doc.chart = b[0].firstChild
    elif mimetype[:40] == 'application/vnd.oasis.opendocument.image':
        doc.image = b[0].firstChild
    elif mimetype[:42] == 'application/vnd.oasis.opendocument.formula':
        doc.formula = b[0].firstChild
    return doc