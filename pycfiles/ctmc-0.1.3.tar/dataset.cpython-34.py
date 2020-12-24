# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\Workspace\py34\py34_projects\ctmatching-project\ctmatching\dataset.py
# Compiled at: 2016-09-08 04:28:42
# Size of source mod 2**32: 1600 bytes
__doc__ = '\n``ctmatching`` algoritm example data set loader. For tests and demo uses. \n\nAbout re78 data:\n\n- 1978 US people earning data by race, age, gender, educations.\n- 429 control samples, 185 treatment samples. Each sample has 10 properties.\n  except ID\n\nFull description of this data: http://users.nber.org/~rdehejia/data/nswdata2.html.\nIf this link is not available, try this:\nhttps://github.com/MacHu-GWU/ctmatching-project/blob/master/ctmatching/testdata/re78-readme.html\n'
import os, numpy as np

def load_re78():
    """re78 dataset loader.

    Usage::

        >>> from ctmatching import load_re78
        >>> control, treat = load_re78()
        >>> len(control)
        429
        >>> len(treat)
        185
    """
    abspath = os.path.join(os.path.dirname(__file__), 'testdata', 're78.txt')
    with open(abspath, 'rb') as (f):
        lines = f.read().decode('utf-8').split('\n')
    columns = lines[0].strip().split(',')
    control = list()
    treatment = list()
    for line in lines[1:]:
        record = line.strip().split(',')
        for i in [1, 2, 3, 4, 5, 6, 7]:
            record[i] = int(record[i])

        for i in [8, 9, 10]:
            record[i] = float(record[i])

        if record[1]:
            treatment.append(record)
        else:
            control.append(record)

    return (control, treatment)


if __name__ == '__main__':
    control, treatment = load_re78()
    assert len(control) == 429
    assert len(treatment) == 185