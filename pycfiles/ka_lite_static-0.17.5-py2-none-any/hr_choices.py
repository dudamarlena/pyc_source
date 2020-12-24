# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/localflavor/hr/hr_choices.py
# Compiled at: 2018-07-11 18:15:30
"""
Sources:
    Croatian Counties: http://en.wikipedia.org/wiki/ISO_3166-2:HR

    Croatia doesn't have official abbreviations for counties.
    The ones provided are in common use.
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
HR_COUNTY_CHOICES = (
 (
  b'GZG', _(b'Grad Zagreb')),
 (
  b'BBŽ', _(b'Bjelovarsko-bilogorska županija')),
 (
  b'BPŽ', _(b'Brodsko-posavska županija')),
 (
  b'DNŽ', _(b'Dubrovačko-neretvanska županija')),
 (
  b'IŽ', _(b'Istarska županija')),
 (
  b'KŽ', _(b'Karlovačka županija')),
 (
  b'KKŽ', _(b'Koprivničko-križevačka županija')),
 (
  b'KZŽ', _(b'Krapinsko-zagorska županija')),
 (
  b'LSŽ', _(b'Ličko-senjska županija')),
 (
  b'MŽ', _(b'Međimurska županija')),
 (
  b'OBŽ', _(b'Osječko-baranjska županija')),
 (
  b'PSŽ', _(b'Požeško-slavonska županija')),
 (
  b'PGŽ', _(b'Primorsko-goranska županija')),
 (
  b'SMŽ', _(b'Sisačko-moslavačka županija')),
 (
  b'SDŽ', _(b'Splitsko-dalmatinska županija')),
 (
  b'ŠKŽ', _(b'Šibensko-kninska županija')),
 (
  b'VŽ', _(b'Varaždinska županija')),
 (
  b'VPŽ', _(b'Virovitičko-podravska županija')),
 (
  b'VSŽ', _(b'Vukovarsko-srijemska županija')),
 (
  b'ZDŽ', _(b'Zadarska županija')),
 (
  b'ZGŽ', _(b'Zagrebačka županija')))
HR_LICENSE_PLATE_PREFIX_CHOICES = (
 ('BJ', 'BJ'),
 ('BM', 'BM'),
 ('ČK', 'ČK'),
 ('DA', 'DA'),
 ('DE', 'DE'),
 ('DJ', 'DJ'),
 ('DU', 'DU'),
 ('GS', 'GS'),
 ('IM', 'IM'),
 ('KA', 'KA'),
 ('KC', 'KC'),
 ('KR', 'KR'),
 ('KT', 'KT'),
 ('KŽ', 'KŽ'),
 ('MA', 'MA'),
 ('NA', 'NA'),
 ('NG', 'NG'),
 ('OG', 'OG'),
 ('OS', 'OS'),
 ('PU', 'PU'),
 ('PŽ', 'PŽ'),
 ('RI', 'RI'),
 ('SB', 'SB'),
 ('SK', 'SK'),
 ('SL', 'SL'),
 ('ST', 'ST'),
 ('ŠI', 'ŠI'),
 ('VK', 'VK'),
 ('VT', 'VT'),
 ('VU', 'VU'),
 ('VŽ', 'VŽ'),
 ('ZD', 'ZD'),
 ('ZG', 'ZG'),
 ('ŽU', 'ŽU'))
HR_PHONE_NUMBER_PREFIX_CHOICES = (
 ('1', '01'),
 ('20', '020'),
 ('21', '021'),
 ('22', '022'),
 ('23', '023'),
 ('31', '031'),
 ('32', '032'),
 ('33', '033'),
 ('34', '034'),
 ('35', '035'),
 ('40', '040'),
 ('42', '042'),
 ('43', '043'),
 ('44', '044'),
 ('47', '047'),
 ('48', '048'),
 ('49', '049'),
 ('51', '051'),
 ('52', '052'),
 ('53', '053'),
 ('91', '091'),
 ('92', '092'),
 ('95', '095'),
 ('97', '097'),
 ('98', '098'),
 ('99', '099'))