# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tonio/sources/odooselenium/odooselenium/api.py
# Compiled at: 2016-12-06 01:58:53
"""API shortcuts.

Everything declared (or imported) in this module is exposed in
:mod:`odooselenium` root package, i.e. available when one does
``import odooselenium``.

Here are the motivations of such an "api" module:

* as a `odooselenium` library user, in order to use the library, I just do
  ``import odooselenium``. It is enough for most use cases. I do not need to
  bother with more library's internals. I know this API will be maintained,
  documented, and not deprecated/refactored without notice.

* as a `odooselenium` library developer, in order to maintain the API, I focus
  on things declared in :mod:`odooselenium.api`. It is enough. It is required.
  I take care of this API. If there is a change in this API between consecutive
  releases, then I use :class:`DeprecationWarning` and I mention it in release
  notes.

It also means that things not exposed in :mod:`odooselenium.api` are not part
of the deprecation policy. They can be moved, changed, removed without notice.

"""
from odooselenium.test import TestCase
from odooselenium.ui import OdooUI