# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topper/utils/parser.py
# Compiled at: 2020-05-05 04:56:07
# Size of source mod 2**32: 938 bytes
"""
Argument parser
"""
import argparse

def create_parser():
    """
    Parser
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--landing_folder',
      help='Folder of file reception',
      required=True)
    parser.add_argument('--checkpoint_directory',
      help='Directory used to persist data across days',
      required=True)
    parser.add_argument('--output_directory',
      help='Path to output directory',
      required=True)
    parser.add_argument('--mode',
      help='Path to output directory',
      required=False,
      default='country',
      choices=[
     'country', 'user'])
    return parser


def parse_args(args):
    """
    Parse arguments
    :param args: raw args
    :return: Parsed arguments
    """
    parser = create_parser()
    return parser.parse_args(args=args)