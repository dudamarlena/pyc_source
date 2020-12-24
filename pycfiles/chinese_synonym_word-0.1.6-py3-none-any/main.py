# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/chinese_slugify/main.py
# Compiled at: 2014-09-20 13:56:27
import re, unicodedata, jieba
from slugify import slugify
import pypinyin
re_en = re.compile("([a-zA-Z\\']+)")
re_all_en = re.compile("^([a-zA-Z\\']+)$")
re_chinese = re.compile('([⺀-\u9fff]+)')
re_all_chinese = re.compile('^([⺀-\u9fff]+)$')

def chinese_slugify(text, delimiter='-'):
    if not type(text) == unicode:
        raise ValueError('should be unicode')
    slug_list = []
    segments_split_by_space = text.split()
    segments_split_by_chinese = []
    for segment in segments_split_by_space:
        segments_split_by_chinese.extend(re_chinese.split(segment))

    for segment in segments_split_by_chinese:
        if not segment:
            continue
        segment = segment.strip()
        if not segment:
            continue
        elif re_all_en.match(segment):
            slug_list.append(segment)
        elif re_all_chinese.match(segment):
            sig_list = jieba.cut(segment, cut_all=False)
            for sig in sig_list:
                arr_pinyin = sum(pypinyin.pinyin(sig, pypinyin.NORMAL), [])
                pinyin = ('').join([ pinyin.capitalize() for pinyin in arr_pinyin
                                   ])
                slug_list.append(pinyin)

        else:
            slug_list.append(slugify(segment))

    slugged = delimiter.join(slug_list)
    slugged = unicode(unicodedata.normalize('NFKD', slugged).encode('ascii', 'ignore'))
    slugged = re.sub("[^\\w\\s%s']" % re.escape(delimiter), '', slugged).strip()
    slugged = re.sub('[%s\\s]+' % delimiter, delimiter, slugged)
    return unicode(slugged)