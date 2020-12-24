# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/dal/dal_quit.py
# Compiled at: 2016-06-22 17:23:26
from doubanfm.dal.dal_main import MainDal
from termcolor import colored

class QuitDal(MainDal):

    def __init__(self, data):
        super(QuitDal, self).__init__(data)

    @property
    def info(self):
        return colored('  (╭￣3￣)╭♡ ', 'red') + colored('Quit(q)?', 'green')