# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zhihu\models\column.py
# Compiled at: 2017-08-17 03:46:25
# Size of source mod 2**32: 2054 bytes
import re
from zhihu.decorators.auth import authenticated
from zhihu.models.base import Model
from zhihu.error import ZhihuError
from zhihu.settings import ZHUANLAN_HEADERS
from zhihu.url import URL

class Column(Model):
    __doc__ = '\n    专栏\n    '

    def __init__(self, slug=None, url=None):
        super(Column, self).__init__()
        slug = slug if slug is not None else self._extract_slug(url)
        if not slug:
            raise ZhihuError('没有指定专栏的的slug或者url')
        self.slug = slug
        self.headers = ZHUANLAN_HEADERS
        self.headers['x-xsrf-token'] = self._get_xsrf()

    @staticmethod
    def _extract_slug(url):
        """
        从url中提取目标slug
        """
        pattern = re.compile('https://zhuanlan.zhihu.com/(\\w+)/?.*?')
        match = pattern.search(url)
        if match:
            return match.group(1)

    def followers(self, limit=500, offset=0):
        """
        用户关注列表
        :param limit: 最大获取条数,不能超过500条
        :param offset: 偏移量
        :return: 返回用户列表
        """
        r = self._execute(method='get', url=(URL.column_followers(self.slug)), params={'limit':limit,  'offset':offset})
        return r.json()

    @authenticated
    def follow(self):
        """关注某专栏"""
        r = self._execute(method='put', url=(URL.follow_column(self.slug)))
        if r.ok:
            print('关注专栏成功')
        else:
            raise ZhihuError('操作失败：%s' % r.text)

    @authenticated
    def unfollow(self):
        """取消关注某专栏"""
        r = self._execute(method='delete', url=(URL.unfollow_column(self.slug)))
        if r.ok:
            print('取消关注专栏成功')
        else:
            raise ZhihuError('操作失败：%s' % r.text)

    def _get_xsrf(self):
        response = self._execute(method='get', url=(URL.column_index(self.slug)))
        return response.cookies['XSRF-TOKEN']