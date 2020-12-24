# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/utils/utils.py
# Compiled at: 2009-05-10 21:48:50
import os, sys, datetime, traceback, subprocess, unittest

def under_svn_control(path):
    version = get_svnversion(path)
    if version == 'exported':
        return False
    return True


def get_svnversion_persistent(store_path, version_str):
    svnversion = get_svnversion()
    save_version = True
    if svnversion == 'exported':
        save_version = False
        g = {}
        l = {}
        execfile(store_path, g, l)
        svnversion = l['__svnrev__']
    version = version_str % {'svnversion': svnversion}
    if save_version:
        fd = open(store_path, 'wb')
        fd.write('#automatically generated on %s\n' % datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000'))
        fd.write('__svnrev__="%s"\n' % svnversion)
        fd.write('__version__="%s"\n' % version)
        fd.close()
    return version


def get_svnversion(path=None):
    if path is None:
        path = os.path.abspath(os.curdir)
    if sys.platform.startswith('win'):
        prog = 'C:\\Program Files\\Subversion\\bin\\svnversion.exe'
    else:
        prog = '/usr/bin/svnversion'
        if not os.path.exists(prog):
            prog = '/usr/local/bin/svnversion'
    if not os.path.exists(prog):
        if os.path.exists(os.path.join(path, '.svn')):
            import warnings
            warnings.warn('No svnversion program found at %s, pretending svnversion=1' % prog)
            return '1'
        else:
            return 'exported'
    args = [
     prog, '-n', '-c', path]
    res = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.wait():
        errstr = res.stderr.read().strip()
        if errstr.endswith('not versioned, and not exported'):
            return 'not versioned, and not exported'
        raise RuntimeError('"%s" returned error: "%s"' % ((' ').join(args), errstr))
    val = res.stdout.read()
    colon_idx = val.find(':')
    if colon_idx != -1:
        val = val[colon_idx + 1:]
    if val.endswith('M'):
        val = val[:-1]
    if val.endswith('S'):
        val = val[:-1]
    return val


def get_motmot_test_suite():

    def my_import(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

        return mod

    module_names = [
     'motmot.cam_iface.tests',
     'motmot.flytrax.tests',
     'motmot.FastImage.tests',
     'motmot.realtime_image_analysis.tests',
     'motmot.FlyMovieFormat.tests']
    all_suites = []
    for module_name in module_names:
        try:
            tests_sub_module = my_import(module_name)
        except Exception, err:
            print 'ERROR: Could not import module "%s" - skipping tests for this module' % module_name
            traceback.print_exc(err)
            continue

        suite = tests_sub_module.get_test_suite()
        all_suites.append(suite)

    suite = unittest.TestSuite(all_suites)
    return suite


def test_motmot():
    suite = get_motmot_test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    print 'SVN version:', get_svnversion()


if __name__ == '__main__':
    main()