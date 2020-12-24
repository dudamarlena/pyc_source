# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/pyi.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' \nDefines helper methods for the PyInstaller utility\n'
import os, projex, sys

def collect(basepath, exclude=None, processPlugins=True):
    """
    Collects all the packages associated with the inputted filepath.
    
    :param      module | <module>
    
    :return     ([<str> pkg, ..], [(<str> path, <str> relpath), ..] data)
    """
    if exclude is None:
        exclude = [
         '.py', '.pyc', '.pyo', '.css', '.exe']
    imports = []
    datas = []
    basename = os.path.basename(basepath)
    basepath = os.path.abspath(basepath)
    baselen = len(basepath) - len(basename)
    plugfiles = []
    for root, folders, files in os.walk(basepath):
        if '.svn' in root or '.git' in root:
            continue
        plugdata = None
        if processPlugins and '__plugins__.py' in files:
            filename = os.path.join(root, '__plugins__.py')
            package = projex.packageFromPath(filename) + '.__plugins__'
            pkgpath = projex.packageRootPath(filename)
            if pkgpath not in sys.path:
                sys.path.insert(0, pkgpath)
            __import__(package)
            pkg = sys.modules[package]
            recurse = getattr(pkg, '__recurse__', False)
            plugdata = {'recurse': recurse, 'packages': [], 'path': root}
            plugfiles.append(plugdata)
        else:
            for data in plugfiles:
                if data['recurse'] and root.startswith(data['path']):
                    plugdata = data
                    break

            if plugdata is not None:
                packages = plugdata['packages']
                for folder in folders:
                    pkgpath = os.path.join(root, folder, '__init__.py')
                    if os.path.exists(pkgpath):
                        packages.append(projex.packageFromPath(pkgpath))

            for file_ in files:
                module, ext = os.path.splitext(file_)
                if ext == '.py':
                    package_path = projex.packageFromPath(os.path.join(root, file_))
                    if not package_path:
                        continue
                    if module != '__init__':
                        package_path += '.' + module
                    imports.append(package_path)
                    if plugdata is not None and module not in ('__init__', '__plugins__'):
                        plugdata['packages'].append(package_path)
                elif ext not in exclude:
                    src = os.path.join(root, file_)
                    targ = os.path.join(root[baselen:])
                    datas.append((src, targ))

    for plugdata in plugfiles:
        fname = os.path.join(plugdata['path'], '__plugins__.py')
        packages = plugdata['packages']
        plugs = (',\n').join(map(lambda x: ("r'{0}'").format(x), packages))
        data = [
         ('__recurse__ = {0}').format(plugdata['recurse']),
         ('__toc__ = [{0}]').format(plugs)]
        f = open(fname, 'w')
        f.write(('\n').join(data))
        f.close()

    return (
     imports, datas)