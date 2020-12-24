# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\commands.py
# Compiled at: 2011-03-24 10:24:06
"""
Has the different commands used by the application.
"""
import argparse, logging, os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(choices=['web', 'initialize', 'delete_tmpfiles'], dest='program')
    args = parser.parse_args()
    if args.program == 'initialize':
        logging.basicConfig(level=logging.INFO, filename='initialize.log', filemode='w')
        from pywebuml.parsers.main import ParserExecuter
        parser = ParserExecuter()
        parser.parse('.')
    if args.program == 'web':
        logging.basicConfig(level=logging.INFO)
        from pywebuml.web import start_app
        start_app()
    if args.program == 'delete_tmpfiles':
        logging.basicConfig(level=logging.INFO)
        logging.info('Deliting images and dot files.')
        current_path = os.path.abspath(os.path.dirname(__file__))
        tmp_dir = os.path.join(current_path, 'static', 'tmp_dir')
        for filename in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, filename))