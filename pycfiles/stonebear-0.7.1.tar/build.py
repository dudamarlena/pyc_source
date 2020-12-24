# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cb/Projekter/stonebear/stonebear/build.py
# Compiled at: 2011-09-06 18:41:31
import os, shutil, fnmatch, subprocess
from clean import clean

def match_files_to_filter(dir, files, filter, do):
    """
    pass all files in dir that matches filter to do
    """
    for fl in filter:
        for fn in fnmatch.filter(files, fl):
            do(dir + '/' + fn)


def walk_dir_n_do(dir, filter, do):
    """ 
    call [do] on all files inside dir, call [walk_dir_n_dor] on directories
    """
    for root, dirs, files in os.walk(dir):
        match_files_to_filter(root, files, filter, do)
        for dir in dirs:
            walk_dir_n_do(dir, filter, do)


def enable_dir_nesting(dir_str):
    """
    check if [dir_str] represents a nested directory or file, and if so, create
    the nested directories
    """
    tree = []
    path = os.getcwd()
    for t in dir_str.split('/'):
        if t:
            tree.append(t)

    del tree[-1]
    for t in tree:
        n_path = path + '/' + t
        if not os.path.exists(n_path):
            try:
                os.mkdir(n_path)
            except OSError:
                raise
                sys.exit(1)

        path = n_path


def copy(input, output, remove_fn, copy_fn):
    """
    provides a copy-interface for file operations
    arguments:
        input = input file or directory
        output = output file or directory
        remove_fn = lambda function that takes one argument [output]
            (intentionally to remove this)
        copy_fn = lambda function that takes two arguments [input] and [output]
            (intentionally to copy input to output)
    """
    enable_dir_nesting(output)
    if os.path.exists(output):
        try:
            remove_fn(output)
        except OSError:
            raise
            sys.exit(1)

    try:
        copy_fn(input, output)
    except OSError:
        raise
        sys.exit(1)


def build(args, config):
    """
    will run [prebuild] commands, copy [input] to [output], remove files matching
    [remove_from_output_dirs] from directories in [output], run compilers on
    matching files in [output] and then run [postbuild] commands
    dirs in [output]
    """
    subprocess.call(config['prebuild'], shell=True)
    cwd = os.getcwd() + '/'
    input = config['input']
    output = config['output']
    remove_from_output_dirs = config['remove_from_output_dirs']
    files = []
    for i, obj in enumerate(input):
        is_dir = True if os.path.isdir(cwd + obj) else False
        if obj != output[i]:
            if is_dir:
                copy(obj, output[i], lambda o: shutil.rmtree(o), lambda i, o: shutil.copytree(i, o))
            else:
                copy(obj, output[i], lambda o: os.remove(o), lambda i, o: shutil.copyfile(i, o))
            obj = output[i]
        if is_dir:
            for compiler in config['compilers']:
                walk_dir_n_do(obj, compiler[0], lambda f: subprocess.call(compiler[1].format(file=f), shell=True))

            walk_dir_n_do(obj, remove_from_output_dirs, lambda f: os.remove(f))
        else:
            files.append(obj)

    for compiler in config['compilers']:
        match_files_to_filter(cwd, files, compiler[0], lambda f: subprocess.call(compiler[1].format(file=f), shell=True))

    subprocess.call(config['postbuild'], shell=True)