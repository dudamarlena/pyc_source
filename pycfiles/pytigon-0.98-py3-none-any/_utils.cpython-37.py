# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/_utils.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 544 bytes
from .utils import CUR_OS, IS_WIN, IS_NIX, RE_ANSI, _range, _unich, _unicode, colorama, WeakSet, _basestring, _OrderedDict, FormatReplace, Comparable, SimpleTextIOWrapper, _is_utf, _supports_unicode, _is_ascii, _environ_cols_wrapper, _environ_cols_windows, _environ_cols_tput, _environ_cols_linux, _term_move_up
from .std import TqdmDeprecationWarning
from warnings import warn
warn('This function will be removed in tqdm==5.0.0\nPlease use `tqdm.utils.*` instead of `tqdm._utils.*`', TqdmDeprecationWarning,
  stacklevel=2)