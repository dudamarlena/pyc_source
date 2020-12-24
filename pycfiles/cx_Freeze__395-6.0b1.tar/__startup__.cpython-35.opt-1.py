# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\initscripts\__startup__.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 1658 bytes
import os, sys, importlib.machinery, importlib.util

class ExtensionFinder(importlib.machinery.PathFinder):

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        """This finder is only for extension modules found within packages that
           are included in the zip file (instead of as files on disk);
           extension modules cannot be found within zip files but are stored in
           the lib subdirectory; if the extension module is found in a package,
           however, its name has been altered so this finder is needed."""
        if path is None:
            return
        suffixes = importlib.machinery.EXTENSION_SUFFIXES
        loaderClass = importlib.machinery.ExtensionFileLoader
        for entry in sys.path:
            if '.zip' in entry:
                pass
            else:
                for ext in suffixes:
                    location = os.path.join(entry, fullname + ext)
                    if os.path.isfile(location):
                        loader = loaderClass(fullname, location)
                        return importlib.util.spec_from_loader(fullname, loader)


sys.meta_path.append(ExtensionFinder)

def run():
    baseName = os.path.normcase(os.path.basename(sys.executable))
    name, ext = os.path.splitext(baseName)
    module = __import__(name + '__init__')
    module.run()