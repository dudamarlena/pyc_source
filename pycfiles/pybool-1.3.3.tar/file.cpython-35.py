# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/file.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1011 bytes
import uuid, os, re
from fabric.operations import get as get_file, put as upload_file

def insert_line_in_file_after_regex(path, line, after_regex, use_sudo=False):
    """ inserts a line in the middle of a file """
    tmpfile = str(uuid.uuid4())
    get_file(path, tmpfile, use_sudo=use_sudo)
    with open(tmpfile) as (f):
        original = f.read()
    has_it_changed = False
    if line not in original:
        has_it_changed = True
        outfile = str(uuid.uuid4())
        with open(outfile, 'w') as (output):
            for l in original.split('\n'):
                output.write(l + '\n')
                if re.match(after_regex, l) is not None:
                    output.write(line + '\n')

        upload_file(local_path=outfile, remote_path=path, use_sudo=use_sudo)
        os.unlink(outfile)
    os.unlink(tmpfile)
    return has_it_changed