# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\support\handler_support.py
# Compiled at: 2020-02-17 23:18:22
# Size of source mod 2**32: 12693 bytes
""" support/handler_support.py - Class to encapsulate handler plugin management """
import os, pkgutil, databrowse.plugins, re, magic
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class handler_support:
    __doc__ = ' Class to encapsulate handler plugin management '
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
        pluginlist = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
        pluginlist.sort()
        for filename in pluginlist:
            if filename.startswith('db_'):
                modulename = filename
                functions = None
                try:
                    exec('import databrowse.plugins.%s.handlers' % modulename)
                    functions = eval('dir(databrowse.plugins.%s.handlers)' % modulename)
                    for function in functions:
                        if not function.startswith('dbh_'):
                            continue
                        exec("self._handlers['%s']=(databrowse.plugins.%s.handlers.%s)" % (function, modulename, function))

                except Exception as e:
                    try:
                        print(e)
                    finally:
                        e = None
                        del e

        self._icondb = None
        self._icondb = configparser.ConfigParser()
        self._icondb.read(icondbpath)
        self._hiddenfiledb = None
        self._hiddenfiledb = configparser.ConfigParser()
        self._hiddenfiledb.read(hiddenfiledbpath)
        self.directoryplugins = {}
        self.directorystylesheets = []
        directorypluginconfig = configparser.ConfigParser()
        directorypluginconfig.read(directorypluginpath)
        for item in directorypluginconfig.items('directory_plugins'):
            self.directoryplugins[item[0]] = item[1]

        for item in directorypluginconfig.items('directory_plugin_stylesheets'):
            self.directorystylesheets.append(item[0])

        for item in directorypluginconfig.items('hidden_plugin_stylesheets'):
            self.hiddenstylesheets.append(item[0])

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
                contenttype = magic.from_file((os.path.realpath(fullpath)), mime=True)

            if contenttype is None:
                contenttype = 'text/plain'
            else:
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
                contenttype = magic.from_file((os.path.realpath(fullpath)), mime=True)

            if contenttype is None:
                contenttype = 'text/plain'
            else:
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
            except configparser.NoOptionError:
                try:
                    iconname = self._icondb.get('Extension', extension)
                except:
                    iconname = 'unknown.png'

            return (
             handler, iconname)

    def GetIcon(self, contenttype, extension):
        """ Return the icon for a contenttype or extension """
        try:
            iconname = self._icondb.get('Content-Type', contenttype.split(';')[0])
        except configparser.NoOptionError:
            try:
                iconname = self._icondb.get('Extension', extension)
            except:
                iconname = 'unknown.png'

        return iconname

    def GetHiddenFileList(self):
        """ Return the list of files marked to be hidden """
        return (
         self._hiddenfiledb.items('Hidden'), self._hiddenfiledb.items('Shown'))

    def GetXMLRootAndNamespace--- This code section failed: ---

 L. 208         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'f'

 L. 209         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              fstat
               12  LOAD_FAST                'f'
               14  LOAD_METHOD              fileno
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  LOAD_ATTR                st_size
               22  STORE_FAST               'size'

 L. 210        24  LOAD_CONST               True
               26  STORE_FAST               'flag'

 L. 211        28  SETUP_LOOP          278  'to 278'
               30  LOAD_FAST                'flag'
            32_34  POP_JUMP_IF_FALSE   276  'to 276'

 L. 212        36  SETUP_LOOP          274  'to 274'
             38_0  COME_FROM            54  '54'

 L. 213        38  LOAD_FAST                'f'
               40  LOAD_METHOD              read
               42  LOAD_CONST               1
               44  CALL_METHOD_1         1  '1 positional argument'
               46  STORE_FAST               'c'

 L. 214        48  LOAD_FAST                'c'
               50  LOAD_STR                 '<'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    38  'to 38'

 L. 215        56  LOAD_FAST                'c'
               58  STORE_FAST               'buf'

 L. 217        60  LOAD_FAST                'f'
               62  LOAD_METHOD              read
               64  LOAD_CONST               1
               66  CALL_METHOD_1         1  '1 positional argument'
               68  STORE_FAST               'c'

 L. 218        70  LOAD_FAST                'buf'
               72  LOAD_FAST                'c'
               74  BINARY_ADD       
               76  STORE_FAST               'buf'

 L. 219        78  LOAD_FAST                'c'
               80  LOAD_STR                 '!'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   144  'to 144'

 L. 221        86  SETUP_LOOP          270  'to 270'
             88_0  COME_FROM           132  '132'
               88  LOAD_FAST                'buf'
               90  LOAD_CONST               -3
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  LOAD_STR                 '-->'
              100  COMPARE_OP               !=
              102  POP_JUMP_IF_FALSE   140  'to 140'

 L. 222       104  LOAD_FAST                'f'
              106  LOAD_METHOD              read
              108  LOAD_CONST               1
              110  CALL_METHOD_1         1  '1 positional argument'
              112  STORE_FAST               'c'

 L. 223       114  LOAD_FAST                'buf'
              116  LOAD_FAST                'c'
              118  BINARY_ADD       
              120  STORE_FAST               'buf'

 L. 224       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'buf'
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  LOAD_FAST                'size'
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE    88  'to 88'

 L. 225       134  LOAD_CONST               ('', '')
              136  RETURN_VALUE     

 L. 226       138  JUMP_BACK            88  'to 88'
            140_0  COME_FROM           102  '102'
              140  POP_BLOCK        
              142  JUMP_BACK            38  'to 38'
            144_0  COME_FROM            84  '84'

 L. 227       144  LOAD_FAST                'c'
              146  LOAD_STR                 '?'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   210  'to 210'

 L. 229       152  SETUP_LOOP          270  'to 270'
            154_0  COME_FROM           198  '198'
              154  LOAD_FAST                'buf'
              156  LOAD_CONST               -2
              158  LOAD_CONST               None
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  LOAD_STR                 '?>'
              166  COMPARE_OP               !=
              168  POP_JUMP_IF_FALSE   206  'to 206'

 L. 230       170  LOAD_FAST                'f'
              172  LOAD_METHOD              read
              174  LOAD_CONST               1
              176  CALL_METHOD_1         1  '1 positional argument'
              178  STORE_FAST               'c'

 L. 231       180  LOAD_FAST                'buf'
              182  LOAD_FAST                'c'
              184  BINARY_ADD       
              186  STORE_FAST               'buf'

 L. 232       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'buf'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  LOAD_FAST                'size'
              196  COMPARE_OP               >
              198  POP_JUMP_IF_FALSE   154  'to 154'

 L. 233       200  LOAD_CONST               ('', '')
              202  RETURN_VALUE     

 L. 234       204  JUMP_BACK           154  'to 154'
            206_0  COME_FROM           168  '168'
              206  POP_BLOCK        
              208  JUMP_BACK            38  'to 38'
            210_0  COME_FROM           150  '150'

 L. 238       210  SETUP_LOOP          264  'to 264'
            212_0  COME_FROM           254  '254'
              212  LOAD_FAST                'buf'
              214  LOAD_CONST               -1
              216  BINARY_SUBSCR    
              218  LOAD_STR                 '>'
              220  COMPARE_OP               !=
          222_224  POP_JUMP_IF_FALSE   262  'to 262'

 L. 239       226  LOAD_FAST                'f'
              228  LOAD_METHOD              read
              230  LOAD_CONST               1
              232  CALL_METHOD_1         1  '1 positional argument'
              234  STORE_FAST               'c'

 L. 240       236  LOAD_FAST                'buf'
              238  LOAD_FAST                'c'
              240  BINARY_ADD       
              242  STORE_FAST               'buf'

 L. 241       244  LOAD_GLOBAL              len
              246  LOAD_FAST                'buf'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  LOAD_FAST                'size'
              252  COMPARE_OP               >
              254  POP_JUMP_IF_FALSE   212  'to 212'

 L. 242       256  LOAD_CONST               ('', '')
              258  RETURN_VALUE     

 L. 243       260  JUMP_BACK           212  'to 212'
            262_0  COME_FROM           222  '222'
              262  POP_BLOCK        
            264_0  COME_FROM_LOOP      210  '210'

 L. 244       264  LOAD_CONST               False
              266  STORE_FAST               'flag'

 L. 245       268  BREAK_LOOP       
            270_0  COME_FROM_LOOP      152  '152'
            270_1  COME_FROM_LOOP       86  '86'
              270  JUMP_BACK            38  'to 38'
              272  POP_BLOCK        
            274_0  COME_FROM_LOOP       36  '36'

 L. 246       274  JUMP_BACK            30  'to 30'
            276_0  COME_FROM            32  '32'
              276  POP_BLOCK        
            278_0  COME_FROM_LOOP       28  '28'

 L. 249       278  LOAD_FAST                'buf'
              280  LOAD_CONST               1
              282  LOAD_FAST                'buf'
              284  LOAD_METHOD              find
              286  LOAD_STR                 ' '
              288  CALL_METHOD_1         1  '1 positional argument'
              290  BUILD_SLICE_2         2 
              292  BINARY_SUBSCR    
              294  STORE_FAST               'fullroot'

 L. 250       296  LOAD_FAST                'fullroot'
              298  LOAD_METHOD              find
              300  LOAD_STR                 ':'
              302  CALL_METHOD_1         1  '1 positional argument'
              304  STORE_FAST               'colonidx'

 L. 251       306  LOAD_FAST                'colonidx'
              308  LOAD_CONST               0
              310  COMPARE_OP               <
          312_314  POP_JUMP_IF_FALSE   326  'to 326'

 L. 252       316  LOAD_FAST                'fullroot'
              318  STORE_FAST               'roottag'

 L. 253       320  LOAD_STR                 ''
              322  STORE_DEREF              'localns'
              324  JUMP_FORWARD        354  'to 354'
            326_0  COME_FROM           312  '312'

 L. 255       326  LOAD_FAST                'fullroot'
              328  LOAD_FAST                'colonidx'
              330  LOAD_CONST               1
              332  BINARY_ADD       
              334  LOAD_CONST               None
              336  BUILD_SLICE_2         2 
              338  BINARY_SUBSCR    
              340  STORE_FAST               'roottag'

 L. 256       342  LOAD_FAST                'fullroot'
              344  LOAD_CONST               None
              346  LOAD_FAST                'colonidx'
              348  BUILD_SLICE_2         2 
              350  BINARY_SUBSCR    
              352  STORE_DEREF              'localns'
            354_0  COME_FROM           324  '324'

 L. 257       354  LOAD_DEREF               'localns'
              356  LOAD_STR                 ''
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   406  'to 406'

 L. 258       364  LOAD_GLOBAL              re
              366  LOAD_METHOD              search
              368  LOAD_STR                 'xmlns=[\'"](.*?)[\'"]'
              370  LOAD_FAST                'buf'
              372  CALL_METHOD_2         2  '2 positional arguments'
              374  STORE_FAST               't'

 L. 259       376  LOAD_FAST                't'
              378  LOAD_CONST               None
              380  COMPARE_OP               is-not
          382_384  POP_JUMP_IF_FALSE   400  'to 400'

 L. 260       386  LOAD_FAST                't'
              388  LOAD_METHOD              groups
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  LOAD_CONST               0
              394  BINARY_SUBSCR    
              396  STORE_FAST               'nsurl'
              398  JUMP_FORWARD        404  'to 404'
            400_0  COME_FROM           382  '382'

 L. 262       400  LOAD_STR                 ''
              402  STORE_FAST               'nsurl'
            404_0  COME_FROM           398  '398'
              404  JUMP_FORWARD        440  'to 440'
            406_0  COME_FROM           360  '360'

 L. 264       406  LOAD_GLOBAL              re
              408  LOAD_METHOD              findall
              410  LOAD_STR                 'xmlns:(.*?)=[\'"](.*?)[\'"]'
              412  LOAD_FAST                'buf'
              414  CALL_METHOD_2         2  '2 positional arguments'
              416  STORE_FAST               't'

 L. 265       418  LOAD_CLOSURE             'localns'
              420  BUILD_TUPLE_1         1 
              422  LOAD_LISTCOMP            '<code_object <listcomp>>'
              424  LOAD_STR                 'handler_support.GetXMLRootAndNamespace.<locals>.<listcomp>'
              426  MAKE_FUNCTION_8          'closure'
              428  LOAD_FAST                't'
              430  GET_ITER         
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  LOAD_CONST               0
              436  BINARY_SUBSCR    
              438  STORE_FAST               'nsurl'
            440_0  COME_FROM           404  '404'

 L. 266       440  LOAD_FAST                'roottag'
              442  LOAD_FAST                'nsurl'
              444  BUILD_TUPLE_2         2 
              446  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 270_1