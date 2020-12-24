# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyle/projects/top30/pyenv/lib/python3.7/site-packages/top30/__init__.py
# Compiled at: 2019-04-09 15:20:17
# Size of source mod 2**32: 3039 bytes
"""
Runs the Rundown creator
"""
import argparse, os
from top30.chart import Chart
from top30.handlers import UserInterface
from top30.top_30_creator import Top30Creator
from top30.settings import Settings
VERSION = '2.0.0'
SETTINGS = Settings()

def get_format(filename):
    """ Returns the file type from a filename """
    extension = os.path.splitext(filename)[1]
    if extension.startswith('.'):
        extension = extension[1:]
    return extension


def cli():
    """
    Main function. Runs the command-line program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--current-chart', dest='current_chart', help='chart document to create the rundowns from, required for command line operation')
    parser.add_argument('-p', '--previous-chart', dest='previous_chart', help='the previous chart document, required for command line operation')
    parser.add_argument('-v', '--version', action='store_true', help='prints the version information and exits')
    args = parser.parse_args()
    creator = Top30Creator()
    if args.version:
        print('top30', VERSION)
        print('This project comes with NO WARRENTY, to the extent permitted by the law.')
        print('You may redistribute it under the terms of the GNU General Public License')
        print('version 3; see the file named LICENSE for details.')
        print('\nWritten by Kyle Robbertze')
        return
    if args.previous_chart == None or args.current_chart == None:
        print('Missing chart file arguments')
        parser.print_help()
        exit(120)
    chart = Chart(args.current_chart)
    previous_chart = Chart(args.previous_chart, 'last-week_')
    print('Creating 30 - 21 rundown...')
    creator.create_rundown(30, 21, chart)
    print('Creating 20 - 11 rundown...')
    creator.create_rundown(20, 11, chart)
    print('Creating 10 - 2 rundown...')
    creator.create_rundown(10, 2, chart)
    print("Creating last week's 10 - 1 rundown...")
    creator.create_rundown(10, 1, previous_chart)


def gui():
    creator = Top30Creator()
    gui = UserInterface()
    gui.run(creator)