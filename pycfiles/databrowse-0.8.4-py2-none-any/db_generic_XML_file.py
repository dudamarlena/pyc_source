# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_generic_XML_file\db_generic_XML_file.py
# Compiled at: 2020-02-17 13:30:46
""" plugins/renderers/db_xml_generic.py - Default Text Renderer """
import os, os.path, time, platform
if platform.system() == 'Linux':
    import pwd, grp
from stat import *
from lxml import etree
from databrowse.support.renderer_support import renderer_class
import magic

class db_generic_XML_file(renderer_class):
    """ Default Renderer - Basic Output for Any XML File """
    _namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/dbxml'
    _namespace_local = 'dbxml'
    _default_content_mode = 'full'
    _default_style_mode = 'XML_preview'
    _default_recursion_depth = 2

    def getContent(self):
        if self._caller != 'databrowse':
            return
        else:
            if self._content_mode == 'full' and self._style_mode == 'no_provenance':
                try:
                    st = os.stat(self._fullpath)
                except IOError:
                    return 'Failed To Get File Information: %s' % self._fullpath

                file_size = st[ST_SIZE]
                file_mtime = time.asctime(time.localtime(st[ST_MTIME]))
                file_ctime = time.asctime(time.localtime(st[ST_CTIME]))
                file_atime = time.asctime(time.localtime(st[ST_ATIME]))
                if platform.system() is 'Windows':
                    contenttype = magic.from_file(self._fullpath, mime=True)
                else:
                    magicstore = magic.open(magic.MAGIC_MIME)
                    magicstore.load()
                    contenttype = magicstore.file(self._fullpath)
                extension = os.path.splitext(self._fullpath)[1][1:]
                icon = self._handler_support.GetIcon(contenttype, extension)
                downlink = self.getURL(self._relpath, content_mode='raw', download='true')
                xmlroot = etree.Element('{%s}dbxml' % self._namespace_uri, nsmap=self.nsmap, name=os.path.basename(self._relpath), resurl=self._web_support.resurl, downlink=downlink, icon=icon)
                xmlchild = etree.SubElement(xmlroot, 'filename', nsmap=self.nsmap)
                xmlchild.text = os.path.basename(self._fullpath)
                xmlchild = etree.SubElement(xmlroot, 'path', nsmap=self.nsmap)
                xmlchild.text = os.path.dirname(self._fullpath)
                xmlchild = etree.SubElement(xmlroot, 'size', nsmap=self.nsmap)
                xmlchild.text = self.ConvertUserFriendlySize(file_size)
                xmlchild = etree.SubElement(xmlroot, 'mtime', nsmap=self.nsmap)
                xmlchild.text = file_mtime
                xmlchild = etree.SubElement(xmlroot, 'ctime', nsmap=self.nsmap)
                xmlchild.text = file_ctime
                xmlchild = etree.SubElement(xmlroot, 'atime', nsmap=self.nsmap)
                xmlchild.text = file_atime
                xmlchild = etree.SubElement(xmlroot, 'contenttype', nsmap=self.nsmap)
                xmlchild.text = contenttype
                xmlchild = etree.SubElement(xmlroot, 'permissions', nsmap=self.nsmap)
                xmlchild.text = self.ConvertUserFriendlyPermissions(st[ST_MODE])
                if platform.system() == 'Linux':
                    try:
                        username = pwd.getpwuid(st[ST_UID])[0]
                    except KeyError:
                        username = ''

                    groupname = grp.getgrgid(st[ST_GID])[0]
                    xmlchild = etree.SubElement(xmlroot, 'owner', nsmap=self.nsmap)
                    xmlchild.text = '%s:%s' % (username, groupname)
                f = open(self._fullpath)
                xmlchild = etree.SubElement(xmlroot, 'contents', nsmap=self.nsmap)
                tree = etree.XML(f.read())
                for bad in tree.xpath('//lip:*', namespaces={'lip': 'http://limatix.org/provenance'}):
                    bad.getparent().remove(bad)

                attributes = tree.xpath("name(//@*[namespace-uri()='lip'])", namespaces={'lip': 'http://limatix.org/provenance'})
                if attributes:
                    if not isinstance(attributes, list):
                        attributes = [
                         attributes]
                    for bad in tree.xpath('//@lip:*', namespaces={'lip': 'http://limatix.org/provenance'}):
                        parent = bad.getparent()
                        for attribute in attributes:
                            val = parent.attrib.get('{http://limatix.org/provenance}' + attribute.split(':')[1])
                            if val:
                                parent.attrib.pop('{http://limatix.org/provenance}' + attribute.split(':')[1])

                xmlchild.append(tree)
                xmlchild.text = etree.tostring(tree)
                f.close()
                return xmlroot
            elif self._content_mode == 'full':
                try:
                    st = os.stat(self._fullpath)
                except IOError:
                    return 'Failed To Get File Information: %s' % self._fullpath

                file_size = st[ST_SIZE]
                file_mtime = time.asctime(time.localtime(st[ST_MTIME]))
                file_ctime = time.asctime(time.localtime(st[ST_CTIME]))
                file_atime = time.asctime(time.localtime(st[ST_ATIME]))
                if platform.system() is 'Windows':
                    contenttype = magic.from_file(self._fullpath, mime=True)
                else:
                    magicstore = magic.open(magic.MAGIC_MIME)
                    magicstore.load()
                    contenttype = magicstore.file(self._fullpath)
                extension = os.path.splitext(self._fullpath)[1][1:]
                icon = self._handler_support.GetIcon(contenttype, extension)
                downlink = self.getURL(self._relpath, content_mode='raw', download='true')
                xmlroot = etree.Element('{%s}dbxml' % self._namespace_uri, nsmap=self.nsmap, name=os.path.basename(self._relpath), resurl=self._web_support.resurl, downlink=downlink, icon=icon)
                xmlchild = etree.SubElement(xmlroot, 'filename', nsmap=self.nsmap)
                xmlchild.text = os.path.basename(self._fullpath)
                xmlchild = etree.SubElement(xmlroot, 'path', nsmap=self.nsmap)
                xmlchild.text = os.path.dirname(self._fullpath)
                xmlchild = etree.SubElement(xmlroot, 'size', nsmap=self.nsmap)
                xmlchild.text = self.ConvertUserFriendlySize(file_size)
                xmlchild = etree.SubElement(xmlroot, 'mtime', nsmap=self.nsmap)
                xmlchild.text = file_mtime
                xmlchild = etree.SubElement(xmlroot, 'ctime', nsmap=self.nsmap)
                xmlchild.text = file_ctime
                xmlchild = etree.SubElement(xmlroot, 'atime', nsmap=self.nsmap)
                xmlchild.text = file_atime
                xmlchild = etree.SubElement(xmlroot, 'contenttype', nsmap=self.nsmap)
                xmlchild.text = contenttype
                xmlchild = etree.SubElement(xmlroot, 'permissions', nsmap=self.nsmap)
                xmlchild.text = self.ConvertUserFriendlyPermissions(st[ST_MODE])
                if platform.system() == 'Linux':
                    try:
                        username = pwd.getpwuid(st[ST_UID])[0]
                    except KeyError:
                        username = ''

                    groupname = grp.getgrgid(st[ST_GID])[0]
                    xmlchild = etree.SubElement(xmlroot, 'owner', nsmap=self.nsmap)
                    xmlchild.text = '%s:%s' % (username, groupname)
                f = open(self._fullpath)
                xmlchild = etree.SubElement(xmlroot, 'contents', nsmap=self.nsmap)
                xmlchild.append(etree.XML(f.read()))
                f.close()
                return xmlroot
            elif self._content_mode == 'raw':
                size = os.path.getsize(self._fullpath)
                if platform.system() is 'Windows':
                    contenttype = magic.from_file(self._fullpath, mime=True)
                else:
                    magicstore = magic.open(magic.MAGIC_MIME)
                    magicstore.load()
                    contenttype = magicstore.file(self._fullpath)
                f = open(self._fullpath, 'rb')
                self._web_support.req.response_headers['Content-Type'] = contenttype
                self._web_support.req.response_headers['Content-Length'] = str(size)
                self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(self._fullpath)
                self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                self._web_support.req.output_done = True
                if 'wsgi.file_wrapper' in self._web_support.req.environ:
                    return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                return iter(lambda : f.read(1024), '')
            else:
                raise self.RendererException('Invalid Content Mode')
            return