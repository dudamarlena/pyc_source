# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/pep517/_in_process.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 7792 bytes
"""This is invoked in a subprocess to call the build backend hooks.

It expects:
- Command line args: hook_name, control_dir
- Environment variables:
      PEP517_BUILD_BACKEND=entry.point:spec
      PEP517_BACKEND_PATH=paths (separated with os.pathsep)
- control_dir/input.json:
  - {"kwargs": {...}}

Results:
- control_dir/output.json
  - {"return_val": ...}
"""
from glob import glob
from importlib import import_module
import os, os.path
import os.path as pjoin
import re, shutil, sys, traceback, compat

class BackendUnavailable(Exception):
    __doc__ = 'Raised if we cannot import the backend'

    def __init__(self, traceback):
        self.traceback = traceback


class BackendInvalid(Exception):
    __doc__ = 'Raised if the backend is invalid'

    def __init__(self, message):
        self.message = message


class HookMissing(Exception):
    __doc__ = 'Raised if a hook is missing and we are not executing the fallback'


def contained_in(filename, directory):
    """Test if a file is located within the given directory."""
    filename = os.path.normcase(os.path.abspath(filename))
    directory = os.path.normcase(os.path.abspath(directory))
    return os.path.commonprefix([filename, directory]) == directory


def _build_backend():
    """Find and load the build backend"""
    backend_path = os.environ.get('PEP517_BACKEND_PATH')
    if backend_path:
        extra_pathitems = backend_path.split(os.pathsep)
        sys.path[:0] = extra_pathitems
    ep = os.environ['PEP517_BUILD_BACKEND']
    mod_path, _, obj_path = ep.partition(':')
    try:
        obj = import_module(mod_path)
    except ImportError:
        raise BackendUnavailable(traceback.format_exc())

    if backend_path:
        if not any((contained_in(obj.__file__, path) for path in extra_pathitems)):
            raise BackendInvalid('Backend was not loaded from backend-path')
    if obj_path:
        for path_part in obj_path.split('.'):
            obj = getattr(obj, path_part)

    return obj


def get_requires_for_build_wheel(config_settings):
    """Invoke the optional get_requires_for_build_wheel hook

    Returns [] if the hook is not defined.
    """
    backend = _build_backend()
    try:
        hook = backend.get_requires_for_build_wheel
    except AttributeError:
        return []
    else:
        return hook(config_settings)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings, _allow_fallback):
    """Invoke optional prepare_metadata_for_build_wheel

    Implements a fallback by building a wheel if the hook isn't defined,
    unless _allow_fallback is False in which case HookMissing is raised.
    """
    backend = _build_backend()
    try:
        hook = backend.prepare_metadata_for_build_wheel
    except AttributeError:
        if not _allow_fallback:
            raise HookMissing()
        return _get_wheel_metadata_from_wheel(backend, metadata_directory, config_settings)
    else:
        return hook(metadata_directory, config_settings)


WHEEL_BUILT_MARKER = 'PEP517_ALREADY_BUILT_WHEEL'

def _dist_info_files(whl_zip):
    """Identify the .dist-info folder inside a wheel ZipFile."""
    res = []
    for path in whl_zip.namelist():
        m = re.match('[^/\\\\]+-[^/\\\\]+\\.dist-info/', path)
        if m:
            res.append(path)

    if res:
        return res
    raise Exception('No .dist-info folder found in wheel')


def _get_wheel_metadata_from_wheel(backend, metadata_directory, config_settings):
    """Build a wheel and extract the metadata from it.

    Fallback for when the build backend does not
    define the 'get_wheel_metadata' hook.
    """
    from zipfile import ZipFile
    whl_basename = backend.build_wheel(metadata_directory, config_settings)
    with open(os.path.join(metadata_directory, WHEEL_BUILT_MARKER), 'wb'):
        pass
    whl_file = os.path.join(metadata_directory, whl_basename)
    with ZipFile(whl_file) as (zipf):
        dist_info = _dist_info_files(zipf)
        zipf.extractall(path=metadata_directory, members=dist_info)
    return dist_info[0].split('/')[0]


def _find_already_built_wheel(metadata_directory):
    """Check for a wheel already built during the get_wheel_metadata hook.
    """
    if not metadata_directory:
        return
    else:
        metadata_parent = os.path.dirname(metadata_directory)
        if not os.path.isfile(pjoin(metadata_parent, WHEEL_BUILT_MARKER)):
            return
        whl_files = glob(os.path.join(metadata_parent, '*.whl'))
        whl_files or print('Found wheel built marker, but no .whl files')
        return
    if len(whl_files) > 1:
        print('Found multiple .whl files; unspecified behaviour. Will call build_wheel.')
        return
    return whl_files[0]


def build_wheel(wheel_directory, config_settings, metadata_directory=None):
    """Invoke the mandatory build_wheel hook.

    If a wheel was already built in the
    prepare_metadata_for_build_wheel fallback, this
    will copy it rather than rebuilding the wheel.
    """
    prebuilt_whl = _find_already_built_wheel(metadata_directory)
    if prebuilt_whl:
        shutil.copy2(prebuilt_whl, wheel_directory)
        return os.path.basename(prebuilt_whl)
    return _build_backend().build_wheel(wheel_directory, config_settings, metadata_directory)


def get_requires_for_build_sdist(config_settings):
    """Invoke the optional get_requires_for_build_wheel hook

    Returns [] if the hook is not defined.
    """
    backend = _build_backend()
    try:
        hook = backend.get_requires_for_build_sdist
    except AttributeError:
        return []
    else:
        return hook(config_settings)


class _DummyException(Exception):
    __doc__ = 'Nothing should ever raise this exception'


class GotUnsupportedOperation(Exception):
    __doc__ = 'For internal use when backend raises UnsupportedOperation'

    def __init__(self, traceback):
        self.traceback = traceback


def build_sdist(sdist_directory, config_settings):
    """Invoke the mandatory build_sdist hook."""
    backend = _build_backend()
    try:
        return backend.build_sdist(sdist_directory, config_settings)
    except getattr(backend, 'UnsupportedOperation', _DummyException):
        raise GotUnsupportedOperation(traceback.format_exc())


HOOK_NAMES = {
 'get_requires_for_build_wheel',
 'prepare_metadata_for_build_wheel',
 'build_wheel',
 'get_requires_for_build_sdist',
 'build_sdist'}

def main():
    if len(sys.argv) < 3:
        sys.exit('Needs args: hook_name, control_dir')
    else:
        hook_name = sys.argv[1]
        control_dir = sys.argv[2]
        if hook_name not in HOOK_NAMES:
            sys.exit('Unknown hook: %s' % hook_name)
        hook = globals()[hook_name]
        hook_input = compat.read_json(pjoin(control_dir, 'input.json'))
        json_out = {'unsupported':False, 
         'return_val':None}
        try:
            json_out['return_val'] = hook(**hook_input['kwargs'])
        except BackendUnavailable as e:
            try:
                json_out['no_backend'] = True
                json_out['traceback'] = e.traceback
            finally:
                e = None
                del e

        except BackendInvalid as e:
            try:
                json_out['backend_invalid'] = True
                json_out['backend_error'] = e.message
            finally:
                e = None
                del e

        except GotUnsupportedOperation as e:
            try:
                json_out['unsupported'] = True
                json_out['traceback'] = e.traceback
            finally:
                e = None
                del e

        except HookMissing:
            json_out['hook_missing'] = True

    compat.write_json(json_out, (pjoin(control_dir, 'output.json')), indent=2)


if __name__ == '__main__':
    main()