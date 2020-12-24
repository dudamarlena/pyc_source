# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\files\research\databrowse\databrowse\plugins\db_specimen_database\db_specimen_database.py
# Compiled at: 2018-06-29 17:51:46
""" plugins/renderers/db_specimen_database.py - Basic Output for Any Folder """
import databrowse.plugins.db_directory.db_directory as db_directory_module
from lxml import etree
import os
from errno import EEXIST
import databrowse.support.specimen_support as ss
try:
    import databrowse.plugins.db_mercurial_repository.db_mercurial_repository as hgmodule
    hgrepo = hgmodule.db_mercurial_repository
    hgavailable = True
except:
    hgavailable = False

class db_specimen_database(db_directory_module.db_directory):
    """ Image Directory Renderer """
    _default_content_mode = 'title'
    _default_style_mode = 'specimen_list'
    _default_recursion_depth = 1

    def __init__(self, relpath, fullpath, web_support, handler_support, caller, handlers, content_mode=_default_content_mode, style_mode=_default_style_mode, recursion_depth=_default_recursion_depth):
        if caller == 'databrowse':
            self._namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/specimendb'
            self._namespace_local = 'specimendb'
        else:
            self._namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/dir'
            self._namespace_local = 'dir'
            self._disable_load_style = True
        if style_mode not in ('add_specimen', 'add_specimen_group'):
            tmpref = self.getDirectoryList
            self.getDirectoryList = self.getSpecimenDatabaseDirectoryList
            super(db_specimen_database, self).__init__(relpath, fullpath, web_support, handler_support, caller, handlers, content_mode, style_mode)
            self.getDirectoryList = tmpref
            if hgavailable:
                uncommitted = hgrepo.uncommittedlist(fullpath)
                if len(uncommitted) > 0:
                    self._xml.set('uncommitted', str(len(uncommitted)))
        else:
            super(db_directory_module.db_directory, self).__init__(relpath, fullpath, web_support, handler_support, caller, handlers, content_mode, style_mode)

    def getSpecimenDatabaseDirectoryList(self, fullpath, sort=None, order='asc'):
        """ Build a Sorted List of Files with Appropriate Files Removed """
        reallist = os.listdir(fullpath)
        returnlist = [ n for n in reallist if n.endswith('.sdb') or n.endswith('.sdg') ]
        exec 'returnlist.sort(%s%s)' % ('reverse=True' if order == 'desc' else 'reverse=False', ',key=%s' % sort if sort is not None else ',key=str.lower')
        return returnlist

    def getContent(self):
        if self._style_mode not in ('add_specimen', 'add_specimen_group'):
            return super(db_specimen_database, self).getContent()
        else:
            if 'ajax' in self._web_support.req.form and 'save' in self._web_support.req.form:
                if 'file' in self._web_support.req.form and self._style_mode == 'add_specimen':
                    filestring = self._web_support.req.form['file'].value
                    xml = etree.XML(filestring)
                    specimentag = xml.xpath('/specimen:specimen/specimen:specimenid/.', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'})
                    dirtags = xml.xpath('/specimen:specimen/specimen:reldests/specimen:reldest', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'})
                    specimenid = specimentag[0].text
                    fullfilename = os.path.join(self._fullpath, specimenid + '.sdb')
                    if not os.access(os.path.dirname(fullfilename), os.W_OK):
                        self._web_support.req.output = 'Error Saving File:  Save Directory Not Writable ' + os.path.dirname(fullfilename)
                        self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                        return [
                         self._web_support.req.return_page()]
                    if os.path.exists(fullfilename):
                        self._web_support.req.output = 'Error Saving File:  Specimen ' + specimenid + ' already exists'
                        self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                        return [
                         self._web_support.req.return_page()]
                    try:
                        for dirtag in dirtags:
                            newdirname = None
                            if dirtag.get('{http://www.w3.org/1999/xlink}href') is not None:
                                newdirname = dirtag.get('{http://www.w3.org/1999/xlink}href')
                            else:
                                newdirname = dirtag.text
                            if newdirname is not None:
                                os.makedirs(os.path.join(self._fullpath, newdirname))

                    except OSError as err:
                        if err.errno == EEXIST:
                            pass
                        else:
                            self._web_support.req.output = 'Error Creating Files Directory: ' + str(err)
                            self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                            return [self._web_support.req.return_page()]

                    f = open(fullfilename, 'wb')
                    f.write(filestring)
                    f.close
                    self._web_support.req.output = 'File Saved Successfully'
                    self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                    return [self._web_support.req.return_page()]
                elif 'file' in self._web_support.req.form and self._style_mode == 'add_specimen_group':
                    filestring = self._web_support.req.form['file'].value
                    xml = etree.XML(filestring)
                    specimentag = xml.xpath('/specimen:specimengroup/specimen:groupid/.', namespaces={'specimen': 'http://thermal.cnde.iastate.edu/specimen'})
                    specimenid = specimentag[0].text
                    fullfilename = os.path.join(self._fullpath, specimenid + '.sdg')
                    if not os.access(os.path.dirname(fullfilename), os.W_OK):
                        self._web_support.req.output = 'Error Saving File:  Save Directory Not Writable ' + os.path.dirname(fullfilename)
                        self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                        return [
                         self._web_support.req.return_page()]
                    if os.path.exists(fullfilename):
                        self._web_support.req.output = 'Error Saving File:  Specimen Group ' + specimenid + ' already exists'
                        self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                        return [
                         self._web_support.req.return_page()]
                    try:
                        os.makedirs(os.path.join(self._fullpath, specimenid + '_files'))
                    except OSError as err:
                        if err.errno == EEXIST:
                            pass
                        else:
                            self._web_support.req.output = 'Error Creating Files Directory: ' + str(err)
                            self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                            return [self._web_support.req.return_page()]

                    f = open(fullfilename, 'wb')
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
            else:
                if self._style_mode == 'add_specimen':
                    xmlroot = etree.Element('{%s}specimendb' % self._namespace_uri, nsmap=self.nsmap, templatefile=self.getURL('/specimens/src/specimen.xhtml', handler='db_default', content_mode='raw', ContentType='application/xml'))
                elif self._style_mode == 'add_specimen_group':
                    xmlroot = etree.Element('{%s}specimendb' % self._namespace_uri, nsmap=self.nsmap, templatefile=self.getURL('/specimens/src/specimengroup.xhtml', handler='db_default', content_mode='raw', ContentType='application/xml'))
                return xmlroot
            return