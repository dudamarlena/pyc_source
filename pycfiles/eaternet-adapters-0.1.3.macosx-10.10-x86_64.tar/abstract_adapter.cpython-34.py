# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robb/src/adapters-python/venv/lib/python3.4/site-packages/eaternet/adapters/framework/abstract_adapter.py
# Compiled at: 2015-07-24 00:06:09
# Size of source mod 2**32: 1970 bytes
"""Every adapter for local restaurant inspection data implements these
interfaces.

This module contains one abstract class, ``AbstractAdapter``, which each
adapter implementation must inherit from. In a nutshell, an adapter (say, for
Multnomah County, Oregon) must only implement the four callback methods:
``businesses()``, ``inspections()``, ``violations()``, and
``violation_kinds()``.

Each of these methods returns an ``iterable`` of Data Transfer Objects. The
DTO's have a locked-down definition, here in this module. And so these classes,
all together, create a simple interface for application-level code.

"""
from abc import ABCMeta, abstractmethod
import collections

class AbstractAdapter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def businesses(self) -> collections.Iterable:
        pass

    @abstractmethod
    def inspections(self) -> collections.Iterable:
        pass

    @abstractmethod
    def violations(self) -> collections.Iterable:
        pass

    @abstractmethod
    def violation_kinds(self) -> collections.Iterable:
        pass


class BusinessData:

    def __init__(self, name, address, city, zipcode, orig_key):
        self.name = name
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.orig_key = orig_key


class InspectionData:

    def __init__(self, orig_key, business_orig_key, score, date):
        self.orig_key = orig_key
        self.business_orig_key = business_orig_key
        self.score = score
        self.date = date


class ViolationData:

    def __init__(self, orig_key, inspection_id, violation_kind_id):
        self.orig_key = orig_key
        self.inspection_id = inspection_id
        self.violation_kind_id = violation_kind_id


class ViolationKindData:

    def __init__(self, orig_key, code, demerits, description):
        self.orig_key = orig_key
        self.code = code
        self.demerits = demerits
        self.description = description