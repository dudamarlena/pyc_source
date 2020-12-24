# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfs/file_system.py
# Compiled at: 2018-12-26 02:58:12
# Size of source mod 2**32: 7553 bytes
import collections, functools, json, pickle, os
import sfs.exceptions as exceptions
import sfs.helper as helper

class AlreadyExists(exceptions.SFSException):
    __doc__ = 'Exception class for attempts to overwrite an existing resource'


class DoesNotExist(exceptions.SFSException):
    __doc__ = 'Exception class for attempts to access unavailable resources'


SeparatedNodes = collections.namedtuple('SeparatedNodes', 'files dirs links')

@helper.frozen
@helper.has_cached_methods
class FSNode:
    __doc__ = "\n    An adaptor class for access to a file, symlink or directory\n    It is essentially a wrapper around an instance of DirEntry obtained from the iterator returned by by 'os.scandir'\n    "

    class NodeStats:
        __doc__ = 'Persisted metadata of a node'

        def __init__(self, ctime=None, size=0, dest=None):
            self.ctime = ctime
            self.size = size
            self.dest = dest

        def __repr__(self):
            return '{}.{}(ctime={}, size={}, dest={})'.format(FSNode.__name__, FSNode.NodeStats.__name__, self.ctime, self.size, self.dest)

    def __init__(self, dir_entry):
        self.dir_entry = dir_entry

    @property
    def name(self):
        return self.dir_entry.name

    @property
    def path(self):
        return self.dir_entry.path

    @property
    @helper.cached_method()
    def is_dir(self):
        return self.dir_entry.is_dir(follow_symlinks=False)

    @property
    @helper.cached_method()
    def is_file(self):
        return self.dir_entry.is_file(follow_symlinks=False)

    @property
    @helper.cached_method()
    def is_symlink(self):
        return self.dir_entry.is_symlink()

    @property
    @helper.cached_method()
    def stat(self):
        raw_stats = self.dir_entry.stat(follow_symlinks=False)
        return FSNode.NodeStats(ctime=(raw_stats.st_ctime),
          size=(raw_stats.st_size),
          dest=(os.readlink(self.path) if self.is_symlink else None))


def scan_dir(path):
    """Scan a directory with 'os.scandir' converting the iterator of DirEntry to FSNode"""
    return map(lambda dir_entry: FSNode(dir_entry), os.scandir(path))


def separate_nodes(nodes):
    """
    Separates a list of FSNode instances as files, directories and symlinks
    :param nodes: A list of FSNode instances to be separated
    :return: A named tuple of type SeparatedNodes
    """
    separated = SeparatedNodes([], [], [])
    for node in nodes:
        if node.is_dir:
            add_to = separated.dirs
        else:
            if node.is_file:
                add_to = separated.files
            else:
                add_to = separated.links
        add_to.append(node)

    return separated


def walk_bfs(dir_path):
    """
    Recursively Generates all the contents of a directory in Breadth First Order
    :param dir_path: Base path for which to enumerate contents
    :return: Contents of directory (dir_path, file_nodes, directory_nodes, symlink_nodes)
    """
    pending = collections.deque([dir_path])
    while len(pending) > 0:
        curr_dir = pending.popleft()
        nodes = scan_dir(curr_dir)
        separated = separate_nodes(nodes)
        yield (curr_dir, *separated)
        pending.extend(map(lambda n: n.path, separated.dirs))


def walk_dfs(dir_path, mode='pre-order'):
    """
    Recursively Generates all the contents of a directory in Depth First Order
    :param dir_path: Base path for which to enumerate contents
    :param mode: 'pre-order' for pre-order traversal and 'post-order' for post-order traversal
    :return: Contents of directory (dir_path, file_nodes, directory_nodes, symlink_nodes)
    """
    nodes = scan_dir(dir_path)
    separated = separate_nodes(nodes)
    if mode == 'pre-order':
        yield (
         
          dir_path, *separated)
    for d in separated.dirs:
        yield from walk_dfs(d.path, mode)

    if mode == 'post-order':
        yield (
         
          dir_path, *separated)


def create_symlink(src, dest, override=False):
    """Create a symlink from 'source' to 'destination', optionally allowing overrides"""
    abs_src_path = os.path.abspath(src)
    abs_dest_path = os.path.abspath(dest)
    if os.path.islink(abs_dest_path):
        if override:
            os.unlink(abs_dest_path)
        else:
            raise AlreadyExists('Destination path %s already exists' % abs_dest_path)
    os.symlink(abs_src_path, abs_dest_path)


def del_symlink(path, ignore_already_del=False):
    """Delete a symlink at 'path' optionally ignoring the case when the symlink does not exist"""
    if os.path.islink(path):
        os.unlink(path)
    else:
        if not ignore_already_del:
            raise DoesNotExist('Symbolic link does not exist at path %s' % path)


def copy_symlink(source_path, dest_path):
    """Create a new symlink at 'dest_path' which points to the same file as the symlink at 'source_path'"""
    actual_path = os.readlink(source_path)
    os.symlink(actual_path, dest_path)


def get_hidden_directory_path(name, path):
    """Compute the path of a hidden directory"""
    return os.path.join(path, '.' + name)


def create_hidden_directory(name, path):
    """Create a hidden directory named 'name' at 'path'"""
    final_path = get_hidden_directory_path(name, path)
    os.mkdir(final_path)
    return final_path


def is_empty_dir(dir_path):
    """Check whether a directory is empty"""
    return os.path.isdir(dir_path) and len(os.listdir(dir_path)) <= 0


def is_parent_dir(child_path, parent_path):
    """Check whether a directory is a parent of another (Returns True if both are same)"""
    child_path = expand_path(child_path)
    parent_path = expand_path(parent_path)
    while child_path == parent_path:
        return True
        next_child = os.path.dirname(child_path)
        if child_path == next_child:
            return False
        child_path = next_child


def count_nodes(dir_path):
    """Get count of all files, directories and symlinks (recursively) in a directory"""
    count = collections.defaultdict(int)
    for root, files, dirs, links in walk_bfs(dir_path):
        count['files'] += len(files)
        count['dirs'] += len(dirs)
        count['links'] += len(links)

    return count


def save_pickled(data, *path):
    """Save an object to a path or path components specified by 'path'"""
    final_path = (os.path.join)(*path)
    with open(final_path, 'wb') as (mfile):
        pickle.dump(data, mfile)


def load_unpickled(*path):
    """Load an object from a path or path components specified by 'path'"""
    final_path = (os.path.join)(*path)
    with open(final_path, 'rb') as (mfile):
        data = pickle.load(mfile)
    return data


def save_json(data, path, serializer=None):
    """Save an object to a JSON file, optionally with a custom serializer"""
    with open(path, 'w') as (jf):
        json.dump(data, jf, default=serializer, indent=4)


def load_json(path, deserializer=None):
    """Load an object from a JSON file, optionally with a custom deserializer"""
    with open(path, 'r') as (jf):
        data = json.load(jf, object_hook=deserializer)
    return data


def expand_path(path):
    """Computes absolute path and expands user to achieve an application wide standard path format"""
    return os.path.abspath(os.path.expanduser(path))