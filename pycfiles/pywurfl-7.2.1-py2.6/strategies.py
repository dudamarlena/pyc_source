# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywurfl/algorithms/wurfl/strategies.py
# Compiled at: 2011-01-06 14:57:12
"""
This module contains the supporting classes for the Two Step Analysis user agent
algorithm that is used as the primary way to match user agents with the Java API
for the WURFL.

A description of the way the following source is intended to work can be found
within the source for the original Java API implementation here:
http://sourceforge.net/projects/wurfl/files/WURFL Java API/

The original Java code is GPLd and Copyright (c) WURFL-Pro srl
"""
__author__ = 'Armand Lynch <lyncha@users.sourceforge.net>'
__copyright__ = 'Copyright 2011, Armand Lynch'
__license__ = 'LGPL'
__url__ = 'http://celljam.net/'
__version__ = '1.2.1'
import Levenshtein

def ris_match(candidates, needle, tolerance):
    match = ''
    needle_length = len(needle)
    best_distance = -1
    best_match_index = -1
    low = 0
    high = len(candidates) - 1
    while low <= high and best_distance < needle_length:
        mid = (low + high) / 2
        mid_candidate = candidates[mid]
        distance = longest_common_prefix(needle, mid_candidate)
        if distance > best_distance:
            best_match_index = mid
            best_distance = distance
        if mid_candidate < needle:
            low = mid + 1
        elif mid_candidate > needle:
            high = mid - 1
        else:
            break

    if best_distance >= tolerance:
        match = first_of_best_matches(needle, candidates, best_match_index, best_distance)
    return match


def longest_common_prefix(t1, t2):
    i = 0
    t = min(len(t1), len(t2))
    for j in xrange(0, t):
        if t1[j] == t2[j]:
            i += 1
        else:
            break

    return i


def first_of_best_matches(needle, candidates, best_match_index, best_distance):
    best_match = candidates[best_match_index]
    for candidate in reversed(candidates[:best_match_index - 1]):
        if best_distance == longest_common_prefix(needle, candidate):
            best_match = candidate
        else:
            break

    return best_match


def ld_match(candidates, needle, tolerance):
    needle_length = len(needle)
    user_agent = ''
    matches = [ (Levenshtein.distance(needle, c), c) for c in candidates if abs(needle_length - len(c)) <= tolerance
              ]
    if matches:
        (score, user_agent) = min(matches)
        if score > tolerance:
            user_agent = ''
    return user_agent