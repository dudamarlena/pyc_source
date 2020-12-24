# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattpease/DevTools/Workspaces/flask-spawn/flaskspawn/snippets/file_routines.py
# Compiled at: 2015-07-21 18:35:49
import re

def copy_contents_of_file(source_file, destination_file):
    with open(source_file) as (f):
        source_contents = f.read()
    with open(destination_file, 'w') as (f):
        f.write(source_contents)


def append_to_file(file_path, source_file):
    with open(source_file) as (f):
        source_contents = f.read()
    with open(file_path, 'a') as (f):
        f.write(source_contents)


def append_text_to_file(file_path, source_text):
    with open(file_path, 'a') as (f):
        f.write(source_text)


def add_text_to_file_after_pattern(text, pattern, destination_file):
    with open(destination_file, 'r+') as (f):
        contents = f.readlines()
        line_index = None
        for idx, line in enumerate(contents):
            result = re.search(pattern, line)
            if result:
                line_index = idx
                break

        if line_index:
            contents.insert(line_index + 1, text)
            contents = ('').join(contents)
            f.seek(0)
            f.write(contents)
            f.truncate()
    return


def add_text_to_top_of_file(destination_file, text):
    with open(destination_file, 'r+') as (f):
        contents = f.readlines()
        contents.insert(0, text)
        contents = ('').join(contents)
        f.seek(0)
        f.write(contents)
        f.truncate()