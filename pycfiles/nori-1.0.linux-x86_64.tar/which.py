# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nori/which.py
# Compiled at: 2013-10-03 18:50:13
"""
Backport of Python 3.3's shutil.which().
Requires 2.6+, for sets.
"""
import sys
if sys.hexversion >= 50528256:
    from shutil import which
else:
    import os

    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.

        `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.

        """

        def _access_check(fn, mode):
            return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)

        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return
        if path is None:
            path = os.environ.get('PATH', os.defpath)
        if not path:
            return
        else:
            path = path.split(os.pathsep)
            if sys.platform == 'win32':
                if os.curdir not in path:
                    path.insert(0, os.curdir)
                pathext = os.environ.get('PATHEXT', '').split(os.pathsep)
                if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                    files = [
                     cmd]
                else:
                    files = [ cmd + ext for ext in pathext ]
            else:
                files = [
                 cmd]
            seen = set()
            for dir in path:
                normdir = os.path.normcase(dir)
                if normdir not in seen:
                    seen.add(normdir)
                    for thefile in files:
                        name = os.path.join(dir, thefile)
                        if _access_check(name, mode):
                            return name

            return