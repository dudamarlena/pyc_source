# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/admin/plugins/create_movable.py
# Compiled at: 2007-01-12 09:05:01
import sys, os, shutil, distutils.sysconfig, simpleweb.utils
try:
    import pkg_resources
except ImportError:
    simpleweb.utils.optional_dependency_err('Standalone Deployment', 'setuptools')

def create_movable(name, args):
    """Usage: simpleweb-admin create-movable [lib-folder]

The create-movable plugin packs all the modules used for the application 
including simpleweb itself and any dependencies that are not part of the
standard library, into a single folder which is then added to sys.path, 
using a custom sitecustomize.py

This helps in deployments that are supposed to be contained, for instance
Shared Web Hosts.
"""
    lib_dir = 'site-packages'
    try:
        lib_dir = args[0]
    except IndexError:
        pass

    lib_dir = os.path.join(os.getcwd(), lib_dir)
    try:
        os.mkdir(lib_dir)
    except OSError, (code, msg):
        if code == 17:
            cleanup_site(os.getcwd(), lib_dir)
        else:
            raise

    from simpleweb.app import SimplewebApp
    import simpleweb._urls as urls
    from simpleweb.settings import Config
    SimplewebApp(urls, Config('config'))
    for (name, module) in sys.modules.items():
        if module and hasattr(module, '__file__'):
            dest_path = lib_dir
            if is_filtered(lib_dir, name, module):
                continue
            if is_package(name, module):
                dest_path = create_pkg_dir(name, root_dir=dest_path)
            elif is_nested_module(name, module):
                dest_path = create_pkg_dir(name, root_dir=dest_path, is_pkg=False)
            src_path = get_module_file(module)
            copy_module_file(src_path, dest_path)

    create_sitecustomize(os.getcwd(), lib_dir)


def cleanup_site(root_dir, lib_dir):
    try:
        dest_path = os.path.join(root_dir, 'sitecustomize.py')
        os.unlink(dest_path)
        dest_path = os.path.join(root_dir, 'sitecustomize.pyc')
        os.unlink(dest_path)
        dest_path = os.path.join(root_dir, 'sitecustomize.pyo')
        os.unlink(dest_path)
        shutil.rmtree(lib_dir)
    except OSError, (code, msg):
        if code == 2:
            pass


def create_sitecustomize(root_dir, lib_dir):
    sitecustomize_py = '\nimport sys\nimport os\n\nlibdir = \'%s\'\npath = os.path.join(os.getcwd(), libdir)\nsys.path.append(path)\n\nif __name__ == \'__main__\':\n\tprint path, "will be added to sys.path"\n' % lib_dir
    dest_path = os.path.join(root_dir, 'sitecustomize.py')
    f = open(dest_path, 'w')
    f.write(sitecustomize_py)
    f.close()


def create_pkg_dir(pkgname, root_dir, is_pkg=True, dummy_run=False):
    if is_pkg:
        rel_path = build_pkg_path(pkgname)
    else:
        rel_path = build_nested_module_path(pkgname)
    path = os.path.join(root_dir, rel_path)
    if not dummy_run:
        try:
            os.makedirs(path)
        except OSError, (code, msg):
            if code == 17:
                pass
            else:
                raise

    return path


def build_pkg_path(pkgname):
    path = pkgname
    return path.replace('.', os.path.sep)


def build_nested_module_path(pkgname):
    path = pkgname[:pkgname.rfind('.')]
    return path.replace('.', os.path.sep)


def conv_obj2src(filename):
    """conv_obj2src('afilename.py[c|o]') -> 'afilename.py'

        Converts the extention from python object file (pyc or pyo) to py.
        .py files should stay unchanged.
        """
    ext = os.path.splitext(filename)[1]
    if ext == '.pyc':
        filename = filename.replace('.pyc', '.py')
    if ext == '.pyo':
        filename = filename.replace('.pyo', '.py')
    if ext == '.so' or ext == '.a' or ext == '.dll':
        pass
    return filename


def get_module_file(module):
    (module_file_path, module_file) = os.path.split(module.__file__)
    module_file = conv_obj2src(module_file)
    src_path = pkg_resources.resource_filename(module.__name__, module_file)
    return src_path


def copy_module_file(src_path, dst_path):
    shutil.copy(src_path, dst_path)


def is_filtered(lib_dir, modulename, module):
    if is_stdlib(module):
        return True
    elif is_in_libdir(lib_dir, module):
        return True
    elif is_in_current_app(module):
        return True
    elif is_simpleweb_module(modulename):
        return True
    else:
        return False


def is_stdlib(module):
    site_packages_prefix = distutils.sysconfig.get_python_lib()
    stdlib_prefix = os.path.split(site_packages_prefix)[0]
    if not module.__file__.startswith(site_packages_prefix) and module.__file__.startswith(stdlib_prefix):
        return True
    else:
        return False


def is_in_libdir(lib_dir, module):
    if module.__file__.startswith(lib_dir):
        return True
    else:
        return False


def is_in_current_app(module):
    if module.__file__.startswith('.') or os.path.split(module.__file__)[1].startswith('sitecustomize'):
        return True
    else:
        return False


def is_simpleweb_module(name):
    if name.startswith('simpleweb'):
        return True
    else:
        return False


def is_package(modulename, module):
    filename = os.path.split(module.__file__)[1]
    if filename.startswith('__init__.py'):
        return True
    else:
        return False


def is_nested_module(modulename, module):
    if modulename.find('.') >= 0:
        return True
    else:
        return False