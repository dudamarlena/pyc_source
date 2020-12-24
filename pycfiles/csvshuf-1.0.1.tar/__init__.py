# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ae/bzr/csvsee/tests/__init__.py
# Compiled at: 2010-09-14 13:11:28
__doc__ = 'Setup and teardown methods for csvsee unit tests.\n'
import os, sys, tempfile, shutil
data_dir = os.path.join(os.path.dirname(__file__), 'data')
temp_dir = tempfile.mkdtemp(prefix='csvsee_test')

def setup():
    """Package-level setup.
    """
    sys.path.append(os.path.abspath('..'))


def teardown():
    """Package-level teardown.
    """
    shutil.rmtree(temp_dir)


def write_tempfile(data):
    """Write a temporary file containing the given ``data`` string,
    and return the filename. Leading whitespace in each line is
    automatically stripped. Caller is responsible for deleting the
    temporary file after using it.
    """
    outfile = tempfile.NamedTemporaryFile(dir=temp_dir, delete=False)
    for line in data.splitlines():
        outfile.write(line.lstrip() + '\n')

    outfile.close()
    return outfile.name


def temp_filename(ext=''):
    """Get a temporary filename with an optional extension.
    """
    temp = tempfile.NamedTemporaryFile(dir=temp_dir, delete=False)
    temp.close()
    if ext:
        return temp.name + '.' + ext.lstrip('.')
    else:
        return temp.name