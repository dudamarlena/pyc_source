# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/site.py
# Compiled at: 2019-09-28 16:02:16
# Size of source mod 2**32: 2897 bytes
import json
from dataclasses import dataclass
from enum import Enum
from typing import List
from werkzeug.utils import cached_property
RoleType = Enum('RoleType', ['manager', 'staff'])
role_names = {RoleType.manager: 'kierownik', 
 RoleType.staff: 'pracownik'}

@dataclass
class Address:
    __slots__ = [
     'street', 'zip_code', 'town']
    street: str
    zip_code: str
    town: str

    @cached_property
    def display_value(self):
        return f"{self.street}, {self.zip_code} {self.town}"


@dataclass
class Contact:
    phone: str
    email: str
    name = ''
    name: str

    @cached_property
    def basic_information(self):
        return [
         (
          'nazwa', self.name),
         (
          'telefon', self.phone),
         (
          'email', self.email)]


@dataclass
class StaffMember:
    role_name: str
    role_type: RoleType
    person_name: str
    photo_url = ''
    photo_url: str
    phone = ''
    phone: str
    email = ''
    email: str

    @cached_property
    def basic_information(self):
        return (
         (
          'nazwisko', self.person_name),
         (
          'stanowisko', self.role_name),
         (
          'telefon', self.phone),
         (
          'email', self.email))


@dataclass
class Department:
    name: str
    staff: List[StaffMember]
    domain = ''
    domain: str
    location = ''
    location: str
    phone = ''
    phone: str
    email = ''
    email: str

    @classmethod
    def from_dict(cls, d):
        staff = [StaffMember(**s) for s in d.pop('staff', [])]
        return cls(staff=staff, **d)

    @cached_property
    def basic_information(self):
        return (
         (
          'nazwa', self.name),
         (
          'zakres działalności', self.domain),
         (
          'lokalizacja', self.location),
         (
          'telefon', self.phone),
         (
          'email', self.email))


@dataclass
class Site:
    name: str
    short_name: str
    address: Address
    contacts: List[Contact]
    departments: List[Department]
    bip_url = ''
    bip_url: str
    NIP = ''
    NIP: str
    REGON = ''
    REGON: str
    KRS = ''
    KRS: str

    @classmethod
    def from_json(cls, s):
        return cls.from_dict(json.loads(s, encoding='utf-8'))

    @classmethod
    def from_dict(cls, d):
        address = Address(**d.pop('address'))
        contacts = [Contact(**c) for c in d.pop('contacts')]
        departments = [Department.from_dict(data) for data in d.pop('departments')]
        return cls(address=address, contacts=contacts, departments=departments, **d)

    @cached_property
    def basic_information(self):
        data = [
         (
          'nazwa', self.name),
         (
          'NIP', self.NIP),
         (
          'REGON', self.REGON)]
        if self.KRS:
            data.append(('KRS', self.KRS))
        return data


def test_site():
    site = Site(name='Test Site',
      short_name='Test',
      address=Address(street='Street 1', zip_code='05-200', town='Test Town'),
      contacts=[],
      departments=[])
    return site