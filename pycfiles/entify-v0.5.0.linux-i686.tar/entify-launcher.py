# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/entify-launcher.py
# Compiled at: 2015-01-05 13:39:33
import argparse, entify.lib.processing as processing, entify.lib.config_entify as config, logging
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='entify-launcher.py - entify-launcher.py is a program designed to extract using regular expressions all the entities from the files on a given folder. This software also provides an interface to look for these entities in any given text.', prog='entify-launcher.py', epilog='', add_help=False)
    parser._optionals.title = 'Input options (one required)'
    general = parser.add_mutually_exclusive_group(required=True)
    listAll = config.getAllRegexpNames()
    general.add_argument('-r', '--regexp', metavar='<name>', choices=listAll, action='store', nargs='+', help='select the regular expressions to be looked for amongst the following: ' + str(listAll))
    general.add_argument('-R', '--new_regexp', metavar='<regular_expression>', action='store', nargs='+', help='add a new regular expression, for example, for testing purposes.')
    groupInput = parser.add_mutually_exclusive_group(required=True)
    groupInput.add_argument('-i', '--input_folder', metavar='<path_to_input_folder>', default=None, action='store', help='path to the folder to analyse.')
    groupInput.add_argument('-w', '--web', metavar='<url>', action='store', default=None, help='URI to be recovered and analysed.')
    groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the processing parameters.')
    groupProcessing.add_argument('-e', '--extension', metavar='<sum_ext>', nargs='+', choices=['json'], required=False, default=['json'], action='store', help='output extension for the summary files (if not provided, json is assumed).')
    groupProcessing.add_argument('-o', '--output_folder', metavar='<path_to_output_folder>', action='store', help='path to the output folder where the results will be stored.', required=False)
    groupProcessing.add_argument('--recursive', action='store_true', default=False, required=False, help='Variable to tell the system to perform a recursive search on the folder tree.')
    groupProcessing.add_argument('-v', '--verbose', metavar='<verbosity>', choices=[0, 1, 2], required=False, action='store', default=1, help='select the verbosity level: 0 - none; 1 - normal (default); 2 - debug.', type=int)
    groupProcessing.add_argument('-L', '--logfolder', metavar='<path_to_log_folder', required=False, default='./logs', action='store', help='path to the log folder. If none was provided, ./logs is assumed.')
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    groupAbout.add_argument('--version', action='version', version='%(prog)s 0.4.1', help='shows the version of the program and exists.')
    args = parser.parse_args()
    processing.entify_main(args)