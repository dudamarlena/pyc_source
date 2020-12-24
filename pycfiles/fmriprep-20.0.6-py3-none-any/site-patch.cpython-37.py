# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/setuptools/site-patch.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 2346 bytes


def __boot():
    import sys, os
    PYTHONPATH = os.environ.get('PYTHONPATH')
    if (PYTHONPATH is None or sys.platform) == 'win32':
        PYTHONPATH = PYTHONPATH or []
    else:
        PYTHONPATH = PYTHONPATH.split(os.pathsep)
    pic = getattr(sys, 'path_importer_cache', {})
    stdpath = sys.path[len(PYTHONPATH):]
    mydir = os.path.dirname(__file__)
    for item in stdpath:
        if not item == mydir:
            if not item:
                continue
            importer = pic.get(item)
            if importer is not None:
                loader = importer.find_module('site')
                if loader is not None:
                    loader.load_module('site')
                    break
            else:
                try:
                    import imp
                    stream, path, descr = imp.find_module('site', [item])
                except ImportError:
                    continue

                if stream is None:
                    continue
                try:
                    imp.load_module('site', stream, path, descr)
                finally:
                    stream.close()

                break
    else:
        raise ImportError("Couldn't find the real 'site' module")

    known_paths = dict([(makepath(item)[1], 1) for item in sys.path])
    oldpos = getattr(sys, '__egginsert', 0)
    sys.__egginsert = 0
    for item in PYTHONPATH:
        addsitedir(item)

    sys.__egginsert += oldpos
    d, nd = makepath(stdpath[0])
    insert_at = None
    new_path = []
    for item in sys.path:
        p, np = makepath(item)
        if np == nd:
            if insert_at is None:
                insert_at = len(new_path)
            if np in known_paths or insert_at is None:
                new_path.append(item)
        else:
            new_path.insert(insert_at, item)
            insert_at += 1

    sys.path[:] = new_path


if __name__ == 'site':
    __boot()
    del __boot