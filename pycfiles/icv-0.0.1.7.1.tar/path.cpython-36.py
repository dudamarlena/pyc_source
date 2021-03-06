# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/path.py
# Compiled at: 2019-11-21 06:16:37
# Size of source mod 2**32: 3391 bytes
import shutil, os, six
from .itis import is_seq, is_file, is_dir

def mkfile(filepath, content=''):
    if not is_dir(os.path.dirname(filepath)):
        mkdir(os.path.dirname(filepath))
    with open(filepath, 'w') as (f):
        f.write(content)


def mkdir(dir_name, mode=511):
    if six.PY3:
        os.makedirs(dir_name, mode=mode, exist_ok=True)
    elif not os.path.isdir(dir_name):
        os.makedirs(dir_name, mode=mode)


def mkdir_force(dir_name, subdirs=None, mode=511):
    if not subdirs is None:
        if not is_seq(subdirs):
            raise AssertionError('param subdirs should be none or a sequence')
    else:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        mkdir(dir_name, mode)
        if subdirs is not None:
            for subdir in subdirs:
                mkdir(os.path.join(dir_name, subdir), mode)


def reset_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)


def fcopy(source_path, dist_path, rename=True):
    """拷贝文件或文件列表到目标目录中
    :param source_path: 源文件或源文件列表
    :param dist_path: 目标目录或目标文件
    :param rename: 是否重命名
    :return: 目标文件路径
    """
    if is_seq(source_path):
        source_path = list(source_path)
        dist_file_list = []
        for source_file in source_path:
            dist_file_list.extend(fcopy(source_file, dist_path, rename))

        return dist_file_list
    else:
        if not not (is_dir(source_path) and is_file(dist_path)):
            raise AssertionError("Can't copy dir to file")
        else:
            if not is_file(source_path):
                if not is_dir(source_path):
                    return
            if is_file(source_path):
                dist_path = os.path.join(dist_path, os.path.basename(source_path)) if is_dir(dist_path) else dist_path
                i = 0
                while is_file(dist_path) and rename:
                    i += 1
                    dist_name, dist_ext = os.path.basename(dist_path).rsplit('.', 1)
                    dist_path = os.path.join(os.path.dirname(dist_path), '%s_%d.%s' % (dist_name, i, dist_ext))

                shutil.copyfile(source_path, dist_path)
                return [dist_path]
        dist_file_list = []
        for f in os.listdir(source_path):
            source_file = os.path.join(source_path, f)
            dist_file_list.extend(fcopy(source_file, dist_path, rename))

        return dist_file_list


def list_from_file(filename, prefix='', offset=0, max_num=0):
    """Load a text file and parse the content as a list of strings.

    Args:
        filename (str): Filename.
        prefix (str): The prefix to be inserted to the begining of each item.
        offset (int): The offset of lines.
        max_num (int): The maximum number of lines to be read,
            zeros and negatives mean no limitation.

    Returns:
        list[str]: A list of strings.
    """
    cnt = 0
    item_list = []
    with open(filename, 'r') as (f):
        for _ in range(offset):
            f.readline()

        for line in f:
            if max_num > 0:
                if cnt >= max_num:
                    break
            item_list.append(prefix + line.rstrip('\n'))
            cnt += 1

    return item_list


def list_to_file(seq, filename, prefix='', append=False):
    seq = [prefix + str(s) for s in seq]
    mode = 'a' if (is_file(filename) and append) else 'w'
    with open(filename, mode) as (f):
        f.write('\n'.join(seq))
    return filename