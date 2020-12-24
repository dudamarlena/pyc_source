# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/downutils.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 4870 bytes
from noval import GetApp, _
from tkinter import messagebox
import os, noval.ui_base as ui_base
from dummy.userdb import UserDataDb
import requests, noval.util.appdirs as appdirs, noval.python.parser.utils as dirutils, threading

class DownloadProgressDialog(ui_base.GenericProgressDialog):
    __doc__ = '\n        下载进度显示对话框\n    '

    def __init__(self, parent, file_sie, file_name):
        welcome_msg = _('Please wait a minute for Downloading')
        ui_base.GenericProgressDialog.__init__(self, parent, _('Downloading %s') % file_name, info=welcome_msg, maximum=file_sie)


class FileDownloader(object):
    __doc__ = '\n        下载文件公用类\n    '

    def __init__(self, file_length, file_name, req, call_back=None):
        self._file_size = file_length
        self._file_name = file_name
        self._req = req
        self._call_back = call_back
        self._is_dowloading = False
        self.progress_dlg = None

    def StartDownload(self):

        def DownloadCallBack():
            self.DestoryDialog()
            if self._call_back is not None and not self.IsCanceled():
                GetApp().MainFrame.after(300, self._call_back, download_file_path)

        download_tmp_path = os.path.join(appdirs.get_user_data_path(), 'download')
        if not os.path.exists(download_tmp_path):
            dirutils.MakeDirs(download_tmp_path)
        self._is_dowloading = True
        GetApp().MainFrame.after(1000, self.ShowDownloadProgressDialog)
        download_file_path = os.path.join(download_tmp_path, self._file_name)
        try:
            self.DownloadFile(download_file_path, callback=DownloadCallBack, err_callback=self.DestoryDialog)
        except:
            return

    def DestoryDialog(self):
        """
            下载完成后关闭进度条
        """
        if self.progress_dlg is None:
            return
        self.progress_dlg.keep_going = False
        self.progress_dlg.destroy()

    def IsCanceled(self):
        if self.progress_dlg is None:
            return False
        return self.progress_dlg.is_cancel

    def ShowDownloadProgressDialog(self):
        if self._is_dowloading:
            download_progress_dlg = DownloadProgressDialog(GetApp().GetTopWindow(), int(self._file_size), self._file_name)
            self.progress_dlg = download_progress_dlg
            download_progress_dlg.ShowModal()

    def DownloadFile(self, download_file_path, callback, err_callback=None):
        t = threading.Thread(target=self.DownloadFileContent, args=(download_file_path, self._req, callback, err_callback))
        t.start()

    def DownloadFileContent(self, download_file_path, req, callback, err_callback=None):
        f = open(download_file_path, 'wb')
        try:
            ammount = 0
            for chunk in req.iter_content(chunk_size=512):
                if chunk:
                    if self.IsCanceled():
                        break
                    f.write(chunk)
                    ammount += len(chunk)
                    if self.progress_dlg is not None:
                        self.progress_dlg.SetValue(ammount)

        except Exception as e:
            messagebox.showerror('', _('Download fail:%s') % e)
            if err_callback:
                err_callback()
            f.close()
            return

        f.close()
        self._is_dowloading = False
        callback()


def download_file(download_url, call_back=None, **payload):
    """
        下载文件公用函数
        download_url:下载地址
        call_back:下载完成后回调函数
        payload:url参数
    """
    user_id = UserDataDb().GetUserId()
    if user_id:
        payload.update({'member_id': user_id})
    req = requests.get(download_url, params=payload, stream=True)
    if 'Content-Length' not in req.headers:
        data = req.json()
        if data['code'] != 0:
            messagebox.showerror(GetApp().GetAppName(), data['message'])
    else:
        file_length = req.headers['Content-Length']
        content_disposition = req.headers['Content-Disposition']
        file_name = content_disposition[content_disposition.find(';') + 1:].replace('filename=', '').replace('"', '')
        file_downloader = FileDownloader(file_length, file_name, req, call_back)
        file_downloader.StartDownload()