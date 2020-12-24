# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/basic/ctxmgr.py
# Compiled at: 2008-10-01 10:39:53
import thread, threading

class ContextManager:
    __module__ = __name__

    def __init__(self):
        self.__dic = {}
        self.__lock = threading.Lock()

    def getContextForThread(self):
        self.__lock.acquire()
        try:
            return self.__dic[thread.get_ident()]
        finally:
            self.__lock.release()

    def registerContextForThread(self, ctx):
        self.__lock.acquire()
        try:
            self.__dic[thread.get_ident()] = ctx
        finally:
            self.__lock.release()

    def unregisterContextForThread(self):
        self.__lock.acquire()
        try:
            del self.__dic[thread.get_ident()]
        finally:
            self.__lock.release()