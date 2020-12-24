# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/setuptools_mtn.py
# Compiled at: 2008-03-29 18:37:12
import popen2, os, distutils.log, shlex
__all__ = [
 'find_files_in_mtn']

class PopenWrapper(object):

    def __init__(self, popen):
        self.popen = popen
        self.readline = popen.fromchild.readline

    def __iter__(self):
        return iter(self.popen.fromchild)

    def close(self):
        popen = self.popen
        popen.fromchild.close()
        result = popen.wait()
        if os.WIFEXITED(result):
            return os.WEXITSTATUS(result) == 0
        else:
            return False


def automate_monotone(command, capture_stderr=False):
    if capture_stderr:
        popen_constructor = popen2.Popen4
    else:
        popen_constructor = popen2.Popen3
    mtn_executable = os.environ.get('MTN', 'mtn')
    popen = popen_constructor('%s --xargs -' % (mtn_executable,))
    popen.tochild.write(('').join(('automate ', command, '\n')))
    popen.tochild.close()
    return PopenWrapper(popen)


def get_monotone_version():
    mtn = automate_monotone('interface_version', capture_stderr=True)
    version = mtn.readline()
    if mtn.close() and version:
        try:
            (major, minor) = (int(n) for n in version.split('.', 1))
        except (ValueError, TypeError):
            pass
        else:
            return (
             major, minor)
    return (None, None)


def get_monotone_inventory():
    (major, minor) = get_monotone_version()
    inventory_reader = inventory_readers.get(major)
    if inventory_reader:
        (mtn, inventory) = inventory_reader()
        if mtn.close():
            return inventory
    return ()


inventory_readers = {}

def read_v4_inventory():
    mtn = automate_monotone('inventory')
    inventory = []
    for line in mtn:
        line = line.rstrip()
        if line[0] == ' ' and line[2] in ' P':
            inventory.append(line[4:].split(' ', 2)[2])

    return (
     mtn, inventory)


inventory_readers.update({4: read_v4_inventory, 5: read_v4_inventory})

def parse_v6_values(value_str):
    return shlex.split(value_str)


def read_v6_entry(mtn):
    entry = {}
    for line in mtn:
        line = line.strip()
        if not line:
            break
        (key, value_str) = line.split(None, 1)
        values = parse_v6_values(value_str)
        entry[key] = values

    return entry


def read_v6_inventory():
    mtn = automate_monotone('inventory')
    inventory = []
    while True:
        entry = read_v6_entry(mtn)
        if not entry:
            break
        path = entry.get('path')
        if path and len(path) == 1 and 'known' in entry.get('status'):
            inventory.append(path[0])

    return (
     mtn, inventory)


inventory_readers.update({6: read_v6_inventory, 7: read_v6_inventory})

def find_mtn_root(a_path):
    assert os.path.isabs(a_path)
    assert a_path == os.path.normpath(a_path)
    if os.path.isdir(os.path.join(a_path, '_MTN')):
        return a_path
    else:
        (head, tail) = os.path.split(a_path)
        if head != a_path:
            return find_mtn_root(head)
        else:
            return
    return


def get_path_relative_to_mtn_root(mtn_root, abs_path):
    common_path = os.path.commonprefix([mtn_root, abs_path])
    return abs_path[len(common_path) + 1:]


def call_with_cwd(temp_cwd, callable, *args, **kwargs):
    orig_cwd = os.getcwd()
    try:
        try:
            os.chdir(temp_cwd)
        except OSError, e:
            distutils.log.warn('error with mtn plug-in: %s' % (str(e),))
            return

        return callable(*args, **kwargs)
    finally:
        os.chdir(orig_cwd)

    return


def filter_inventory(rel_path, abs_path, mtn_root):
    inventory = call_with_cwd(mtn_root, get_monotone_inventory)
    mtn_relative_path = get_path_relative_to_mtn_root(mtn_root, abs_path)
    if mtn_relative_path:
        mtn_relative_path += '/'
        strip_before = len(mtn_relative_path)
    else:
        strip_before = 0
    for inventory_path in call_with_cwd(mtn_root, get_monotone_inventory):
        inventory_path = inventory_path.rstrip('/')
        if inventory_path and inventory_path.startswith(mtn_relative_path):
            inventory_rel_path = os.path.join(rel_path, inventory_path[strip_before:])
            yield os.path.normpath(inventory_rel_path)


def find_files_in_mtn(a_path):
    abs_path = os.path.normpath(os.path.abspath(a_path))
    mtn_root = find_mtn_root(abs_path)
    if mtn_root is None:
        return ()
    return filter_inventory(a_path, abs_path, mtn_root)


if __name__ == '__main__':
    import sys
    assert len(sys.argv) <= 2, 'only an optional path argument can be given'
    if len(sys.argv) == 2:
        a_path = sys.argv[1]
    else:
        a_path = ''
    for name in find_files_in_mtn(a_path):
        print name