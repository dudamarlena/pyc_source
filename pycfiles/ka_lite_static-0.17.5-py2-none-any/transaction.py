# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/middleware/transaction.py
# Compiled at: 2018-07-11 18:15:30
from django.db import transaction

class TransactionMiddleware(object):
    """
    Transaction middleware. If this is enabled, each view function will be run
    with commit_on_response activated - that way a save() doesn't do a direct
    commit, the commit is done when a successful response is created. If an
    exception happens, the database is rolled back.
    """

    def process_request(self, request):
        """Enters transaction management"""
        transaction.enter_transaction_management()
        transaction.managed(True)

    def process_exception(self, request, exception):
        """Rolls back the database and leaves transaction management"""
        if transaction.is_dirty():
            transaction.rollback()
        transaction.leave_transaction_management()

    def process_response(self, request, response):
        """Commits and leaves transaction management."""
        if transaction.is_managed():
            if transaction.is_dirty():
                try:
                    transaction.commit()
                except Exception:
                    transaction.rollback()
                    transaction.leave_transaction_management()
                    raise

            transaction.leave_transaction_management()
        return response