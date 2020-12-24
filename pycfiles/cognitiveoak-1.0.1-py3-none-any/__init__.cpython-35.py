# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Haibin\AppData\Local\Temp\pip-build-8dr99z6a\segpy\segpy\ext\__init__.py
# Compiled at: 2017-02-16 13:30:25
# Size of source mod 2**32: 561 bytes
import pkg_resources
loaded = set()

def load_entry_points(name=None):
    """Load extension packages into the segpy.ext namespace.

    Any packages registered against the 'segpy.ext' entry-point group will be
    installed dynamically into the segpy.ext namespace.
    """
    for entry_point in pkg_resources.iter_entry_points(group='segpy.ext', name=name):
        package = entry_point.load()
        if package not in loaded:
            loaded.add(package)
            __path__.extend(package.__path__)
            package.load()


load_entry_points()