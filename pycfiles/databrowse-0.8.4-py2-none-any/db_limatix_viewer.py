# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_limatix_viewer\db_limatix_viewer.py
# Compiled at: 2020-02-18 00:16:42
""" plugins/renderers/db_xlg_viewer.py - Experiment Log Viewer """
import sys, os, glob, zipfile, tempfile
from urllib import pathname2url
from lxml import etree
from databrowse.support.renderer_support import renderer_class
from databrowse.plugins.db_data_table.db_data_table import db_data_table
import magic

class db_limatix_viewer(renderer_class):
    """ Experiment Log Viewer """
    _namespace_uri = 'http://limatix.org/datacollect'
    _namespace_local = 'dc'
    _default_content_mode = 'full'
    _default_style_mode = 'log_view'
    _default_recursion_depth = 2

    def getContent(self):
        if self._caller != 'databrowse':
            return
        else:
            if self._content_mode == 'full' and self._style_mode in ('old_log_view',
                                                                     'old_tabular_view'):
                p = etree.XMLParser(huge_tree=True)
                xmlroot = etree.parse(self._fullpath, parser=p).getroot()
                try:
                    reldest = xmlroot.xpath('dc:summary/dc:reldest', namespaces={'dc': 'http://limatix.org/datacollect'})[0].text
                    reldesturl = self.getURL(os.path.abspath(os.path.join(os.path.dirname(self._relpath), reldest)))
                    xmlroot.set('reldesturl', reldesturl)
                except:
                    xmlroot.set('reldesturl', '')

                configlist = xmlroot.xpath('dc:configstr', namespaces={'dc': 'http://limatix.org/datacollect'})
                for item in configlist:
                    try:
                        fname = item.get('fname')
                        fnames = item.get('fnames')
                        if fname:
                            path = os.path.realpath(fname)
                            if path.startswith(os.path.normpath(self._web_support.dataroot)) and os.access(path, os.R_OK) and os.path.exists(path):
                                relpath = path.replace(self._web_support.dataroot, '')
                                url = self.getURL(relpath)
                                item.set('url', url)
                        elif fnames:
                            if fnames[0] == '[' and fnames[(-1)] == ']':
                                urls = []
                                fnamelist = fnames[1:-1].split(',')
                                for fname in fnamelist:
                                    fname = fname.replace("'", '').replace('"', '').strip()
                                    path = os.path.realpath(fname)
                                    if path.startswith(os.path.normpath(self._web_support.dataroot)) and os.access(path, os.R_OK) and os.path.exists(path):
                                        relpath = path.replace(self._web_support.dataroot, '')
                                        url = self.getURL(relpath)
                                        urls.append(url)
                                    else:
                                        urls.append('')

                                item.set('urls', repr(urls))
                    except:
                        pass

                specimenlist = xmlroot.xpath('//dc:specimen', namespaces={'dc': 'http://limatix.org/datacollect', 'dcv': 'http://limatix.org/dcvalue'})
                for item in specimenlist:
                    if item.text:
                        relpath = '/specimens/' + item.text + '.sdb'
                        if os.access(os.path.abspath(self._web_support.dataroot + '/' + relpath), os.R_OK) and os.path.exists(os.path.abspath(self._web_support.dataroot + '/' + relpath)):
                            url = self.getURL(relpath)
                            item.set('url', url)

                transducerlist = xmlroot.xpath('//dc:xducer', namespaces={'dc': 'http://limatix.org/datacollect', 'dcv': 'http://limatix.org/dcvalue'})
                for item in transducerlist:
                    if item.text:
                        relpath = '/transducers/' + item.text + '.tdb'
                        if os.access(os.path.abspath(self._web_support.dataroot + '/' + relpath), os.R_OK) and os.path.exists(os.path.abspath(self._web_support.dataroot + '/' + relpath)):
                            url = self.getURL(relpath)
                            item.set('url', url)

                return xmlroot
            if self._content_mode == 'full' and self._style_mode != 'limatix_custom_view':
                p = etree.XMLParser(huge_tree=True)
                xmlroot = etree.parse(self._fullpath, parser=p).getroot()
                configlist = xmlroot.xpath('dc:config/dc:configfile', namespaces={'dc': 'http://limatix.org/datacollect'})
                for item in configlist:
                    try:
                        xlink = item.get('{http://www.w3.org/1999/xlink}href')
                        if xlink:
                            path = os.path.realpath(fname)
                            if path.startswith(os.path.normpath(self._web_support.dataroot)) and os.access(path, os.R_OK) and os.path.exists(path):
                                relpath = path.replace(self._web_support.dataroot, '')
                                url = self.getURL(relpath)
                                item.set('url', url)
                    except:
                        pass

                specimenlist = xmlroot.xpath('//dc:specimen', namespaces={'dc': 'http://limatix.org/datacollect', 'dcv': 'http://limatix.org/dcvalue'})
                for item in specimenlist:
                    if item.text:
                        relpath = '/specimens/' + item.text + '.sdb'
                        if os.access(os.path.abspath(self._web_support.dataroot + '/' + relpath), os.R_OK) and os.path.exists(os.path.abspath(self._web_support.dataroot + '/' + relpath)):
                            url = self.getURL(relpath)
                            item.set('url', url)

                transducerlist = xmlroot.xpath('//dc:xducer', namespaces={'dc': 'http://limatix.org/datacollect', 'dcv': 'http://limatix.org/dcvalue'})
                for item in transducerlist:
                    if item.text:
                        relpath = '/transducers/' + item.text + '.tdb'
                        if os.access(os.path.abspath(self._web_support.dataroot + '/' + relpath), os.R_OK) and os.path.exists(os.path.abspath(self._web_support.dataroot + '/' + relpath)):
                            url = self.getURL(relpath)
                            item.set('url', url)

                return xmlroot
            if self._content_mode == 'full' and self._style_mode == 'limatix_custom_view':
                self._namespace_local = 'dt'
                self._namespace_uri = 'http://limatix.org/databrowse/datatable'
                if 'custom_view' not in self._web_support.req.form:
                    raise self.RendererException('Custom View Selection Required')
                xml = etree.parse(os.path.join(os.path.dirname(self._fullpath), self._web_support.req.form['custom_view'].value))
                namespaces = (' ').join([ 'xmlns:' + str(item) + '="' + str(value) + '"' for item, value in xml.getroot().nsmap.iteritems() ])
                root = xml.getroot()
                root.set('filenamematch', os.path.basename(self._fullpath))
                ext_module = db_data_table.MyExt(os.path.join(os.path.dirname(self._fullpath), self._web_support.req.form['custom_view'].value))
                extensions = etree.Extension(ext_module, ('data', 'xmlassert'), ns='http://limatix.org/databrowse/datatable/functions')
                root = xml.xslt(etree.XML(db_data_table._table_transform % (namespaces, self._web_support.siteurl, self.getURL(os.path.join(os.path.dirname(self._relpath), self._web_support.req.form['custom_view'].value)), self._web_support.req.form['custom_view'].value)), extensions=extensions).getroot()
                root.set('custom_view', self._web_support.req.form['custom_view'].value)
                return root
            if self._content_mode == 'raw':
                if 'filetype' in self._web_support.req.form:
                    self._namespace_local = 'dt'
                    self._namespace_uri = 'http://limatix.org/databrowse/datatable'
                    if 'custom_view' not in self._web_support.req.form:
                        raise self.RendererException('Custom View Selection Required')
                    xml = etree.parse(os.path.join(os.path.dirname(self._fullpath), self._web_support.req.form['custom_view'].value))
                    namespaces = (' ').join([ 'xmlns:' + str(item) + '="' + str(value) + '"' for item, value in xml.getroot().nsmap.iteritems() ])
                    root = xml.getroot()
                    root.set('filenamematch', os.path.basename(self._fullpath))
                    ext_module = db_data_table.MyExt(os.path.join(os.path.dirname(self._fullpath), self._web_support.req.form['custom_view'].value))
                    extensions = etree.Extension(ext_module, ('data', 'xmlassert'), ns='http://limatix.org/databrowse/datatable/functions')
                    base = xml.xslt(etree.XML(db_data_table._table_transform % (namespaces, self._web_support.siteurl, self.getURL(os.path.join(os.path.dirname(self._relpath), self._web_support.req.form['custom_view'].value)), self._web_support.req.form['custom_view'].value)), extensions=extensions)
                    filename = str(base.xpath('//@title')[0])
                    if self._web_support.req.form['filetype'].value == 'ods':
                        result = etree.tostring(base.xslt(etree.XML(db_data_table._ods_transform)))
                        f = tempfile.TemporaryFile()
                        if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
                            zipfile_compression = zipfile.ZIP_STORED
                        else:
                            zipfile_compression = zipfile.ZIP_DEFLATED
                        zf = zipfile.ZipFile(f, 'w', zipfile_compression)
                        if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
                            zf.writestr('mimetype', 'application/vnd.oasis.opendocument.spreadsheet')
                        else:
                            zf.writestr('mimetype', 'application/vnd.oasis.opendocument.spreadsheet', compress_type=zipfile.ZIP_STORED)
                        zf.writestr('META-INF/manifest.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">\n    <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.spreadsheet" manifest:full-path="/"/>\n    <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>\n    <!-- manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/-->\n    <!-- manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/-->\n    <!-- manifest:file-entry manifest:media-type="text/xml" manifest:full-path="settings.xml"/-->\n</manifest:manifest>\n')
                        zf.writestr('content.xml', result)
                        zf.close()
                        self._web_support.req.response_headers['Content-Type'] = 'application/vnd.oasis.opendocument.spreadsheet'
                        self._web_support.req.response_headers['Content-Length'] = str(f.tell())
                        f.seek(0, 0)
                        self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + filename + '.ods'
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                        return iter(lambda : f.read(1024), '')
                    elif self._web_support.req.form['filetype'].value == 'csv':
                        f = tempfile.TemporaryFile()
                        coldef = base.xpath('dt:header/dt:coldef', namespaces={'dt': 'http://limatix.org/databrowse/datatable'})
                        f.write((',').join([ x.text for x in coldef ]) + '\n')
                        for row in base.xpath('dt:row', namespaces={'dt': 'http://limatix.org/databrowse/datatable'}):
                            datadef = row.xpath('dt:data/.', namespaces={'dt': 'http://limatix.org/databrowse/datatable'})
                            f.write((',').join([ x.text if x.text is not None else '' for x in datadef ]) + '\n')

                        f.flush()
                        f.seek(0, 2)
                        self._web_support.req.response_headers['Content-Type'] = 'text/csv'
                        self._web_support.req.response_headers['Content-Length'] = str(f.tell())
                        f.seek(0, 0)
                        self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + filename + '.csv'
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                        return iter(lambda : f.read(1024), '')
                    else:
                        raise self.RendererException('Invalid File Type')
                else:
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

    def loadMenu(self):
        """ Load Menu Items for all current handlers """
        newmenu = etree.Element('{http://thermal.cnde.iastate.edu/databrowse}navbar')
        isDirectory = os.path.isdir(self._fullpath)
        for handler in reversed(self._handlers):
            dirlist = [ os.path.splitext(item)[0][4:] for item in os.listdir(os.path.abspath(os.path.dirname(sys.modules[('databrowse.plugins.' + handler)].__file__) + '/')) if item.lower().startswith('dbs_') ]
            additionalitems = []
            if isDirectory:
                if os.path.exists(os.path.join(self._fullpath, '.databrowse', 'stylesheets', handler)):
                    additionalitems = [ os.path.splitext(item)[0][4:] for item in os.listdir(os.path.join(self._fullpath, '.databrowse', 'stylesheets', handler)) if item.lower().startswith('dbs_') ]
            else:
                if os.path.exists(os.path.join(os.path.dirname(self._fullpath), '.databrowse', 'stylesheets', handler)):
                    additionalitems = [ os.path.splitext(item)[0][4:] for item in os.listdir(os.path.join(os.path.dirname(self._fullpath), '.databrowse', 'stylesheets', handler)) if item.lower().startswith('dbs_') ]
                dirlist = dirlist + additionalitems
                navelem = etree.SubElement(newmenu, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
                title = etree.SubElement(navelem, '{http://www.w3.org/1999/xhtml}a')
                title.text = (' ').join([ i[0].title() + i[1:] for i in handler[3:].split('_') ])
                navitems = etree.SubElement(navelem, '{http://thermal.cnde.iastate.edu/databrowse}navdir', alwaysopen='true')
                for item in dirlist:
                    if item not in self._handler_support.hiddenstylesheets:
                        if not isDirectory and item not in self._handler_support.directorystylesheets:
                            link = self.getURL(self._relpath, handler=handler, style_mode=item)
                            if self._style_mode == item and self.__class__.__name__ == handler:
                                itemelem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem', selected='true')
                            else:
                                itemelem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
                            menuitem = etree.SubElement(itemelem, '{http://www.w3.org/1999/xhtml}a', href=link)
                            menuitem.text = (' ').join([ i[0].title() + i[1:] for i in item.split('_') ])
                        elif isDirectory:
                            link = self.getURL(self._relpath, handler=handler, style_mode=item)
                            if self._style_mode == item and self.__class__.__name__ == handler:
                                itemelem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem', selected='true')
                            else:
                                itemelem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
                            menuitem = etree.SubElement(itemelem, '{http://www.w3.org/1999/xhtml}a', href=link)
                            menuitem.text = (' ').join([ i[0].title() + i[1:] for i in item.split('_') ])
                        else:
                            continue

        curdirlist = [ item for item in os.listdir(os.path.abspath(os.path.dirname(self._fullpath))) if os.path.splitext(item)[1] == '.tbl' ]
        customitems = {}
        cwd = os.getcwd()
        os.chdir(os.path.dirname(self._fullpath))
        for item in curdirlist:
            try:
                xml = etree.parse(os.path.abspath(os.path.join(os.path.dirname(self._fullpath), item)))
                filename = xml.xpath('@filenamematch')[0]
                filelist = glob.glob(filename)
                for filename in filelist:
                    if filename == os.path.basename(self._fullpath):
                        it = item if not item.startswith('.') else item[1:]
                        title = (' ').join([ i[0].title() + i[1:] for i in os.path.splitext(it)[0].split('_') ])
                        customitems[item] = title
                        continue

            except:
                pass

        os.chdir(cwd)
        navelem = newmenu[0]
        navitems = navelem[1]
        for item in customitems:
            link = self.getURL(self._relpath, handler='db_limatix_viewer', style_mode='limatix_custom_view', custom_view=item)
            if self._style_mode == 'limatix_custom_view' and self._web_support.req.form['custom_view'].value == item:
                itemelem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem', selected='true')
            else:
                itemelem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
            menuitem = etree.SubElement(itemelem, '{http://www.w3.org/1999/xhtml}a', href=link)
            menuitem.text = customitems[item]

        self._web_support.menu.AddMenu(newmenu)

    def loadStyleFunction(self):
        """ Override Load Style Function to Replace URL """
        custompath = os.path.abspath((self._fullpath if os.path.isdir(self._fullpath) else os.path.dirname(self._fullpath)) + '/.databrowse/stylesheets/' + self.__class__.__name__ + '/dbs_' + self._style_mode + '.xml')
        defaultpath = os.path.abspath(os.path.dirname(sys.modules[('databrowse.plugins.' + self.__class__.__name__)].__file__) + '/dbs_' + self._style_mode + '.xml')
        filename = custompath if os.path.exists(custompath) else None
        override = False
        if filename is not None:
            override = True if os.path.exists(defaultpath) or hasattr(self, '_style_' + self._style_mode) else False
        if filename is None:
            if self._web_support.style.IsStyleLoaded(self._namespace_uri) and override != True:
                return
            filename = defaultpath if os.path.exists(defaultpath) else None
        if filename is None:
            if hasattr(self, '_style_' + self._style_mode):
                stylestring = getattr(self, '_style_' + self._style_mode)
            else:
                raise self.RendererException('Unable To Locate Stylesheet for Style Mode %s in %s' % (self._style_mode, self.__class__.__name__))
        else:
            f = open(filename, 'r')
            stylestring = f.read()
            f.close()
        stylestring = stylestring.replace('/usr/local/limatix-qautils/checklist/datacollect2.xsl', pathname2url(os.path.join(self._web_support.limatix_qautils, 'checklist/datacollect2.xsl')).replace('///', ''))
        if override is True:
            randomid = ('').join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
            newnamespace = self._namespace_uri + randomid
            newlocalns = self._namespace_local + randomid
            newnamedtemplates = self.__class__.__name__ + '-' + randomid + '-'
            stylestring = stylestring.replace(self._namespace_uri, newnamespace)
            stylestring = stylestring.replace(self._namespace_local + ':', newlocalns + ':')
            stylestring = stylestring.replace('xmlns:' + self._namespace_local, 'xmlns:' + newlocalns)
            stylestring = stylestring.replace(self.__class__.__name__ + '-', newnamedtemplates)
            self._namespace_uri = newnamespace
            self._namespace_local = newlocalns
        self._web_support.style.AddStyle(self._namespace_uri, stylestring)
        return