# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\baker\storage.py
# Compiled at: 2018-11-12 15:41:18
# Size of source mod 2**32: 2360 bytes
import json
from os import makedirs, path
from itertools import chain

class Storage:
    __doc__ = '\n    Storage control of data in files\n    '

    @staticmethod
    def json(location, content=None):
        """
        Read and write json format from file
        """
        dir_path = location.rsplit('/', 1)[0]
        if content is not None:
            Storage.create_folders(dir_path)
            with open(location, 'w+') as (lines):
                json.dump(content, lines)
        else:
            data = {}
            if path.isfile(location):
                with open(location) as (lines):
                    data = json.load(lines)
            return data

    @staticmethod
    def parser(location, parser, write_mod=False, chain_items=None):
        """
        Read and write file using parser of ini data
        """
        try:
            if write_mod:
                with open(location, 'w+') as (lines):
                    parser.write(lines)
            else:
                with open(location) as (lines):
                    lines = chain(chain_items, lines)
                    parser.read_file(lines)
        except FileNotFoundError:
            raise FileNotFoundError("File not found at: '%s' Are you sure that it is available on this path?" % location)

    @staticmethod
    def file(location, content=None, mode=None):
        """
        Read and write raw values from file
        """
        if content:
            directory = path.split(location)[0]
            Storage.create_folders(directory)
            mode = mode or 'w+'
            with open(location, mode) as (f):
                f.write(content)
        try:
            with open(location) as (f):
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError("File not found at: '%s' Are you sure that it is available on this path?" % location)

    @staticmethod
    def create_folders(directory):
        """
        Create structure of folders if it not exists
        """
        if not path.exists(directory):
            makedirs(directory, mode=(int('0755', 8)))