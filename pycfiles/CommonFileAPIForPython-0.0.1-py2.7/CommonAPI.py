# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/CommonFileAPI/CommonAPI.py
# Compiled at: 2014-10-19 07:00:31
import hashlib, os, subprocess, ntpath, json

def walk_directory(location_to_walk, function_to_run_on_each_file):
    for root, dirs, filenames in os.walk(location_to_walk):
        for f in filenames:
            function_to_run_on_each_file(os.path.join(root, f))


def get_contents_of_file(filename):
    file_contents = open(filename, 'r').read()
    return file_contents


def get_filename_of_path(path):
    return ntpath.basename(path)


def write_string_to_file(string, file_name):
    fo = open(file_name, 'w+')
    fo.write(string)
    fo.close()


def get_command_output(command_to_run):
    result = subprocess.check_output(command_to_run, shell=True)
    return result


def get_hash(content):
    ochash = hashlib.sha256()
    ochash.update(content)
    return ochash.hexdigest()


def get_immediate_subdirectories(dir):
    return [ name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))
           ]


def json_file_to_object(file_path):
    json_data = open(file_path).read()
    data = json.loads(json_data)
    return data