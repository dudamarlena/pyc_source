# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/_utils.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 567 bytes
from .utils import CUR_OS, IS_WIN, IS_NIX, RE_ANSI, _range, _unich, _unicode, colorama, WeakSet, _basestring, _OrderedDict, FormatReplace, Comparable, SimpleTextIOWrapper, _is_utf, _supports_unicode, _is_ascii, _screen_shape_wrapper, _screen_shape_windows, _screen_shape_tput, _screen_shape_linux, _environ_cols_wrapper, _term_move_up
from .std import TqdmDeprecationWarning
from warnings import warn
warn('This function will be removed in tqdm==5.0.0\nPlease use `tqdm.utils.*` instead of `tqdm._utils.*`', TqdmDeprecationWarning,
  stacklevel=2)