# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../CNParticipation/jieba_participator.py
# Compiled at: 2016-07-07 04:27:29
import jieba

class JiebaParticipator(object):

    @staticmethod
    def participate(setence):
        seg_list = jieba.cut(setence, cut_all=False)
        return seg_list


if __name__ == '__main__':
    seg_list = JiebaParticipator.participate('今天的电影很不好看,看的非常不开心。你呢？怎么样？')
    for item in seg_list:
        print item