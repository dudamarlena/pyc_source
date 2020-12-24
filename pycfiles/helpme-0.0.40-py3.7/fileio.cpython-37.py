# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/utils/fileio.py
# Compiled at: 2019-12-09 18:49:03
# Size of source mod 2**32: 4119 bytes
"""

Copyright (C) 2018-2020 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import configparser, errno, os, pwd, re, tempfile, json, io, sys
from helpme.logger import bot

def get_userhome():
    """get the user home based on the effective uid
    """
    return pwd.getpwuid(os.getuid())[5]


def mkdir_p(path):
    """mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        try:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                bot.error('Error creating path %s, exiting.' % path)
                sys.exit(1)
        finally:
            e = None
            del e


def write_config(filename, config, mode='w'):
    """use configparser to write a config object to filename
    """
    with open(filename, mode) as (filey):
        config.write(filey)
    return filename


def read_config(filename):
    """use configparser to write a config object to filename
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def generate_temporary_file(folder='/tmp', prefix='helpme', ext='json'):
    """write a temporary file, in base directory with a particular extension.
      
       Parameters
       ==========
       folder: the base directory to write in. 
       prefix: the prefix to use
       ext: the extension to use.

    """
    tmp = next(tempfile._get_candidate_names())
    return '%s/%s.%s.%s' % (folder, prefix, tmp, ext)


def copyfile(source, destination, force=True):
    """copy a file from a source to its destination.
    """
    if os.path.exists(destination):
        if force is True:
            os.remove(destination)
    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode='w'):
    """write_file will open a file, "filename" and write content, "content"
    and properly close the file
    """
    with open(filename, mode) as (filey):
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode='w', print_pretty=True):
    """write_json will (optionally,pretty print) a json object to file
    :param json_obj: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting
    """
    with open(filename, mode) as (filey):
        if print_pretty:
            filey.writelines(print_json(json_obj))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def print_json(json_obj):
    """ just dump the json in a "pretty print" format
    """
    return json.dumps(json_obj, indent=4, separators=(',', ': '))


def read_file(filename, mode='r', readlines=True):
    """write_file will open a file, "filename" and write content, "content"
    and properly close the file
    """
    with open(filename, mode) as (filey):
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode='r'):
    """read_json reads in a json file and returns
    the data structure as dict.
    """
    with open(filename, mode) as (filey):
        data = json.load(filey)
    return data