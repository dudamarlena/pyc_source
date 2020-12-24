# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/deprecation.py
# Compiled at: 2020-02-11 04:03:56
"""Internal support for handling deprecations in Review Board.

The version-specific objects in this module are not considered stable between
releases, and may be removed at any point. The base objects are considered
stable.
"""
from __future__ import unicode_literals

class BaseRemovedInReviewBoardVersionWarning(DeprecationWarning):
    """Base class for a Review Board deprecation warning.

    All version-specific deprecation warnings inherit from this, allowing
    callers to check for Review Board deprecations without being tied to a
    specific version.
    """
    pass


class RemovedInReviewBoard40Warning(BaseRemovedInReviewBoardVersionWarning):
    """Deprecations for features removed in Review Board 4.0.

    Note that this class will itself be removed in Review Board 4.0. If you
    need to check against Review Board deprecation warnings, please see
    :py:class:`BaseRemovedInReviewBoardVersionWarning`. Alternatively, you
    can use the alias for this class,
    :py:data:`RemovedInNextReviewBoardVersionWarning`.
    """
    pass


RemovedInNextReviewBoardVersionWarning = RemovedInReviewBoard40Warning