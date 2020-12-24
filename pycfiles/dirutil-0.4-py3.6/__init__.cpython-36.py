# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dirutil\__init__.py
# Compiled at: 2018-12-25 04:35:32
# Size of source mod 2**32: 9179 bytes
"""
"""
__author__ = 'Dmitri Dolzhenko'
__email__ = 'd.dolzhenko@gmail.com'
import os, stat, shutil, tempfile

class Error:
    pass


def abspath(path):
    return os.path.abspath(path)


def cwd():
    return os.getcwd()


def chdir(path):
    if path:
        os.chdir(path)
    return path


def home():
    return os.path.expanduser('~')


if os.name == 'nt':
    if os.environ['USERPROFILE']:

        def home():
            return os.environ['USERPROFILE']


def split_path(path):
    os.path.normpath(path).split(os.sep)


def exists(path):
    return os.path.exists(path)


def isdir(path):
    return os.path.isdir(path)


def isfile(path):
    return os.path.isfile(path)


def touch(path):
    with open(path, 'w'):
        pass


def file_write(path, data, mode=''):
    with open(path, 'w' + mode) as (f):
        f.write(data)


def file_append(path, data, mode=''):
    with open(path, 'a' + mode) as (f):
        f.write(data)


def rmfile(path):
    os.remove(path)


def safe_rmfile(path):
    if exists(path):
        os.remove(path)


def mkdir(path):
    os.mkdir(path)
    return path


def safe_mkdir(path):
    if not exists(path):
        mkdir(path)
    return path


def force_mkdir(path):
    safe_rmdir(path)
    return mkdir(path)


def safe_mktree(path):
    """Creates not only last folder in path but all
    for mktree('1/2/3')
    will create 1/
                1/2
                1/2/3
    """
    folders = split_path(path)
    for i, folder in enumerate(folders):
        f = os.sep.join(folders[:i + 1])
        safe_mkdir(f)

    return path


def rmdir(path):
    """Forced directory remove"""

    def onerror(func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    shutil.rmtree(path, onerror=onerror)


def safe_rmdir(path):
    if exists(path):
        rmdir(path)


def remove(path):
    if not exists(path):
        raise Error('object "{}" not found'.format(path))
    else:
        if isfile(path):
            rmfile(path)
        else:
            if isdir(path):
                rmdir(path)
            else:
                raise Error('unknown object type "{}"'.format(path))


def safe_remove(path):
    if exists(path):
        remove(path)


def create_structure(structure, path=''):
    """Creates folder structure in path according dict from parameters
    example:

    structure = {
        folder_l0_1: {                          #this is a folder because dict inside
            folder_l1_1 : {},                   #this is a empty folder inside upper folder
            file_l1_1.txt: 'Hello world!',      #this is file with contents 'Hello world'
            file_l1_2.ext: open('filename.txt') #this will create a file with contents from file stream
        },
        file_l0_1: some text inside # file on top
    }

    create_structure(structure)
    """
    assert isinstance(structure, dict)
    with work_dir(path):
        for name, data in structure.items():
            assert data is not None
            if isinstance(data, dict):
                safe_mkdir(name)
                create_structure(data, path=name)
            else:
                if isinstance(data, str):
                    file_write(name, data)
                else:
                    file_write(name, (data.read()), mode=('b' if 'b' in data.mode else ''))


class work_dir(object):
    __doc__ = "change working dir within 'with' context\n    Usage:\n        with work_dir('otherdir/foo/'):\n            print(os.getcwd())\n        print(os.getcwd()) # oldone\n    "

    def __init__(self, directory):
        self._previous = None
        self._wanted = os.path.abspath(directory)

    def __enter__(self):
        self._previous = os.getcwd()
        chdir(self._wanted)
        return self

    def __exit__(self, *args):
        chdir(self._previous)
        self._previous = None

    @property
    def current(self):
        return os.getcwd()

    @property
    def previous(self):
        return self._previous

    def __repr__(self):
        return self.current


class work_mkdir(work_dir):

    def __init__(self, path):
        super().__init__(mkdir(path))


class work_safe_mkdir(work_dir):

    def __init__(self, path):
        super().__init__(safe_mkdir(path))


class work_force_mkdir(work_dir):

    def __init__(self, path):
        super().__init__(force_mkdir(path))


class work_tempdir(work_dir):

    def __init__(self):
        super().__init__(tempfile.mkdtemp())

    def __exit__(self, *args):
        tmp = self.current
        super().__exit__()
        rmdir(tmp)


import unittest

class TestCase(unittest.TestCase):

    def test_1(self):
        import yaml, json
        with work_force_mkdir('1-test1'):
            with work_mkdir('.jacis'):
                with work_mkdir('available'):
                    touch('list.yml')
                with work_mkdir('installed'):
                    touch('list.yml')
                with open('config.yml', 'w') as (f):
                    f.write(json.dumps([1, 2, 3, 4]))
        with work_force_mkdir('1-test2'):
            struct = {'.jacis': {'available':{'list.yml': ''}, 
                        'installed':{'list.yml': ''}, 
                        'config.yml':json.dumps([1, 2, 3, 4])}}
            create_structure(struct)
        with work_force_mkdir('1-test3'):
            yml = '\n            .jacis:\n                available:\n                    list.yml: ""\n                installed:\n                    list.yml: ""\n                config.yml: "[1,2,3,4]"\n            '
            create_structure(yaml.load(yml))
        for x in ('1-test1', '1-test2', '1-test3'):
            rmdir(x)

        print(os.getcwd())
        print('-' * 100)
        with work_tempdir():
            print('path1: ', os.getcwd())
        with work_tempdir():
            print('path2: ', os.getcwd())
        print('-' * 100)
        print(os.getcwd())