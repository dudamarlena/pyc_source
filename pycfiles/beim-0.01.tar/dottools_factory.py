# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/mm/dottools_factory.py
# Compiled at: 2013-12-08 21:45:16
from ..paths.InstallationNotFound import InstallationNotFound

def render_file(path, dependencies, export_root, build_root, merlin_dir, target='shared,opt', customization_path=None):
    """
    path: path of the .tools file
    dependencies: dependencies of the project
    export_root: path of export root
    build_root: path to build
    merlin_dir: path to merlin 
    target: build target
    customization_path: path of the .tools-customization, if necessary
    """
    f = Factory(export_root, build_root, merlin_dir, target, customization_path=customization_path)
    lines = f(dependencies)
    open(path, 'w').write(('\n').join(lines))


class DependencyMissing(Exception):

    def __init__(self, packagename, packageid=None, errormessage=None, suggestion=None):
        self.packagename = packagename
        self.packageid = packageid or packagename
        self.errormessage = errormessage
        self.suggestion = suggestion


class Factory:

    def __init__(self, export_root, build_root, merlin_dir, target='shared,opt', customization_path=None):
        self.target = target
        self.export_root = export_root
        self.build_root = build_root
        self.merlin_dir = merlin_dir
        self.customization_path = customization_path

    def __call__(self, dependencies=[
 'Python']):
        import os
        merlin_dir = self.merlin_dir
        build_root = self.build_root
        export_root = self.export_root
        from . import dottools
        header = dottools.render_header(self.target, export_root, build_root, merlin_dir)
        lines = header
        for dep in dependencies:
            try:
                print 'rendering .tools codes for %r ...' % dep
                lines += dottools.render_dependency(dep)
            except InstallationNotFound as err:
                pkgname = err.packagename or dep
                pkgid = err.packageid or dep
                msg = err.errormessage
                if not msg:
                    import traceback
                    msg = traceback.format_exc()
                raise DependencyMissing(pkgname, packageid=pkgid, errormessage=msg, suggestion=err.possible_solution)

            continue

        customization_path = self.customization_path
        if customization_path:
            if not os.path.exists(customization_path):
                open(customization_path, 'w').write('')
            lines.append('. %s' % customization_path)
        return lines


__id__ = '$Id$'