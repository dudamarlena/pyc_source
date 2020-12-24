# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/commodity_project_ir/package1/commodity_tool.py
# Compiled at: 2019-02-24 23:19:27
# Size of source mod 2**32: 489 bytes
__doc__ = 'This module runs as a pseudo main function and data set into a dataframe'

def load_data():
    """load_data takes no arugments (currently) and loads in the dataset identified in this project.
    it then calls TODO"""
    print('load data here')


def main():
    """Runs if this module is imported"""
    print('Other main ran')
    load_data()


if __name__ == 'main':
    print('main ran')
    load_data()