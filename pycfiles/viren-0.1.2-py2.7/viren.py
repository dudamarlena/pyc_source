# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/viren/viren.py
# Compiled at: 2013-12-12 20:04:38
import os, random, subprocess, sys, tempfile

class VirenError(RuntimeError):
    pass


def verify_rename_list(old_names, new_names):
    """
    Sanity check a rename proposal.

    If there is a problem (new names not provided, or they collide among
    themselves, etc), raises VirenError.
    """
    if len(old_names) != len(new_names):
        raise VirenError(('Edited list has {} names, expected {}').format(len(new_names), len(old_names)))
    seen_names = set()
    for lineno, name in enumerate(new_names, 1):
        if not name:
            raise VirenError(('Line {}: empty filename').format(lineno))
        if '/' in name:
            raise VirenError(('Line {}: slash in filename').format(lineno))
        if name in ('.', '..'):
            raise VirenError(('Line {}: filename is . or ..').format(lineno))
        if name in seen_names:
            raise VirenError(('Line {}: duplicate filename').format(lineno))
        seen_names.add(name)


def mk_temp_subdir(dir_path, forbidden_names):
    """
    Make a temp subdir in pwd and return its path.

    The directory name is assigned randomly, and checked not to collide with
    `forbidden_names`.
    """
    for attempt in xrange(10):
        name = 'viren-' + hex(random.randint(1000000000.0, 10000000000.0))[2:]
        path = os.path.join(dir_path, name)
        if name in forbidden_names or os.path.exists(path):
            continue
        os.mkdir(path)
        return path

    raise VirenError('Failed to create temp subdir')


def get_names(dir_path):
    """
    Return list of filenames in given dir, in sorted order.
    """
    names = os.listdir(dir_path)
    names.sort()
    return names


def do_rename(dir_path, new_names):
    """
    Rename files in dir_path (in sorted order) to new_names.

    Leading or trailing whitespace in `new_names` is ignored.

    Raises VirenError if the rename cannot be performed.
    """
    new_names = [ name.strip() for name in new_names ]
    old_names = get_names(dir_path)
    verify_rename_list(old_names, new_names)
    subdir_path = mk_temp_subdir(dir_path, old_names + new_names)
    for name in old_names:
        old_path = os.path.join(dir_path, name)
        new_path = os.path.join(subdir_path, name)
        ret = subprocess.call(['mv', old_path, new_path])
        if ret != 0:
            raise VirenError(('mv failed with return code {}').format(ret))

    for i in xrange(len(old_names)):
        old_path = os.path.join(subdir_path, old_names[i])
        new_path = os.path.join(dir_path, new_names[i])
        ret = subprocess.call(['mv', old_path, new_path])
        if ret != 0:
            raise VirenError(('mv failed with return code {}').format(ret))

    os.rmdir(subdir_path)


def main():
    """
    Run viren in the current directory.
    """
    old_names = get_names('.')
    _, temp_path = tempfile.mkstemp(prefix='viren-')
    temp = open(temp_path, 'w')
    temp.write(('\n').join(old_names))
    temp.close()
    try:
        ret = subprocess.call(['editor', temp_path])
        if ret != 0:
            raise VirenError(('editor failed with return code {}').format(ret))
        new_names = [ line.strip() for line in open(temp_path).xreadlines() ]
        if new_names == old_names:
            print 'No change.'
        else:
            do_rename('.', new_names)
            print 'Done renaming.'
        os.remove(temp_path)
    except VirenError as err:
        print >> sys.stderr, 'Something went wrong:'
        print >> sys.stderr, err.message
        print >> sys.stderr, ('File list saved to {}').format(temp_path)
        sys.exit(1)


if __name__ == '__main__':
    main()