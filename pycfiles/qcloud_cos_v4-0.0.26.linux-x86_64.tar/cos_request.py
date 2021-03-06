# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.14/lib/python2.7/site-packages/qcloud_cos/cos_request.py
# Compiled at: 2018-03-19 03:53:29
"""the request type in tencent qcloud cos"""
from cos_params_check import ParamCheck
import collections

class BaseRequest(object):
    """BaseRequest基本类型的请求"""

    def __init__(self, bucket_name, cos_path):
        u""" 类初始化

        :param bucket_name: bucket的名称
        :param cos_path: cos的绝对路径, 即从bucket下的根/开始
        """
        self._bucket_name = bucket_name.strip()
        self._cos_path = cos_path.strip()
        self._param_check = ParamCheck()

    def set_bucket_name(self, bucket_name=''):
        u"""设置bucket_name

        :param bucket_name:
        :return:
        """
        self._bucket_name = bucket_name.strip()

    def get_bucket_name(self):
        u"""获取bucket_name

        :return:
        """
        return self._bucket_name

    def set_cos_path(self, cos_path=''):
        u"""设置cos_path

        :param cos_path:
        :return:
        """
        self._cos_path = cos_path.strip()

    def get_cos_path(self):
        u"""获取cos_path

        :return:
        """
        return self._cos_path

    def get_err_tips(self):
        u"""获取错误信息

        :return:
        """
        return self._param_check.get_err_tips()

    def check_params_valid(self):
        u"""检查参数是否合法

        :return:
        """
        if not self._param_check.check_param_unicode('bucket', self._bucket_name):
            return False
        return self._param_check.check_param_unicode('cos_path', self._cos_path)


class CreateFolderRequest(BaseRequest):
    """CreateFolderRequest  创建目录类型的请求"""

    def __init__(self, bucket_name, cos_path, biz_attr=''):
        u"""

        :param bucket_name: bucket的名称
        :param cos_path: cos的绝对路径, 从bucket根/开始
        :param biz_attr: 目录的属性
        """
        super(CreateFolderRequest, self).__init__(bucket_name, cos_path)
        self._biz_attr = biz_attr

    def set_biz_attr(self, biz_attr):
        u"""设置biz_attr

        :param biz_attr:
        :return:
        """
        self._biz_attr = biz_attr

    def get_biz_attr(self):
        u""" 获取biz_attr

        :return:
        """
        return self._biz_attr

    def check_params_valid(self):
        u"""检查参数是否合法

        :return:
        """
        if not super(CreateFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_param_unicode('biz_attr', self._biz_attr):
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=False):
            return False
        return self._param_check.check_not_cos_root(self._cos_path)


class UploadFileRequest(BaseRequest):
    """
    UploadFileRequest  单文件上传请求
    """

    def __init__(self, bucket_name, cos_path, local_path, biz_attr='', insert_only=1, verify_sha1=False):
        u"""

        :param bucket_name:  bucket的名称
        :param cos_path: cos的绝对路径(目的路径), 从bucket根/开始
        :param local_path: 上传的本地文件路径(源路径)
        :param biz_attr: 文件的属性
        :param insert_only: 是否覆盖写, 0覆盖, 1不覆盖,返回错误
        :param verify_sha1: 分片上传是否带sha1上传,默认为False
        """
        super(UploadFileRequest, self).__init__(bucket_name, cos_path)
        self._local_path = local_path.strip()
        self._biz_attr = biz_attr
        self._insert_only = insert_only
        self._verify_sha1 = verify_sha1

    def set_local_path(self, local_path):
        u"""设置local_path

        :param local_path:
        :return:
        """
        self._local_path = local_path.strip()

    def get_local_path(self):
        u"""获取local_path

        :return:
        """
        return self._local_path

    def set_biz_attr(self, biz_attr):
        u"""设置biz_attr

        :param biz_attr:
        :return:
        """
        self._biz_attr = biz_attr

    def get_biz_attr(self):
        u"""获取biz_attr

        :return:
        """
        return self._biz_attr

    def set_insert_only(self, insert_only):
        u"""设置insert_only，0表示如果文件存在, 则覆盖

        :param insert_only:
        :return:
        """
        self._insert_only = insert_only

    def get_insert_only(self):
        u"""获取insert_only

        :return:
        """
        return self._insert_only

    def set_verify_sha1(self, verify_sha1):
        u"""设置enable_sha1

        :param verify_sha1:
        :return:
        """
        self._verify_sha1 = verify_sha1

    def get_verify_sha1(self):
        u"""获取verify_sha1

        :return:
        """
        return self._verify_sha1

    def check_params_valid(self):
        u"""检查参数是否有效

        :return:
        """
        if not super(UploadFileRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=True):
            return False
        if not self._param_check.check_param_unicode('biz_attr', self._biz_attr):
            return False
        if not self._param_check.check_param_unicode('local_path', self._local_path):
            return False
        if not self._param_check.check_local_file_valid(self._local_path):
            return False
        if not self._param_check.check_param_int('insert_only', self._insert_only):
            return False
        return self._param_check.check_insert_only(self._insert_only)


class UploadSliceFileRequest(UploadFileRequest):
    """
    UploadSliceFileRequest  分片文件上传请求
    """

    def __init__(self, bucket_name, cos_path, local_path, slice_size=1048576, biz_attr='', enable_sha1=False, max_con=1, insert_only=1):
        u"""

        :param bucket_name: bucket的名称
        :param cos_path: cos的绝对路径(目的路径), 从bucket根/开始
        :param local_path: 上传的本地文件路径(源路径)
        :param slice_size: 文件的属性
        :param biz_attr: 分片大小(字节, 默认1MB)
        :param enable_sha1: 是否启用sha1校验
        :param insert_only: 是否覆盖,默认为1不覆盖
        """
        super(UploadSliceFileRequest, self).__init__(bucket_name, cos_path, local_path, biz_attr, insert_only)
        self._slice_size = slice_size
        self._enable_sha1 = enable_sha1
        self._max_con = max_con

    @property
    def enable_sha1(self):
        return self._enable_sha1

    @enable_sha1.setter
    def enable_sha1(self, val):
        if val in (True, False):
            self._enable_sha1 = val
        else:
            raise ValueError('enable_sha1 should be True/False')

    def set_slice_size(self, slice_size):
        u"""设置分片大小

        :param slice_size:
        :return:
        """
        self._slice_size = slice_size

    def get_slice_size(self):
        u"""获取分片大小

        :return:
        """
        return self._slice_size

    def check_params_valid(self):
        u"""检查参数是否有效

        :return:
        """
        if not super(UploadSliceFileRequest, self).check_params_valid():
            return False
        if self._enable_sha1 and self._slice_size != 1048576:
            self._param_check._err_tips = 'slice_size is invalid, slice must be 1MB with enable_sha1'
            return False
        return self._param_check.check_slice_size(self._slice_size)


class UploadFileFromBufferRequest(BaseRequest):
    """
    UploadFileFromBufferRequest  内存单文件上传请求
    """

    def __init__(self, bucket_name, cos_path, data, biz_attr='', insert_only=1, verify_sha1=False):
        u"""

        :param bucket_name:  bucket的名称
        :param cos_path: cos的绝对路径(目的路径), 从bucket根/开始
        :param data: 文件内容
        :param biz_attr: 文件的属性
        :param insert_only: 是否覆盖写, 0覆盖, 1不覆盖,返回错误
        """
        super(UploadFileFromBufferRequest, self).__init__(bucket_name, cos_path)
        self._data = data
        self._biz_attr = biz_attr
        self._insert_only = insert_only
        self._verify_sha1 = verify_sha1

    def set_data(self, data):
        u"""设置local_path

        :param local_path:
        :return:
        """
        self._data = data

    def get_data(self):
        u"""获取local_path

        :return:
        """
        return self._data

    def set_biz_attr(self, biz_attr):
        u"""设置biz_attr

        :param biz_attr:
        :return:
        """
        self._biz_attr = biz_attr

    def get_biz_attr(self):
        u"""获取biz_attr

        :return:
        """
        return self._biz_attr

    def set_insert_only(self, insert_only):
        u"""设置insert_only，0表示如果文件存在, 则覆盖

        :param insert_only:
        :return:
        """
        self._insert_only = insert_only

    def get_insert_only(self):
        u"""获取insert_only

        :return:
        """
        return self._insert_only

    def set_verify_sha1(self, verify_sha1):
        u"""设置enable_sha1

        :param verify_sha1:
        :return:
        """
        self._verify_sha1 = verify_sha1

    def get_verify_sha1(self):
        u"""获取verify_sha1

        :return:
        """
        return self._verify_sha1

    def check_params_valid(self):
        u"""检查参数是否有效

        :return:
        """
        if not super(UploadFileFromBufferRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=True):
            return False
        if not self._param_check.check_param_unicode('biz_attr', self._biz_attr):
            return False
        if not self._param_check.check_param_int('insert_only', self._insert_only):
            return False
        return self._param_check.check_insert_only(self._insert_only)


class UploadSliceFileFromBufferRequest(UploadFileFromBufferRequest):
    """
    UploadSliceFileFromBufferRequest  内存分片文件上传请求
    """

    def __init__(self, bucket_name, cos_path, data, slice_size=1048576, biz_attr='', enable_sha1=False, max_con=1, insert_only=1):
        u"""

        :param bucket_name: bucket的名称
        :param cos_path: cos的绝对路径(目的路径), 从bucket根/开始
        :param data: 文件内容
        :param slice_size: 文件的属性
        :param biz_attr: 分片大小(字节, 默认1MB)
        :param enable_sha1: 是否启用sha1校验
        :param insert_only: 是否覆盖,默认为1不覆盖
        """
        super(UploadSliceFileFromBufferRequest, self).__init__(bucket_name, cos_path, data, biz_attr, insert_only)
        self._slice_size = slice_size
        self._enable_sha1 = enable_sha1
        self._max_con = max_con

    @property
    def enable_sha1(self):
        return self._enable_sha1

    @enable_sha1.setter
    def enable_sha1(self, val):
        if val in (True, False):
            self._enable_sha1 = val
        else:
            raise ValueError('enable_sha1 should be True/False')

    def set_slice_size(self, slice_size):
        u"""设置分片大小

        :param slice_size:
        :return:
        """
        self._slice_size = slice_size

    def get_slice_size(self):
        u"""获取分片大小

        :return:
        """
        return self._slice_size

    def check_params_valid(self):
        u"""检查参数是否有效

        :return:
        """
        if not super(UploadSliceFileFromBufferRequest, self).check_params_valid():
            return False
        if self._enable_sha1 and self._slice_size != 1048576:
            self._param_check._err_tips = 'slice_size is invalid, slice must be 1MB with enable_sha1'
            return False
        return self._param_check.check_slice_size(self._slice_size)


class UpdateFolderRequest(BaseRequest):
    """UpdateFolderRequest 更新目录请求"""

    def __init__(self, bucket_name, cos_path, biz_attr=''):
        """

        :param bucket_name: bucket name
        :param cos_path: the path on cos
        :param biz_attr: biz attributes
        """
        super(UpdateFolderRequest, self).__init__(bucket_name, cos_path)
        self._biz_attr = biz_attr

    def set_biz_attr(self, biz_attr):
        u"""设置biz_attr

        :param biz_attr:
        :return:
        """
        self._biz_attr = biz_attr

    def get_biz_attr(self):
        u"""获取biz_attr

        :return:
        """
        return self._biz_attr

    def check_params_valid(self):
        u"""检查参数是否有效

        :return:
        """
        if not super(UpdateFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=False):
            return False
        if not self._param_check.check_not_cos_root(self._cos_path):
            return False
        return self._param_check.check_param_unicode('biz_attr', self._biz_attr)


class UpdateFileRequest(BaseRequest):
    """UpdateFileRequest 更新文件请求 """

    def __init__(self, bucket_name, cos_path):
        u""" 初始化类

            biz_attr:     要更新的文件的属性
            authority:              文件权限:
                             eInvalid(继承bucket),
                             eWRPrivate(私有读写),
                             eWPrivateRPublic(私有写, 公有读)
            customer_header:        用户自定义的HTTP请求头,包括以下成员
            cache_control:          文件的缓存机制,参见HTTP的Cache-Control
            content_type:           文件的MIME信息,参见HTTP的Content-Type
            content_disposition:    MIME协议的扩展,参见HTTP的Content-Disposition
            content_language:       文件的语言, 参见HTTP的Content-Language
            content_encoding:       body的编码, 参见HTTP的Content-Encoding
            _x_cos_meta_dict:       用户自定义的属性, key是以x-cos-meta-开头,value为属性值

        :param bucket_name: bucket的名称
        :param cos_path: cos的绝对路径, 从bucket根/开始
        """
        super(UpdateFileRequest, self).__init__(bucket_name, cos_path)
        self._biz_attr = None
        self._custom_headers = {}
        self._authority = None
        self._cache_control = None
        self._content_type = None
        self._content_disposition = None
        self._content_language = None
        self._content_encoding = None
        self._x_cos_meta_dict = dict()
        return

    def set_biz_attr(self, biz_attr):
        u"""设置biz_attr"""
        self._biz_attr = biz_attr

    def get_biz_attr(self):
        u"""获取biz_attr"""
        return self._biz_attr

    def set_authority(self, authority):
        u"""设置authority,

        合法取值:eInvalid(继承bucket),eWRPrivate(私有读写),eWPrivateRPublic(私有写, 公有读)
        :param authority:
        :return:
        """
        self._authority = authority

    def get_authority(self):
        u"""获取authority"""
        return self._authority

    def set_cache_control(self, cache_control):
        u"""设置缓存机制Cache-Control"""
        self._cache_control = cache_control
        self._custom_headers['Cache-Control'] = cache_control

    def set_content_type(self, content_type):
        u"""设置Content-Type"""
        self._content_type = content_type
        self._custom_headers['Content-Type'] = content_type

    def set_content_disposition(self, content_disposition):
        u"""设置Content-Disposition"""
        self._content_disposition = content_disposition
        self._custom_headers['Content-Disposition'] = content_disposition

    def set_content_language(self, content_language):
        u"""设置Content-Language"""
        self._content_language = content_language
        self._custom_headers['Content-Language'] = content_language

    def set_content_encoding(self, content_encoding):
        u"""设置Content-Encoding"""
        self._content_encoding = content_encoding
        self._custom_headers['Content-Encoding'] = content_encoding

    def set_x_cos_meta(self, key, value):
        u"""设置自定义的x-cos-meta

        key以x-cos-meta-开头,例如自定义key为u'x-cos-meta-len', value为u'1024'
        :param key:
        :param value:
        :return:
        """
        self._x_cos_meta_dict[key] = value
        self._custom_headers[key] = value

    def _convert_dict(self, data):
        """convert a dict's keys & values from `unicode` to `str`

        :param data:
        :return:
        """
        if isinstance(data, basestring):
            return str(data)
        else:
            if isinstance(data, collections.Mapping):
                return dict(map(self._convert_dict, data.iteritems()))
            if isinstance(data, collections.Iterable):
                return type(data)(map(self._convert_dict, data))
            return data

    def get_custom_headers(self):
        u""" 获取自定义的HTTP头"""
        return self._convert_dict(self._custom_headers)

    def check_params_valid(self):
        u""" 检查参数是否合法"""
        if not super(UpdateFileRequest, self).check_params_valid():
            return False
        else:
            if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=True):
                return False
            if self._biz_attr is not None:
                if not self._param_check.check_param_unicode('biz_attr', self._biz_attr):
                    return False
            if self._authority is not None:
                if not self._param_check.check_param_unicode('authority', self._authority):
                    return False
            if self._authority is not None:
                if not self._param_check.check_file_authority(self._authority):
                    return False
            if self._cache_control is not None:
                if not self._param_check.check_param_unicode('cache_control', self._cache_control):
                    return False
            if self._content_type is not None:
                if not self._param_check.check_param_unicode('content_type', self._content_type):
                    return False
            if self._content_disposition is not None:
                if not self._param_check.check_param_unicode('content_disposition', self._content_disposition):
                    return False
            if self._content_language is not None:
                if not self._param_check.check_param_unicode('content_language', self._content_language):
                    return False
            if self._content_encoding is not None:
                if not self._param_check.check_param_unicode('content_encoding', self._content_encoding):
                    return False
            return self._param_check.check_x_cos_meta_dict(self._x_cos_meta_dict)


class StatFileRequest(BaseRequest):
    """StatRequest 获取文件属性请求"""

    def __init__(self, bucket_name, cos_path):
        u"""
        :param bucket_name: bucket的名称
        :param cos_path: cos的文件路径, 从bucket根/开始, 不以/结束
        """
        super(StatFileRequest, self).__init__(bucket_name, cos_path)

    def check_params_valid(self):
        u"""检查参数是否合法"""
        if not super(StatFileRequest, self).check_params_valid():
            return False
        return self._param_check.check_cos_path_valid(self._cos_path, is_file_path=True)


class StatFolderRequest(BaseRequest):
    """StatRequest 获取目录属性请求 """

    def __init__(self, bucket_name, cos_path):
        u"""

        :param bucket_name: bucket的名称
        :param cos_path: cos的目录路径, 从bucket根/开始, 以/结束
        """
        super(StatFolderRequest, self).__init__(bucket_name, cos_path)

    def check_params_valid(self):
        u"""检查参数是否合法"""
        if not super(StatFolderRequest, self).check_params_valid():
            return False
        return self._param_check.check_cos_path_valid(self._cos_path, is_file_path=False)


class DelFileRequest(BaseRequest):
    """ DelFileRequest 删除文件请求 """

    def __init__(self, bucket_name, cos_path):
        u"""

        :param bucket_name: bucket的名称
        :param cos_path: cos的文件路径, 从bucket根/开始, 不以/结束
        """
        super(DelFileRequest, self).__init__(bucket_name, cos_path)

    def check_params_valid(self):
        u"""检查参数是否合法"""
        if not super(DelFileRequest, self).check_params_valid():
            return False
        return self._param_check.check_cos_path_valid(self._cos_path, is_file_path=True)


class DelFolderRequest(BaseRequest):
    """DelFolderRequest 删除目录请求"""

    def __init__(self, bucket_name, cos_path):
        u"""

        :param bucket_name: bucket的名称
        :param cos_path: cos的目录路径, 从bucket根/开始, 以/结束
        """
        super(DelFolderRequest, self).__init__(bucket_name, cos_path)

    def check_params_valid(self):
        u""" 检查参数合法"""
        if not super(DelFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=False):
            return False
        return self._param_check.check_not_cos_root(self._cos_path)


class ListFolderRequest(BaseRequest):
    """ListFolderRequest 获取目录列表的请求"""

    def __init__(self, bucket_name, cos_path, num=199, prefix='', context='', delimiter=''):
        u"""
        :param bucket_name: bucket的名称
        :param cos_path: cos的绝对路径, 从bucket根/开始
        :param num: 搜索数量
        :param prefix: 搜索前缀
        :param context: 搜索上下文
        :param delimiter: 定义分隔符
        """
        super(ListFolderRequest, self).__init__(bucket_name, cos_path)
        self._num = num
        self._prefix = prefix
        self._context = context
        self._delimiter = delimiter

    def set_num(self, num):
        u"""设置List数量

        :param num:
        :return:
        """
        self._num = num

    def get_num(self):
        u"""获取List数量

        :return:
        """
        return self._num

    def set_prefix(self, prefix):
        u"""设置前缀"""
        self._prefix = prefix

    def get_prefix(self):
        u"""获取前缀"""
        return self._prefix

    def set_context(self, context):
        u"""设置搜索上下文"""
        self._context = context

    def get_context(self):
        u"""获取搜索上下文"""
        return self._context

    def set_delimiter(self, delimiter):
        u"""设置分割符"""
        self._delimiter = delimiter

    def get_delimiter(self):
        u"""获取分隔符"""
        return self._delimiter

    def check_params_valid(self):
        u"""检查参数是否有效"""
        if not super(ListFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=False):
            return False
        if not self._param_check.check_param_unicode('prefix', self._prefix):
            return False
        if not self._param_check.check_param_unicode('delimeter', self._delimiter):
            return False
        return self._param_check.check_param_unicode('context', self._context)


class DownloadFileRequest(BaseRequest):

    def __init__(self, bucket_name, cos_path, local_filename, range_start=None, range_end=None, *args, **kwargs):
        super(DownloadFileRequest, self).__init__(bucket_name, cos_path)
        self._local_filename = local_filename
        self._range_start = range_start
        self._range_end = range_end
        self._custom_headers = None
        if 'headers' in kwargs:
            self._custom_headers = kwargs['headers']
        return

    def check_params_valid(self):
        if not super(DownloadFileRequest, self).check_params_valid():
            return False
        from os import path
        if path.exists(self._local_filename):
            return False


class DownloadObjectRequest(BaseRequest):

    def __init__(self, bucket_name, cos_path, range_start=None, range_end=None, *args, **kwargs):
        super(DownloadObjectRequest, self).__init__(bucket_name, cos_path)
        self._range_start = range_start
        self._range_end = range_end
        self._custom_headers = None
        if 'headers' in kwargs:
            self._custom_headers = kwargs['headers']
        return

    def check_params_valid(self):
        if not super(DownloadObjectRequest, self).check_params_valid():
            return False


class MoveFileRequest(BaseRequest):

    def __init__(self, bucket_name, cos_path, dest_path, overwrite=False):
        super(MoveFileRequest, self).__init__(bucket_name, cos_path)
        self._dest_path = dest_path
        if isinstance(overwrite, bool):
            if overwrite:
                self._overwrite = 1
            else:
                self._overwrite = 0
        else:
            raise ValueError('overwrite must be an instance of Boolean')

    @property
    def dest_path(self):
        return self._dest_path

    @property
    def overwrite(self):
        return self._overwrite