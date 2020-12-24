# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/utils/check_new_namespace.py
# Compiled at: 2009-05-10 21:48:50
import sys, re
old_top_level_modules = [
 'motmot_utils',
 'cam_iface',
 'FastImage',
 'fview_UDP_logger',
 'fview',
 'wxvalidatedtext',
 'wxvideo',
 'imops',
 'fview_PLUGIN_TEMPLATE',
 'fview_c_callback', 'motmot_utils',
 'FlyMovieFormat',
 'wxglvideo',
 'flytrax',
 'FastImage',
 'realtime_image_analysis',
 'trackem',
 'fview_UDP_logger']

def main():
    filenames = sys.argv[1:]
    for filename in filenames:
        fd = open(filename, mode='r')
        lineno = 0
        for line in fd.readlines():
            lineno += 1
            split = line.strip().split()
            if not len(split):
                continue
            if split[0].startswith('#'):
                continue
            if '__import__' in line:
                if line == "__import__('pkg_resources').declare_namespace(__name__)\n":
                    continue
                else:
                    print 'WARNING: could not parse line %s(%d): %s' % (filename, lineno, repr(line))
                    continue
            if len(split) < 2:
                continue
            if split[0] in ('from', 'import'):
                top = split[1].split('.')[0]
                if top in old_top_level_modules:
                    print '%s(%d): %s' % (filename, lineno, repr(line))

        fd.close()


if __name__ == '__main__':
    main()