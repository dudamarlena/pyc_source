# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marketplacecli/utils/compare_utils.py
# Compiled at: 2016-06-03 07:47:35
__author__ = 'UShareSoft'
import fnmatch

def compare(list, values, attrName, subattrName=None, otherList=None, linkProperties=None):
    if len(values) == 0:
        return Exception
    else:
        returnList = []
        for value in values:
            for item in list:
                if otherList is None:
                    compareName = getattr(item, attrName)
                    if subattrName is None:
                        if fnmatch.fnmatch(compareName, value):
                            returnList.append(item)
                    else:
                        compareName2 = getattr(compareName, subattrName)
                        if fnmatch.fnmatch(compareName2, value):
                            returnList.append(item)
                else:
                    for otherItem in otherList:
                        if getattr(item, linkProperties[0]) == getattr(otherItem, linkProperties[1]):
                            compareName = getattr(otherItem, attrName)
                            if subattrName is None:
                                if fnmatch.fnmatch(compareName, value):
                                    returnList.append(item)
                            else:
                                compareName2 = getattr(compareName, subattrName)
                                if fnmatch.fnmatch(compareName2, value):
                                    returnList.append(item)

        return returnList