# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_directory\db_directory.py
# Compiled at: 2020-03-19 13:42:49
""" plugins/renderers/db_directory.py - Basic Output for Any Folder """
import sys, os, os.path
from difflib import get_close_matches
from urllib import pathname2url
from lxml import etree
from lxml import objectify
from databrowse.support.renderer_support import renderer_class

class db_directory(renderer_class):
    """ Default Folder Renderer - Basic Output for Any Folder """
    _xml = None
    _namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/dir'
    _namespace_local = 'dir'
    _default_content_mode = 'title'
    _default_style_mode = 'list'
    _default_recursion_depth = 1

    def specimen_search(self, rootpath, fileexts):
        filelist = []
        dirlist = self.getDirectoryList(rootpath)
        for item in dirlist:
            itemfullpath = os.path.join(rootpath, item).replace('\\', '/')
            if not os.path.isdir(itemfullpath):
                ext = os.path.splitext(itemfullpath)[1]
                if ext in fileexts:
                    filelist.append(itemfullpath)

        return filelist

    def recursiveloop(self, dirname, chxlist):
        chxpath = os.path.abspath(self._web_support.dataroot + '/' + self._web_support.checklistpath + '/' + dirname)
        if os.path.exists(chxpath):
            chxdirlist = self.getDirectoryList(chxpath)
            for item in chxdirlist:
                if item.endswith('.chx'):
                    itemurl = self.getURL(os.path.normpath(self._web_support.checklistpath + '/' + dirname + '/' + item).replace('\\', '/'), handler=None)
                    etree.SubElement(chxlist, '{%s}chxfile' % self._namespace_uri, nsmap=self.nsmap, url=itemurl, name=item)
                if os.path.isdir(os.path.abspath(self._web_support.dataroot + '/' + self._web_support.checklistpath + '/' + dirname + '/' + item)):
                    if len([ x for x in self.getDirectoryList(os.path.abspath(self._web_support.dataroot + '/' + self._web_support.checklistpath + '/' + os.path.normpath(dirname + '/' + item))) if x.endswith('.chx') or os.path.isdir(os.path.abspath(self._web_support.dataroot + '/' + self._web_support.checklistpath + '/' + os.path.normpath(dirname + '/' + item + '/' + x)))
                           ]) > 0:
                        subchxlist = etree.SubElement(chxlist, '{%s}chxdir' % self._namespace_uri, nsmap=self.nsmap, url=self.getURL(os.path.normpath(self._web_support.checklistpath + '/' + dirname + '/' + item), handler=None), name=item)
                        self.recursiveloop(os.path.normpath(dirname + '/' + item), subchxlist)
                    else:
                        continue

        return

    def __init__(self, relpath, fullpath, web_support, handler_support, caller, handlers, content_mode=_default_content_mode, style_mode=_default_style_mode, recursion_depth=_default_recursion_depth):
        """ Load all of the values provided by initialization """
        super(db_directory, self).__init__(relpath, fullpath, web_support, handler_support, caller, handlers, content_mode, style_mode)
        if caller == 'databrowse':
            uphref = self.getURLToParent(self._relpath)
            xmlroot = etree.Element('{%s}dir' % self._namespace_uri, nsmap=self.nsmap, path=self._fullpath, relpath=self._relpath, dataroot=self._web_support.dataroot, uphref=uphref, resurl=self._web_support.resurl, siteurl=self._web_support.siteurl, root='True')
            topmenu = etree.Element('{http://thermal.cnde.iastate.edu/databrowse}navbar', nsmap=self.nsmap, xmlns='http://www.w3.org/1999/xhtml')
            navelem = etree.SubElement(topmenu, '{http://thermal.cnde.iastate.edu/databrowse}navelem', nsmap=self.nsmap)
            title = etree.SubElement(navelem, '{http://www.w3.org/1999/xhtml}a', nsmap=self.nsmap)
            title.text = 'View Options'
            navitems = etree.SubElement(navelem, '{http://thermal.cnde.iastate.edu/databrowse}navdir', alwaysopen='true', nsmap=self.nsmap)
            if 'showhiddenfiles' not in self._web_support.req.form:
                menuitem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem', nsmap=self.nsmap)
                menulink = etree.SubElement(menuitem, '{http://www.w3.org/1999/xhtml}a', href=self.getURL(self._relpath, showhiddenfiles=''), nsmap=self.nsmap)
                menulink.text = 'Show Hidden Files'
            else:
                menuitem = etree.SubElement(navitems, '{http://thermal.cnde.iastate.edu/databrowse}navelem', nsmap=self.nsmap)
                menulink = etree.SubElement(menuitem, '{http://www.w3.org/1999/xhtml}a', href=self.getURL(self._relpath, showhiddenfiles=None), nsmap=self.nsmap)
                menulink.text = 'Hide Hidden Files'
            self._web_support.menu.AddMenu(topmenu)
        else:
            link = self.getURL(self._relpath, handler=None)
            xmlroot = etree.Element('{%s}dir' % self._namespace_uri, nsmap=self.nsmap, name=os.path.basename(self._relpath), path=self._fullpath, relpath=self._relpath, dataroot=self._web_support.dataroot, href=link, resurl=self._web_support.resurl)
        if 'ajax' in self._web_support.req.form:
            xmlroot.set('ajaxreq', 'True')
        if recursion_depth != 0:
            caller = self.__class__.__name__
            dirlist = self.getDirectoryList(self._fullpath)
            for item in dirlist:
                itemrelpath = os.path.join(self._relpath, item).replace('\\', '/')
                itemfullpath = os.path.join(self._fullpath, item).replace('\\', '/')
                handlers, icon = self._handler_support.GetHandlerAndIcon(itemfullpath)
                handler = handlers[(-1)]
                if handler in self._handler_support.directoryplugins:
                    icon = self._handler_support.directoryplugins[handler]
                if handler in self._handler_support.directoryplugins:
                    renderer = self.__class__(itemrelpath, itemfullpath, self._web_support, self._handler_support, caller, handlers, content_mode=content_mode, style_mode=style_mode, recursion_depth=recursion_depth - 1)
                else:
                    exec 'import databrowse.plugins.%s.%s as %s_module' % (handler, handler, handler)
                    exec "renderer = %s_module.%s(itemrelpath, itemfullpath, self._web_support, self._handler_support, caller, handlers, content_mode='%s', style_mode='%s', recursion_depth=%i)" % (
                     handler, handler, content_mode, style_mode, recursion_depth - 1)
                content = renderer.getContent()
                if os.path.islink(itemfullpath):
                    overlay = 'link'
                elif not os.access(itemfullpath, os.W_OK):
                    overlay = 'readonly'
                elif not os.access(itemfullpath, os.R_OK):
                    overlay = 'unreadable'
                else:
                    overlay = 'none'
                if content is not None and content.tag.startswith('{%s}' % self._namespace_uri):
                    content.set('icon', icon)
                    content.set('overlay', overlay)
                    xmlroot.append(content)
                else:
                    xmlchild = etree.SubElement(xmlroot, '{%s}file' % self._namespace_uri, nsmap=self.nsmap, fullpath=itemfullpath, relpath=itemrelpath, basename=os.path.basename(itemfullpath), link=self.getURL(itemrelpath, handler=None), icon=icon, overlay=overlay)
                    if content is not None:
                        xmlchild.append(content)
                        continue

        else:
            xmlroot.set('ajax', 'True')
            xmlroot.set('ajaxurl', self.getURL(self._relpath, recursion_depth=1, nopagestyle=True, content_mode=self._content_mode, style_mode=self._style_mode))
        if self._caller == 'databrowse' and self._web_support.checklistpath is not None:
            chxlist = etree.SubElement(xmlroot, '{%s}chxlist' % self._namespace_uri, nsmap=self.nsmap)
            self.recursiveloop('/', chxlist)
        if self._style_mode in ('fusion', ):
            if self._caller == 'databrowse':
                sens = 0.85
                try:
                    search_terms = self._web_support.req.form['search'].value
                except KeyError:
                    search_terms = None

                if not self.CacheFileExists(tag='searches', extension='txt'):
                    ft = self.getCacheFileHandler('wb', 'searches', 'txt')
                    ft.close()
                ft = self.getCacheFileHandler('rb', 'searches', 'txt')
                prevsearches = ft.read().split(',')
                ft.close()
                if prevsearches == ['']:
                    prevsearches = []
                if search_terms:
                    if search_terms in prevsearches:
                        if prevsearches[(-1)] != search_terms:
                            prevsearches.remove(search_terms)
                            prevsearches.append(search_terms)
                    elif search_terms:
                        prevsearches.append(search_terms)
                if len(prevsearches) > 5:
                    prevsearches = prevsearches[-5:]
                ft = self.getCacheFileHandler('wb', 'searches', 'txt')
                ft.write((',').join(prevsearches))
                ft.close()
                p = etree.XMLParser(huge_tree=True, remove_blank_text=True)
                specimen_file_types = ['.xlg', '.xlp']
                filelist = self.specimen_search(self._fullpath, specimen_file_types)
                if len(filelist) > 0:
                    xmllogs = etree.Element('{%s}logs' % self._namespace_uri, nsmap=self.nsmap)
                    for specfile in filelist:
                        specxml = etree.parse(specfile, parser=p).getroot()
                        self.nsmap.update(dict(set(specxml.xpath('//namespace::*'))))
                        xmllogs.append(specxml)

                    specimens = xmllogs.xpath('//dc:specimen[not(preceding::dc:specimen/text() = text())]/text()', namespaces=self.nsmap)
                    xmlsearch = etree.Element('{%s}search' % self._namespace_uri, resurl=self._web_support.resurl, path=self.getURL(self._relpath, style_mode='fusion'), nsmap=self.nsmap)
                    xmlspecimens = etree.SubElement(xmlsearch, '{%s}specimens' % self._namespace_uri, nsmap=self.nsmap)
                    xmlsearchterm = etree.SubElement(xmlspecimens, '{%s}searchterm' % self._namespace_uri, nsmap=self.nsmap)
                    xmlsearchterm.text = search_terms
                    if prevsearches:
                        xmlprevsearchterms = etree.SubElement(xmlspecimens, '{%s}prevsearches' % self._namespace_uri, nsmap=self.nsmap)
                        for searchterm in list(reversed(prevsearches)):
                            xmlprevsearchterm = etree.SubElement(xmlprevsearchterms, '{%s}prevsearch' % self._namespace_uri, nsmap=self.nsmap)
                            xmlprevsearchterm.text = searchterm

                    for specimen in specimens:
                        xmlspecimen = etree.SubElement(xmlspecimens, '{%s}specimen' % self._namespace_uri, nsmap=self.nsmap)
                        xmlspecimen.text = specimen

                    xmlcontent = etree.SubElement(xmlsearch, '{%s}content' % self._namespace_uri, nsmap=self.nsmap)
                    if search_terms:
                        all_elements = list(xmllogs.iter())[1:]
                        for search_term in search_terms.split(' '):
                            for child in xmlcontent:
                                xmlcontent.remove(child)

                            for element in all_elements:
                                res = []
                                tag = element.tag
                                attributes = element.attrib
                                attrib_keys = attributes.keys()
                                attrib_values = attributes.values()
                                text = element.text
                                if tag:
                                    res += get_close_matches(search_term, [tag.split('}')[1]], cutoff=sens, n=1)
                                if attrib_keys:
                                    res += get_close_matches(search_term, attrib_keys, cutoff=sens, n=1)
                                if attrib_values:
                                    res += get_close_matches(search_term, attrib_values, cutoff=sens, n=1)
                                if text:
                                    res += get_close_matches(search_term, text.split(' '), cutoff=sens, n=1)
                                res = list(set(res))
                                if res:
                                    parent = element
                                    while True:
                                        if parent.text and parent != xmllogs:
                                            parent = parent.getparent()
                                        else:
                                            break

                                    if not xmlcontent.xpath("//dir:_[@title = '%s']" % parent.tag.split('}')[1], namespaces=self.nsmap):
                                        grandparent = etree.SubElement(xmlcontent, '{%s}_' % self._namespace_uri, nsmap=self.nsmap)
                                        grandparent.attrib['title'] = parent.tag.split('}')[1]
                                    grandparent = xmlcontent.xpath("//dir:_[@title = '%s']" % parent.tag.split('}')[1], namespaces=self.nsmap)[0]
                                    if parent not in grandparent:
                                        grandparent.append(parent)

                            all_elements = list(xmlcontent.iter())[1:]

                    xmlroot = xmlsearch
                    fusions = xmlroot.xpath('//dc:fusion', namespaces={'dc': 'http://limatix.org/datacollect'})
                    for fusion in fusions:
                        fusionmodellist = fusion.xpath('dc:greensinversion_3d', namespaces={'dc': 'http://limatix.org/datacollect'})
                        for model in fusionmodellist:
                            try:
                                xlink = model.get('{http://www.w3.org/1999/xlink}href')
                                if xlink:
                                    path = os.path.join(self._fullpath, xlink)
                                    if path.startswith(os.path.normpath(self._web_support.dataroot)) and os.access(path, os.R_OK) and os.path.exists(path):
                                        relpath = path.replace(self._web_support.dataroot, '')
                                        url = self.getURL(relpath, content_mode='raw', model='true').replace('\\', '/')
                                        model.attrib['url'] = url
                            except Exception:
                                pass

                    xlinks = xmlroot.xpath('//*[@xlink:href]', namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
                    for xlink in xlinks:
                        path = os.path.join(self._fullpath, xlink.attrib['{http://www.w3.org/1999/xlink}href'])
                        if path.startswith(os.path.normpath(self._web_support.dataroot)) and os.access(path, os.R_OK) and os.path.exists(path):
                            relpath = path.replace(self._web_support.dataroot, '')
                            url = self.getURL(relpath).replace('\\', '/')
                            xlink.attrib['{http://www.w3.org/1999/xlink}href'] = url

        self._xml = xmlroot
        return

    def getContent(self):
        if self._content_mode == 'detailed' or self._content_mode == 'summary' or self._content_mode == 'title':
            return self._xml
        raise self.RendererException('Invalid Content Mode')

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