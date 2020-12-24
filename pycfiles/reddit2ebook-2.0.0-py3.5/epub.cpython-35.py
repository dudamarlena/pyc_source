# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reddit2ebook/ebooklib_patched/epub.py
# Compiled at: 2016-05-13 06:16:04
# Size of source mod 2**32: 50075 bytes
import zipfile, six, mimetypes, logging, uuid, posixpath as zip_path, os.path
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from lxml import etree
import ebooklib
from ebooklib.utils import parse_string, parse_html_string
mimetypes.init()
mimetypes.add_type('application/xhtml+xml', '.xhtml')
VERSION = (
 0, 15, 0)
NAMESPACES = {'XML': 'http://www.w3.org/XML/1998/namespace', 
 'EPUB': 'http://www.idpf.org/2007/ops', 
 'DAISY': 'http://www.daisy.org/z3986/2005/ncx/', 
 'OPF': 'http://www.idpf.org/2007/opf', 
 'CONTAINERNS': 'urn:oasis:names:tc:opendocument:xmlns:container', 
 'DC': 'http://purl.org/dc/elements/1.1/', 
 'XHTML': 'http://www.w3.org/1999/xhtml'}
CONTAINER_PATH = 'META-INF/container.xml'
CONTAINER_XML = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n  <rootfiles>\n    <rootfile media-type="application/oebps-package+xml" full-path="%(folder_name)s/content.opf"/>\n  </rootfiles>\n</container>\n'
NCX_XML = six.b('<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" />')
NAV_XML = six.b('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"/>')
CHAPTER_XML = six.b('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"  epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#"></html>')
COVER_XML = six.b('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n <head>\n  <style>\n    body { margin: 0em; padding: 0em; }\n    img { max-width: 100%; max-height: 100%; }\n  </style>\n </head>\n <body>\n   <img src="" alt="" />\n </body>\n</html>')
IMAGE_MEDIA_TYPES = [
 'image/jpeg', 'image/jpg', 'image/png', 'image/svg+xml']

class Section(object):

    def __init__(self, title, href=''):
        self.title = title
        self.href = href


class Link(object):

    def __init__(self, href, title, uid=None):
        self.href = href
        self.title = title
        self.uid = uid


class EpubException(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class EpubItem(object):
    __doc__ = '\n    Base class for the items in a book.\n    '

    def __init__(self, uid=None, file_name='', media_type='', content=six.b(''), manifest=True):
        """
        :Args:
          - uid: Unique identifier for this item (optional)
          - file_name: File name for this item (optional)
          - media_type: Media type for this item (optional)
          - content: Content for this item (optional)
          - manifest: Manifest for this item (optional)
        """
        self.id = uid
        self.file_name = file_name
        self.media_type = media_type
        self.content = content
        self.is_linear = True
        self.manifest = manifest
        self.book = None

    def get_id(self):
        """
        Returns unique identifier for this item.

        :Returns:
          Returns uid number as string.
        """
        return self.id

    def get_name(self):
        """
        Returns name for this item. By default it is always file name but it does not have to be.

        :Returns:
          Returns file name for this item.
        """
        return self.file_name

    def get_type(self):
        """
        Guess type according to the file extension. Might not be the best way how to do it, but it works for now.

        Items can be of type:
          - ITEM_UNKNOWN = 0
          - ITEM_IMAGE = 1
          - ITEM_STYLE = 2
          - ITEM_SCRIPT = 3
          - ITEM_NAVIGATION = 4
          - ITEM_VECTOR = 5
          - ITEM_FONT = 6
          - ITEM_VIDEO = 7
          - ITEM_AUDIO = 8
          - ITEM_DOCUMENT = 9

        We map type according to the extensions which are defined in ebooklib.EXTENSIONS.

        :Returns:
          Returns type of the item as number.
        """
        _, ext = zip_path.splitext(self.get_name())
        ext = ext.lower()
        for uid, ext_list in six.iteritems(ebooklib.EXTENSIONS):
            if ext in ext_list:
                return uid

        return ebooklib.ITEM_UNKNOWN

    def get_content(self, default=six.b('')):
        """
        Returns content of the item. Content should be of type 'str' (Python 2) or 'bytes' (Python 3)

        :Args:
          - default: Default value for the content if it is not already defined.

        :Returns:
          Returns content of the item.
        """
        return self.content or default

    def set_content(self, content):
        """
        Sets content value for this item.

        :Args:
          - content: Content value
        """
        self.content = content

    def __str__(self):
        return '<EpubItem:%s>' % self.id


class EpubNcx(EpubItem):
    __doc__ = 'Represents Navigation Control File (NCX) in the EPUB.'

    def __init__(self, uid='ncx', file_name='toc.ncx'):
        super(EpubNcx, self).__init__(uid=uid, file_name=file_name, media_type='application/x-dtbncx+xml')

    def __str__(self):
        return '<EpubNcx:%s>' % self.id


class EpubCover(EpubItem):
    __doc__ = '\n    Represents Cover image in the EPUB file.\n    '

    def __init__(self, uid='cover-img', file_name=''):
        super(EpubCover, self).__init__(uid=uid, file_name=file_name)

    def __str__(self):
        return '<EpubCover:%s:%s>' % (self.id, self.file_name)


class EpubHtml(EpubItem):
    __doc__ = '\n    Represents HTML document in the EPUB file.\n    '
    _template_name = 'chapter'

    def __init__(self, uid=None, file_name='', media_type='', content=None, title='', lang=None):
        super(EpubHtml, self).__init__(uid, file_name, media_type, content)
        self.title = title
        self.lang = lang
        self.links = []
        self.properties = []

    def is_chapter(self):
        """
        Returns if this document is chapter or not.

        :Returns:
          Returns book value.
        """
        return True

    def get_type(self):
        """
        Always returns ebooklib.ITEM_DOCUMENT as type of this document.

        :Returns:
          Always returns ebooklib.ITEM_DOCUMENT
        """
        return ebooklib.ITEM_DOCUMENT

    def set_language(self, lang):
        """
        Sets language for this book item. By default it will use language of the book but it
        can be overwritten with this call.
        """
        self.lang = lang

    def get_language(self):
        """
        Get language code for this book item. Language of the book item can be different from
        the language settings defined globaly for book.

        :Returns:
          As string returns language code.
        """
        return self.lang

    def add_link(self, **kwgs):
        """
        Add additional link to the document. Links will be embeded only inside of this document.

        >>> add_link(href='styles.css', rel='stylesheet', type='text/css')
        """
        self.links.append(kwgs)

    def get_links(self):
        """
        Returns list of additional links defined for this document.

        :Returns:
          As tuple return list of links.
        """
        return (link for link in self.links)

    def get_links_of_type(self, link_type):
        """
        Returns list of additional links of specific type.

        :Returns:
          As tuple returns list of links.
        """
        return (link for link in self.links if link.get('type', '') == link_type)

    def add_item(self, item):
        """
        Add other item to this document. It will create additional links according to the item type.

        :Args:
          - item: item we want to add defined as instance of EpubItem
        """
        if item.get_type() == ebooklib.ITEM_STYLE:
            self.add_link(href=item.get_name(), rel='stylesheet', type='text/css')
        if item.get_type() == ebooklib.ITEM_SCRIPT:
            self.add_link(src=item.get_name(), type='text/javascript')

    def get_body_content(self):
        """
        Returns content of BODY element for this HTML document. Content will be of type 'str' (Python 2) or 'bytes' (Python 3).

        :Returns:
          Returns content of this document.
        """
        content = self.get_content()
        try:
            html_tree = parse_html_string(self.content)
        except:
            return ''

        html_root = html_tree.getroottree()
        if len(html_root.find('body')) != 0:
            body = html_tree.find('body')
            tree_str = etree.tostring(body, pretty_print=True, encoding='utf-8', xml_declaration=False)
            if tree_str.startswith(six.b('<body>')):
                n = tree_str.rindex(six.b('</body>'))
                return tree_str[7:n]
            return tree_str
        return ''

    def get_content(self, default=None):
        """
        Returns content for this document as HTML string. Content will be of type 'str' (Python 2) or 'bytes' (Python 3).

        :Args:
          - default: Default value for the content if it is not defined.

        :Returns:
          Returns content of this document.
        """
        tree = parse_string(self.book.get_template(self._template_name))
        tree_root = tree.getroot()
        tree_root.set('lang', self.lang or self.book.language)
        tree_root.attrib['{%s}lang' % NAMESPACES['XML']] = self.lang or self.book.language
        try:
            html_tree = parse_html_string(self.content)
        except:
            return ''

        html_root = html_tree.getroottree()
        _head = etree.SubElement(tree_root, 'head')
        if self.title != '':
            _title = etree.SubElement(_head, 'title')
            _title.text = self.title
        for lnk in self.links:
            if lnk.get('type') == 'text/javascript':
                _lnk = etree.SubElement(_head, 'script', lnk)
                _lnk.text = ''
            else:
                _lnk = etree.SubElement(_head, 'link', lnk)

        _body = etree.SubElement(tree_root, 'body')
        body = html_tree.find('body')
        if body is not None:
            for i in body.getchildren():
                _body.append(i)

        tree_str = etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return tree_str

    def __str__(self):
        return '<EpubHtml:%s:%s>' % (self.id, self.file_name)


class EpubCoverHtml(EpubHtml):
    __doc__ = '\n    Represents Cover page in the EPUB file.\n    '

    def __init__(self, uid='cover', file_name='cover.xhtml', image_name='', title='Cover'):
        super(EpubCoverHtml, self).__init__(uid=uid, file_name=file_name, title=title)
        self.image_name = image_name
        self.is_linear = False

    def is_chapter(self):
        """
        Returns if this document is chapter or not.

        :Returns:
          Returns book value.
        """
        return False

    def get_content(self):
        """
        Returns content for cover page as HTML string. Content will be of type 'str' (Python 2) or 'bytes' (Python 3).

        :Returns:
          Returns content of this document.
        """
        self.content = self.book.get_template('cover')
        tree = parse_string(super().get_content())
        tree_root = tree.getroot()
        images = tree_root.xpath('//xhtml:img', namespaces={'xhtml': NAMESPACES['XHTML']})
        images[0].set('src', self.image_name)
        images[0].set('alt', self.title)
        tree_str = etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return tree_str

    def __str__(self):
        return '<EpubCoverHtml:%s:%s>' % (self.id, self.file_name)


class EpubNav(EpubHtml):
    __doc__ = '\n    Represents Navigation Document in the EPUB file.\n    '

    def __init__(self, uid='nav', file_name='nav.xhtml', media_type='application/xhtml+xml'):
        super(EpubNav, self).__init__(uid=uid, file_name=file_name, media_type=media_type)

    def is_chapter(self):
        """
        Returns if this document is chapter or not.

        :Returns:
          Returns book value.
        """
        return False

    def __str__(self):
        return '<EpubNav:%s:%s>' % (self.id, self.file_name)


class EpubImage(EpubItem):
    __doc__ = '\n    Represents Image in the EPUB file.\n    '

    def __init__(self):
        super(EpubImage, self).__init__()

    def get_type(self):
        return ebooklib.ITEM_IMAGE

    def __str__(self):
        return '<EpubImage:%s:%s>' % (self.id, self.file_name)


class EpubBook(object):

    def __init__(self):
        self.EPUB_VERSION = None
        self.reset()

    def reset(self):
        """Initialises all needed variables to default values"""
        self.metadata = {}
        self.items = []
        self.spine = []
        self.guide = []
        self.toc = []
        self.bindings = []
        self.IDENTIFIER_ID = 'id'
        self.FOLDER_NAME = 'EPUB'
        self._id_html = 0
        self._id_image = 0
        self._id_static = 0
        self.title = ''
        self.language = 'en'
        self.templates = {'ncx': NCX_XML, 
         'nav': NAV_XML, 
         'chapter': CHAPTER_XML, 
         'cover': COVER_XML}
        self.add_metadata('OPF', 'generator', '', {'name': 'generator', 'content': 'Ebook-lib %s' % '.'.join([str(s) for s in VERSION])})
        self.set_identifier(str(uuid.uuid4()))
        self.prefixes = []
        self.namespaces = {}

    def set_identifier(self, uid):
        """
        Sets unique id for this epub

        :Args:
          - uid: Value of unique identifier for this book
        """
        self.uid = uid
        self.set_unique_metadata('DC', 'identifier', self.uid, {'id': self.IDENTIFIER_ID})

    def set_title(self, title):
        """
        Set title. You can set multiple titles.

        :Args:
          - title: Title value
        """
        self.title = title
        self.add_metadata('DC', 'title', self.title)

    def set_language(self, lang):
        """
        Set language for this epub. You can set multiple languages. Specific items in the book can have
        different language settings.

        :Args:
          - lang: Language code
        """
        self.language = lang
        self.add_metadata('DC', 'language', lang)

    def set_cover(self, file_name, content, create_page=True):
        """
        Set cover and create cover document if needed.

        :Args:
          - file_name: file name of the cover page
          - content: Content for the cover image
          - create_page: Should cover page be defined. Defined as bool value (optional). Default value is True.
        """
        c0 = EpubCover(file_name=file_name)
        c0.content = content
        self.add_item(c0)
        if create_page:
            c1 = EpubCoverHtml(image_name=file_name)
            self.add_item(c1)
        self.add_metadata(None, 'meta', '', {'name': 'cover', 'content': 'cover-img'})

    def add_author(self, author, file_as=None, role=None, uid='creator'):
        """Add author for this document"""
        self.add_metadata('DC', 'creator', author, {'id': uid})
        if file_as:
            self.add_metadata(None, 'meta', file_as, {'refines': '#' + uid, 
             'property': 'file-as', 
             'scheme': 'marc:relators'})
        if role:
            self.add_metadata(None, 'meta', role, {'refines': '#' + uid, 
             'property': 'role', 
             'scheme': 'marc:relators'})

    def add_metadata(self, namespace, name, value, others=None):
        """Add metadata"""
        if namespace in NAMESPACES:
            namespace = NAMESPACES[namespace]
        if namespace not in self.metadata:
            self.metadata[namespace] = {}
        if name not in self.metadata[namespace]:
            self.metadata[namespace][name] = []
        self.metadata[namespace][name].append((value, others))

    def get_metadata(self, namespace, name):
        """Retrieve metadata"""
        if namespace in NAMESPACES:
            namespace = NAMESPACES[namespace]
        return self.metadata[namespace][name]

    def set_unique_metadata(self, namespace, name, value, others=None):
        """Add metadata if metadata with this identifier does not already exist, otherwise update existing metadata."""
        if namespace in NAMESPACES:
            namespace = NAMESPACES[namespace]
        if namespace in self.metadata and name in self.metadata[namespace]:
            self.metadata[namespace][name] = [
             (
              value, others)]
        else:
            self.add_metadata(namespace, name, value, others)

    def add_item(self, item):
        """
        Add additional item to the book. If not defined, media type and chapter id will be defined
        for the item.

        :Args:
          - item: Item instance
        """
        if item.media_type == '':
            has_guessed, media_type = mimetypes.guess_type(item.get_name().lower())
            if has_guessed:
                if media_type is not None:
                    item.media_type = media_type
                else:
                    item.media_type = has_guessed
            else:
                item.media_type = 'application/octet-stream'
            if not item.get_id():
                if isinstance(item, EpubHtml):
                    item.id = 'chapter_%d' % self._id_html
                    self._id_html += 1
                else:
                    if isinstance(item, EpubImage):
                        item.id = 'image_%d' % self._id_image
                        self._id_image += 1
                    else:
                        item.id = 'static_%d' % self._id_image
                        self._id_image += 1
                item.book = self
                self.items.append(item)
                return item

    def get_item_with_id(self, uid):
        """
        Returns item for defined UID.

        >>> book.get_item_with_id('image_001')

        :Args:
          - uid: UID for the item

        :Returns:
          Returns item object. Returns None if nothing was found.
        """
        for item in self.get_items():
            if item.id == uid:
                return item

    def get_item_with_href(self, href):
        """
        Returns item for defined HREF.

        >>> book.get_item_with_href('EPUB/document.xhtml')

        :Args:
          - href: HREF for the item we are searching for

        :Returns:
          Returns item object. Returns None if nothing was found.
        """
        for item in self.get_items():
            if item.get_name() == href:
                return item

    def get_items(self):
        """
        Returns all items attached to this book.

        :Returns:
          Returns all items as tuple.
        """
        return (item for item in self.items)

    def get_items_of_type(self, item_type):
        """
        Returns all items of specified type.

        >>> book.get_items_of_type(epub.ITEM_IMAGE)

        :Args:
          - item_type: Type for items we are searching for

        :Returns:
          Returns found items as tuple.
        """
        return (item for item in self.items if item.get_type() == item_type)

    def get_items_of_media_type(self, media_type):
        """
        Returns all items of specified media type.

        :Args:
          - media_type: Media type for items we are searching for

        :Returns:
          Returns found items as tuple.
        """
        return (item for item in self.items if item.media_type == media_type)

    def set_template(self, name, value):
        """
        Defines templates which are used to generate certain types of pages. When defining new value for the template
        we have to use content of type 'str' (Python 2) or 'bytes' (Python 3).

        At the moment we use these templates:
          - ncx
          - nav
          - chapter
          - cover

        :Args:
          - name: Name for the template
          - value: Content for the template
        """
        self.templates[name] = value

    def get_template(self, name):
        """
        Returns value for the template.

        :Args:
          - name: template name

        :Returns:
          Value of the template.
        """
        return self.templates.get(name)

    def add_prefix(self, name, uri):
        """
        Appends custom prefix to be added to the content.opf document

        >>> epub_book.add_prefix('bkterms', 'http://booktype.org/')

        :Args:
          - name: namespave name
          - uri: URI for the namespace
        """
        self.prefixes.append('%s: %s' % (name, uri))


class EpubWriter(object):
    DEFAULT_OPTIONS = {'epub2_guide': True, 
     'epub3_landmark': True, 
     'landmark_title': 'Guide'}

    def __init__(self, name, book, options=None):
        self.file_name = name
        self.book = book
        self.options = dict(self.DEFAULT_OPTIONS)
        if options:
            self.options.update(options)

    def process(self):
        for plg in self.options.get('plugins', []):
            if hasattr(plg, 'before_write'):
                plg.before_write(self.book)

        for item in self.book.get_items():
            if isinstance(item, EpubHtml):
                for plg in self.options.get('plugins', []):
                    if hasattr(plg, 'html_before_write'):
                        plg.html_before_write(self.book, item)

    def _write_container(self):
        container_xml = CONTAINER_XML % {'folder_name': self.book.FOLDER_NAME}
        self.out.writestr(CONTAINER_PATH, container_xml)

    def _write_opf_file(self):
        root = etree.Element('package', {'xmlns': NAMESPACES['OPF'], 
         'unique-identifier': self.book.IDENTIFIER_ID, 
         'version': '3.0'})
        prefixes = [
         'rendition: http://www.idpf.org/vocab/rendition/#'] + self.book.prefixes
        root.attrib['prefix'] = ' '.join(prefixes)
        nsmap = {'dc': NAMESPACES['DC'], 'opf': NAMESPACES['OPF']}
        nsmap.update(self.book.namespaces)
        metadata = etree.SubElement(root, 'metadata', nsmap=nsmap)
        el = etree.SubElement(metadata, 'meta', {'property': 'dcterms:modified'})
        if 'mtime' in self.options:
            mtime = self.options['mtime']
        else:
            import datetime
            mtime = datetime.datetime.now()
        el.text = mtime.strftime('%Y-%m-%dT%H:%M:%SZ')
        for ns_name, values in six.iteritems(self.book.metadata):
            if ns_name == NAMESPACES['OPF']:
                for values in values.values():
                    for v in values:
                        if 'property' in v[1] and v[1]['property'] == 'dcterms:modified':
                            pass
                        else:
                            try:
                                el = etree.SubElement(metadata, 'meta', v[1])
                                if v[0]:
                                    el.text = v[0]
                            except ValueError:
                                logging.error('Could not create metadata.')

            else:
                for name, values in six.iteritems(values):
                    for v in values:
                        try:
                            if ns_name:
                                el = etree.SubElement(metadata, '{%s}%s' % (ns_name, name), v[1])
                            else:
                                el = etree.SubElement(metadata, '%s' % name, v[1])
                            el.text = v[0]
                        except ValueError:
                            logging.error('Could not create metadata "{}".'.format(name))

        manifest = etree.SubElement(root, 'manifest')
        _ncx_id = None
        for item in self.book.get_items():
            if not item.manifest:
                continue
            if isinstance(item, EpubNav):
                etree.SubElement(manifest, 'item', {'href': item.get_name(), 
                 'id': item.id, 
                 'media-type': item.media_type, 
                 'properties': 'nav'})
            elif isinstance(item, EpubNcx):
                _ncx_id = item.id
                etree.SubElement(manifest, 'item', {'href': item.file_name, 
                 'id': item.id, 
                 'media-type': item.media_type})
            elif isinstance(item, EpubCover):
                etree.SubElement(manifest, 'item', {'href': item.file_name, 
                 'id': item.id, 
                 'media-type': item.media_type, 
                 'properties': 'cover-image'})
            else:
                opts = {'href': item.file_name, 
                 'id': item.id, 
                 'media-type': item.media_type}
                if hasattr(item, 'properties') and len(item.properties) > 0:
                    opts['properties'] = ' '.join(item.properties)
                etree.SubElement(manifest, 'item', opts)

        spine = etree.SubElement(root, 'spine', {'toc': _ncx_id or 'ncx'})
        for _item in self.book.spine:
            is_linear = True
            if isinstance(_item, tuple):
                item = _item[0]
                if len(_item) > 1 and _item[1] == 'no':
                    is_linear = False
            else:
                item = _item
            if isinstance(item, EpubHtml):
                opts = {'idref': item.get_id()}
                if not item.is_linear or not is_linear:
                    opts['linear'] = 'no'
            else:
                if isinstance(item, EpubItem):
                    opts = {'idref': item.get_id()}
                    if not item.is_linear or not is_linear:
                        opts['linear'] = 'no'
                else:
                    opts = {'idref': item}
                    try:
                        itm = self.book.get_item_with_id(item)
                        if not itm.is_linear or not is_linear:
                            opts['linear'] = 'no'
                    except:
                        pass

            etree.SubElement(spine, 'itemref', opts)

        if len(self.book.guide) > 0 and self.options.get('epub2_guide'):
            guide = etree.SubElement(root, 'guide', {})
            for item in self.book.guide:
                if 'item' in item:
                    chap = item.get('item')
                    if chap:
                        _href = chap.file_name
                        _title = chap.title
                else:
                    _href = item.get('href', '')
                    _title = item.get('title', '')
                if _title is None:
                    _title = ''
                ref = etree.SubElement(guide, 'reference', {'type': item.get('type', ''), 
                 'title': _title, 
                 'href': _href})

        if len(self.book.bindings) > 0:
            bindings = etree.SubElement(root, 'bindings', {})
            for item in self.book.bindings:
                etree.SubElement(bindings, 'mediaType', item)

        tree_str = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        self.out.writestr('%s/content.opf' % self.book.FOLDER_NAME, tree_str)

    def _get_nav(self, item):
        ncx = parse_string(self.book.get_template('nav'))
        root = ncx.getroot()
        root.set('lang', self.book.language)
        root.attrib['{%s}lang' % NAMESPACES['XML']] = self.book.language
        nav_dir_name = os.path.dirname(item.file_name)
        head = etree.SubElement(root, 'head')
        title = etree.SubElement(head, 'title')
        title.text = self.book.title
        for _link in item.links:
            _lnk = etree.SubElement(head, 'link', {'href': _link.get('href', ''), 'rel': 'stylesheet', 'type': 'text/css'})

        body = etree.SubElement(root, 'body')
        nav = etree.SubElement(body, 'nav', {'{%s}type' % NAMESPACES['EPUB']: 'toc', 'id': 'id'})
        content_title = etree.SubElement(nav, 'h2')
        content_title.text = self.book.title

        def _create_section(itm, items):
            ol = etree.SubElement(itm, 'ol')
            for item in items:
                if isinstance(item, tuple) or isinstance(item, list):
                    li = etree.SubElement(ol, 'li')
                    if isinstance(item[0], EpubHtml):
                        a = etree.SubElement(li, 'a', {'href': os.path.relpath(item[0].file_name, nav_dir_name)})
                    else:
                        if isinstance(item[0], Section) and item[0].href != '':
                            a = etree.SubElement(li, 'a', {'href': os.path.relpath(item[0].href, nav_dir_name)})
                        else:
                            if isinstance(item[0], Link):
                                a = etree.SubElement(li, 'a', {'href': os.path.relpath(item[0].href, nav_dir_name)})
                            else:
                                a = etree.SubElement(li, 'span')
                    a.text = item[0].title
                    _create_section(li, item[1])
                else:
                    if isinstance(item, Link):
                        li = etree.SubElement(ol, 'li')
                        a = etree.SubElement(li, 'a', {'href': os.path.relpath(item.href, nav_dir_name)})
                        a.text = item.title
                    elif isinstance(item, EpubHtml):
                        li = etree.SubElement(ol, 'li')
                        a = etree.SubElement(li, 'a', {'href': os.path.relpath(item.file_name, nav_dir_name)})
                        a.text = item.title

        _create_section(nav, self.book.toc)
        if len(self.book.guide) > 0 and self.options.get('epub3_landmark'):
            guide_to_landscape_map = {'notes': 'rearnotes', 
             'text': 'bodymatter'}
            guide_nav = etree.SubElement(body, 'nav', {'{%s}type' % NAMESPACES['EPUB']: 'landmarks'})
            guide_content_title = etree.SubElement(guide_nav, 'h2')
            guide_content_title.text = self.options.get('landmark_title', 'Guide')
            guild_ol = etree.SubElement(guide_nav, 'ol')
            for elem in self.book.guide:
                li_item = etree.SubElement(guild_ol, 'li')
                if 'item' in elem:
                    chap = elem.get('item', None)
                    if chap:
                        _href = chap.file_name
                        _title = chap.title
                else:
                    _href = elem.get('href', '')
                    _title = elem.get('title', '')
                guide_type = elem.get('type', '')
                a_item = etree.SubElement(li_item, 'a', {'{%s}type' % NAMESPACES['EPUB']: guide_to_landscape_map.get(guide_type, guide_type), 'href': os.path.relpath(_href, nav_dir_name)})
                a_item.text = _title

        tree_str = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return tree_str

    def _get_ncx(self):
        ncx = parse_string(self.book.get_template('ncx'))
        root = ncx.getroot()
        head = etree.SubElement(root, 'head')
        uid = etree.SubElement(head, 'meta', {'content': self.book.uid, 'name': 'dtb:uid'})
        uid = etree.SubElement(head, 'meta', {'content': '0', 'name': 'dtb:depth'})
        uid = etree.SubElement(head, 'meta', {'content': '0', 'name': 'dtb:totalPageCount'})
        uid = etree.SubElement(head, 'meta', {'content': '0', 'name': 'dtb:maxPageNumber'})
        doc_title = etree.SubElement(root, 'docTitle')
        title = etree.SubElement(doc_title, 'text')
        title.text = self.book.title
        nav_map = etree.SubElement(root, 'navMap')

        def _create_section(itm, items, uid):
            for item in items:
                if isinstance(item, tuple) or isinstance(item, list):
                    section, subsection = item[0], item[1]
                    np = etree.SubElement(itm, 'navPoint', {'id': section.get_id() if isinstance(section, EpubHtml) else 'sep_%d' % uid})
                    nl = etree.SubElement(np, 'navLabel')
                    nt = etree.SubElement(nl, 'text')
                    nt.text = section.title
                    href = ''
                    if isinstance(section, EpubHtml):
                        href = section.file_name
                    else:
                        if isinstance(section, Section) and section.href != '':
                            href = section.href
                        elif isinstance(section, Link):
                            href = section.href
                    nc = etree.SubElement(np, 'content', {'src': href})
                    uid = _create_section(np, subsection, uid + 1)
                else:
                    if isinstance(item, Link):
                        _parent = itm
                        _content = _parent.find('content')
                        if _content != None and _content.get('src') == '':
                            _content.set('src', item.href)
                        np = etree.SubElement(itm, 'navPoint', {'id': item.uid})
                        nl = etree.SubElement(np, 'navLabel')
                        nt = etree.SubElement(nl, 'text')
                        nt.text = item.title
                        nc = etree.SubElement(np, 'content', {'src': item.href})
                    elif isinstance(item, EpubHtml):
                        _parent = itm
                        _content = _parent.find('content')
                        if _content != None and _content.get('src') == '':
                            _content.set('src', item.file_name)
                        np = etree.SubElement(itm, 'navPoint', {'id': item.get_id()})
                        nl = etree.SubElement(np, 'navLabel')
                        nt = etree.SubElement(nl, 'text')
                        nt.text = item.title
                        nc = etree.SubElement(np, 'content', {'src': item.file_name})

            return uid

        _create_section(nav_map, self.book.toc, 0)
        tree_str = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return tree_str

    def _write_items(self):
        for item in self.book.get_items():
            if isinstance(item, EpubNcx):
                self.out.writestr('%s/%s' % (self.book.FOLDER_NAME, item.file_name), self._get_ncx())
            else:
                if isinstance(item, EpubNav):
                    self.out.writestr('%s/%s' % (self.book.FOLDER_NAME, item.file_name), self._get_nav(item))
                else:
                    if item.manifest:
                        self.out.writestr('%s/%s' % (self.book.FOLDER_NAME, item.file_name), item.get_content())
                    else:
                        self.out.writestr('%s' % item.file_name, item.get_content())

    def write(self):
        self.out = zipfile.ZipFile(self.file_name, 'w', zipfile.ZIP_DEFLATED)
        self.out.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        self._write_container()
        self._write_opf_file()
        self._write_items()
        self.out.close()


class EpubReader(object):
    DEFAULT_OPTIONS = {}

    def __init__(self, epub_file_name, options=None):
        self.file_name = epub_file_name
        self.book = EpubBook()
        self.zf = None
        self.opf_file = ''
        self.opf_dir = ''
        self.options = dict(self.DEFAULT_OPTIONS)
        if options:
            self.options.update(options)

    def process(self):
        for plg in self.options.get('plugins', []):
            if hasattr(plg, 'after_read'):
                plg.after_read(self.book)

        for item in self.book.get_items():
            if isinstance(item, EpubHtml):
                for plg in self.options.get('plugins', []):
                    if hasattr(plg, 'html_after_read'):
                        plg.html_after_read(self.book, item)

    def load(self):
        self._load()
        return self.book

    def read_file(self, name):
        return self.zf.read(name)

    def _load_container(self):
        meta_inf = self.read_file('META-INF/container.xml')
        tree = parse_string(meta_inf)
        for root_file in tree.findall('//xmlns:rootfile[@media-type]', namespaces={'xmlns': NAMESPACES['CONTAINERNS']}):
            if root_file.get('media-type') == 'application/oebps-package+xml':
                self.opf_file = root_file.get('full-path')
                self.opf_dir = zip_path.dirname(self.opf_file)

    def _load_metadata(self):
        container_root = self.container.getroot()
        self.book.version = container_root.get('version', None)
        if container_root.get('unique-identifier', None):
            self.book.IDENTIFIER_ID = container_root.get('unique-identifier')
        metadata = self.container.find('{%s}%s' % (NAMESPACES['OPF'], 'metadata'))
        nsmap = metadata.nsmap
        nstags = dict((k, '{%s}' % v) for k, v in six.iteritems(nsmap))
        default_ns = nstags.get(None, '')
        nsdict = dict((v, {}) for v in nsmap.values())

        def add_item(ns, tag, value, extra):
            if ns not in nsdict:
                nsdict[ns] = {}
            values = nsdict[ns].setdefault(tag, [])
            values.append((value, extra))

        for t in metadata:
            if not not etree.iselement(t):
                if t.tag is etree.Comment:
                    pass
                else:
                    if t.tag == default_ns + 'meta':
                        name = t.get('name')
                        others = dict((k, v) for k, v in t.items())
                        if name and ':' in name:
                            prefix, name = name.split(':', 1)
                        else:
                            prefix = None
                        add_item(t.nsmap.get(prefix, prefix), name, t.text, others)
                    else:
                        tag = t.tag[t.tag.rfind('}') + 1:]
                        if t.prefix and t.prefix.lower() == 'dc' and tag == 'identifier':
                            _id = t.get('id', None)
                            if _id:
                                self.book.IDENTIFIER_ID = _id
                            others = dict((k, v) for k, v in t.items())
                            add_item(t.nsmap[t.prefix], tag, t.text, others)

        self.book.metadata = nsdict
        titles = self.book.get_metadata('DC', 'title')
        if len(titles) > 0:
            self.book.title = titles[0][0]
        for value, others in self.book.get_metadata('DC', 'identifier'):
            if others.get('id') == self.book.IDENTIFIER_ID:
                self.book.uid = value

    def _load_manifest(self):
        for r in self.container.find('{%s}%s' % (NAMESPACES['OPF'], 'manifest')):
            if r is not None and r.tag != '{%s}item' % NAMESPACES['OPF']:
                pass
            else:
                media_type = r.get('media-type')
                _properties = r.get('properties', '')
                if _properties:
                    properties = _properties.split(' ')
                else:
                    properties = []
                if media_type == 'image/jpg':
                    media_type = 'image/jpeg'
                if media_type == 'application/x-dtbncx+xml':
                    ei = EpubNcx(uid=r.get('id'), file_name=unquote(r.get('href')))
                    ei.content = self.read_file(zip_path.join(self.opf_dir, ei.file_name))
                else:
                    if media_type == 'application/xhtml+xml':
                        if 'nav' in properties:
                            ei = EpubNav(uid=r.get('id'), file_name=unquote(r.get('href')))
                            ei.content = self.read_file(zip_path.join(self.opf_dir, r.get('href')))
                        else:
                            if 'cover' in properties:
                                ei = EpubCoverHtml()
                                ei.content = self.read_file(os_path.join(self.opf_dir, unquote(r.get('href'))))
                            else:
                                ei = EpubHtml()
                                ei.id = r.get('id')
                                ei.file_name = unquote(r.get('href'))
                                ei.media_type = media_type
                                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
                                ei.properties = properties
                    else:
                        if media_type in IMAGE_MEDIA_TYPES:
                            if 'cover-image' in properties:
                                ei = EpubCover(uid=r.get('id'), file_name=unquote(r.get('href')))
                                ei.media_type = media_type
                                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
                            else:
                                ei = EpubImage()
                                ei.id = r.get('id')
                                ei.file_name = unquote(r.get('href'))
                                ei.media_type = media_type
                                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
                        else:
                            ei = EpubItem()
                            ei.id = r.get('id')
                            ei.file_name = unquote(r.get('href'))
                            ei.media_type = media_type
                            ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
                self.book.add_item(ei)

    def _parse_ncx(self, data):
        tree = parse_string(data)
        tree_root = tree.getroot()
        nav_map = tree_root.find('{%s}navMap' % NAMESPACES['DAISY'])

        def _get_children(elems, n, nid):
            label, content = ('', '')
            children = []
            _id = ''
            for a in elems.getchildren():
                if a.tag == '{%s}navLabel' % NAMESPACES['DAISY']:
                    label = a.getchildren()[0].text
                if a.tag == '{%s}content' % NAMESPACES['DAISY']:
                    content = a.get('src', '')
                if a.tag == '{%s}navPoint' % NAMESPACES['DAISY']:
                    children.append(_get_children(a, n + 1, a.get('id', '')))

            if len(children) > 0:
                if n == 0:
                    return children
                return (
                 Section(label, href=content),
                 children)
            else:
                return Link(content, label, nid)

        self.book.toc = _get_children(nav_map, 0, '')

    def _parse_nav(self, data, base_path):
        html_node = parse_html_string(data)
        nav_node = html_node.xpath("//nav[@*='toc']")[0]

        def parse_list(list_node):
            items = []
            for item_node in list_node.findall('li'):
                sublist_node = item_node.find('ol')
                link_node = item_node.find('a')
                if sublist_node is not None:
                    title = item_node[0].text
                    children = parse_list(sublist_node)
                    if link_node is not None:
                        href = zip_path.normpath(zip_path.join(base_path, link_node.get('href')))
                        items.append((Section(title, href=href), children))
                    else:
                        items.append((Section(title), children))
                elif link_node is not None:
                    title = link_node.text
                    href = zip_path.normpath(zip_path.join(base_path, link_node.get('href')))
                    items.append(Link(href, title))

            return items

        self.book.toc = parse_list(nav_node.find('ol'))

    def _load_spine(self):
        spine = self.container.find('{%s}%s' % (NAMESPACES['OPF'], 'spine'))
        self.book.spine = [(t.get('idref'), t.get('linear', 'yes')) for t in spine]
        toc = spine.get('toc', '')
        if toc:
            try:
                ncxFile = self.read_file(zip_path.join(self.opf_dir, self.book.get_item_with_id(toc).get_name()))
            except KeyError:
                raise EpubError(-1, 'Can not find ncx file.')

            self._parse_ncx(ncxFile)

    def _load_guide(self):
        guide = self.container.find('{%s}%s' % (NAMESPACES['OPF'], 'guide'))
        if guide is not None:
            self.book.guide = [{'href': t.get('href'), 'title': t.get('title'), 'type': t.get('type')} for t in guide]

    def _load_opf_file(self):
        try:
            s = self.read_file(self.opf_file)
        except KeyError:
            raise EpubError(-1, 'Can not find container file')

        self.container = parse_string(s)
        self._load_metadata()
        self._load_manifest()
        self._load_spine()
        self._load_guide()
        if not self.book.toc:
            nav_item = next((item for item in self.book.items if isinstance(item, EpubNav)), None)
            if nav_item:
                self._parse_nav(nav_item.content, zip_path.dirname(nav_item.file_name))

    def _load(self):
        try:
            self.zf = zipfile.ZipFile(self.file_name, 'r', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        except zipfile.BadZipfile as bz:
            raise EpubException(0, 'Bad Zip file')
        except zipfile.LargeZipFile as bz:
            raise EpubException(1, 'Large Zip file')

        self._load_container()
        self._load_opf_file()
        self.zf.close()


def write_epub(name, book, options=None):
    """
    Creates epub file with the content defined in EpubBook.

    >>> ebooklib.write_epub('book.epub', book)

    :Args:
      - name: file name for the output file
      - book: instance of EpubBook
      - options: extra opions as dictionary (optional)
    """
    epub = EpubWriter(name, book, options)
    epub.process()
    try:
        epub.write()
    except IOError:
        pass


def read_epub(name, options=None):
    """
    Creates new instance of EpubBook with the content defined in the input file.

    >>> book = ebooklib.read_epub('book.epub')

    :Args:
      - name: full path to the input file
      - options: extra options as dictionary (optional)

    :Returns:
      Instance of EpubBook.
    """
    reader = EpubReader(name, options)
    book = reader.load()
    reader.process()
    return book