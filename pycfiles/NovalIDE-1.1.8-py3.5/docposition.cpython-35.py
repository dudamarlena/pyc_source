# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/docposition.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 8880 bytes
import os
from noval.util import hiscache
import tkinter as tk, noval.util.utils as utils, noval.python.parser.utils as dirutils, noval.consts as consts, codecs

def jumpto(func):
    """Decorator method to notify clients about jump actions"""

    def WrapJumpto(*args, **kwargs):
        """Wrapper for capturing before/after pos of a jump action"""
        arg = args[0]
        if isinstance(arg, tk.Text):
            text_ctrl = arg
            doc_view = text_ctrl.master.master.GetView()
        else:
            doc_view = arg
            text_ctrl = doc_view.GetCtrl()
        col = text_ctrl.GetCurrentColumn()
        line = text_ctrl.GetCurrentLine()
        func(*args, **kwargs)
        ccol = text_ctrl.GetCurrentColumn()
        cline = text_ctrl.GetCurrentLine()
        fname = doc_view.GetDocument().GetFilename()
        mdata = dict(fname=fname, precol=col, preline=line, lnum=cline, col=ccol)
        UpdatePositionCache(**mdata)

    WrapJumpto.__name__ = func.__name__
    WrapJumpto.__doc__ = func.__doc__
    return WrapJumpto


def jump(func):
    """Decorator method to notify clients about jump actions"""

    def WrapJump(*args, **kwargs):
        """Wrapper for capturing before/after pos of a jump action"""
        arg = args[0]
        if isinstance(arg, tk.Text):
            text_ctrl = arg
            doc_view = text_ctrl.master.master.GetView()
        else:
            doc_view = arg
            text_ctrl = doc_view.GetCtrl()
        func(*args, **kwargs)
        ccol = text_ctrl.GetCurrentColumn()
        cline = text_ctrl.GetCurrentLine()
        fname = doc_view.GetDocument().GetFilename()
        mdata = dict(fname=fname, lnum=cline, col=ccol)
        UpdatePositionCache(**mdata)

    WrapJump.__name__ = func.__name__
    WrapJump.__doc__ = func.__doc__
    return WrapJump


GOTO_PREV_POS = 0
GOTO_NEXT_POS = 1

class DocPositionMgr(object):
    __doc__ = 'Object for managing the saving and setting of a collection of\n    documents positions between sessions. Through the use of an in memory\n    dictionary during run time and on disk dictionary to use when starting\n    and stopping the editor.\n    @note: saves config to ~/.Editra/cache/\n\n    '
    _poscache = hiscache.HistoryCache(100)
    _pos_action = -1

    def __init__(self):
        """Creates the position manager object"""
        super(DocPositionMgr, self).__init__()
        self._init = False
        self._book = None
        self._records = dict()

    def InitPositionCache(self):
        """Initialize and load the on disk document position cache.
        @param book_path: path to on disk cache

        """
        self._init = True
        cache_path = os.path.join(utils.get_user_data_path(), consts.USER_CACHE_DIR)
        if not os.path.exists(cache_path):
            dirutils.MakeDirs(cache_path)
        self._book = os.path.join(cache_path, 'positions')
        if utils.profile_get_int('SAVE_DOCUMENT_POS', True):
            self.LoadBook(self._book)

    @classmethod
    def AddNaviPosition(cls, fname, line, col):
        """Add a new position to the navigation cache
        @param fname: file name
        @param pos: position

        """
        pre = cls._poscache.PeekPrevious()
        next = cls._poscache.PeekNext()
        if (fname, line, col) in (pre, next):
            return
        if cls._pos_action == GOTO_PREV_POS:
            cls._poscache.cpos += 1
            cls._pos_action = -1
        cls._poscache.PutItem((fname, line, col))

    def AddRecord(self, vals):
        """Adds a record to the dictionary from a list of the
        filename vals[0] and the position value vals[1].
        @param vals: (file path, cursor position)

        """
        if len(vals) == 2:
            self._records[vals[0]] = vals[1]
            return True
        else:
            return False

    @classmethod
    def CanNavigateNext(cls):
        """Are there more cached navigation positions?
        @param cls: Class
        @return: bool

        """
        return cls._poscache.HasNext()

    @classmethod
    def CanNavigatePrev(cls):
        """Are there previous cached navigation positions?
        @param cls: Class
        @return: bool

        """
        return cls._poscache.HasPrevious()

    @classmethod
    def FlushNaviCache(cls):
        """Clear the navigation cache"""
        cls._poscache.Clear()

    @classmethod
    def GetNaviCacheSize(cls):
        return cls._poscache.GetSize()

    def GetBook(self):
        """Returns the current book used by this object
        @return: path to book used by this manager

        """
        return self._book

    @classmethod
    def GetNextNaviPos(cls, fname=None):
        """Get the next stored navigation position
        The optional fname parameter will get the next found position for
        the given file.
        @param cls: Class
        @param fname: filename (note currently not supported)
        @return: int or None
        @note: fname is currently not used

        """
        item = cls._poscache.GetNextItem()
        cls._pos_action = GOTO_NEXT_POS
        return item

    @classmethod
    def GetPreviousNaviPos(cls, fname=None):
        """Get the last stored navigation position
        The optional fname parameter will get the last found position for
        the given file.
        @param cls: Class
        @param fname: filename (note currently not supported)
        @return: int or None
        @note: fname is currently not used

        """
        item = cls._poscache.GetPreviousItem()
        cls._pos_action = GOTO_PREV_POS
        return item

    def GetPos(self, name):
        """Get the position record for a given filename
        returns 0 if record is not found.
        @param name: file name
        @return: position value for the given filename

        """
        return self._records.get(name, (None, None))

    def IsInitialized(self):
        """Has the cache been initialized
        @return: bool

        """
        return self._init

    def LoadBook(self, book):
        """Loads a set of records from an on disk dictionary
        the entries are formated as key=value with one entry
        per line in the file.
        @param book: path to saved file
        @return: whether book was loaded or not

        """
        if not os.path.exists(book):
            return False
        reader = codecs.open(book, 'r', 'utf-8')
        if reader != -1:
            lines = list()
            try:
                lines = reader.readlines()
            except:
                reader.close()
                return False
            else:
                reader.close()
            for line in lines:
                line = line.strip()
                vals = line.rsplit('=', 1)
                if not len(vals) != 2:
                    if not os.path.exists(vals[0]):
                        pass
                    else:
                        try:
                            line, col = map(int, vals[1].split(','))
                        except:
                            continue
                        else:
                            self._records[vals[0]] = (
                             line, col)

            return True

    @classmethod
    def PeekNavi(cls, pre=False):
        """Peek into the navigation cache
        @param cls: Class
        @keyword pre: bool

        """
        if pre:
            if cls._poscache.HasPrevious():
                return cls._poscache.PeekPrevious()
        elif cls._poscache.HasNext():
            return cls._poscache.PeekNext()
        return (None, None)

    def WriteBook(self):
        """Writes the collection of files=pos to the config file
        @postcondition: in memory doc data is written out to disk

        """
        if self._book is None:
            return
        writer = codecs.open(self.GetBook(), 'w', 'utf-8')
        if writer != -1:
            try:
                for key, val in self._records.items():
                    try:
                        writer.write('%s=%d,%d\n' % (key, val[0], val[1]))
                    except UnicodeDecodeError:
                        continue

                writer.close()
            except IOError:
                pass


DocMgr = DocPositionMgr()

def UpdatePositionCache(**data):
    if 'precol' in data:
        DocMgr.AddNaviPosition(data['fname'], data['preline'], data['precol'])
    DocMgr.AddNaviPosition(data['fname'], data['lnum'], data['col'])