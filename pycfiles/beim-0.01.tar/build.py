# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/scripts/build.py
# Compiled at: 2013-12-08 21:45:16


def build(export_root):
    import sys, os
    pwd = os.path.abspath(os.curdir)
    import sys
    sys.path = [
     pwd] + sys.path
    from beim.build import build_release, clean_up
    rt = build_release(pwd, export_root=export_root)
    if rt:
        import sys
        sys.exit(1)


def getsrc():
    p = 'src'
    if hasSubdirs(p):
        return
    from .getsrc import main
    main()


def hasSubdirs(p):
    skip = '.svn'
    import os
    entries = os.listdir(p)
    for e in entries:
        if e in skip:
            continue
        p1 = os.path.join(p, e)
        if os.path.isdir(p1):
            return True
            continue

    return False


def main():
    getsrc()
    import sys, os, shlex
    from beim.datastore import open
    build_info = open('build_info')
    if len(sys.argv) == 2:
        export_root = sys.argv[1]
    elif build_info.get('export_root'):
        export_root = build_info['export_root']
    else:
        export_root = os.path.abspath('EXPORT')
    build_info['export_root'] = export_root
    del build_info
    deps_root = os.path.join(export_root, 'deps')
    env = os.environ.copy()
    env['PATH'] = '%s:%s' % (
     os.path.join(deps_root, 'bin'), env['PATH'])
    env['LD_LIBRARY_PATH'] = '%s:%s' % (
     os.path.join(deps_root, 'lib'), env.get('LD_LIBRARY_PATH') or '')
    env['DYLD_LIBRARY_PATH'] = '%s:%s' % (
     os.path.join(deps_root, 'lib'), env.get('DYLD_LIBRARY_PATH') or '')
    env['PYTHONPATH'] = '%s:%s' % (
     os.path.join(deps_root, 'python'), env.get('PYTHONPATH', ''))
    cmd = '%s -c "from beim.scripts.build import build; build(%r)"' % (
     sys.executable, export_root)
    args = shlex.split(cmd)
    import subprocess
    p = subprocess.Popen(args, env=env)
    while 1:
        p.communicate()
        rt = p.poll()
        if rt is not None:
            break
        else:
            continue

    if rt:
        raise RuntimeError('Command %s failed or aborted' % cmd)
    return


__id__ = '$Id$'