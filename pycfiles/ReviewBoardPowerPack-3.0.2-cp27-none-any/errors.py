# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/errors.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

class CannotPostReviewRequestError(Exception):
    """Error indicating that a review request is not allowed to be posted."""

    def __init__(self, repo_type_name):
        """Initialize the error.

        Args:
            repo_type_name (unicode):
                The name of the type of repository that the user tried posting
                against.
        """
        super(CannotPostReviewRequestError, self).__init__(_(b'You are not licensed to post review requests against %s repositories. Please contact your system administrator.') % repo_type_name)