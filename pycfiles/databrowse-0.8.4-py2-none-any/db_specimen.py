# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_specimen\db_specimen.py
# Compiled at: 2018-09-22 17:12:57
""" plugins/renderers/db_specimen.py - Default Text Renderer """
import os, qrcode
from urllib import quote, unquote
from PIL import Image
import StringIO, subprocess
from lxml import etree
from databrowse.support.renderer_support import renderer_class
import databrowse.support.specimen_support as ss

class db_specimen(renderer_class):
    """ Default Renderer - Basic Output for Any XML File """
    _namespace_uri = 'http://thermal.cnde.iastate.edu/specimen'
    _namespace_local = 'specimen'
    _default_content_mode = 'full'
    _default_style_mode = 'view_specimen_data'
    _default_recursion_depth = 2

    def getContent(self):
        if self._content_mode != 'raw' and self._caller == 'databrowse' and 'ajax' not in self._web_support.req.form:
            filerelpath = None
            specimen = os.path.splitext(os.path.basename(self._fullpath))[0]
            if self._style_mode == 'edit_specimen_data':
                xml = etree.parse(self._fullpath)
            else:
                xml = ss.GetSpecimen(specimen, ss.OUTPUT_ETREE, os.path.dirname(self._fullpath))
            xmlroot = xml.getroot()
            reldests = [ x for x in xmlroot.xpath('specimen:reldests/specimen:reldest', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'}) ]
            for reldest in reldests:
                if reldest.get('{http://www.w3.org/1999/xlink}href') is not None:
                    reldesttext = reldest.get('{http://www.w3.org/1999/xlink}href')
                else:
                    reldesttext = reldest.text
                filerelpath = os.path.join(os.path.dirname(self._relpath), reldesttext)
                filefullpath = os.path.abspath(self._web_support.dataroot + '/' + filerelpath)
                if os.path.exists(filefullpath) and self._style_mode == 'view_specimen_data':
                    import databrowse.plugins.db_directory.db_directory as db_directory_module
                    renderer = db_directory_module.db_directory(filerelpath, filefullpath, self._web_support, self._handler_support, 'db_specimen', 'db_directory', style_mode='empty')
                    content = renderer.getContent()
                    reldest.set('link', self.getURL(filerelpath))
                    if reldest.get('fromgroup'):
                        content.set('fromgroup', reldest.get('fromgroup'))
                    xmlroot.append(content)

            groups = [ x for x in xmlroot.xpath('specimen:groups/specimen:groupid', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'}) ]
            for group in groups:
                groupid = group.text
                if os.access(os.path.join(self._web_support.dataroot, 'specimens/' + groupid + '.sdg'), os.R_OK) and os.path.exists(os.path.join(self._web_support.dataroot, 'specimens/' + groupid + '.sdg')):
                    group.set('link', self.getURL('/specimens/' + groupid + '.sdg'))

            templatefile = self.getURL('/specimens/src/specimen.xhtml', handler='db_default', content_mode='raw', ContentType='application/xml')
            xmlroot.set('templatefile', templatefile)
            xmlroot.set('barcode', self.getURL(self._relpath, content_mode='raw', barcode='barcode'))
            xmlroot.set('printbarcode', self.getURL(self._relpath, content_mode='raw', printbarcode='printbarcode'))
            if filerelpath:
                try:
                    __import__('imp').find_module('NDI_app')
                    xmlroot.set('nditoolboxlink', self.getURL(self._relpath, content_mode='nditoolbox', dest=quote(filefullpath)))
                except ImportError:
                    xmlroot.set('nditoolboxlink', '')

            return xmlroot
        if self._content_mode != 'raw' and self._caller == 'db_specimen_database' and self._style_mode == 'specimen_list':
            specimen = os.path.splitext(os.path.basename(self._fullpath))[0]
            xml = ss.GetSpecimen(specimen, ss.OUTPUT_ELEMENT, os.path.dirname(self._fullpath))
            groups = [ x for x in xml.xpath('specimen:groups/specimen:groupid', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'}) ]
            for group in groups:
                groupid = group.text
                if os.access(os.path.join(self._web_support.dataroot, 'specimens/' + groupid + '.sdg'), os.R_OK) and os.path.exists(os.path.join(self._web_support.dataroot, 'specimens/' + groupid + '.sdg')):
                    group.set('link', self.getURL('/specimens/' + groupid + '.sdg'))

            return xml
        if self._content_mode != 'raw' and 'ajax' in self._web_support.req.form and 'save' in self._web_support.req.form:
            if 'file' in self._web_support.req.form:
                filestring = self._web_support.req.form['file'].value
                fullfilename = self._fullpath
                if not os.access(os.path.dirname(fullfilename), os.W_OK):
                    self._web_support.req.output = 'Error Saving File:  Save Directory Not Writable ' + os.path.dirname(fullfilename)
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                if not os.access(fullfilename, os.W_OK):
                    self._web_support.req.output = 'Error Saving File:  File Not Writable ' + fullfilename
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                if os.path.exists(fullfilename):
                    filenum = 1
                    while os.path.exists('%s.bak.%.2d' % (fullfilename, filenum)):
                        filenum += 1

                    os.rename(fullfilename, '%s.bak.%.2d' % (fullfilename, filenum))
                f = open(fullfilename, 'w')
                f.write(filestring)
                f.close
                self._web_support.req.output = 'File Saved Successfully'
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [self._web_support.req.return_page()]
            else:
                self._web_support.req.output = 'Error Saving File: Incomplete Request'
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [self._web_support.req.return_page()]
        elif self._content_mode != 'raw' and 'ajax' in self._web_support.req.form and 'checkdigit' in self._web_support.req.form:
            if 'specimen' in self._web_support.req.form:
                spcstr = self._web_support.req.form['specimen'].value
                chkdgt = ss.GenerateCheckdigit(spcstr)
                self._web_support.req.output = spcstr + chkdgt
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [
                 self._web_support.req.return_page()]
            raise self.RendererException('Incomplete Request')
        elif self._content_mode != 'raw' and 'ajax' in self._web_support.req.form and 'addactionitem' in self._web_support.req.form:
            if 'date' not in self._web_support.req.form or self._web_support.req.form['date'].value == '':
                self._web_support.req.output = 'Date is a Required Field'
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [
                 self._web_support.req.return_page()]
            else:
                if 'perfby' not in self._web_support.req.form or self._web_support.req.form['perfby'].value == '':
                    self._web_support.req.output = 'Performed By is a Required Field'
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                if 'action' not in self._web_support.req.form or self._web_support.req.form['action'].value == '':
                    self._web_support.req.output = 'Action is a Required Field'
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                fullfilename = self._fullpath
                xmltree = etree.parse(fullfilename)
                xmlroot = xmltree.getroot()
                actionlog = xmlroot.xpath('specimen:actionlog', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'})
                if actionlog:
                    actionlog = actionlog[0]
                else:
                    actionlog = etree.SubElement(xmlroot, 'actionlog')
                actionevent = etree.SubElement(actionlog, 'actionevent')
                actiondate = etree.SubElement(actionevent, 'date')
                actiondate.text = self._web_support.req.form['date'].value
                actionperfby = etree.SubElement(actionevent, 'perfby')
                actionperfby.text = self._web_support.req.form['perfby'].value
                actionaction = etree.SubElement(actionevent, 'action')
                actionaction.text = self._web_support.req.form['action'].value
                actionnotes = etree.SubElement(actionevent, 'notes')
                actionnotes.text = self._web_support.req.form['notes'].value
                if not os.access(os.path.dirname(fullfilename), os.W_OK):
                    self._web_support.req.output = 'Save Directory Not Writable ' + os.path.dirname(fullfilename)
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                if not os.access(fullfilename, os.W_OK):
                    self._web_support.req.output = 'File Not Writable ' + fullfilename
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [
                     self._web_support.req.return_page()]
                if os.path.exists(fullfilename):
                    filenum = 1
                    while os.path.exists('%s.bak.%.2d' % (fullfilename, filenum)):
                        filenum += 1

                    os.rename(fullfilename, '%s.bak.%.2d' % (fullfilename, filenum))
                f = open(fullfilename, 'w')
                f.write(etree.tostring(xmltree))
                f.close
                self._web_support.req.output = 'Action Item Added Successfully'
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [self._web_support.req.return_page()]

        else:
            if self._content_mode == 'nditoolbox' and 'ajax' in self._web_support.req.form:
                import NDI_app
                subprocess.Popen(['python', NDI_app.__file__, unquote(self._web_support.req.form['dest'].value)], cwd=os.path.dirname(NDI_app.__file__))
                self._web_support.req.output = 'NDITOOlBOX Called Successfully'
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [
                 self._web_support.req.return_page()]
            if self._content_mode == 'raw':
                if 'barcode' in self._web_support.req.form:
                    if self.CacheFileExists('barcode', 'png'):
                        size = os.path.getsize(self.getCacheFileName('barcode', 'png'))
                        f = self.getCacheFileHandler('rb', 'barcode', 'png')
                        self._web_support.req.response_headers['Content-Type'] = 'image/png'
                        self._web_support.req.response_headers['Content-Length'] = str(size)
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                        return iter(lambda : f.read(1024), '')
                    else:
                        sf = open(self._fullpath, 'rb')
                        sdbfile = etree.parse(sf)
                        sf.close()
                        sdbroot = sdbfile.getroot()
                        sdbelem = sdbroot.xpath('specimen:specimenid', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'})[0]
                        img = qrcode.make('<specimen/>' + sdbelem.text)._img
                        img.thumbnail((201, 201), Image.ANTIALIAS)
                        output = StringIO.StringIO()
                        img.save(output, format='png')
                        f = self.getCacheFileHandler('wb', 'barcode', 'png')
                        img.save(f, format='png')
                        f.close()
                        self._web_support.req.response_headers['Content-Type'] = 'image/png'
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        return [output.getvalue()]
                if 'printbarcode' in self._web_support.req.form:
                    try:
                        sf = open(self._fullpath, 'rb')
                        sdbfile = etree.parse(sf)
                        sf.close()
                        sdbroot = sdbfile.getroot()
                        sdbelem = sdbroot.xpath('specimen:specimenid', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'})[0]
                        os.environ['HOME'] = '/home/www/.home'
                        subprocess.call(['/usr/local/bin/printQRcode', '<specimen/>' + sdbelem.text])
                    except Exception as err:
                        self._web_support.req.output = 'Error Printing Barcode:  ' + err
                        self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                        return [self._web_support.req.return_page()]

                    self._web_support.req.output = 'Barcode Sent to Printer!'
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [self._web_support.req.return_page()]
                else:
                    raise self.RendererException('Raw Mode is Not Supported by this Plugin')
            else:
                return
        return