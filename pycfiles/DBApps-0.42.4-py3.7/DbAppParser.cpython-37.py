# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/DbAppParser.py
# Compiled at: 2020-04-14 15:22:04
# Size of source mod 2**32: 2668 bytes
"""
Base class for all parsers for Db Applications
"""
import argparse, pathlib, datetime, os

class DbArgNamespace:
    __doc__ = '\n    Empty arguments, holds output of arg parsing\n    '


class DbAppParser:
    __doc__ = '\n    Base class for database arguments. When a subclass calls\n    argparse.parseArguments, this class returns a structure containing\n    a member drsDbConfig: str\n    '
    _parser = None
    _parser: argparse.ArgumentParser
    _args = None
    _args: DbArgNamespace

    def __init__(self, description: str, usage: str):
        self._parser = argparse.ArgumentParser(description=description, usage=('%(prog)s | -d DBAppSection:DbAppFile ' + usage))
        self._parser.add_argument('-d', '--drsDbConfig', help='specify section:configFileName', required=True)

    @property
    def parsedArgs(self) -> DbArgNamespace:
        """
        Readonly, calc once
        parses the classes arguments, and returns the namespace
        :return:
        """
        if self._args is None:
            self._args = DbArgNamespace()
            self._parser.parse_args(namespace=(self._args))
        return self._args


def str2date(arg: str) -> datetime.datetime:
    """
    parses date given in yyyy-mm-dd
    """
    return datetime.datetime.strptime(arg, '%Y-%m-%d')


def writableExpandoFile(path: str):
    """
    argparse type for a file in a writable directory
    :param path:
    :return:
    """
    osPath = os.path.expanduser(path)
    p = pathlib.Path(osPath)
    if os.path.isdir(osPath):
        raise argparse.ArgumentTypeError(f"{osPath} is a directory. A file name is required.")
    pDir = p.parent
    if not os.access(str(pDir), os.W_OK):
        raise argparse.ArgumentTypeError(f"{osPath} is in a readonly directory ")
    return path


def mustExistDirectory(path: str):
    """
    Argparse type specifying a string which represents
    an existing file path
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError
    for root, dirs, files in os.walk(path, True):
        if len(dirs) == 0:
            raise argparse.ArgumentTypeError
        else:
            return path


def mustExistFile(path: str):
    """
    Common utility. Returns
    :param path:
    :return:
    """
    fullPath = os.path.expanduser(path)
    if not os.path.exists(fullPath):
        raise argparse.ArgumentTypeError
    else:
        return fullPath