# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/domain_lang/middleware.py
# Compiled at: 2020-01-26 07:46:02
# Size of source mod 2**32: 1463 bytes
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
from django.utils import translation
from domain_lang.models import DomainLanguageMapping

class DomainLanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.META.get('HTTP_HOST', '')
        query = DomainLanguageMapping.objects.filter(domain=domain)
        if query.exists():
            mapping = query[0]
            translation.activate(mapping.language)
        response = self.get_response(request)
        return response