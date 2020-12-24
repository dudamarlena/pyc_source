# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.14/lib/python2.7/site-packages/qcloud_cos/cos_client.py
# Compiled at: 2018-03-19 03:53:29
import requests
from cos_cred import CredInfo
from cos_config import CosConfig
from cos_op import FileOp
from cos_op import FolderOp
from cos_request import UploadFileRequest
from cos_request import UploadSliceFileRequest
from cos_request import UploadFileFromBufferRequest
from cos_request import UploadSliceFileFromBufferRequest
from cos_request import UpdateFileRequest
from cos_request import UpdateFolderRequest
from cos_request import DelFileRequest
from cos_request import DelFolderRequest
from cos_request import CreateFolderRequest
from cos_request import StatFolderRequest
from cos_request import StatFileRequest
from cos_request import ListFolderRequest
from cos_request import DownloadFileRequest
from cos_request import DownloadObjectRequest
try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass

class CosClient(object):
    """Cos客户端类"""

    def __init__(self, appid, secret_id, secret_key, region='shanghai'):
        u""" 设置用户的相关信息

        :param appid: appid
        :param secret_id: secret_id
        :param secret_key: secret_key
        """
        self._cred = CredInfo(appid, secret_id, secret_key)
        self._config = CosConfig(region=region)
        self._http_session = requests.session()
        self._file_op = FileOp(self._cred, self._config, self._http_session)
        self._folder_op = FolderOp(self._cred, self._config, self._http_session)

    def set_config(self, config):
        u"""设置config"""
        assert isinstance(config, CosConfig)
        self._config = config
        self._file_op.set_config(config)
        self._folder_op.set_config(config)

    def get_config(self):
        u"""获取config"""
        return self._config

    def set_cred(self, cred):
        u"""设置用户的身份信息

        :param cred:
        :return:
        """
        assert isinstance(cred, CredInfo)
        self._cred = cred
        self._file_op.set_cred(cred)
        self._folder_op.set_cred(cred)

    def get_cred(self):
        u"""获取用户的相关信息

        :return:
        """
        return self._cred

    def upload_file(self, request):
        u""" 上传文件(自动根据文件大小，选择上传策略, 强烈推荐使用),上传策略: 8MB以下适用单文件上传, 8MB(含)适用分片上传

        :param request:
        :return:
        """
        assert isinstance(request, UploadFileRequest)
        return self._file_op.upload_file(request)

    def upload_single_file(self, request):
        u"""单文件上传接口, 适用用小文件8MB以下, 最大不得超过20MB, 否则会返回参数错误

        :param request:
        :return:
        """
        assert isinstance(request, UploadFileRequest)
        return self._file_op.upload_single_file(request)

    def upload_slice_file(self, request):
        u""" 分片上传接口, 适用于大文件8MB及以上

        :param request:
        :return:
        """
        assert isinstance(request, UploadSliceFileRequest)
        return self._file_op.upload_slice_file(request)

    def upload_file_from_buffer(self, request):
        u""" 从内存上传文件(自动根据文件大小，选择上传策略, 强烈推荐使用),上传策略: 8MB以下适用单文件上传, 8MB(含)适用分片上传

        :param request:
        :return:
        """
        assert isinstance(request, UploadFileFromBufferRequest)
        return self._file_op.upload_file_from_buffer(request)

    def upload_single_file_from_buffer(self, request):
        u"""从内存单文件上传接口, 适用用小文件8MB以下, 最大不得超过20MB, 否则会返回参数错误

        :param request:
        :return:
        """
        assert isinstance(request, UploadFileFromBufferRequest)
        return self._file_op.upload_single_file_from_buffer(request)

    def upload_slice_file_from_buffer(self, request):
        u""" 从内存分片上传接口, 适用于大文件8MB及以上

        :param request:
        :return:
        """
        assert isinstance(request, UploadSliceFileFromBufferRequest)
        return self._file_op.upload_slice_file_from_buffer(request)

    def del_file(self, request):
        u""" 删除文件

        :param request:
        :return:
        """
        assert isinstance(request, DelFileRequest)
        return self._file_op.del_file(request)

    def move_file(self, request):
        return self._file_op.move_file(request)

    def stat_file(self, request):
        u"""获取文件属性

        :param request:
        :return:
        """
        assert isinstance(request, StatFileRequest)
        return self._file_op.stat_file(request)

    def update_file(self, request):
        u"""更新文件属性

        :param request:
        :return:
        """
        assert isinstance(request, UpdateFileRequest)
        return self._file_op.update_file(request)

    def download_file(self, request):
        assert isinstance(request, DownloadFileRequest)
        return self._file_op.download_file(request)

    def download_object(self, request):
        assert isinstance(request, DownloadObjectRequest)
        return self._file_op.download_object(request)

    def create_folder(self, request):
        u"""创建目录

        :param request:
        :return:
        """
        assert isinstance(request, CreateFolderRequest)
        return self._folder_op.create_folder(request)

    def del_folder(self, request):
        u"""删除目录

        :param request:
        :return:
        """
        assert isinstance(request, DelFolderRequest)
        return self._folder_op.del_folder(request)

    def stat_folder(self, request):
        u"""获取folder属性请求

        :param request:
        :return:
        """
        assert isinstance(request, StatFolderRequest)
        return self._folder_op.stat_folder(request)

    def update_folder(self, request):
        u"""更新目录属性

        :param request:
        :return:
        """
        assert isinstance(request, UpdateFolderRequest)
        return self._folder_op.update_folder(request)

    def list_folder(self, request):
        u"""获取目录下的文件和目录列表

        :param request:
        :return:
        """
        assert isinstance(request, ListFolderRequest)
        return self._folder_op.list_folder(request)