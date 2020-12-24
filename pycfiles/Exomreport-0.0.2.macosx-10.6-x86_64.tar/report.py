# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/anaconda/anaconda2/lib/python2.7/site-packages/bin/report.py
# Compiled at: 2019-05-30 02:02:46
import sys
pos_list = [
 0, 2, 3, 4, 5, 6, 7, 8, 9, 12, 20, 21, 22, 23, 24, 26, 27, 28, 29, 34, 36, 37, 38, 39, 40]

def report(file):
    r_list = []
    with open(file, 'r') as (f):
        for i in f:
            if i.startswith('#'):
                continue
            else:
                line = i.strip()
                r_list.append(line)

    f_list = [ r_list[i] for i in pos_list ]
    return f_list


def write_cov(f_list):
    with open('simple_covreport.txt', 'w') as (f):
        for line in f_list:
            f.write(line + '\n')


if __name__ == '__main__':
    file = sys.argv[1]
    f_list = report(file)
    write_cov(f_list)