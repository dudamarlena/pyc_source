# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\support\renderer_support.py
# Compiled at: 2020-02-18 00:16:42
""" support/renderer_support.py - Encapsulation Class for Renderer Plugins """
from lxml import etree
from errno import EEXIST
from stat import *
import sys, os, string, random, copy, fnmatch

class renderer_class(object):
    """ Renderer Plugin Support - Encapsulation Class for Renderer Plugins """
    _relpath = None
    _fullpath = None
    _web_support = None
    _handler_support = None
    _caller = None
    _handlers = None
    _content_mode = None
    _style_mode = None
    _dynamic_style = None
    _default_content_mode = 'title'
    _default_style_mode = 'list'
    _default_recursion_depth = 2
    _disable_load_style = False
    nsmap = {}

    class RendererException(Exception):
        pass

    def __init__(self, relpath, fullpath, web_support, handler_support, caller, handlers, content_mode=None, style_mode=None, recursion_depth=None):
        """ Default Initialization Function """
        self._relpath = relpath
        self._fullpath = fullpath
        self._web_support = web_support
        self._handler_support = handler_support
        self._caller = caller
        self._handlers = handlers
        if content_mode is None:
            self._content_mode = self._default_content_mode
        else:
            self._content_mode = content_mode
        if style_mode is None:
            self._style_mode = self._default_style_mode
        else:
            self._style_mode = style_mode
        if recursion_depth is None:
            self._recursion_depth = self._default_recursion_depth
        else:
            self._recursion_depth = recursion_depth
        self.nsmap = {}
        self.nsmap['db'] = 'http://thermal.cnde.iastate.edu/databrowse'
        if not self._disable_load_style:
            self.loadStyle()
            self.nsmap[self._namespace_local] = self._namespace_uri
        return

    def getContent(self):
        """ Default getContent """
        return

    def getSize(self, fullpath=None):
        """ Get Size of A File - Returns size of current file if none specified """
        if fullpath is None:
            fullpath = self._fullpath
        st = os.stat(fullpath)
        return st[ST_SIZE]

    def getUserFriendlySize(self, fullpath=None, mode='alternative', custom=None):
        return self.ConvertUserFriendlySize(self.getSize(fullpath), mode, custom)

    def ConvertUserFriendlySize(self, bytes, mode='alternative', custom=None, rounding=None):
        """Human-readable file size. """
        if custom is not None:
            formatstrings = custom
        else:
            if mode == 'traditional':
                formatstrings = [(1125899906842624, 'P'),
                 (1099511627776, 'T'),
                 (1073741824, 'G'),
                 (1048576, 'M'),
                 (1024, 'K'),
                 (1, 'B')]
            elif mode == 'alternative':
                formatstrings = [(1125899906842624, ' PB'),
                 (1099511627776, ' TB'),
                 (1073741824, ' GB'),
                 (1048576, ' MB'),
                 (1024, ' KB'),
                 (
                  1, (' byte', ' bytes'))]
            elif mode == 'bitrate':
                formatstrings = [(1125899906842624, ' Pbps'),
                 (1099511627776, ' Tbps'),
                 (1073741824, ' Gbps'),
                 (1048576, ' Mbps'),
                 (1024, ' Kbps'),
                 (1, ' bps')]
            elif mode == 'frequency':
                formatstrings = [(1000000000000000, ' PHz'),
                 (1000000000000, ' THz'),
                 (1000000000, ' GHz'),
                 (1000000, ' MHz'),
                 (1000, ' KHz'),
                 (1, ' Hz')]
            elif mode == 'time':
                formatstrings = [(256, (' week', ' weeks')),
                 (
                  343, (' day', ' days')),
                 (
                  576, (' hr', ' hrs')),
                 (60, ' min'),
                 (1, ' sec')]
            elif mode == 'verbose':
                formatstrings = [(1125899906842624, (' petabyte', ' petabytes')),
                 (
                  1099511627776, (' terabyte', ' terabytes')),
                 (
                  1073741824, (' gigabyte', ' gigabytes')),
                 (
                  1048576, (' megabyte', ' megabytes')),
                 (
                  1024, (' kilobyte', ' kilobytes')),
                 (
                  1, (' byte', ' bytes'))]
            elif mode == 'iec':
                formatstrings = [(1125899906842624, 'Pi'),
                 (1099511627776, 'Ti'),
                 (1073741824, 'Gi'),
                 (1048576, 'Mi'),
                 (1024, 'Ki'),
                 (1, '')]
            elif mode == 'si':
                formatstrings = [(1000000000000000, 'P'),
                 (1000000000000, 'T'),
                 (1000000000, 'G'),
                 (1000000, 'M'),
                 (1000, 'K'),
                 (1, 'B')]
            else:
                formatstrings = [(1125899906842624, ' PB'),
                 (1099511627776, ' TB'),
                 (1073741824, ' GB'),
                 (1048576, ' MB'),
                 (1024, ' KB'),
                 (
                  1, (' byte', ' bytes'))]
            for factor, suffix in formatstrings:
                if bytes >= factor:
                    break

        amount = float(bytes / factor)
        if isinstance(suffix, tuple):
            singular, multiple = suffix
            if amount == 1:
                suffix = singular
            else:
                suffix = multiple
        if rounding is not None:
            amount = round(amount, rounding)
        return str(amount) + suffix

    def ConvertUserFriendlyPermissions(self, p):
        ts = {49152: 'ssocket', 
           40960: 'llink', 
           32768: '-file', 
           24576: 'bblock', 
           16384: 'ddir', 
           8192: 'cchar', 
           4096: 'pfifo'}
        t = p & 61440
        permstr = ts[t][0] if t in ts else 'u'
        permstr += 'r' if p & 256 else '-'
        permstr += 'w' if p & 128 else '-'
        permstr += 's' if p & 2048 else 'x' if p & 64 else 'S' if p & 2048 else '-'
        permstr += 'r' if p & 32 else '-'
        permstr += 'w' if p & 16 else '-'
        permstr += 's' if p & 1024 else 'x' if p & 8 else 'S' if p & 1024 else '-'
        permstr += 'r' if p & 4 else '-'
        permstr += 'w' if p & 2 else '-'
        permstr += 's' if p & 512 else 'x' if p & 1 else 'S' if p & 512 else '-'
        return permstr

    def isRaw(self):
        if self._content_mode == 'raw':
            return True
        else:
            return False

    def isGit(self):
        if self._web_support.req.agent.startswith('git'):
            return True
        else:
            return False

    def getStyleMode(self):
        return self._style_mode

    def getContentMode(self):
        return self._content_mode

    def getURL(self, relpath, **kwargs):
        """ Return Full URL to a Relative Path """
        if self._handlers[(-1)] != self.__class__.__name__ and 'handler' not in kwargs:
            kwargs['handler'] = self.__class__.__name__
        else:
            if 'handler' in kwargs and kwargs['handler'] is None:
                del kwargs['handler']
            if 'showhiddenfiles' in self._web_support.req.form and 'showhiddenfiles' not in kwargs:
                kwargs['showhiddenfiles'] = ''
            elif 'showhiddenfiles' in kwargs and kwargs['showhiddenfiles'] is None:
                del kwargs['showhiddenfiles']
            if self._web_support.seo_urls is True:
                url = self._web_support.siteurl + relpath
                if len(kwargs) > 0:
                    url = url + '?'
                    z = 1
                for i in kwargs:
                    if z == 1:
                        url = url + i + '=' + str(kwargs[i])
                        z = 2
                    else:
                        url = url + '&' + i + '=' + str(kwargs[i])

            else:
                url = self._web_support.siteurl + '/?path=' + relpath
                for i in kwargs:
                    url = url + '&' + i + '=' + str(kwargs[i])

        return url

    def getURLToParent(self, relpath, **kwargs):
        if relpath == '/':
            return self.getURL(relpath, **kwargs)
        else:
            relpath = os.path.normpath(relpath + '/../')
            return self.getURL(relpath, **kwargs)

    def getDirectoryList(self, fullpath, sort=None, order='asc'):
        """ Build a Sorted List of Files with Appropriate Files Removed """
        hiddenlist, shownlist = self._handler_support.GetHiddenFileList()
        reallist = os.listdir(fullpath)
        if 'showhiddenfiles' in self._web_support.req.form:
            returnlist = reallist
        else:
            removelist = copy.copy(reallist)
            for item in hiddenlist:
                removelist = [ n for n in removelist if not fnmatch.fnmatch(n, item[1]) ]

            addlist = []
            for item in shownlist:
                addlist = [ n for n in reallist if fnmatch.fnmatch(n, item[1]) ]

            returnlist = list(set(removelist + addlist))
        exec 'returnlist.sort(%s%s)' % ('reverse=True' if order == 'desc' else 'reverse=False', ',key=%s' % sort if sort is not None else ',key=str.lower')
        returndirlist = [ f for f in returnlist if os.path.isdir(os.path.join(fullpath, f)) ]
        returnfilelist = [ f for f in returnlist if os.path.isfile(os.path.join(fullpath, f)) ]
        returnlist = returndirlist
        returnlist.extend(returnfilelist)
        return returnlist

    class CacheFileHandler(file):
        """ Overrride File Close Class to Reassign Timestamp """
        timestamp = None

        def __init__(self, filename, mode='r', timestamp=None):
            self.timestamp = timestamp
            super(renderer_class.CacheFileHandler, self).__init__(filename, mode)

        def close(self):
            super(renderer_class.CacheFileHandler, self).close()
            if self.mode not in ('r', 'rb') and self.timestamp is not None:
                st = os.stat(self.name)
                atime = st[ST_ATIME]
                os.utime(self.name, (atime, self.timestamp))
            return

    def getCacheFileHandler(self, mode='r', tag=None, extension=None):
        """ Return File Handler For Cache File """
        filename = self.getCacheFileName(tag, extension)
        st = os.stat(self._fullpath)
        timestamp = st[ST_MTIME]
        if mode not in ('r', 'rb'):
            self.PrepareCacheDir()
            if not os.access(filename, os.W_OK) and os.path.exists(filename):
                raise self.RendererException('Unable to Open Cache File for Writing: ' + filename)
        elif not os.access(filename, os.R_OK):
            raise self.RendererException('Unable to Open Cache File for Reading: ' + filename)
        return self.CacheFileHandler(filename, mode, timestamp)

    def PrepareCacheDir(self):
        cachedirname = self.getCacheDirName()
        if not os.path.exists(cachedirname):
            try:
                os.makedirs(cachedirname)
            except OSError as err:
                if err.errno == EEXIST:
                    pass
                else:
                    raise

    def CacheFileExists(self, tag=None, extension=None):
        """ Return Boolean after Verifying the Existance of a Cache File """
        if 'ignorecache' in self._web_support.req.form:
            return False
        filename = self.getCacheFileName(tag, extension)
        if os.access(filename, os.R_OK) and os.path.exists(filename):
            basestat = os.stat(self._fullpath)
            cachestat = os.stat(filename)
            if basestat[ST_MTIME] > cachestat[ST_MTIME]:
                return False
            return True
        else:
            return False

    def getCacheDirName(self):
        return os.path.abspath(os.path.dirname(self._fullpath) + '/.databrowse/cache/' + self.__class__.__name__ + '/')

    def getCacheFileName(self, tag=None, extension=None):
        """ Get the Name of a Cache File Given a Tag and Extension """
        basefilename = os.path.splitext(os.path.basename(self._fullpath))
        basedirname = self.getCacheDirName()
        filename = basefilename[0]
        if tag is not None:
            filename = filename + '_' + tag
        if extension is not None:
            filename = filename + '.' + extension
        else:
            filename = filename + basefilename[1]
        return os.path.join(basedirname, filename)

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

        self._web_support.menu.AddMenu(newmenu)

    def loadStyle(self):
        """ Safe Function Wrapper To Prevent Errors When Stylesheet Doesn't Exist """
        try:
            self.loadStyleFunction()
        except self.RendererException:
            if self._caller in self._handler_support.directoryplugins:
                pass
            elif self._style_mode == self._default_style_mode:
                raise
            else:
                self._style_mode = self._default_style_mode
                self.loadStyleFunction()

    def loadStyleFunction(self):
        """ Look In Standard Places For the Appropriate Static Stylesheet """
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