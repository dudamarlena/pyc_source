# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\cazipcode-project\cazipcode\pkg\fuzzywuzzy\fuzz.py
# Compiled at: 2017-07-13 17:04:38
# Size of source mod 2**32: 10086 bytes
__doc__ = '\nfuzz.py\n\nCopyright (c) 2011 Adam Cohen\n\nPermission is hereby granted, free of charge, to any person obtaining\na copy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject to\nthe following conditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE\nLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION\nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION\nWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
from __future__ import unicode_literals
import platform, warnings
try:
    from .StringMatcher import StringMatcher as SequenceMatcher
except ImportError:
    from difflib import SequenceMatcher

from . import utils

@utils.check_for_none
@utils.check_empty_string
def ratio(s1, s2):
    s1, s2 = utils.make_type_consistent(s1, s2)
    m = SequenceMatcher(None, s1, s2)
    return utils.intr(100 * m.ratio())


@utils.check_for_none
@utils.check_empty_string
def partial_ratio(s1, s2):
    """"Return the ratio of the most similar substring
    as a number between 0 and 100."""
    s1, s2 = utils.make_type_consistent(s1, s2)
    if len(s1) <= len(s2):
        shorter = s1
        longer = s2
    else:
        shorter = s2
        longer = s1
    m = SequenceMatcher(None, shorter, longer)
    blocks = m.get_matching_blocks()
    scores = []
    for block in blocks:
        long_start = block[1] - block[0] if block[1] - block[0] > 0 else 0
        long_end = long_start + len(shorter)
        long_substr = longer[long_start:long_end]
        m2 = SequenceMatcher(None, shorter, long_substr)
        r = m2.ratio()
        if r > 0.995:
            return 100
        scores.append(r)

    return utils.intr(100 * max(scores))


def _process_and_sort(s, force_ascii, full_process=True):
    """Return a cleaned string with token sorted."""
    ts = utils.full_process(s, force_ascii=force_ascii) if full_process else s
    tokens = ts.split()
    sorted_string = ' '.join(sorted(tokens))
    return sorted_string.strip()


@utils.check_for_none
def _token_sort(s1, s2, partial=True, force_ascii=True, full_process=True):
    sorted1 = _process_and_sort(s1, force_ascii, full_process=full_process)
    sorted2 = _process_and_sort(s2, force_ascii, full_process=full_process)
    if partial:
        return partial_ratio(sorted1, sorted2)
    else:
        return ratio(sorted1, sorted2)


def token_sort_ratio(s1, s2, force_ascii=True, full_process=True):
    """Return a measure of the sequences' similarity between 0 and 100
    but sorting the token before comparing.
    """
    return _token_sort(s1, s2, partial=False, force_ascii=force_ascii, full_process=full_process)


def partial_token_sort_ratio(s1, s2, force_ascii=True, full_process=True):
    """Return the ratio of the most similar substring as a number between
    0 and 100 but sorting the token before comparing.
    """
    return _token_sort(s1, s2, partial=True, force_ascii=force_ascii, full_process=full_process)


@utils.check_for_none
def _token_set(s1, s2, partial=True, force_ascii=True, full_process=True):
    """Find all alphanumeric tokens in each string...
        - treat them as a set
        - construct two strings of the form:
            <sorted_intersection><sorted_remainder>
        - take ratios of those two strings
        - controls for unordered partial matches"""
    p1 = utils.full_process(s1, force_ascii=force_ascii) if full_process else s1
    p2 = utils.full_process(s2, force_ascii=force_ascii) if full_process else s2
    if not utils.validate_string(p1):
        return 0
    if not utils.validate_string(p2):
        return 0
    tokens1 = set(p1.split())
    tokens2 = set(p2.split())
    intersection = tokens1.intersection(tokens2)
    diff1to2 = tokens1.difference(tokens2)
    diff2to1 = tokens2.difference(tokens1)
    sorted_sect = ' '.join(sorted(intersection))
    sorted_1to2 = ' '.join(sorted(diff1to2))
    sorted_2to1 = ' '.join(sorted(diff2to1))
    combined_1to2 = sorted_sect + ' ' + sorted_1to2
    combined_2to1 = sorted_sect + ' ' + sorted_2to1
    sorted_sect = sorted_sect.strip()
    combined_1to2 = combined_1to2.strip()
    combined_2to1 = combined_2to1.strip()
    if partial:
        ratio_func = partial_ratio
    else:
        ratio_func = ratio
    pairwise = [
     ratio_func(sorted_sect, combined_1to2),
     ratio_func(sorted_sect, combined_2to1),
     ratio_func(combined_1to2, combined_2to1)]
    return max(pairwise)


def token_set_ratio(s1, s2, force_ascii=True, full_process=True):
    return _token_set(s1, s2, partial=False, force_ascii=force_ascii, full_process=full_process)


def partial_token_set_ratio(s1, s2, force_ascii=True, full_process=True):
    return _token_set(s1, s2, partial=True, force_ascii=force_ascii, full_process=full_process)


def QRatio(s1, s2, force_ascii=True):
    """
    Quick ratio comparison between two strings.

    Runs full_process from utils on both strings
    Short circuits if either of the strings is empty after processing.

    :param s1:
    :param s2:
    :param force_ascii: Allow only ASCII characters (Default: True)
    :return: similarity ratio
    """
    p1 = utils.full_process(s1, force_ascii=force_ascii)
    p2 = utils.full_process(s2, force_ascii=force_ascii)
    if not utils.validate_string(p1):
        return 0
    if not utils.validate_string(p2):
        return 0
    return ratio(p1, p2)


def UQRatio(s1, s2):
    """
    Unicode quick ratio

    Calls QRatio with force_ascii set to False

    :param s1:
    :param s2:
    :return: similarity ratio
    """
    return QRatio(s1, s2, force_ascii=False)


def WRatio(s1, s2, force_ascii=True):
    """
    Return a measure of the sequences' similarity between 0 and 100, using different algorithms.

    **Steps in the order they occur**

    #. Run full_process from utils on both strings
    #. Short circuit if this makes either string empty
    #. Take the ratio of the two processed strings (fuzz.ratio)
    #. Run checks to compare the length of the strings
        * If one of the strings is more than 1.5 times as long as the other
          use partial_ratio comparisons - scale partial results by 0.9
          (this makes sure only full results can return 100)
        * If one of the strings is over 8 times as long as the other
          instead scale by 0.6

    #. Run the other ratio functions
        * if using partial ratio functions call partial_ratio,
          partial_token_sort_ratio and partial_token_set_ratio
          scale all of these by the ratio based on length
        * otherwise call token_sort_ratio and token_set_ratio
        * all token based comparisons are scaled by 0.95
          (on top of any partial scalars)

    #. Take the highest value from these results
       round it and return it as an integer.

    :param s1:
    :param s2:
    :param force_ascii: Allow only ascii characters
    :type force_ascii: bool
    :return:
    """
    p1 = utils.full_process(s1, force_ascii=force_ascii)
    p2 = utils.full_process(s2, force_ascii=force_ascii)
    if not utils.validate_string(p1):
        return 0
    else:
        if not utils.validate_string(p2):
            return 0
        try_partial = True
        unbase_scale = 0.95
        partial_scale = 0.9
        base = ratio(p1, p2)
        len_ratio = float(max(len(p1), len(p2))) / min(len(p1), len(p2))
        if len_ratio < 1.5:
            try_partial = False
        if len_ratio > 8:
            partial_scale = 0.6
        if try_partial:
            partial = partial_ratio(p1, p2) * partial_scale
            ptsor = partial_token_sort_ratio(p1, p2, full_process=False) * unbase_scale * partial_scale
            ptser = partial_token_set_ratio(p1, p2, full_process=False) * unbase_scale * partial_scale
            return utils.intr(max(base, partial, ptsor, ptser))
        tsor = token_sort_ratio(p1, p2, full_process=False) * unbase_scale
        tser = token_set_ratio(p1, p2, full_process=False) * unbase_scale
        return utils.intr(max(base, tsor, tser))


def UWRatio(s1, s2):
    """Return a measure of the sequences' similarity between 0 and 100,
    using different algorithms. Same as WRatio but preserving unicode.
    """
    return WRatio(s1, s2, force_ascii=False)