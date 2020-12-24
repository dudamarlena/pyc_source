# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_naive.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1449 bytes
import unittest, nltk
nltk.usage(nltk.classify.ClassifierI)
train = [
 (
  dict(a=1, b=1, c=1), 'y'),
 (
  dict(a=1, b=1, c=1), 'x'),
 (
  dict(a=1, b=1, c=0), 'y'),
 (
  dict(a=0, b=1, c=1), 'x'),
 (
  dict(a=0, b=1, c=1), 'y'),
 (
  dict(a=0, b=0, c=1), 'y'),
 (
  dict(a=0, b=1, c=0), 'x'),
 (
  dict(a=0, b=0, c=0), 'x'),
 (
  dict(a=0, b=1, c=1), 'y')]
test = [
 dict(a=1, b=0, c=1),
 dict(a=1, b=0, c=0),
 dict(a=0, b=1, c=1),
 dict(a=0, b=1, c=0)]