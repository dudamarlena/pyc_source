# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\support\handler_support.py
# Compiled at: 2020-02-18 00:16:42
""" support/handler_support.py - Class to encapsulate handler plugin management """
import os, os.path, ConfigParser, pkgutil, databrowse.plugins, re, magic

class handler_support:
    """ Class to encapsulate handler plugin management """
    _handlers = {}
    _icondb = None
    _hiddenfiledb = None
    directoryplugins = {}
    directorystylesheets = []
    hiddenstylesheets = []

    def __init__(self, icondbpath, hiddenfiledbpath, directorypluginpath):
        """ Load up all of the handler plugins and icon database """
        self._handlers = {}
        pkgpath = os.path.dirname(databrowse.plugins.__file__)
        pluginlist = [ name for _, name, _ in pkgutil.iter_modules([pkgpath]) ]
        pluginlist.sort()
        for filename in pluginlist:
            if filename.startswith('db_'):
                modulename = filename
                functions = None
                try:
                    exec 'import databrowse.plugins.%s.handlers' % modulename
                    exec 'functions = dir(databrowse.plugins.%s.handlers)' % modulename
                    for function in functions:
                        if not function.startswith('dbh_'):
                            pass
                        else:
                            exec "self._handlers['%s']=(databrowse.plugins.%s.handlers.%s)" % (function, modulename, function)

                except:
                    pass

                continue

        self._icondb = None
        self._icondb = ConfigParser.ConfigParser()
        self._icondb.read(icondbpath)
        self._hiddenfiledb = None
        self._hiddenfiledb = ConfigParser.ConfigParser()
        self._hiddenfiledb.read(hiddenfiledbpath)
        self.directoryplugins = {}
        self.directorystylesheets = []
        directorypluginconfig = ConfigParser.ConfigParser()
        directorypluginconfig.read(directorypluginpath)
        for item in directorypluginconfig.items('directory_plugins'):
            self.directoryplugins[item[0]] = item[1]

        for item in directorypluginconfig.items('directory_plugin_stylesheets'):
            self.directorystylesheets.append(item[0])

        for item in directorypluginconfig.items('hidden_plugin_stylesheets'):
            self.hiddenstylesheets.append(item[0])

        return

    def GetHandler(self, fullpath):
        """ Return the handler given a full path """
        if os.path.isdir(os.path.realpath(fullpath)) is True:
            contenttype = 'directory'
        else:
            try:
                magicstore = magic.open(magic.MAGIC_MIME)
                magicstore.load()
                contenttype = magicstore.file(os.path.realpath(fullpath))
            except AttributeError:
                contenttype = magic.from_file(os.path.realpath(fullpath), mime=True)

            if contenttype is None:
                contenttype = 'text/plain'
            extension = os.path.splitext(fullpath)[1][1:]
            if contenttype.startswith('application/xml') or contenttype.startswith('text/xml'):
                roottag, nsurl = self.GetXMLRootAndNamespace(fullpath)
            else:
                roottag, nsurl = ('', '')
            handler = []
            for function in sorted(self._handlers):
                temp = self._handlers[function](fullpath, contenttype, extension, roottag, nsurl)
                if temp:
                    handler.append(temp)

        return handler

    def GetHandlerAndIcon(self, fullpath):
        """ Return the handler given a full path """
        if os.path.isdir(os.path.realpath(fullpath)) is True:
            contenttype = 'directory'
        else:
            try:
                magicstore = magic.open(magic.MAGIC_MIME)
                magicstore.load()
                contenttype = magicstore.file(os.path.realpath(fullpath))
            except AttributeError:
                contenttype = magic.from_file(os.path.realpath(fullpath), mime=True)

            if contenttype is None:
                contenttype = 'text/plain'
            extension = os.path.splitext(fullpath)[1][1:]
            if contenttype.startswith('application/xml') or contenttype.startswith('text/xml'):
                roottag, nsurl = self.GetXMLRootAndNamespace(fullpath)
            else:
                roottag, nsurl = ('', '')
            handler = []
            for function in sorted(self._handlers):
                temp = self._handlers[function](fullpath, contenttype, extension, roottag, nsurl)
                if temp:
                    handler.append(temp)

            try:
                iconname = self._icondb.get('Content-Type', contenttype.split(';')[0])
            except ConfigParser.NoOptionError:
                try:
                    iconname = self._icondb.get('Extension', extension)
                except:
                    iconname = 'unknown.png'

        return (handler, iconname)

    def GetIcon(self, contenttype, extension):
        """ Return the icon for a contenttype or extension """
        try:
            iconname = self._icondb.get('Content-Type', contenttype.split(';')[0])
        except ConfigParser.NoOptionError:
            try:
                iconname = self._icondb.get('Extension', extension)
            except:
                iconname = 'unknown.png'

        return iconname

    def GetHiddenFileList(self):
        """ Return the list of files marked to be hidden """
        return (
         self._hiddenfiledb.items('Hidden'), self._hiddenfiledb.items('Shown'))

    def GetXMLRootAndNamespace(self, filename):
        """ Extract the root node name and namespace from an XML file without parsing the entire file """
        f = open(filename)
        size = os.fstat(f.fileno()).st_size
        flag = True
        while flag:
            while True:
                c = f.read(1)
                if c == '<':
                    buf = c
                    c = f.read(1)
                    buf = buf + c
                    if c == '!':
                        while buf[-3:] != '-->':
                            c = f.read(1)
                            buf = buf + c
                            if len(buf) > size:
                                return ('', '')

                    elif c == '?':
                        while buf[-2:] != '?>':
                            c = f.read(1)
                            buf = buf + c
                            if len(buf) > size:
                                return ('', '')

                    else:
                        while buf[(-1)] != '>':
                            c = f.read(1)
                            buf = buf + c
                            if len(buf) > size:
                                return ('', '')

                        flag = False
                        break

        fullroot = buf[1:buf.find(' ')]
        colonidx = fullroot.find(':')
        if colonidx < 0:
            roottag = fullroot
            localns = ''
        else:
            roottag = fullroot[colonidx + 1:]
            localns = fullroot[:colonidx]
        if localns == '':
            t = re.search('xmlns=[\'"](.*?)[\'"]', buf)
            if t is not None:
                nsurl = t.groups()[0]
            else:
                nsurl = ''
        else:
            t = re.findall('xmlns:(.*?)=[\'"](.*?)[\'"]', buf)
            nsurl = [ x[1] for x in t if x[0] == localns ][0]
        return (
         roottag, nsurl)