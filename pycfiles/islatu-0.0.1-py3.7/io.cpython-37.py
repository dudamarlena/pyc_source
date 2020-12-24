# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/islatu/io.py
# Compiled at: 2020-04-22 08:47:56
# Size of source mod 2**32: 2779 bytes
"""
Parsers for inputing experiental files.
"""
import pandas as pd

def i07_dat_parser(file_path):
    """
    Parsing the .dat file from I07.

    Args:
        (str): The ``.dat`` file to be read.

    Returns:
        (tuple): tuple containing:
            - (dict): The metadata from the ``.dat`` file.
            - (pd.DataFrame): The data from the ``.dat`` file.
    """
    f_open = open(file_path, 'r')
    data_reading = False
    metadata_reading = False
    data_dict = {}
    metadata_dict = {}
    data_lines = []
    for line in f_open:
        if '<MetaDataAtStart>' in line:
            metadata_reading = True
        else:
            if '</MetaDataAtStart>' in line:
                metadata_reading = False
            if ' &END' in line:
                data_reading = True
                count = -2
            if metadata_reading and '=' in line:
                metadata_in_line = []
                for i in line.split('=')[1:]:
                    try:
                        j = float(i)
                    except ValueError:
                        j = i

                    metadata_in_line.append(j)

                metadata_dict[line.split('=')[0]] = metadata_in_line
        if data_reading:
            count += 1
            if count == 0:
                titles = line.split()
            if count > 0:
                data_lines.append(line.split())

    f_open.close()
    for j in range(len(data_lines[0])):
        list_to_add = []
        for i in range(len(data_lines)):
            try:
                list_to_add.append(float(data_lines[i][j]))
            except ValueError:
                list_to_add.append(data_lines[i][j])

        count = 0
        if j >= len(titles):
            data_dict[str(count)] = list_to_add
            count += 1
        else:
            data_dict[titles[j]] = list_to_add

    return (
     metadata_dict, pd.DataFrame(data_dict))