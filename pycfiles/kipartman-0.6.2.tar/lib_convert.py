# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kicad/lib_convert.py
# Compiled at: 2018-04-29 13:58:18
from helper.exception import print_stack
import imp
try:
    imp.find_module('pcbnew')
    found = True
except ImportError:
    found = False

class KicadLibConvertException(Exception):

    def __init__(self, error):
        super(KicadLibConvertException, self).__init__(error)


if found:
    from pcbnew import *
    import sys, zipfile, os

    def convert_mod_to_pretty(src_libpath, dst_libpath):
        src_type = IO_MGR.GuessPluginTypeFromLibPath(src_libpath)
        dst_type = IO_MGR.GuessPluginTypeFromLibPath(dst_libpath)
        src_plugin = IO_MGR.PluginFind(src_type)
        dst_plugin = IO_MGR.PluginFind(dst_type)
        try:
            dst_plugin.FootprintLibDelete(dst_libpath)
        except:
            print_stack()
            None

        dst_plugin.FootprintLibCreate(dst_libpath)
        list_of_parts = src_plugin.FootprintEnumerate(src_libpath)
        for part_id in list_of_parts:
            module = src_plugin.FootprintLoad(src_libpath, part_id)
            dst_plugin.FootprintSave(dst_libpath, module)

        return (dst_libpath, list_of_parts)


    def convert_mod_to_pretty_zip(src_libpath, dst_libpath):
        src_type = IO_MGR.GuessPluginTypeFromLibPath(src_libpath)
        dst_type = IO_MGR.GuessPluginTypeFromLibPath(dst_libpath)
        src_plugin = IO_MGR.PluginFind(src_type)
        dst_plugin = IO_MGR.PluginFind(dst_type)
        try:
            dst_plugin.FootprintLibDelete(dst_libpath)
        except:
            print_stack()
            None

        dst_plugin.FootprintLibCreate(dst_libpath)
        list_of_parts = src_plugin.FootprintEnumerate(src_libpath)
        for part_id in list_of_parts:
            module = src_plugin.FootprintLoad(src_libpath, part_id)
            dst_plugin.FootprintSave(dst_libpath, module)

        zf = zipfile.ZipFile('%s.zip' % dst_libpath, 'w', zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(dst_libpath)
        for dirname, subdirs, files in os.walk(dst_libpath):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                print 'zipping %s as %s' % (os.path.join(dirname, filename), arcname)
                zf.write(absname, arcname)

        zf.close()
        return dst_libpath + '.zip'


else:

    def convert_mod_to_pretty(src_libpath, dst_libpath):
        raise KicadLibConvertException('Module pcbnew not found, check your python path')


    def convert_mod_to_pretty_zip(src_libpath, dst_libpath):
        raise KicadLibConvertException('Module pcbnew not found, check your python path')