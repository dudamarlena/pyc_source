# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/catalog_cross_matching.py
# Compiled at: 2018-08-25 11:57:28
# Size of source mod 2**32: 5390 bytes
from __future__ import print_function
import os, sys, time, re
if sys.version_info.major >= 3:
    long = int
else:

    def flatten(item, keepcls=(), keepobj=()):
        """ Flatten a list, 
        see -- https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
    """
        if hasattr(item, '__iter__'):
            if isinstance(item, keepcls) or item in keepobj:
                yield item
        else:
            for i in item:
                for j in flatten(i, keepcls, keepobj + (item,)):
                    yield j


    def search_for_matches_in_a_sorted_array(input_array, match_value, start_position=0, search_direction=1, output_allmatches=False):
        """ Example: xmatch2 = search_for_matches_in_a_sorted_array(array2, array1[i1], i2, -1)
    """
        i = start_position
        xmatches = []
        while i >= 0:
            if i <= len(input_array) - 1:
                val = input_array[i]
                if val == match_value:
                    xmatches.append(i)
                    if not output_allmatches:
                        break
            elif search_direction > 0:
                if val > match_value:
                    break
            elif search_direction < 0:
                if val < match_value:
                    break
            i = i + search_direction

        return xmatches


    def cross_match_sorted_arrays(input_array_list, output_allmatches=False, output_nonmatches=False):
        """ Return two index array with common items in the two arrays
        We will search for only one match per item, unless the option 'output_allmatches' is set to True. 
        We have the option 'output_nonmatches' to also output all non-matches.
        TODO: what if input_array has duplicates?
    """
        xmatches = []
        nonmatches = []
        i = []
        if type(input_array_list) is not list:
            print('Error! The input_array_list should be a list!')
            sys.exit()
        if len(input_array_list) == 0:
            print('Error! The input_array_list should be a non-empty list!')
            sys.exit()
        for input_array in input_array_list:
            if len(input_array) == 0:
                print('Error! The input_array should be non-empty!')
                sys.exit()
            xmatches.append([])
            nonmatches.append([])
            i.append(0)

        while i[0] < len(input_array_list[0]):
            input_array_1 = input_array_list[0]
            i1 = i[0]
            val1 = long(input_array_1[i1])
            countxmatches = 1
            if output_allmatches:
                tmpxmatches = [
                 [
                  i1]]
            else:
                tmpxmatches = [
                 i1]
            for j in range(1, len(input_array_list)):
                input_array_2 = input_array_list[j]
                i2 = i[j]
                tmpxmatches2 = []
                tmpxmatches2a = search_for_matches_in_a_sorted_array(input_array_2, val1, i2, (-1), output_allmatches=output_allmatches)
                if len(tmpxmatches2a) > 0:
                    tmpxmatches2.extend(tmpxmatches2a)
                if len(tmpxmatches2a) == 0 or output_allmatches:
                    tmpxmatches2b = search_for_matches_in_a_sorted_array(input_array_2, val1, (i2 + 1), 1, output_allmatches=output_allmatches)
                    if len(tmpxmatches2b) > 0:
                        tmpxmatches2.extend(tmpxmatches2b)
                if len(tmpxmatches2) > 0:
                    countxmatches = countxmatches + 1
                    if output_allmatches:
                        tmpxmatches.append(tmpxmatches2)
                    else:
                        tmpxmatches.append(tmpxmatches2[0])

            if countxmatches == len(input_array_list):
                xmatches[0].append(tmpxmatches[0])
                for j in range(1, len(input_array_list)):
                    xmatches[j].append(tmpxmatches[j])
                    if output_allmatches:
                        i[j] = max(tmpxmatches[j]) + 1
                    else:
                        i[j] = tmpxmatches[j] + 1

            i[0] = i[0] + 1

        if output_nonmatches:
            input_array_1 = input_array_list[0]
            xmatches1 = list(flatten(xmatches[0]))
            allindex1 = range(len(input_array_1))
            nonmatch1 = list(set(allindex1) - set(xmatches1))
            nonmatches[0] = nonmatch1
            for j in range(1, len(input_array_list)):
                input_array_2 = input_array_list[j]
                xmatches2 = list(flatten(xmatches[j]))
                allindex2 = range(len(input_array_2))
                nonmatch2 = list(set(allindex2) - set(xmatches2))
                nonmatches[j] = nonmatch2

            return (
             xmatches, nonmatches)
        return xmatches