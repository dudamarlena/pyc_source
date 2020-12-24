# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/external_services/mailchimp/client.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1678 bytes
from typing import Iterable
from constance import config

class MailchimpIsNotSetException(Exception):
    pass


class MailChimpClient:
    __doc__ = '\n    Helper class to communicate with MailChimp.\n    '

    def __init__(self) -> None:
        """
        Checking if MailChimp API key and username is configured and return a MailChimp API client.
        """
        username = config.MAILCHIMP_USERNAME
        api_key = config.MAILCHIMP_API_KEY
        if api_key:
            if username:
                from mailchimp3 import MailChimp
                self.client = MailChimp(username, api_key)
        else:
            raise MailchimpIsNotSetException('API key or username for mailchimp is not set.')

    def get_lists(self) -> Iterable[str]:
        """
        :return: List of lists with fields ``id`` and ``name``.
        """
        return self.client.lists.all(get_all=True, fields='lists.name,lists.id')

    def subscribe(self, mailing_list_id, email, first_name, last_name) -> None:
        """
        Add a subscriber and return the id (subscriber_hash).
        """
        new_subscriber = self.client.lists.members.create(mailing_list_id, {'email_address':email, 
         'status':'subscribed', 
         'merge_fields':{'FNAME':first_name, 
          'LNAME':last_name}})
        return new_subscriber['id']

    def unsubscribe(self, mailing_list_id, subscriber_hash) -> None:
        """
        Remove a subscriber.
        """
        self.client.lists.members.delete(mailing_list_id, subscriber_hash)