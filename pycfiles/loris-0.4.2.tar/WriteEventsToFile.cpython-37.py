# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gregorlenz/Development/eye-tracking/loris/source/WriteEventsToFile.py
# Compiled at: 2019-05-24 11:56:33
# Size of source mod 2**32: 801 bytes
import loris_extension

def write_events_to_file(parsed_file, output_file_name):
    """store a structured numpy array of events to a given file format
    supported file format is .es
    """
    res = None
    if output_file_name.endswith('.es'):
        res = loris_extension.write_event_stream(parsed_file, output_file_name)
        print('Wrote ' + str(len(parsed_file['events'])) + ' events of type ' + parsed_file['type'] + ' to ' + output_file_name)
    else:
        if output_file_name.endswith('.dat'):
            print('This is not implemented.')
        else:
            if output_file_name.endswith('.aedat'):
                print('This is not implemented.')
            else:
                print("I don't know what kind of format you want to write to. Please specify a valid file name ending such as .es")
    return res