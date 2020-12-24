# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/printmodel/Adherent_0003.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 1844 bytes
"""
Printmodel django module for accounting

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2016 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from diacamma.member.models import Adherent
name = _('Complet listing')
kind = 0
modelname = Adherent.get_long_name()
value = '210\n297\n1//%s//#num\n1//%s//#lastname\n1//%s//#firstname\n1//%s//#address\n1//%s//#postal_code\n1//%s//#city\n1//%s//#tel1\n1//%s//#tel2\n1//%s//#email\n1//%s//#comment\n1//%s//#birthday\n1//%s//#birthplace\n1//%s//#current_subscription.season\n1//%s//#current_subscription.subscriptiontype\n1//%s//#current_subscription.begin_date\n1//%s//#current_subscription.end_date\n1//%s//#current_subscription.license_set.team\n1//%s//#current_subscription.license_set.activity\n1//%s//#current_subscription.license_set.value\n' % (_('numeros'), _('lastname'), _('firstname'), _('address'), _('postal code'), _('city'), _('tel1'), _('tel2'), _('email'),
 _('comment'), _('birthday'), _('birthplace'), _('season'), _('subscription type'), _('begin date'), _('end date'), _('team'), _('activity'), _('license #'))