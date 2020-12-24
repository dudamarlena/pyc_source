# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/recharge/resources.py
# Compiled at: 2019-10-30 11:24:07
# Size of source mod 2**32: 6221 bytes
import logging, time
from urllib.parse import urlencode
import requests
log = logging.getLogger(__name__)

class RechargeResource(object):
    __doc__ = '\n    Resource from the Recharge API. This class handles\n    logging, sending requests, parsing JSON, and rate\n    limiting.\n\n    Refer to the API docs to see the expected responses.\n    https://developer.rechargepayments.com/\n    '
    base_url = 'https://api.rechargeapps.com'
    object_list_key = None

    def __init__(self, access_token=None, log_debug=False):
        self.log_debug = log_debug
        self.headers = {'Accept':'application/json', 
         'Content-Type':'application/json', 
         'X-Recharge-Access-Token':access_token}

    def log(self, url, response):
        if self.log_debug:
            log.info(url)
            log.info(response.headers['X-Recharge-Limit'])

    @property
    def url(self):
        return '{0}/{1}'.format(self.base_url, self.object_list_key)

    def http_delete(self, url):
        response = requests.delete(url, headers=(self.headers))
        log.info(url)
        log.info(response.headers['X-Recharge-Limit'])
        if response.status_code == 429:
            return self.http_delete(url)
        else:
            return response

    def http_get(self, url):
        response = requests.get(url, headers=(self.headers))
        self.log(url, response)
        if response.status_code == 429:
            time.sleep(1)
            return self.http_get(url)
        else:
            return response.json()

    def http_put(self, url, data):
        response = requests.put(url, json=data, headers=(self.headers))
        self.log(url, response)
        if response.status_code == 429:
            time.sleep(1)
            return self.http_put(url, data)
        else:
            return response.json()

    def http_post(self, url, data):
        response = requests.post(url, json=data, headers=(self.headers))
        self.log(url, response)
        if response.status_code == 429:
            time.sleep(1)
            return self.http_post(url, data)
        else:
            return response.json()

    def create(self, data):
        return self.http_post(self.url, data)

    def update(self, resource_id, data):
        return self.http_put('{0}/{1}'.format(self.url, resource_id), data)

    def get(self, resource_id):
        return self.http_get('{0}/{1}'.format(self.url, resource_id))

    def list(self, url_params=None):
        """
        The list method takes a dictionary of filter parameters.
        Refer to the recharge docs for available filters for
        each resource.
        """
        params = ''
        if url_params:
            params = '?' + urlencode(url_params, doseq=True)
        return self.http_get(self.url + params)


class RechargeAddress(RechargeResource):
    __doc__ = '\n    https://developer.rechargepayments.com/#addresses\n    '
    object_list_key = 'addresses'

    def apply_discount(self, address_id, discount_code):
        """ Apply a discount code to an address.
        https://developer.rechargepayments.com/#add-discount-to-address-new
        """
        return self.http_post('{0}/{1}/apply_discount'.format(self.url, address_id), {'discount_code': discount_code})

    def create(self, customer_id, data):
        """Create an address for the customer.
        https://developer.rechargepayments.com/#create-address
        """
        url = '{0}/customers/{1}/{2}'.format(self.base_url, customer_id, self.object_list_key)
        return self.http_post(url, data)


class RechargeCharge(RechargeResource):
    __doc__ = '\n    https://developer.rechargepayments.com/#charges\n    '
    object_list_key = 'charges'

    def change_next_charge_date(self, charge_id, to_date):
        """Change the date of a queued charge.
        https://developer.rechargepayments.com/#change-next-charge-date
        """
        return self.http_put('{0}/{1}/change_next_charge_date'.format(self.url, charge_id), {'next_charge_date': to_date})


class RechargeCheckout(RechargeResource):
    __doc__ = '\n    https://developer.rechargepayments.com/#checkouts\n    '
    object_list_key = 'checkouts'

    def charge(self, checkout_id, data):
        """Process (charge) a checkout.
        https://developer.rechargepayments.com/#process-checkout-beta
        """
        return self.http_post('{0}/{1}/charge'.format(self.url, checkout_id), data)


class RechargeCustomer(RechargeResource):
    __doc__ = '\n    https://developer.rechargepayments.com/#customers\n    '
    object_list_key = 'customers'


class RechargeOrder(RechargeResource):
    __doc__ = '\n    https://developer.rechargepayments.com/#orders\n    '
    object_list_key = 'orders'

    def change_date(self, order_id, to_date):
        """Change the date of a queued order.
        https://developer.rechargepayments.com/#change-order-date
        """
        return self.http_put('{0}/{1}/change_date'.format(self.url, order_id), {'scheduled_at': '{0}T00:00:00'.format(to_date)})

    def delete(self, order_id):
        """
        https://developer.rechargepayments.com/#delete-order-beta
        """
        return self.http_delete('{0}/{1}'.format(self.url, order_id))


class RechargeSubscription(RechargeResource):
    __doc__ = '\n    https://developer.rechargepayments.com/#subscriptions\n    '
    object_list_key = 'subscriptions'

    def cancel(self, subscription_id, reason='Other', send_email=False):
        """Cancel a subsciption.
        https://developer.rechargepayments.com/#cancel-subscription
        """
        return self.http_post('{0}/{1}/cancel'.format(self.url, subscription_id), {'cancellation_reason':reason, 
         'send_email':send_email})

    def set_next_charge_date(self, subscription_id, date):
        """Change the next charge date of a subscription
        https://developer.rechargepayments.com/#change-next-charge-date-on-subscription
        """
        return self.http_post('{0}/{1}/set_next_charge_date'.format(self.url, subscription_id), {'date': date})