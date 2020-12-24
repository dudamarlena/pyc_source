# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyWhatCounts/Wrapper.py
# Compiled at: 2009-05-13 06:43:54
"""
This is a Python wrapper of WhatCounts' Web API.

We're coming from the perspective of a single non-administrative user trying
(non-transparently) to administrate his relationship with a WC realm, so most of
these commands are limited to single user operations, even though WC provides
more flexibility.

There is a good deal of (somewhat brittle) error checking based on the current
responses expected from WC.  The tests are reasonably thorough to facilitate
rapid responses to external changes in the API.  Three custom exceptions deal
with a range of error responses that we anticipate encountering.

For more info on setup pre-requisites, pls consult the README.

"""
import urllib, csv
from exceptions import WCAuthError, WCUserError, WCSystemError
from config import *

class WCWrapper:
    """A Python wrapper for WhatCounts' Web API"""
    realm = ''
    key = ''

    def _setConnectionInfo(self, realm, key):
        """ Sets realm and key.  Might be overridden"""
        self.realm = realm
        self.key = key

    def _getConnectionInfo(self):
        """ Returns realm and key.  Probably should be overridden"""
        return (
         self.realm, self.key)

    def _constructURL(self, cmd, realm, pwd, **kw):
        """ Returns the appropriate url with query string for a WC command.

        Queries to WC's Web API go to the same URL; the query string determines
        what happens.  They all require a command, realm, and pwd; other args
        passed in as keywords get inserted into the query string as you would expect."""
        wc_url = 'http://whatcounts.com/bin/api_web'
        qs = 'cmd=%s&realm=%s&pwd=%s&' % (cmd, realm, pwd)
        for key in kw.keys():
            qs += '%s=%s&' % (key, kw[key])

        return '%s?%s' % (wc_url, qs)

    def _validateResponseWasAuthorized(self, response):
        """Returns True iff realm and api key seemed to be ok else raises
        WCUserAuth error with a friendly account of what was wrong.

        If WC doesn't recognize the realm, it will return something like:
        FAILURE: Unable to determine customer account (realm)

        If WC hasn't authorized API access for that realm, it will return:
        FAILURE: Unable to acquire API user credentials through API User Manager.

        If the key (in this case, "wrong-password") is wrong for the realm, it
        will return something like:
        FAILURE: Password (wrong-password) doesn't match entry for API user credentials in database or 216.65.145.194 isn't an approved IP
        """
        if not response or not isinstance(response, str):
            return True
        elif response.startswith(ERROR_BAD_REALM):
            raise WCAuthError, EXC_INVALID_REALM
        elif response.startswith(ERROR_NO_API_FOR_REALM):
            raise WCAuthError, EXC_API_NOT_AUTHORIZED
        elif ERROR_RE_BAD_KEY.match(response):
            raise WCAuthError, EXC_INVALID_KEY
        else:
            return True

    def _findUser(self, email):
        """ Helper method to returns WC's UID for a user keyed off of an email address.

        WC does most of it's keying off of UID, but most people just know users'
        email addresses.

        "find" command (in csv format) returns:
        "<UID>","<Email>","<First Name>","<Last Name>","<Comma-sep list of list_ids user is sub'ed to>"

        We return a dict of {field: value} if successful.  Otherwise we raise exceptions.
        Field names: "subscriber_id","email","first","last","lists".
        We parse "lists" into an actual list of list_ids.

        If you don't specify an email, WC returns EVERYONE.  We're not checking
        for that now (we might later).  TAKES A LONG TIME.

        Errors:
        User not found: WC returns blank page. Raise WCUserError.
        Bad auth: WC returns a FAILURE msg; raise WCAuthError
        """
        (realm, key) = self._getConnectionInfo()
        kw = {'email': email, 'output_format': 'csv', 'headers': '1'}
        url = self._constructURL('find', realm, key, **kw)
        wc_response = urllib.urlopen(url).readlines()
        self._validateResponseWasAuthorized(wc_response)
        if wc_response:
            reader = csv.reader(wc_response)
            headers = reader.next()
            data = reader.next()
            res = {}
            for i in range(len(headers)):
                res[headers[i]] = data[i]

            if res.has_key('lists'):
                res['lists'] = res['lists'].split(',')
            return res
        else:
            raise WCUserError, EXC_BAD_USER + ' (%s)' % email

    def _deleteUser(self, email):
        """Permanently deletes a single user from WC.

        ONLY for facillitating disposable dummy users in the test suite.
        *** USE CAREFULLY!!! ***

        For a successful deletion, WC returns: 'SUCCESS: 1 record(s) processed. 1 users deleted.'
        Unsuccessful deletion WC returns: 'SUCCESS: 1 record(s) processed. 0 users deleted.'

        We return True on successful deletion of a single user.
        If the user doesn't exists, we raise a WCUserError.
        If authorization (in some way) fails, we raise a WCAuthError.
        In all other cases we raise a WCSystemError.
        """
        (realm, key) = self._getConnectionInfo()
        url = self._constructURL('delete', realm, key, **{'data': 'email^%s' % email})
        wc_response = urllib.urlopen(url).readline()
        self._validateResponseWasAuthorized(wc_response)
        if not wc_response:
            raise WCSystemError, EXC_MISSING_RESPONSE + ' (while trying to delete user "%s")' % email
        elif wc_response.startswith('SUCCESS'):
            return True
        elif wc_response.startswith('FAILURE'):
            reason = wc_response.split(':')[(-1)].strip()
            raise WCUserError, reason
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' "%s" (while trying to delete user "%s")' % (wc_response, email)
        return True

    def subscribeUser(self, email, list_id, force_sub='1'):
        """Subscribe a user to a single list.

        We're not checking for valid email or list_id going in, but we'll check
        the response coming out of WC.

        We set force_sub so that users get signed up even if they had been
        *deleted* from the realm.  (Set mostly to ensure testing works.)

        Possible WC error messages (<angles> denote variables of some kind):

        Bad email address: (raises WCUserError)
        FAILURE: 1 record(s) processed. 0 users subscribed to list(s) <list_id> (0 total subscriptions)

        Bad list: (raises WCUserError)
        FAILURE: Error looking up list ids, one or more list ids specified do not belong to your realm
        """
        (realm, key) = self._getConnectionInfo()
        kw = {'data': 'email^%s' % email, 'list_id': list_id, 'force_sub': force_sub}
        url = self._constructURL('subscribe', realm, key, **kw)
        wc_response = urllib.urlopen(url).readline()
        self._validateResponseWasAuthorized(wc_response)
        if not wc_response:
            raise WCSystemError, EXC_MISSING_RESPONSE + ' (while trying to subscribe "%s" to list %s)' % (email, list_id)
        elif wc_response.startswith(ERROR_BAD_LIST):
            raise WCUserError, EXC_BAD_LIST + ' (while trying to subscribe "%s" to list %s)' % (email, list_id)
        elif wc_response.startswith('SUCCESS'):
            return True
        elif wc_response.startswith('FAILURE'):
            reason = wc_response.split(':')[(-1)].strip()
            raise WCUserError, reason
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' "%s" (while trying to subscribe "%s" to list %s)' % (wc_response, email, list_id)
        return True

    def unsubscribeUser(self, email, list_id):
        """Unsubscribe a single user from a single list.

        Note that even if the user is no longer subscribed to any lists in this
        realm, they should still exist in the system.
        """
        (realm, key) = self._getConnectionInfo()
        kw = {'data': 'email^%s' % email, 'list_id': list_id}
        url = self._constructURL('unsubscribe', realm, key, **kw)
        wc_response = urllib.urlopen(url).readline()
        self._validateResponseWasAuthorized(wc_response)
        if not wc_response:
            raise WCSystemError, EXC_MISSING_RESPONSE + ' (while trying to unsubscribe "%s" from list %s)' % (email, list_id)
        elif wc_response.startswith(ERROR_BAD_LIST):
            raise WCUserError, EXC_BAD_LIST + ' (while trying to subscribe "%s" to list %s)' % (email, list_id)
        elif wc_response.startswith('SUCCESS'):
            match = RE_UNSUBSCRIBED.search(wc_response)
            if match is None:
                raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' "%s" (while trying to unsubscribe "%s" from list %s)' % (wc_response, email, list_id)
            groups = match.groupdict()
            if groups['unsubscribed'] == '0':
                raise WCUserError, EXC_PROBLEM_UNSUB + 'this user (%s), if it even existed, was not subscribed to this list (%s)' % (email, list_id)
            return True
        elif wc_response.startswith('FAILURE'):
            reason = wc_response.split(':')[(-1)].strip()
            raise WCUserError, reason
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' "%s" (while trying to unsubscribe "%s" from list %s)' % (wc_response, email, list_id)
        return True

    def updateUser(self, email, list_id, **data):
        """Updates a single user's contact info EXCEPT for email address (see
        updateEmailAddress below).  We need a list id for reasons I'm not really
        clear on.  Data is a dictionary of WhatCounts field names and straight
        up values -- we handle what escaping needs to happen.

        While email is inexplicably required in the WC data query string arg (as
        well as on its own when we use it as the "identity field", we are not
        expecting users to pass it on as part of the "data" kw dictionary.  (It's
        ok if they do, though.)

        We return True if a user is updated; otherwise we raise exceptions.

        On success, WC returns "SUCCESS: 1 record(s) processed. 1 users updated."
        On most possible failures, WC returns simply "SUCCESS: 1 record(s)
        processed. 0 users updated."

        WC shouldn't protest if you supply non-existant fields.

        You should not have any trouble with values containing spaces or commas.
        Carets, on the other hand,  are not a good idea, although we're not
        checking for them (results unknown).

        """
        (realm, key) = self._getConnectionInfo()
        kw = {'identity_field': 'email', 'identity_value': email, 
           'list_id': list_id}
        field_names = []
        values = []
        if not data.has_key('email'):
            data['email'] = email
        for f in data.keys():
            field_names.append(f)
            values.append(urllib.quote_plus('"%s"' % data[f]))

        kw['data'] = '%s^%s' % ((',').join(field_names), (',').join(values))
        url = self._constructURL('update', realm, key, **kw)
        wc_response = urllib.urlopen(url).readline()
        self._validateResponseWasAuthorized(wc_response)
        if not wc_response:
            raise WCSystemError, EXC_MISSING_RESPONSE + ' (while trying to update info for "%s" )' % email
        elif wc_response.startswith('SUCCESS'):
            match = RE_UPDATED.search(wc_response)
            if match is None:
                raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' (while trying to update info for "%s" )' % email
            groups = match.groupdict()
            if groups['updated'] == '0':
                raise WCUserError, EXC_PROBLEM_UPDATE + ' (while trying to update info for "%s" )' % email
            return True
        elif wc_response.startswith('FAILURE'):
            reason = wc_response.split(':')[(-1)].strip()
            raise WCUserError, reason
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' (while trying to update info for "%s" )' % email
        return

    def updateEmailAddress(self, email_old, email_new):
        """ Changes a single subscriber's email address with WhatCount's change command.
        """
        (realm, key) = self._getConnectionInfo()
        kw = {'email': email_old, 'email_new': email_new}
        url = self._constructURL('change', realm, key, **kw)
        wc_response = urllib.urlopen(url).readline()
        self._validateResponseWasAuthorized(wc_response)
        if not wc_response:
            raise WCSystemError, EXC_MISSING_RESPONSE + ' (while trying to update the email address for "%s" )' % email_old
        elif wc_response.startswith(ERROR_NO_SUCH_USER):
            raise WCUserError, EXC_BAD_USER + ' (%s)' % email_old
        elif wc_response.startswith('FAILURE: %s does not appear to be a valid email address' % email_old):
            raise WCUserError, EXC_BAD_EMAIL + ' (%s)' % email_new
        elif wc_response.startswith('SUCCESS'):
            return True
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' "%s" (while trying to change the email address for  "%s")' % (wc_response, email_old)

    def showLists(self):
        """Returns all available lists for a specific WhatCounts realm.

        Returns a list of pairs of (list id, list name)
        (i.e.: [['123, 'My list'],['153', 'My other list'],])
        """
        (realm, key) = self._getConnectionInfo()
        kw = {'output_format': 'csv'}
        url = self._constructURL('show_lists', realm, key, **kw)
        wc_response = urllib.urlopen(url).readlines()
        self._validateResponseWasAuthorized(wc_response[0])
        if wc_response:
            reader = csv.reader(wc_response)
            return [ line for line in reader ]
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + " (while trying to get list of realm's (%s) lists)" % realm

    def getUserDetails(self, email):
        """Returns contact info and custom fields for a single user in a dictionary
        mapping field names to values.
        """
        (realm, key) = self._getConnectionInfo()
        subscriber_id = self._findUser(email)['subscriber_id']
        kw = {'output_format': 'csv', 'headers': '1', 'subscriber_id': subscriber_id}
        url = self._constructURL('detail', realm, key, **kw)
        wc_response = urllib.urlopen(url).readlines()
        self._validateResponseWasAuthorized(wc_response)
        if wc_response:
            reader = csv.reader(wc_response)
            headers = reader.next()
            data = reader.next()
            res = {}
            for i in range(len(headers)):
                res[headers[i]] = data[i]

            return res
        else:
            raise WCSystemError, EXC_UNEXPECTED_RESPONSE + ' (while trying to get user info on %s)' % email