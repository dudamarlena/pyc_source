# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/XML.py
# Compiled at: 2017-03-19 15:39:15
# Size of source mod 2**32: 1580 bytes
"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
import os, glob, xml.etree.ElementTree as eT, ntpath

class XML:

    @staticmethod
    def get_filename():
        directory = os.getcwd()
        path = directory + '/*.xml'
        files = glob.glob(path)
        length = len(files)
        if length <= 0:
            print('No XML files in directory!')
            return 0
        else:
            file_no = -1
            while file_no < 0 or file_no > length:
                no = 1
                print('Found XML files:')
                for filename in files:
                    string = '%s) %s' % (no, ntpath.basename(filename))
                    print(string)
                    no += 1

                print('')
                string = '%s) %s' % (0, "Don't use MyAnimeList XML file.")
                print(string)
                try:
                    file_no = int(input('Select file: '))
                except ValueError:
                    print('Give a number!')
                    file_no = -1

            file_no -= 1
            if file_no < 0:
                return
            filename = files[file_no]
            return filename

    def get_xml_root(self, file_path=None):
        if not file_path or not os.path.isfile(file_path):
            file_path = self.get_filename()
        if isinstance(file_path, str) and os.path.isfile(file_path):
            tree = eT.parse(file_path)
            root = tree.getroot()
            return root
        else:
            return False