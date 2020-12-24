# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/compat.py
# Compiled at: 2015-02-07 04:24:11
"""Run-time compatiblity helpers with third-party modules

For most standard library moves and discrepancies, you should use `six` instead
"""
from __future__ import absolute_import
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from subprocess import check_output
except ImportError:
    import subprocess

    def check_output(args, stdin=None, stderr=None, shell=False, universal_newlines=False):
        """Mostly compatible `check_output` for python2.6"""
        p = subprocess.Popen(args, stdin=stdin, stderr=stderr, shell=shell, universal_newlines=universal_newlines)
        output, stderr = p.communicate()
        returncode = p.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd=args, output=output)
        return output


import logging, sys
if sys.version >= '2.7':
    captureWarnings = logging.captureWarnings
else:
    import warnings
    _warnings_showwarning = None

    def _showwarning(message, category, filename, lineno, file=None, line=None):
        """
        Implementation of showwarnings which redirects to logging, which will first
        check to see if the file parameter is None. If a file is specified, it will
        delegate to the original warnings implementation of showwarning. Otherwise,
        it will call warnings.formatwarning and will log the resulting string to a
        warnings logger named "py.warnings" with level logging.WARNING.
        """
        global _warnings_showwarning
        if file is not None:
            if _warnings_showwarning is not None:
                _warnings_showwarning(message, category, filename, lineno, file, line)
        else:
            s = warnings.formatwarning(message, category, filename, lineno, line)
            logger = logging.getLogger('py.warnings')
            if not logger.handlers:
                logger.addHandler(logging.NullHandler())
            logger.warning('%s', s)
        return


    def captureWarnings(capture):
        """
        If capture is true, redirect all warnings to the logging package.
        If capture is False, ensure that warnings are not redirected to logging
        but to their original destinations.
        """
        global _warnings_showwarning
        if capture:
            if _warnings_showwarning is None:
                _warnings_showwarning = warnings.showwarning
                warnings.showwarning = _showwarning
        elif _warnings_showwarning is not None:
            warnings.showwarning = _warnings_showwarning
            _warnings_showwarning = None
        return