# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ppd-03020186/anaconda3/lib/python3.6/site-packages/TimeConverter-1.1.0-py3.6.egg/Test.py
# Compiled at: 2018-11-25 08:35:43
# Size of source mod 2**32: 31763 bytes
from TimeNormalizer import TimeNormalizer
tn = TimeNormalizer()
res = tn.parse(target='晚上8点到上午10点之间')
print(res)
res = tn.parse(target='2013年二月二十八日下午四点三十分二十九秒', timeBase='2013-02-28 16:30:29')
print(res)
res = tn.parse(target='我需要大概33天2分钟四秒', timeBase='2013-02-28 16:30:29')
print(res)
res = tn.parse(target='今年儿童节晚上九点一刻')
print(res)
res = tn.parse(target='三日')
print(res)
res = tn.parse(target='7点4')
print(res)
res = tn.parse(target='今年春分')
print(res)