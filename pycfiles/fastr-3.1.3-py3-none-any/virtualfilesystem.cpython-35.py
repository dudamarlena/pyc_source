# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/virtualfilesystem.py
# Compiled at: 2018-10-10 10:24:25
# Size of source mod 2**32: 2861 bytes
"""
This module contains the virtual file system code. This is internally
used object as used as base class for the IOPlugin.
"""
from fastr.core.vfs import VirtualFileSystem
from fastr.core.ioplugin import IOPlugin

class VirtualFileSystem(VirtualFileSystem, IOPlugin):
    __doc__ = "\n    The virtual file system class. This is an IOPlugin, but also heavily used\n    internally in fastr for working with directories. The VirtualFileSystem\n    uses the ``vfs://`` url scheme.\n\n    A typical virtual filesystem url is formatted as ``vfs://mountpoint/relative/dir/from/mount.ext``\n\n    Where the ``mountpoint`` is defined in the :ref:`config-file`. A list of\n    the currently known mountpoints can be found in the ``fastr.config`` object\n\n    .. code-block:: python\n\n        >>> fastr.config.mounts\n        {'example_data': '/home/username/fastr-feature-documentation/fastr/fastr/examples/data',\n         'home': '/home/username/',\n         'tmp': '/home/username/FastrTemp'}\n\n    This shows that a url with the mount ``home`` such as\n    ``vfs://home/tempdir/testfile.txt`` would be translated into\n    ``/home/username/tempdir/testfile.txt``.\n\n    There are a few default mount points defined by Fastr (that can be changed\n    via the config file).\n\n    +--------------+-----------------------------------------------------------------------------+\n    | mountpoint   | default location                                                            |\n    +==============+=============================================================================+\n    | home         | the users home directory (:py:func:`expanduser('~/') <os.path.expanduser>`) |\n    +--------------+-----------------------------------------------------------------------------+\n    | tmp          | the fastr temprorary dir, defaults to ``tempfile.gettempdir()``             |\n    +--------------+-----------------------------------------------------------------------------+\n    | example_data | the fastr example data directory, defaults ``$FASTRDIR/example/data``       |\n    +--------------+-----------------------------------------------------------------------------+\n\n    "
    scheme = 'vfs'