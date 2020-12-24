# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/file_utils.py
# Compiled at: 2014-12-28 23:18:17
import os, shutil, subprocess as sp, logging, re, hashlib
logger = logging.getLogger('file_utils')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
BACKUP_TYPE_SEQUENCE = 1
BACKUP_TYPE_SHA1 = 2
BACKUP_TYPE_NONE = 3
backup_type_default = BACKUP_TYPE_SEQUENCE
backup_types = [BACKUP_TYPE_SEQUENCE, BACKUP_TYPE_SHA1, BACKUP_TYPE_NONE]

def checked_link(point_to, link_name, force=False, backup_type=backup_type_default):
    if backup_type not in backup_types:
        raise ValueError("backup_type '%s' isn't one of %s" % (backup_type, backup_types))
    target_parent = os.path.abspath(os.path.join(link_name, '..'))
    if not os.path.lexists(target_parent):
        os.makedirs(target_parent)
    if not os.path.lexists(link_name):
        os.symlink(point_to, link_name)
        return True
    if not force:
        return False
    if os.path.islink(link_name) and os.path.realpath(link_name) == point_to:
        return True
    if os.path.exists(link_name):
        if backup_type != BACKUP_TYPE_NONE:
            backup_file(link_name, backup_type=backup_type)
        elif not os.path.isdir(link_name) or os.path.islink(link_name):
            os.remove(link_name)
        else:
            shutil.rmtree(link_name)
    os.symlink(point_to, link_name)
    return True


def write_file(file0, what):
    if os.path.isdir(file0):
        raise ValueError('file %s is a directory' % file0)
    if lazy_newline and not what.endswith('\n'):
        what = '%s\n' % what
    file_obj = open(file0, 'w')
    file_obj.write(what)
    file_obj.flush()
    file_obj.close()


def append_file(file0, what, lazy_newline=True):
    if os.path.isdir(file0):
        raise ValueError('file %s is a directory' % file0)
    if lazy_newline and not what.endswith('\n'):
        what = '%s\n' % what
    file_obj = open(file0, 'a')
    file_obj.write(what)
    file_obj.flush()
    file_obj.close()


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        return False
    if not os.path.isdir(dir_path):
        raise ValueError('dir_path has to point to a directory')
    if len(os.listdir(dir_path)) == 0:
        logger.debug('%s is empty' % dir_path)
        return False
    return True


def create_dir(dir_path, allow_content):
    if os.path.exists(dir_path):
        if os.path.isdir(dir_path):
            if len(os.listdir(dir_path)) > 0 and not allow_content:
                raise RuntimeError('%s exists and has content, a directory is supposed to be created. Remove or move the content of the directory' % dir_path)
        else:
            raise RuntimeError('%s exists, a directory is supposed to be created. Remove or move the file' % dir_path)
    else:
        os.makedirs(dir_path)


def check_file(file_path, md5sum):
    if not os.path.exists(file_path):
        return False
    if not os.path.isfile(file_path):
        raise ValueError('file_path has to point to a file')
    retrieved_md5sum = retrieve_hash(file_path)
    if not retrieved_md5sum == md5sum:
        logger.debug('%s has md5 sum %s instead of %s' % (file_path, retrieved_md5sum, md5sum))
        return False
    return True


def retrieve_hash(file_path, hasher='md5', blocksize=65536):
    afile = open(file_path, 'r')
    hasher_instance = hashlib.new(hasher)
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher_instance.update(buf)
        buf = afile.read(blocksize)

    afile.close()
    ret_value = hasher_instance.hexdigest()
    return ret_value


def retrieve_hash_recursive(dir_path, hasher='md5', blocksize=65536):
    logger.debug("generating recursive hash for '%s'" % (dir_path,))
    if not os.path.isdir(dir_path):
        raise ValueError("dir_path '%s' isn't a directory" % (dir_path,))
    ret_value = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            current_file_path = os.path.join(dirpath, filename)
            hasher_instance = hashlib.new(hasher)
            hasher_instance.update(current_file_path)
            ret_value = ret_value ^ int(hasher_instance.hexdigest(), base=16)
            ret_value = ret_value ^ int(retrieve_hash(current_file_path, hasher=hasher, blocksize=65536), base=16)

        for dirname in dirnames:
            current_dir_path = os.path.join(dirpath, dirname)
            hasher_instance = hashlib.new(hasher)
            hasher_instance.update(current_dir_path)
            ret_value = ret_value ^ int(hasher_instance.hexdigest(), base=16)

    return str(ret_value)


def backup_file(file_path, backup_type=backup_type_default, follow_links=False):
    if not os.path.exists(file_path):
        raise ValueError("file_path '%s' doesn't exist, backup_file only accepts an existing file or directory as argument" % (file_path,))
    if backup_type == BACKUP_TYPE_SHA1:
        if os.path.isdir(file_path):
            file_sha1 = retrieve_hash_recursive(file_path, hasher='sha1')
        else:
            file_sha1 = retrieve_hash(file_path, hasher='sha1')
        file_backup_path = '%s.bk-%s' % (file_path, file_sha1)
        if not os.path.exists(file_backup_path):
            os.rename(os.path.realpath(file_path), file_backup_path)
    elif backup_type == BACKUP_TYPE_SEQUENCE:
        renamepostfix = '.bk'
        renamepostfixcount = 0
        backup_file = file_path
        if follow_links:
            backup_file = os.path.realpath(file_path)
        if os.path.lexists(backup_file):
            renamepostfix = '.bk%d' % renamepostfixcount
            renamepostfixcount += 1
        while os.path.lexists(backup_file + renamepostfix):
            renamepostfix = '.bk%d' % renamepostfixcount
            renamepostfixcount += 1

        target_backup_path = backup_file + renamepostfix
        logger.debug('backing up %s to %s' % (backup_file, target_backup_path))
        os.rename(backup_file, target_backup_path)
    else:
        raise ValueError("backup_type '%s' isn't supported" % (backup_type,))