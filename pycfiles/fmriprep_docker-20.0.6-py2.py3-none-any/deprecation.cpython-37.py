# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_internal/utils/deprecation.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 3318 bytes
"""
A module that implements tooling to enable easy warnings about deprecations.
"""
from __future__ import absolute_import
import logging, warnings
from pip._vendor.packaging.version import parse
from pip import __version__ as current_version
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Optional
DEPRECATION_MSG_PREFIX = 'DEPRECATION: '

class PipDeprecationWarning(Warning):
    pass


_original_showwarning = None

def _showwarning(message, category, filename, lineno, file=None, line=None):
    global _original_showwarning
    if file is not None:
        if _original_showwarning is not None:
            _original_showwarning(message, category, filename, lineno, file, line)
    elif issubclass(category, PipDeprecationWarning):
        logger = logging.getLogger('pip._internal.deprecations')
        logger.warning(message)
    else:
        _original_showwarning(message, category, filename, lineno, file, line)


def install_warning_logger():
    global _original_showwarning
    warnings.simplefilter('default', PipDeprecationWarning, append=True)
    if _original_showwarning is None:
        _original_showwarning = warnings.showwarning
        warnings.showwarning = _showwarning


def deprecated(reason, replacement, gone_in, issue=None):
    """Helper to deprecate existing functionality.

    reason:
        Textual reason shown to the user about why this functionality has
        been deprecated.
    replacement:
        Textual suggestion shown to the user about what alternative
        functionality they can use.
    gone_in:
        The version of pip does this functionality should get removed in.
        Raises errors if pip's current version is greater than or equal to
        this.
    issue:
        Issue number on the tracker that would serve as a useful place for
        users to find related discussion and provide feedback.

    Always pass replacement, gone_in and issue as keyword arguments for clarity
    at the call site.
    """
    sentences = [
     (
      reason, DEPRECATION_MSG_PREFIX + '{}'),
     (
      gone_in, 'pip {} will remove support for this functionality.'),
     (
      replacement, 'A possible replacement is {}.'),
     (
      issue,
      'You can find discussion regarding this at https://github.com/pypa/pip/issues/{}.')]
    message = ' '.join((template.format(val) for val, template in sentences if val is not None))
    if gone_in is not None:
        if parse(current_version) >= parse(gone_in):
            raise PipDeprecationWarning(message)
    warnings.warn(message, category=PipDeprecationWarning, stacklevel=2)