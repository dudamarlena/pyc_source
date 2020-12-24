# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/Settings.py
# Compiled at: 2017-03-19 15:39:15
# Size of source mod 2**32: 2056 bytes
"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
import getopt, sys

class Settings:

    def __init__(self, find=None, site=None, verbose=False, min_chapters=0, azure_account_key=None, manga_xml_file=None, output_file=None):
        self.verbose = verbose
        self.find = find
        self.site = site
        self.min_chapters = min_chapters
        self.azure_account_key = azure_account_key
        self.manga_xml_file = manga_xml_file
        self.output_file = output_file

    def from_sys_parameters(self):
        argv = sys.argv[1:]
        example = 'MangaCrawler -f <find-argument> -s <site>'
        try:
            opts, args = getopt.getopt(argv, 'f:s:c:a:m:o:h:v', [
             'find=', 'site=', 'min-chapters=', 'azure-account-key=',
             'manga-xml-file=', 'output-file=', 'help'])
        except getopt.GetoptError:
            print(example)
            return False
        else:
            for opt, arg in opts:
                if opt == '-v':
                    self.verbose = True
                else:
                    if opt in ('-h', '--help'):
                        print(example)
                        return False
                    if opt in ('-f', '--find'):
                        self.find = arg
                    else:
                        if opt in ('-s', '--site'):
                            self.site = arg
                        else:
                            if opt in ('-c', '--min-chapters'):
                                try:
                                    self.min_chapters = int(arg)
                                except ValueError:
                                    self.min_chapters = 0

                            if opt in ('-a', '--azure-account-key'):
                                self.azure_account_key = arg
                            else:
                                if opt in ('-m', '--manga-xml-file'):
                                    self.manga_xml_file = arg
                                else:
                                    if opt in ('-o', '--output-file'):
                                        self.output_file = arg

            if self.find is False or self.site is False or self.find == 'updated' and not self.azure_account_key:
                print(example)
                return False
            else:
                print(self.azure_account_key)
                return True