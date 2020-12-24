# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/breinify/demo_temporal_data.py
# Compiled at: 2017-04-18 14:25:10
# Size of source mod 2**32: 558 bytes
import breinify, json

def printAt(location):
    """
    Prints out a json of useful information about the given location.
    :param location: A string describing a US city.
    :return: The city's dictionary
    """
    brein = breinify.Breinify('YOURAPIKEY')
    result = brein.temporal_data(location_free_text=location)
    print('Information for ' + location + ':')
    print('-----------------------------')
    print(json.dumps(result, indent=4))
    return result


if __name__ == '__main__':
    printAt('san francisco, ca')
    printAt('nyc')