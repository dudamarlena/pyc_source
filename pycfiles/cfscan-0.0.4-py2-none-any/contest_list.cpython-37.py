# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/cf/contest_list.py
# Compiled at: 2019-07-09 05:11:54
# Size of source mod 2**32: 1770 bytes
from cf.classes import *
from cf.util import *

def contest_list(contests, num):
    contests = contests['result']
    n = len(contests)
    p = []
    for i in range(n):
        p.append(Contest(contests[i]))

    found = False
    for i in range(n):
        if p[i].id == num:
            disp_contest(p[i])
            found = True
            break

    if not found:
        print_head('No Contest with the provided id', 'red')


def disp_contest(contest):
    print('\n')
    print_head('Contest Details', 'red')
    print_color('ID', contest.id, 'cyan')
    print_color('Name', contest.name, 'cyan')
    print_color('Type', contest.type, 'cyan')
    print_color('Phase', contest.phase, 'cyan')
    print_color('Duration', seconds_to_hrs(-contest.durationSeconds), 'cyan')
    if contest.startTimeSeconds:
        print_color('Start Time', format_date(contest.startTimeSeconds), 'cyan')
    if contest.relativeTimeSeconds:
        print_color('Time Left', seconds_to_hrs(contest.relativeTimeSeconds), 'cyan')
    if contest.preparedBy:
        print_color('Prepared By', contest.preparedBy, 'cyan')
    if contest.websiteUrl:
        print_color('Website Url', contest.websiteUrl, 'cyan')
    if contest.difficulty:
        print_color('Difficulty', contest.difficulty, 'cyan')
    if contest.kind:
        print_color('Kind', contest.kind, 'cyan')
    if contest.description:
        print_color('Description', contest.description, 'cyan')
    if contest.icpcRegion:
        print_color('IcpcRegion', contest.icpcRegion, 'cyan')
    if contest.country:
        print_color('Country', contest.country, 'cyan')
    if contest.city:
        print_color('City', contest.city, 'cyan')
    if contest.season:
        print_color('Season', contest.season, 'cyan')