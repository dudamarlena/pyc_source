# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zhihu/comment.py
# Compiled at: 2016-02-17 02:27:50
# Size of source mod 2**32: 943 bytes


class Comment:
    __doc__ = '评论类，一般不直接使用，而是作为``Answer.comments``迭代器的返回类型.'

    def __init__(self, cid, answer, author, upvote_num, content, time, group_id=None):
        """创建评论类实例.

        :param int cid: 评论ID
        :param int group_id: 评论所在的组ID
        :param Answer answer: 评论所在的答案对象
        :param Author author: 评论的作者对象
        :param int upvote_num: 评论赞同数量
        :param str content: 评论内容
        :param datetime.datetime creation_time: 评论发表时间
        :return: 评论对象
        :rtype: Comment
        """
        self.cid = cid
        self.answer = answer
        self.author = author
        self.upvote_num = upvote_num
        self.content = content
        self.creation_time = time
        self._group_id = group_id