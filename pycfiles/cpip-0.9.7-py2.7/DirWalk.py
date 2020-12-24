# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/DirWalk.py
# Compiled at: 2017-10-03 13:07:16
"""Provides various ways of walking a directory tree

Created on Jun 9, 2011
"""
__author__ = 'Paul Ross'
__date__ = '2011-06-09'
__rights__ = 'Copyright (c) Paul Ross'
import os, fnmatch, collections
FileInOut = collections.namedtuple('FileInOut', 'filePathIn, filePathOut')

class ExceptionDirWalk(Exception):
    """Exception class for this module."""
    pass


def genBigFirst(d):
    """Generator that yields the biggest files (name not path) first.
    This is fairly simple in that it it only looks the current directory not
    only sub-directories. Useful for multiprocessing."""
    fileSizeS = []
    for n in os.listdir(d):
        p = os.path.join(d, n)
        if os.path.isfile(p):
            fileSizeS.append((os.path.getsize(p), n))

    for _s, n in reversed(sorted(fileSizeS)):
        yield n


def dirWalk(theIn, theOut=None, theFnMatch=None, recursive=False, bigFirst=False):
    """Walks a directory tree generating file paths.

    *theIn*
        The input directory.

    *theOut*
        The output directory. If None then input file paths as strings
        will be generated If non-None this function will yield
        FileInOut(in, out) objects.
        NOTE: This does not create the output directory structure, it is up to
        the caller to do that.

    *theFnMatch*
        A glob like match pattern for file names (not tested for directory names).
        Can be a list of strings any of which can match. If None or empty list then all files match.

    *recursive*
        Boolean to recurse into directories or not.

    *bigFirst*
        If True then the largest files in  directory are given first. If False it is alphabetical.
    """

    def _matches(file_path, fn_match):
        if fn_match is None:
            return True
        else:
            if isinstance(fn_match, str):
                return fnmatch.fnmatch(file_path, fn_match)
            if isinstance(fn_match, list):
                return len(fn_match) == 0 or any([ fnmatch.fnmatch(file_path, v) for v in fn_match ])
            raise ValueError(('Can not process fn_match: {!r:s} of type {!r:s}').format(fn_match, type(fn_match)))
            return

    if not os.path.isdir(theIn):
        raise ExceptionDirWalk(('{:s} is not a directory.').format(theIn))
    if bigFirst:
        for fn in genBigFirst(theIn):
            fp = os.path.join(theIn, fn)
            if _matches(fp, theFnMatch):
                if theOut is None:
                    yield fp
                else:
                    yield FileInOut(fp, os.path.join(theOut, fn))

        if recursive:
            for n in os.listdir(theIn):
                fp = os.path.join(theIn, n)
                if os.path.isdir(fp):
                    if theOut is None:
                        outP = None
                    else:
                        outP = os.path.join(theOut, n)
                    for aFp in dirWalk(fp, outP, theFnMatch, recursive, bigFirst):
                        yield aFp

    else:
        for fn in os.listdir(theIn):
            fp = os.path.join(theIn, fn)
            if os.path.isfile(fp) and _matches(fp, theFnMatch):
                if theOut is None:
                    yield fp
                else:
                    yield FileInOut(fp, os.path.join(theOut, fn))
            elif os.path.isdir(fp) and recursive:
                if theOut is None:
                    outP = None
                else:
                    outP = os.path.join(theOut, fn)
                for aFp in dirWalk(fp, outP, theFnMatch, recursive):
                    yield aFp

    return