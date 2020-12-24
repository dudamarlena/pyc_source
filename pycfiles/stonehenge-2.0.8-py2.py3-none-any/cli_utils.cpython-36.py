# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rtownley/Projects/stonehenge/stonehenge/cli_utils.py
# Compiled at: 2018-08-31 13:32:27
# Size of source mod 2**32: 673 bytes


def print_help(msg=None):
    """Print out a message for a user who misused the CLI command"""
    if msg is not None:
        print(msg)
    print('Welcome to the Stonehenge project builder!\n\nTo use this utility, you\'ll first create a configuration file, and\nthen build the project based off of that configuration.\n\nYou can either create the config file (stonehenge_config.py)\nyourself, or you can run "stonehenge new" to generate a file with\nsome helpful pre-populated defaults.\n\nOnce the file has been created, you can run "stonehenge build" to\ncreate your project.\n\nFor more information, or for usage examples, visit\nhttps://github.com/RobertTownley/Stonehenge.')