# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ctyfoxylos/SBP/python/commonutilslib/commonutilslib/commonutilslib.py
# Compiled at: 2019-02-26 04:33:40
# Size of source mod 2**32: 8352 bytes
__doc__ = '\nMain code for commonutilslib\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
import logging, os, shutil, stat, tempfile, hashlib, pathlib
from contextlib import contextmanager
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '26-02-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'commonutilslib'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

@contextmanager
def cd(new_directory, clean_up=lambda : True):
    """Changes into a given directory and cleans up after it is done

    Args:
        new_directory: The directory to change to
        clean_up: A method to clean up the working directory once done

    """
    previous_directory = os.getcwd()
    os.chdir(os.path.expanduser(new_directory))
    try:
        yield
    finally:
        os.chdir(previous_directory)
        clean_up()


@contextmanager
def tempdir():
    """Creates a temporary directory"""
    directory_path = tempfile.mkdtemp()

    def clean_up():
        shutil.rmtree(directory_path, onerror=on_error)

    with cd(directory_path, clean_up):
        yield directory_path


def on_error(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``

    # 2007/11/08
    # Version 0.2.6
    # pathutils.py
    # Functions useful for working with files and paths.
    # http://www.voidspace.org.uk/python/recipebook.shtml#utils

    # Copyright Michael Foord 2004
    # Released subject to the BSD License
    # Please see http://www.voidspace.org.uk/python/license.shtml

    # For information about bugfixes, updates and support, please join the Pythonutils mailing list.
    # http://groups.google.com/group/pythonutils/
    # Comments, suggestions and bug reports welcome.
    # Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
    # E-mail fuzzyman@voidspace.org.uk
    """
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


class Pushd:
    """Pushd"""
    cwd = None
    original_dir = None

    def __init__(self, directory_name):
        self.cwd = os.path.realpath(directory_name)

    def __enter__(self):
        self.original_dir = os.getcwd()
        os.chdir(self.cwd)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        os.chdir(self.original_dir)


class RecursiveDictionary(dict):
    """RecursiveDictionary"""

    def rec_update(self, other, **third):
        """Implements the recursion

        Recursively update the dictionary with the contents of other and
        third like dict.update() does - but don't overwrite sub-dictionaries.
        """
        try:
            iterator = other.items()
        except AttributeError:
            iterator = other

        self.iter_rec_update(iterator)
        self.iter_rec_update(third.items())

    def iter_rec_update(self, iterator):
        """Updates recursively"""
        for key, value in iterator:
            if key in self and isinstance(self[key], dict) and isinstance(value, dict):
                self[key] = RecursiveDictionary(self[key])
                self[key].rec_update(value)
            else:
                self[key] = value


class Hasher:
    """Hasher"""

    def __init__(self, buffer_size=65536):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self.buffer_size = buffer_size

    def hash_file(self, file_name):
        """Calculates the sha1 hash  of the provided file

        Args:
            file_name (str): The filename of the file to calculate the hash for

        Returns:
            (str): The hash of the file provided

        """
        digest = hashlib.sha1()
        digest = self._get_digest_of_file(digest, file_name, self.buffer_size)
        return digest.hexdigest()

    def hash_directory(self, path):
        """Calculates the sha1 hash  of the directory in the provided path

        Args:
            path (str): The path to calculate the digest for

        Returns:
            (str): The digest of the path

        """
        digest = hashlib.sha1()
        absolute_path = pathlib.Path(path).absolute()
        if not pathlib.Path.is_dir(absolute_path):
            self._logger.error('Directory "%s" does not exist', absolute_path)
            return digest.hexdigest()
        self._logger.debug('Calculating hash for directory "%s"', absolute_path)
        for root, _, files in sorted(os.walk(path)):
            for names in sorted(files):
                file_path = os.path.join(root, names)
                digest.update(hashlib.sha1(file_path[len(path):].encode()).digest())
                if os.path.isfile(file_path):
                    digest = self._get_digest_of_file(digest, file_path, self.buffer_size)

        return digest.hexdigest()

    def _get_digest_of_file(self, digest, file_name, buffer_size):
        """Calculated the sha1 digest of a file using the provided buffer size

        Args:
            digest (str): The digest to update
            file_name (str): The filename of the file to update the digest with
            buffer_size (int): The size of the buffer to be used for the digest calculation

        Returns:
            (str): The updated digest

        """
        try:
            original_digest = digest.hexdigest()
            with open(file_name, 'rb') as (ifile):
                while True:
                    data = ifile.read(buffer_size)
                    if not data:
                        break
                    digest.update(data)

            self._logger.debug('Updated original digest "%s" with file "%s" to "%s"', original_digest, file_name, digest.hexdigest())
        except FileNotFoundError:
            self._logger.exception('Could not find/read file %s', file_name)

        return digest