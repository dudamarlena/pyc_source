# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/utils/compare_utils.py
# Compiled at: 2017-03-01 08:38:06
"""
     * Compare a list values attributs with a given value to return
     * a new list that include only the matched values.
     *
     * @param list               The list to analyse first
     * @param values             The values the attributs will be compared to.
     * @param attrName           Name of the object's attribut that will be compared.
     *                           Normally in list but if otherList is filled it's in
     *                           otherlist.
     * @param subattrName        If needed, parameter that allows to check a sub-attribut
     *                           from attrName.
     * @param otherList          In case a match is necessary with cross-lists, fill this
     *                           parameter with the second list where the attribut enquired
     *                           is.
     * @param linkProperties     List of two items that correspond to the two attribut that
     *                           links the two lists. item[0] is in list and item[1] is in
     *                           otherList.
     * @see User
"""
import fnmatch

def compare(list, values, attrName, subattrName=None, otherList=None, linkProperties=None):
    if len(values) == 0:
        return Exception
    returnList = []
    if isinstance(values, basestring):
        returnList.extend(filter_with_single_value(list, values, attrName, subattrName, otherList, linkProperties))
    for value in values:
        returnList.extend(filter_with_single_value(list, value, attrName, subattrName, otherList, linkProperties))

    return returnList


def filter_with_single_value(list, value, attrName, subattrName=None, otherList=None, linkProperties=None):
    filtered = []
    for item in list:
        if otherList is None:
            compareName = getattr(item, attrName)
            if subattrName is None:
                if fnmatch.fnmatch(compareName, value):
                    filtered.append(item)
            else:
                compareName2 = getattr(compareName, subattrName)
                if fnmatch.fnmatch(compareName2, value):
                    filtered.append(item)
        else:
            for otherItem in otherList:
                if getattr(item, linkProperties[0]) == getattr(otherItem, linkProperties[1]):
                    compareName = getattr(otherItem, attrName)
                    if subattrName is None:
                        if fnmatch.fnmatch(compareName, value):
                            filtered.append(item)
                    else:
                        compareName2 = getattr(compareName, subattrName)
                        if fnmatch.fnmatch(compareName2, value):
                            filtered.append(item)

    return filtered