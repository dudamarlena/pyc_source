# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/__init__.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 4798 bytes
__version__ = '1.7'
from . import EditorApp
from . import models
from . import BugReport
import os, sys, io, argparse, locale

def _workaroundNCurses():
    """
    This routine works around the ncurses library.
    It must be called before everything else, so that ncurses is not
    loaded.
    The problem is that python installs and links by default to
    ncurses, instead of ncursesw (wide characters). The result is that unicode
    stuff gets corrupted. We work around the problem as explained in the
    comments. The two libraries appear to be compatible, so if I just "mimic"
    the library name, it behaves correctly.

    Unfortunately, we _must_ rely on a shell script to export LD_LIBRARY_PATH
    for us. I found out that dlopen does not honor LD_LIBRARY_PATH if changed
    after startup.

    The end result is that I always copy the ncurses wide character when not
    in a local lib source.
    """
    import platform, os, sys
    if platform.system() != 'Linux':
        return
    local_lib_path = os.path.expanduser('~/.local/lib/vai/')
    if os.path.exists(os.path.join(local_lib_path, 'libncurses.so')):
        return
    if platform.processor() == 'x86_64':
        ncurses_path = '/lib/x86_64-linux-gnu/libncursesw.so.5.9'
    else:
        ncurses_path = '/lib/i386-linux-gnu/libncursesw.so.5.9'
    if not os.path.exists(ncurses_path):
        from . import models
        models.Configuration.flags['has_wide_ncurses'] = False
        return
    import shutil
    os.makedirs(local_lib_path, exist_ok=True)
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, 'libncurses.so.5.9'))
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, 'libncurses.so.5'))
    shutil.copyfile(ncurses_path, os.path.join(local_lib_path, 'libncurses.so'))
    sys.exit(42)


def main():
    _workaroundNCurses()
    locale.setlocale(locale.LC_ALL, '')
    parser = argparse.ArgumentParser(description='A Vim-like editor, with big dreams.')
    parser.add_argument('filename', nargs='?', help='The filename to open')
    parser.add_argument('--dump-default-config', help='Dump the default configuration to the config file. Useful to reset a broken configuration.', action='store_true')
    parser.add_argument('--profile', help='Enable profiling at the end of the run.', action='store_true')
    parser.add_argument('--pdb', help='Enable debugging with pdb in case of crash.', action='store_true')
    parser.add_argument('--noreport', help='Skip request for bug reporting.', action='store_true')
    parser.add_argument('--version', '-v', help='Print the version number.', action='version', version='vai {0}'.format(__version__))
    args = parser.parse_args()
    app = None
    try:
        if args.dump_default_config:
            filename = models.Configuration.filename()
            if os.path.exists(filename):
                print('Refusing to overwrite existing config file %s. Delete the file manually and try again.' % filename)
                sys.exit(1)
            models.Configuration.save()
            print('Dumped default configuration in %s' % filename)
            sys.exit(0)
        app = EditorApp.EditorApp(sys.argv)
        if args.filename:
            app.openFile(args.filename)
        if args.profile:
            import cProfile
            pr = cProfile.Profile()
            pr.enable()
        app.exec_()
        if args.profile:
            pr.disable()
            s = io.StringIO()
            sortby = 'tottime'
            import pstats
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            print(s.getvalue())
        app.resetScreen()
    except Exception as e:
        import traceback, contextlib
        saved_files = []
        if app is not None:
            saved_files = app.dumpBuffers()
            app.resetScreen()
        with contextlib.closing(open('vai_crashreport.out', 'w')) as (f):
            f.write(traceback.format_exc())
        if args.pdb:
            import pdb
            pdb.post_mortem()
        if not args.noreport:
            BugReport.report(saved_files)

    return 0