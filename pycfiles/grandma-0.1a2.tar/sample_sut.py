# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/tests/sample_sut.py
# Compiled at: 2010-10-25 04:29:35


def sut(p1, p2, p3):
    """
    Sample SUT used to demonstrate the applicattion of grandma.
    """
    data = {'p1': [
            'v1_1', 'v1_2', 'v1_3'], 
       'p2': [
            'v2_1', 'v2_2', 'v2_3', 'v2_4'], 
       'p3': [
            'v3_1', 'v3_2', 'v3_3', 'v3_4', 'v3_5']}
    if p1 in data['p1'] and p2 in data['p2'] and p3 in data['p3']:
        return True
    else:
        return False