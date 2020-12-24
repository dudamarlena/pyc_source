# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/shortfuse_test/integration.py
# Compiled at: 2019-03-06 13:38:37
# Size of source mod 2**32: 10260 bytes
import logging, os, math, time, traceback
from stat import S_IFREG, S_IFMT, S_IFDIR
from shortfuse_test.fixtures import build_random_string
TMP_DIR_PREFIX = 'int_test_dir_'
TMP_FILE_PREFIX = 'int_test_file_'
LOGGER = logging.getLogger('shortfuse_test.integration')

def failable_test(test_func):

    def wrapper_test(node_path, fuse_os, failure_expected=False, check_parent=False, **kwargs):
        LOGGER.debug('Gathering node stats for potential failure. Include parent = %s' % check_parent)
        parent_path = os.path.dirname(node_path)
        parent_stats = fuse_os.stat(parent_path) if check_parent else None
        node_stats = fuse_os.stat(node_path)
        try:
            test_func(node_path, fuse_os, node_stats=node_stats, **kwargs)
        except Exception as e:
            try:
                if failure_expected:
                    u_node_stats = fuse_os.stat(node_path)
                    u_parent_stats = fuse_os.stat(parent_path)
                    assert node_stats == u_node_stats
                    if check_parent:
                        assert parent_stats == u_parent_stats
                traceback.print_exc()
                raise e
            finally:
                e = None
                del e

    return wrapper_test


def retry_assertion(expression, timeout=5, polling_freq=0.01):
    num_tries = 0
    while True:
        try:
            assert expression
            break
        except AssertionError as e:
            try:
                wait_for = polling_freq * math.pow(num_tries)
                if wait_for >= timeout:
                    raise AssertionError(e)
                time.sleep(wait_for)
                num_tries += 1
            finally:
                e = None
                del e


def parent_stat_after_mod_test(stats, new_stats, diff=1):
    retry_assertion(lambda : stats.st_nlink + diff == new_stats.st_nlink)
    assert int(stats.st_atime) <= int(new_stats.st_atime)
    assert int(stats.st_mtime) <= int(new_stats.st_mtime)
    assert int(stats.st_ctime) == int(new_stats.st_ctime)


def chmod_test(node_path, fuse_os, noop=False):
    node_stats = fuse_os.stat(node_path)
    fuse_os.chmod(node_path, 73)
    if noop and not node_stats == fuse_os.stat(node_path):
        raise AssertionError
    else:
        stat_test((fuse_os.stat(node_path)),
          mode=(73 if not noop else node_stats.st_mode & 511),
          nlink=(node_stats.st_nlink),
          node_type=(S_IFMT(node_stats.st_mode)))
    fuse_os.chmod(node_path, node_stats.st_mode & 511)


def chown_test(node_path, fuse_os, uid, gid, noop=False):
    node_stats = fuse_os.stat(node_path)
    fuse_os.chown(node_path, uid, gid)
    if noop and not node_stats == fuse_os.stat(node_path):
        raise AssertionError
    else:
        stat_test((fuse_os.stat(node_path)),
          uid=uid,
          gid=gid,
          mode=(node_stats.st_mode & 511),
          nlink=(node_stats.st_nlink),
          node_type=(S_IFMT(node_stats.st_mode)))
    fuse_os.chown(node_path, os.getuid(), os.getgid())


@failable_test
def create_test(dir_path, fuse_os, node_stats=None):
    parent_stats = node_stats
    file_name = TMP_FILE_PREFIX + build_random_string(10)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'w') as (f):
        assert 0 <= f.fileno()
    stat_test((fuse_os.stat(file_path)), mode=420)
    parent_stat_after_mod_test(parent_stats, fuse_os.stat(dir_path))
    assert file_name in fuse_os.listdir(dir_path)


@failable_test
def mkdir_test(dir_path, fuse_os, node_stats=None, mode=457, nlink=2):
    dir_stat = node_stats
    new_dir_name = TMP_DIR_PREFIX + build_random_string(10)
    new_dir_path = os.path.join(dir_path, new_dir_name)
    fuse_os.mkdir(new_dir_path, 457)
    stat_test((fuse_os.stat(new_dir_path)), node_type=S_IFDIR, mode=mode, nlink=nlink)
    parent_stat_after_mod_test(dir_stat, fuse_os.stat(dir_path))
    assert new_dir_name in fuse_os.listdir(dir_path)


def read_test(file_path, fuse_os, file_content):
    with open(file_path, 'r') as (file_handle):
        assert file_content == file_handle.read()
        file_handle.seek(5)
        assert file_content[5:] == file_handle.read()
        file_handle.seek(5)
        assert file_content[5:35] == file_handle.read(30)
        assert file_content[35:] == file_handle.read()
        assert '' == file_handle.read()


@failable_test
def rmdir_test(dir_path, fuse_os, node_stats=None):
    dir_name = os.path.basename(dir_path)
    parent_path = os.path.dirname(dir_path)
    parent_stats = fuse_os.stat(parent_path)
    fuse_os.rmdir(dir_path)
    parent_stat_after_mod_test(parent_stats, (fuse_os.stat(parent_path)), diff=(-1))
    assert dir_name not in fuse_os.listdir(parent_path)


def stat_test(stats, node_type=S_IFREG, mode=511, size=0, nlink=1, uid=os.getuid(), gid=os.getgid()):
    retry_assertion(lambda : node_type == S_IFMT(stats.st_mode))
    retry_assertion(lambda : mode == stats.st_mode & 511)
    assert uid == stats.st_uid
    assert gid == stats.st_gid
    assert nlink == stats.st_nlink
    if node_type is S_IFREG:
        assert size == stats.st_size


@failable_test
def symlink_test(dir_path, fuse_os, target, node_stats=None):
    link_name = build_random_string(10)
    link_path = os.path.join(dir_path, link_name)
    fuse_os.symlink(target, link_path)
    raise NotImplemented


def truncate_test(file_path, fuse_os):
    file_content = build_random_string(50)
    with open(file_path, 'w+') as (file_handle):
        file_handle.write(file_content)
    with open(file_path, 'r+') as (file_handle):
        file_handle.truncate(70)
        file_handle.seek(0)
        assert file_content + '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' == file_handle.read()
        stat_test((fuse_os.stat(file_handle.name)),
          mode=420,
          node_type=S_IFREG,
          size=70)
        file_handle.truncate(20)
        file_handle.seek(0)
        assert file_content[0:20] == file_handle.read()
        stat_test((fuse_os.stat(file_handle.name)),
          mode=420,
          node_type=S_IFREG,
          size=20)
        file_handle.truncate(0)
        file_handle.seek(0)
        assert '' == file_handle.read()
        stat_test((fuse_os.stat(file_handle.name)),
          mode=420,
          node_type=S_IFREG,
          size=0)


@failable_test
def unlink_test(file_path, fuse_os, node_stats=None):
    file_name = os.path.basename(file_path)
    parent_path = os.path.dirname(file_path)
    parent_stats = fuse_os.stat(parent_path)
    fuse_os.unlink(file_path)
    parent_stat_after_mod_test(parent_stats, (fuse_os.stat(parent_path)), diff=(-1))
    assert file_name not in fuse_os.listdir(parent_path)


def utime_test(node_path, times, fuse_os, noop=True):
    node_stats = fuse_os.stat(node_path)
    fuse_os.utime(node_path, times)
    if noop and not node_stats == fuse_os.stat(node_path):
        raise AssertionError
    else:
        raise NotImplemented


def write_test(file_path, fuse_os):
    with open(file_path, 'w+') as (file_handle):
        file_content = build_random_string(50)
        file_content_1 = build_random_string(50)
        file_handle.write(file_content)
        file_handle.seek(0)
        assert file_content == file_handle.read()
        stat_test((fuse_os.stat(file_handle.name)),
          mode=420,
          node_type=S_IFREG,
          size=50)
        file_handle.seek(5)
        file_handle.write(file_content_1[5:15])
        file_handle.seek(0)
        assert file_content[0:5] + file_content_1[5:15] + file_content[15:] == file_handle.read()
        stat_test((fuse_os.stat(file_handle.name)),
          mode=420,
          node_type=S_IFREG,
          size=50)
        file_handle.seek(45)
        file_handle.write(file_content_1[40:])
        file_handle.seek(0)
        assert file_content[0:5] + file_content_1[5:15] + file_content[15:45] + file_content_1[40:] == file_handle.read()
        stat_test((fuse_os.stat(file_handle.name)),
          mode=420,
          node_type=S_IFREG,
          size=55)


def get_xattr_test(node_path, fuse_os, noop=False):
    node_stats = fuse_os.stat(node_path)
    key = build_random_string(10)
    assert None == fuse_os.get_xattr(node_path, key)
    value = build_random_string(10)
    fuse_os.set_xattr(node_path, key, value)
    if not node_stats == fuse_os.stat(node_path):
        raise AssertionError
    elif noop and not None == fuse_os.get_xattr(node_path, key):
        raise AssertionError
    else:
        assert value == fuse_os.get_xattr(node_path, key)


def get_xattrs_test(node_path, fuse_os, noop=False):
    node_stats = fuse_os.stat(node_path)
    key = build_random_string(10)
    if not node_stats == fuse_os.stat(node_path):
        raise AssertionError
    else:
        attrs = fuse_os.get_xattrs(node_path)
        if not 0 <= len(attrs):
            raise AssertionError
        else:
            value = build_random_string(10)
            fuse_os.set_xattr(node_path, key, value)
            assert node_stats == fuse_os.stat(node_path)
            u_attrs = fuse_os.get_xattrs(node_path)
            if noop:
                assert len(attrs) == len(u_attrs)
                if not None == u_attrs.get(key):
                    raise AssertionError
            else:
                assert len(attrs) + 1 == len(u_attrs)
                assert value == u_attrs.get(key)


def set_xattr_test(node_path, fuse_os, noop=False):
    get_xattr_test(node_path, fuse_os, noop)


def delete_xattr_test(node_path, fuse_os, noop=False):
    node_stats = fuse_os.stat(node_path)
    key = build_random_string(10)
    if not None == fuse_os.get_xattr(node_path, key):
        raise AssertionError
    else:
        value = build_random_string(10)
        fuse_os.set_xattr(node_path, key, value)
        if noop and not None == fuse_os.get_xattr(node_path, key):
            raise AssertionError
        else:
            assert value == fuse_os.get_xattr(node_path, key)
    fuse_os.delete_xattr(node_path, key)
    u_node_stats = fuse_os.stat(node_path)
    assert node_stats == u_node_stats
    assert None == fuse_os.get_xattr(node_path, key)