# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/acquisition.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node
from .utils import parse_date

@six.python_2_unicode_compatible
class Acquisition(Node):
    """Represents a Acquisition on CrunchBase"""
    KNOWN_PROPERTIES = [
     'api_path',
     'web_path',
     'price',
     'price_currency_code',
     'price_usd',
     'payment_type',
     'acquisition_type',
     'acquisition_status',
     'disposition_of_acquired',
     'announced_on',
     'announced_on_trust_code',
     'completed_on',
     'completed_on_trust_code',
     'created_at',
     'updated_at',
     'permalink']
    KNOWN_RELATIONSHIPS = [
     'acquirer',
     'acquiree']

    def _coerce_values(self):
        for attr in ['announced_on', 'completed_on']:
            if getattr(self, attr, None):
                setattr(self, attr, parse_date(getattr(self, attr)))

        return

    def __str__(self):
        return ('{acq_type} {status} {announced_on} ${price}').format(acq_type=self.acquisition_type, status=self.acquisition_status, announced_on=self.announced_on, price=self.price)

    def __repr__(self):
        return self.__str__()