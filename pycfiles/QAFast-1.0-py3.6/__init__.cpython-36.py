# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\QAFast\__init__.py
# Compiled at: 2019-04-28 15:01:48
# Size of source mod 2**32: 146 bytes
import QUANTAXIS as QA
user = QA.QA_User(username='quantaxis', password='quantaxis')
portfolio = user.new_portfolio('test_portfolio')