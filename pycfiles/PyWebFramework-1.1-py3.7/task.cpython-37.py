# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyWebFramework\core\task.py
# Compiled at: 2020-02-06 07:13:16
# Size of source mod 2**32: 2895 bytes
import pyWebFramework.dll.IeWebFramework as TaskBase_
from .exception import dispatch_task_func

class TaskBase(TaskBase_):
    pages = []

    def __init__(self):
        super(TaskBase, self).__init__()
        self.task_manager = None
        self.page_insts = []

    def OnCreatePage(self, url):
        split = url.split('?')
        pureUrl = url
        if split:
            pureUrl = split[0]
        else:
            page = None
            for cls in self.pages:
                if not cls.url:
                    if cls.matcher:
                        if cls.matcher(url):
                            page = cls()
                            break
                        elif not cls.params:
                            if cls.url == pureUrl:
                                page = cls()
                                break
                        elif self._IsUrlMatch(url, cls.url, cls.params):
                            page = cls()
                            break

            if page:
                page.orig_url = url
                self.page_insts.append(page)
                self.SetCreatedPageInst(page)
            else:
                print('Unknown url: ' + url)

    def OnReleasePage(self, pageInst):
        if pageInst in self.page_insts:
            self.page_insts.remove(pageInst)

    def OnReleaseAllPages(self):
        self.page_insts.clear()

    def _IsUrlMatch(self, srcUrl, dstUrl, params):
        if not srcUrl.startswith(dstUrl):
            return False
        ret = True
        src_params = self._ParseUrlParams(srcUrl)
        for param in params:
            if param not in src_params:
                ret = False
                break

        return ret

    def _ParseUrlParams(self, url):
        ret = []
        q_idx = url.find('?')
        if q_idx != -1:
            params = url[q_idx + 1:]
            ret = params.split('&')
        return ret

    def PyInitTask(self):
        return dispatch_task_func(self, self.InitTask)

    def PyBeginTask(self):
        return dispatch_task_func(self, self.BeginTask)

    def PyOnNewPage(self, page):
        dispatch_task_func(self, self.OnNewPage, page)

    def PyOnRelease(self):
        dispatch_task_func(self, self.OnRelease)

    def InitTask(self):
        return True

    def BeginTask(self):
        return True

    def OnNewPage(self, page):
        pass

    def GetCookieDict(self, cookie_name='', path=''):
        cookies = self.GetCookie(cookie_name, path)
        if not cookies:
            return cookies
        result = {}
        for cookie in cookies.split('; '):
            cookie_sep = cookie.split('=')
            result[cookie_sep[0]] = cookie_sep[1]

        return result