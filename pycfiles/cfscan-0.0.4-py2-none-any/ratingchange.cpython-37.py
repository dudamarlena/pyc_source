# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/cf/ratingchange.py
# Compiled at: 2019-07-09 05:11:54
# Size of source mod 2**32: 1285 bytes
from cf.util import *
from cf.classes import *
import pydoc

def ratingchange(res):
    res = res['result']
    rc = []
    for i in range(len(res)):
        rc.append(RatingChange(res[i]))

    st = get_colored('Rating Changes for contest: ' + str(rc[0].contestId) + ' ' + rc[0].contestName, 'magenta') + '\n\n'
    for r in rc:
        st += get_rc(r)

    return st


def get_rc(rc):
    rank = get_colored(str(rc.rank), 'blue')
    h = get_colored(rc.handle, 'blue')
    if rc.oldRating > rc.newRating:
        old = get_colored(str(rc.oldRating), 'green')
        new = get_colored(str(rc.newRating), 'red')
    elif rc.oldRating < rc.newRating:
        old = get_colored(str(rc.oldRating), 'red')
        new = get_colored(str(rc.newRating), 'green')
    else:
        old = get_colored(str(rc.oldRating), 'green')
        new = get_colored(str(rc.newRating), 'green')
    arrow = get_colored(' > ', 'cyan')
    st = rank + ' ' + h + ' ' + old + arrow + new + '\n'
    return st


def ratc(res):
    pydoc.pager(ratingchange(res))


def rath(res, han):
    found = False
    for r in res['result']:
        if r['handle'] == han:
            print(get_rc(RatingChange(r)))
            found = True
            break

    if not found:
        print(get_colored('\nUser did not participate in contest', 'red'))