# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/archivedb/common.py
# Compiled at: 2011-12-23 18:02:52
import os, re, hashlib
try:
    from progressbar import ProgressBar, Bar, ETA
    pbar_enabled = True
except ImportError:
    pbar_enabled = False

def md5sum(f, block_size=1048576):
    md5 = hashlib.md5()
    if not os.path.isfile(f):
        return
    else:
        file_size = os.stat(f).st_size
        if pbar_enabled and file_size > 0:
            widgets = [
             Bar(left='[', right=']', marker='#'), ' ', ETA()]
            bar = ProgressBar(widgets=widgets, maxval=file_size).start()
        else:
            bar = None
        try:
            with open(f, 'rb') as (fp):
                bytes_read = 0
                while True:
                    if not os.path.isfile(f):
                        pass
                    else:
                        return
                        data = fp.read(block_size)
                        if not data:
                            break
                        md5.update(data)
                        bytes_read += len(data)
                        if bar is not None:
                            bar.update(bytes_read)

        except IOError:
            return
        else:
            if bar is not None:
                bar.finish()

        return md5.hexdigest()


def split_path(watch_dirs, p):
    """
    Parses out a path to a file in a format suitable for
    inserting into and searching the database
    
    Args:
    watch_dirs - list of directories script is watching
    p - full path to file (if p is a directory [requires trailing slash], file_name will be "")
    
    Returns: tuple (watch_dir, base_path, file_name)
    """
    watch_dir = ''
    base_path = ''
    file_name = ''
    for d in watch_dirs:
        split = re.split(('^{0}').format(d), p)
        if split[0] == '':
            watch_dir = d.rstrip(os.sep)
            base_path = split[1].lstrip(os.sep)
            break

    (base_path, file_name) = os.path.split(base_path)
    return (
     watch_dir, base_path, file_name)


def join_path(watch_dir, path, file_name):
    return os.path.join(watch_dir, path, file_name)


def list_to_enum(watch_dirs):
    out = ("enum('{0}')").format(("','").join(watch_dirs))
    return out


def enum_to_list(enum):
    regex = "'([^']*)'[\\,\\)]"
    watch_list = re.findall(regex, enum)
    return watch_list