# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gregorlenz/Development/eye-tracking/loris/source/ReadFile.py
# Compiled at: 2019-05-25 04:08:13
# Size of source mod 2**32: 1488 bytes
import loris_extension
from . import CSV as csv
import os

def read_file(file_name, file_name_dat_aps=None):
    """parse a file from a neuromorphic camera and return events
    supported file formats are .aedat, .dat, .es and .csv
    """
    if file_name.endswith('.aedat'):
        print('Not yet implemented')
        return
    if file_name.endswith('.dat') and '_td' in file_name and file_name_dat_aps == None:
        parsed_file = loris_extension.read_dat_td(file_name)
    else:
        if file_name.endswith('.dat') and '_aps' in file_name and file_name_dat_aps == None:
            parsed_file = loris_extension.read_dat_aps(file_name)
        else:
            if file_name.endswith('.dat'):
                if file_name_dat_aps.endswith('.dat'):
                    parsed_file = loris_extension.read_dat_td_aps(file_name, file_name_dat_aps)
                else:
                    if file_name.endswith('.es'):
                        parsed_file = loris_extension.read_event_stream(file_name)
                    else:
                        if file_name.endswith('.csv'):
                            parsed_file = csv.parse_file(file_name)
                        else:
                            print("I don't know what kind of format you want to read. Please specify a valid file name ending such as .aedat etc")
                            return
            elif file_name_dat_aps == None:
                print('Read ' + str(len(parsed_file['events'])) + ' events of type ' + parsed_file['type'] + ' from ' + os.path.split(file_name)[(-1)])
            else:
                print('Read ' + str(len(parsed_file['events'])) + ' events from combined files with dvs and atis events.')
            return parsed_file