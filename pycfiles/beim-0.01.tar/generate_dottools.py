# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/build/generate_dottools.py
# Compiled at: 2013-12-08 21:45:16


def render(path, export_root, build_root, merlin_dir):
    import os
    from deps import packages
    dependencies = [
     'Python'] + packages
    dottoolspath = os.path.join(path, 'dottools')
    customization_path = os.path.join(path, 'dottools.customized')
    from ..mm.dottools_factory import render_file
    render_file(dottoolspath, dependencies, export_root, build_root, merlin_dir, customization_path=customization_path)
    return dottoolspath


from ..mm.dottools_factory import DependencyMissing
__id__ = '$Id$'