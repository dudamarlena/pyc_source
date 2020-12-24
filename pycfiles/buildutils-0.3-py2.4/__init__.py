# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/__init__.py
# Compiled at: 2007-08-08 19:58:56
"""Distutils extensions for developing Python libraries and applications.

The `buildutils` package contains extensions to Python's standard
distribution utilities (`distutils`) that are often useful during the
development of Python projects. `buildutils` was created to scratch an
itch: removing ``make`` from the Python development process and partially
to gain a better understanding of how `distutils` works.

The following extension commands are included:

announce
  send a release announcement to mailing lists
  like python-announce-list@python.org
checksum
  generate MD5 and SHA-1 checksum files for distributables.
etags
  generate an TAGS file over all packages and module (for use in Emacs).
flakes
  find lint using the pyflakes utility.
info
  dumps information about the project.
publish
  push distributables and documentation up to a project site using
  ssh/scp/sftp.
pudge
  build Python documentation from restructured text documents and
  Python doc strings.
pytest
  run py.test unit tests.
stats
  dump statistics on the number of lines, files, modules, packages,
  etc.
svntag
  make a Subversion tag for a versioned release
use
  bring in a working version of a dependency (uses setuptools egg
  stuff).

"""
import buildutils.compat as compat, buildutils.command as command