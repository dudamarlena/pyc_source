# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adversarials/core/utils.py
# Compiled at: 2018-12-21 01:06:52
# Size of source mod 2**32: 9425 bytes
"""Utility file for Adversarial package.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Software Engineer.
     Email: javafolabi@gmail.com | victor.afolabi@zephyrtel.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: utils.py
     Created on 20 December, 2018 @ 07:00 PM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
import os, sys, logging
from abc import ABCMeta
from typing import Iterable
from logging.config import fileConfig
from adversarials.core.consts import FS, LOGGER
__all__ = [
 'File', 'Log']

class File(metaclass=ABCMeta):

    @staticmethod
    def make_dirs(path: str, verbose: int=0):
        """Create Directory if it doesn't exist.

        Args:
            path (str): Directory/directories to be created.
            verbose (bool, optional): Defaults to 0. 0 turns of logging,
                while 1 gives feedback on creation of director(y|ies).

        Example:
            ```python
            >>> path = os.path.join("path/to", "be/created/")
            >>> File.make_dirs(path, verbose=1)
            INFO  |  "path/to/be/created/" has been created.
            ```
        """
        if not os.path.isdir(path):
            os.makedirs(path)
            if verbose:
                Log.info('"{}" has been created.'.format(os.path.relpath(path)))

    @staticmethod
    def get_dirs(path: str, exclude: Iterable[str]=None, optimize: bool=False):
        """Retrieve all directories in a given path.

        Args:
            path (str): Base directory of directories to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on,
                otherwise list of directories in given path.
        """
        return File.listdir(path, exclude=exclude, dirs_only=True, optimize=optimize)

    @staticmethod
    def get_files(path: str, exclude: Iterable[str]=None, optimize: bool=False):
        """Retrieve all files in a given path.

        Args:
            path (str): Base directory of files to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on,
                otherwise list of files in given path.
        """
        return File.listdir(path, exclude=exclude, files_only=True, optimize=optimize)

    @staticmethod
    def listdir(path: str, exclude: Iterable[str]=None, dirs_only: bool=False, files_only: bool=False, optimize: bool=False):
        """Retrieve files/directories in a given path.

        Args:
            path (str): Base directory of path to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to
                remove from results.
            dirs_only (bool, optional): Defaults to False. Return only directories in `path`.
            files_only (bool, optional): Defaults to False. Return only files in `path`.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on,
                otherwise list of directories in given path.
        """
        if not os.path.isdir(path):
            raise FileNotFoundError('"{}" was not found!'.format(path))
        else:
            if files_only:
                paths = (os.path.join(path, p) for p in os.listdir(path) if os.path.isfile(os.path.join(path, p)))
            else:
                if dirs_only:
                    paths = (os.path.join(path, p) for p in os.listdir(path) if os.path.isdir(os.path.join(path, p)))
                else:
                    paths = (os.path.join(path, p) for p in os.listdir(path))
            if exclude is not None:
                paths = filter(lambda p: os.path.basename(p) not in exclude, paths)
            paths = optimize or list(paths)
        return paths


class Log(metaclass=ABCMeta):
    fileConfig(LOGGER.ROOT)
    _logger = logging.getLogger()
    level = _logger.level

    @staticmethod
    def setLevel(level: int):
        Log._logger.setLevel(level=level)

    @staticmethod
    def debug(*args, **kwargs):
        sep = kwargs.pop('sep', ' ')
        (Log._logger.debug)((sep.join(map(repr, args))), **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        sep = kwargs.pop('sep', ' ')
        (Log._logger.info)((sep.join(map(repr, args))), **kwargs)

    @staticmethod
    def warn(*args, **kwargs):
        sep = kwargs.pop('sep', ' ')
        (Log._logger.warning)((sep.join(map(repr, args))), **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        sep = kwargs.pop('sep', ' ')
        (Log._logger.error)((sep.join(map(repr, args))), **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        sep = kwargs.pop('sep', ' ')
        (Log._logger.critical)((sep.join(map(repr, args))), **kwargs)

    @staticmethod
    def log(*args, **kwargs):
        """Logging method avatar based on verbosity.

        Args:
            *args

        Keyword Args:
            verbose (int, optional): Defaults to 1.
            level (int, optional): Defaults to ``Log.level``.
            sep (str, optional): Defaults to " ".

        Returns:
            None
        """
        if not kwargs.pop('verbose', 1):
            return
        sep = kwargs.pop('sep', ' ')
        (Log._logger.log)(
         (Log.level), (sep.join(map(repr, args))), **kwargs)

    @staticmethod
    def progress(count: int, max_count: int):
        """Prints task progress *(in %)*.

        Args:
            count {int}: Current progress so far.
            max_count {int}: Total progress length.
        """
        pct_complete = count / max_count
        msg = '\r- Progress: {0:.02%}'.format(pct_complete)
        sys.stdout.write(msg)
        sys.stdout.flush()

    @staticmethod
    def report_hook(block_no: int, read_size: bytes, file_size: bytes):
        """Calculates download progress given the block number, read size,
        and the total file size of the URL target.

        Args:
            block_no {int}: Current download state.
            read_size {bytes}: Current downloaded size.
            file_size {bytes}: Total file size.

        Returns:
            None.
        """
        pct_complete = float(block_no * read_size) / float(file_size)
        msg = '\r\t -Download progress {:.02%}'.format(pct_complete)
        sys.stdout.stdwrite(msg)
        sys.stdout.flush()