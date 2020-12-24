# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_plain_text_file\db_plain_text_file.py
# Compiled at: 2020-02-17 13:30:46
""" plugins/renderers/db_text_generic.py - Default Text Renderer """
import os, os.path, time
from stat import *
from lxml import etree
import magic
from databrowse.support.renderer_support import renderer_class
import platform
if platform.system() == 'Linux':
    import pwd, grp

class db_plain_text_file(renderer_class):
    """ Default Renderer - Basic Output for Any File """
    _namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/text'
    _namespace_local = 'text'
    _default_content_mode = 'full'
    _default_style_mode = 'plain_text_preview'
    _default_recursion_depth = 2

    def getContent(self):
        if self._caller != 'databrowse':
            return
        else:
            if 'ajax' in self._web_support.req.form and 'save' in self._web_support.req.form:
                if 'file' in self._web_support.req.form:
                    filestring = self._web_support.req.form['file'].value
                    if not os.access(self._fullpath, os.W_OK) and os.path.exists(self._fullpath):
                        self._web_support.req.output = 'Error Saving File:  File Not Writable ' + self._fullpath
                        self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                        return [
                         self._web_support.req.return_page()]
                    if os.path.exists(self._fullpath):
                        filenum = 1
                        while os.path.exists('%s.bak.%.2d' % (self._fullpath, filenum)):
                            filenum += 1

                        os.rename(self._fullpath, '%s.bak.%.2d' % (self._fullpath, filenum))
                    f = open(self._fullpath, 'wb')
                    f.write(filestring)
                    f.close
                    self._web_support.req.output = 'File Saved Successfully'
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                else:
                    self._web_support.req.output = 'Error Saving File: Incomplete Request'
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [self._web_support.req.return_page()]

            elif self._content_mode == 'full':
                try:
                    st = os.stat(self._fullpath)
                except IOError:
                    return 'Failed To Get File Information: %s' % self._fullpath

                file_size = st[ST_SIZE]
                file_mtime = time.asctime(time.localtime(st[ST_MTIME]))
                file_ctime = time.asctime(time.localtime(st[ST_CTIME]))
                file_atime = time.asctime(time.localtime(st[ST_ATIME]))
                try:
                    magicstore = magic.open(magic.MAGIC_MIME)
                    magicstore.load()
                    contenttype = magicstore.file(os.path.realpath(self._fullpath))
                except AttributeError:
                    contenttype = magic.from_file(os.path.realpath(self._fullpath), mime=True)

                if contenttype is None:
                    contenttype = 'text/plain'
                extension = os.path.splitext(self._fullpath)[1][1:]
                icon = self._handler_support.GetIcon(contenttype, extension)
                downlink = self.getURL(self._relpath, content_mode='raw', download='true')
                xmlroot = etree.Element('{%s}text' % self._namespace_uri, nsmap=self.nsmap, name=os.path.basename(self._relpath), resurl=self._web_support.resurl, downlink=downlink, icon=icon)
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
                xmlchild.text = unicode(f.read(), errors='replace')
                f.close()
                return xmlroot
            elif self._content_mode == 'raw':
                size = os.path.getsize(self._fullpath)
                try:
                    magicstore = magic.open(magic.MAGIC_MIME)
                    magicstore.load()
                    contenttype = magicstore.file(os.path.realpath(self._fullpath))
                except AttributeError:
                    contenttype = magic.from_file(os.path.realpath(self._fullpath), mime=True)

                if contenttype is None:
                    contenttype = 'text/plain'
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