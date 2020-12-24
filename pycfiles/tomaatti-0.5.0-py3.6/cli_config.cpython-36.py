# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/cli_config.py
# Compiled at: 2018-10-10 01:53:49
# Size of source mod 2**32: 987 bytes


def script_entry_point():
    from argparse import ArgumentParser
    argument_parser = ArgumentParser(description='Pomodoro timer for i3 - Configuration tool')
    parsed_arguments = argument_parser.parse_args()


if __name__ == '__main__':
    script_entry_point()