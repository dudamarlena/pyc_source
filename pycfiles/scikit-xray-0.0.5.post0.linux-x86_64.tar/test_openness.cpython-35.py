# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/tests/test_openness.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4119 bytes
from __future__ import absolute_import, division, print_function
import six, os, importlib
filetypes = [
 'py', 'txt', 'dat']
blacklisted = [
 ' his ', ' him ', ' guys ', ' guy ']

class ValuesError(ValueError):
    pass


class UnwelcomenessError(ValuesError):
    pass


def _everybody_welcome_here(string_to_check, blacklisted=blacklisted):
    for line in string_to_check.split('\n'):
        for b in blacklisted:
            if b in string_to_check:
                raise UnwelcomenessError("string %s contains '%s' which is blacklisted. Tests will not pass until this language is changed. For tips on writing gender-neutrally, see http://www.lawprose.org/blog/?p=499. Blacklisted words: %s" % (
                 string_to_check, b, blacklisted))


def _openess_tester(module):
    if hasattr(module, '__all__'):
        funcs = module.__all__
    else:
        funcs = dir(module)
    for f in funcs:
        yield (
         _everybody_welcome_here, f.__doc__)


def test_openness():
    """
    Ensure that our library does not contain sexist (intentional or otherwise)
    language. For tips on writing gender-neutrally,
    see http://www.lawprose.org/blog/?p=499

    Notes
    -----
    Inspired by
    https://modelviewculture.com/pieces/gendered-language-feature-or-bug-in-software-documentation
    and
    https://modelviewculture.com/pieces/the-open-source-identity-crisis
    """
    starting_package = 'skxray'
    modules, files = get_modules_in_library(starting_package)
    for m in modules:
        yield (
         _openess_tester, importlib.import_module(m))

    for afile in files:
        with open(afile, 'r') as (f):
            yield (
             _everybody_welcome_here, f.read())


_IGNORE_FILE_EXT = ['pyc', 'so', 'ipynb', 'jpg', 'txt', 'zip']
_IGNORE_DIRS = ['__pycache__', '.git', 'cover', 'build', 'dist', 'tests',
 '.ipynb_checkpoints', 'SOFC']

def get_modules_in_library(library, ignorefileext=None, ignoredirs=None):
    """

    Parameters
    ----------
    library : str
        The library to be imported
    ignorefileext : list, optional
        List of strings (not including the dot) that are file extensions that
        should be ignored
        Defaults to the ``ignorefileext`` list in this module
    ignoredirs : list, optional
        List of strings that, if present in the file path, will cause all
        sub-directories to be ignored
        Defaults to the ``ignoredirs`` list in this module

    Returns
    -------
    modules : str
        List of modules that can be imported with
        ``importlib.import_module(module)``
    other_files : str
        List of other files that
    """
    if ignoredirs is None:
        ignoredirs = _IGNORE_DIRS
    if ignorefileext is None:
        ignorefileext = _IGNORE_FILE_EXT
    module = importlib.import_module(library)
    mods = []
    other_files = []
    top_level = os.sep.join(module.__file__.split(os.sep)[:-1])
    for path, dirs, files in os.walk(top_level):
        skip = False
        for ignore in ignoredirs:
            if ignore in path:
                skip = True
                break

        if skip:
            pass
        else:
            if path.split(os.sep)[(-1)] in ignoredirs:
                pass
            else:
                for f in files:
                    file_base, file_ext = f.split('.')
                    if file_ext not in ignorefileext:
                        if file_ext == 'py':
                            mod_path = path[len(top_level) - len(library):].split(os.sep)
                            if not file_base == '__init__':
                                mod_path.append(file_base)
                            mod_path = '.'.join(mod_path)
                            mods.append(mod_path)
                        else:
                            other_files.append(os.path.join(path, f))

    return (
     mods, other_files)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)