# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/tk/vtkLoadPythonTkWidgets.py
# Compiled at: 2018-11-28 17:07:58
import sys, os, vtkCommonCorePython

def vtkLoadPythonTkWidgets(interp):
    """vtkLoadPythonTkWidgets(interp) -- load vtk-tk widget extensions

    This is a mess of mixed python and tcl code that searches for the
    shared object file that contains the python-vtk-tk widgets.  Both
    the python path and the tcl path are searched.
    """
    X = vtkCommonCorePython.vtkVersion.GetVTKMajorVersion()
    Y = vtkCommonCorePython.vtkVersion.GetVTKMinorVersion()
    modname = 'vtkRenderingPythonTkWidgets'
    name = '%s-%d.%d' % (modname, X, Y)
    pkgname = modname.lower().capitalize()
    loadedpkgs = interp.call('info', 'loaded')
    found = False
    try:
        found = loadedpkgs.find(pkgname) >= 0
    except AttributeError:
        for pkgtuple in loadedpkgs:
            found |= pkgname in pkgtuple

    if found:
        return
    prefix = ''
    if sys.platform == 'cygwin':
        prefix = 'cyg'
    else:
        if os.name == 'posix':
            prefix = 'lib'
        extension = interp.call('info', 'sharedlibextension')
        filename = prefix + name + extension
        pathlist = sys.path
        try:
            auto_paths = interp.getvar('auto_path').split()
        except AttributeError:
            auto_paths = interp.getvar('auto_path')

        for path in auto_paths:
            prev = str(pathlist[(-1)])
            try:
                if len(prev) > 0 and prev[0] == '{' and prev[(-1)] != '}':
                    pathlist[-1] = prev + ' ' + path
                else:
                    pathlist.append(path)
            except AttributeError:
                pass

        if os.name == 'posix':
            pathlist.append('/usr/local/lib')
        if sys.hexversion >= 50331648:
            unicode = str
        else:
            unicode = sys.modules['__builtin__'].unicode
        for path in pathlist:
            try:
                if not isinstance(path, str) and not isinstance(path, unicode):
                    path = path.string
                if len(path) > 0 and path[0] == '{' and path[(-1)] == '}':
                    path = path[1:-1]
                fullpath = os.path.join(path, filename)
            except AttributeError:
                pass

            if ' ' in fullpath:
                fullpath = '{' + fullpath + '}'
            if interp.eval('catch {load ' + fullpath + ' ' + pkgname + '}') == '0':
                return

    interp.call('load', filename, pkgname)