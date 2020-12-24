# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/gutz/getwiencase.py
# Compiled at: 2019-02-23 22:41:15
# Size of source mod 2**32: 1120 bytes
import os, glob, warnings

def get_wiencase():
    case = os.path.basename(os.getcwd())
    if not os.path.isfile(case + '.struct'):
        files = glob.glob('*.struct')
        if len(files) < 1:
            raise Exception('No struct file present.')
        else:
            if len(files) > 1:
                candidates = [os.path.splitext(f)[0] for f in files]
                allheads = [os.path.splitext(f)[0] for f in os.listdir('.')]
                counts = [len([1 for f in allheads if f == candidate]) for candidate in candidates]
                index = counts.index(max(counts))
                case = candidates[index]
                warnings.warn(' case heuristically selected from multiple possibilities!')
            else:
                case, ext = os.path.splitext(os.path.basename(files[0]))
    return case