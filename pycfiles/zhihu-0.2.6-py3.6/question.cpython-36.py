# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zhihu\models\question.py
# Compiled at: 2017-08-17 03:46:25
# Size of source mod 2**32: 1534 bytes
import re
from zhihu.decorators.auth import authenticated
from zhihu.models.base import Model
from zhihu.error import ZhihuError
from zhihu.url import URL

class Question(Model):

    def __init__(self, id=None, url=None):
        id = id if id is not None else self._extract_id(url)
        if not id:
            raise ZhihuError('没有指定问题的id或者url')
        self.id = str(id)
        super(Question, self).__init__()

    @staticmethod
    def _extract_id(url):
        """
        从url中提取目标id
        """
        pattern = re.compile('https://www.zhihu.com/question/(\\d+).*?')
        match = pattern.search(url)
        if match:
            return match.group(1)

    @authenticated
    def follow_question(self, **kwargs):
        """关注某问题"""
        r = (self._execute)(method='post', url=URL.follow_question(self.id), **kwargs)
        if r.ok:
            return r.json()
        raise ZhihuError('操作失败：%s' % r.text)

    @authenticated
    def unfollow_question(self, **kwargs):
        """取消关注某问题"""
        r = (self._execute)(method='delete', url=URL.unfollow_question(self.id), **kwargs)
        if r.ok:
            return {'is_following': False}
        raise ZhihuError('操作失败：%s' % r.text)