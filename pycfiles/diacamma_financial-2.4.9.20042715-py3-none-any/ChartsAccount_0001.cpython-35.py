# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/financial/diacamma/accounting/printmodel/ChartsAccount_0001.py
# Compiled at: 2020-03-20 14:10:57
# Size of source mod 2**32: 1265 bytes
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
from diacamma.accounting.models import ChartsAccount
name = _('listing')
kind = 0
modelname = ChartsAccount.get_long_name()
value = '210\n297\n10//%s//#code\n25//%s//#name\n15//%s//#last_year_total\n15//%s//#current_total\n15//%s//#current_validated\n' % (_('code'), _('name'), _('total of last year'), _('total current'), _('total validated'))