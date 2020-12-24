# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/domain_lang/models.py
# Compiled at: 2020-01-26 07:46:02
# Size of source mod 2**32: 1646 bytes
""" 
    django-domain-language is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import string
from django.conf import settings
from django.db import models
import django.utils.translation as _

def _simple_domain_name_validator(value):
    """
    Validate that the given value contains no whitespaces to prevent common
    typos.
    """
    checks = (s in value for s in string.whitespace)
    if any(checks):
        raise ValidationError((_('The domain name cannot contain any spaces or tabs.')),
          code='invalid')


class DomainLanguageMapping(models.Model):
    domain = models.CharField((_('domain name')),
      max_length=100,
      validators=[
     _simple_domain_name_validator],
      unique=True)
    language = models.CharField((_('language')), max_length=7, choices=(settings.LANGUAGES))

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = _('domain language mapping')
        verbose_name = _('domain language mappings')
        ordering = ['domain']