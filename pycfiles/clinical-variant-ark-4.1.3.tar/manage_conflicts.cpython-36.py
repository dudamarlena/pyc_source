# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/iotools/converters/nifd_to_bids/utils/manage_conflicts.py
# Compiled at: 2019-10-10 04:46:11
# Size of source mod 2**32: 877 bytes
__author__ = 'Adam Wild'
__copyright__ = 'Copyright 2016-2019 The Aramis Lab Team'
__credits__ = ['Adam Wild']
__license__ = 'See LICENSE.txt file'
__version__ = '0.1.0'
__maintainer__ = 'Adam Wild'
__email__ = 'adam.wild@icm-institute.org'
__status__ = 'Development'

class Manage_conflicts:

    def __init__(self, path_choices):
        self.dic = self.parse_choices(path_choices)

    def parse_choices(self, path_choices):
        f = open(path_choices, 'r')
        dic = dict()
        for line in f.readlines():
            line = line.split('-')
            dic[line[0]] = line[1]

        return dic

    def make_decision(self, list_med_names):
        list_med_names.sort()
        return self.dic[str(list_med_names)]

    def __str__(self):
        s = ''
        for key in self.dic:
            s += str(key) + ' -> ' + str(self.dic[key])

        return s