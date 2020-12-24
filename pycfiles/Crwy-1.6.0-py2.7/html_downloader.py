# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/html/html_downloader.py
# Compiled at: 2020-02-03 23:11:43
import requests

class HtmlDownloader(object):
    """ 下载器 """

    def __init__(self):
        self.session = requests.session()

    def download(self, url, method='GET', single=False, timeout=60, **kwargs):
        u"""
        请求页面
        :param url: 目标地址
        :param method: 请求方式
        :param single: 为True时，不使用session
        :param timeout: 初始化超时时间
        :param kwargs: 更多requests参数
        :return: 返回requests session对象
        """
        if single is False:
            if method.upper() == 'GET':
                return self.session.get(url, timeout=timeout, **kwargs)
            return self.session.post(url, timeout=timeout, **kwargs)
        else:
            if method.upper() == 'GET':
                return requests.get(url, timeout=timeout, **kwargs)
            return requests.post(url, timeout=timeout, **kwargs)

    def download_file(self, url, method='GET', single=False, timeout=180, save_path='./data/', file_name=None, **kwargs):
        u"""
        请求文件
        :param url: 目标地址
        :param method: 请求方式
        :param single: 为True时，不使用session
        :param timeout: 初始化超时时间
        :param save_path: 保存路径
        :param file_name: 文件名称，默认为空
        :param kwargs: 更多requests参数
        :return: 返回保存路径
        """
        if not file_name:
            file_name = url.split('/')[(-1)]
        tmp = self.download(url, method=method, single=single, timeout=timeout, stream=True, **kwargs)
        with open(save_path + file_name, 'wb') as (f):
            for chunk in tmp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

            f.close()
        return save_path + file_name