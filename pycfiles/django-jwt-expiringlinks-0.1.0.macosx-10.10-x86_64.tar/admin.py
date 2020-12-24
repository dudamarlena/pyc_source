# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-jwt/lib/python2.7/site-packages/django_jwt/admin.py
# Compiled at: 2015-12-28 14:13:54
"""django_jwt admin models."""
import datetime, json
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.timezone import now as tz_now
from django_jwt.models import RequestToken, RequestTokenLog

def pretty_print(data):
    """Convert dict into formatted HTML."""
    if data is None:
        return
    else:
        pretty = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        return mark_safe('<code>%s</code>' % pretty.replace(' ', '&nbsp;'))


class RequestTokenAdmin(admin.ModelAdmin):
    """Admin model for RequestToken objects."""
    list_display = ('user', 'target_url', 'not_before_time', 'expiration_time', 'max_uses',
                    'used_to_date', 'issued_at', 'is_valid')
    readonly_fields = ('pretty_payload', 'jwt', 'issued_at')
    search_fields = ('user__first_name', 'user__username')

    def pretty_payload(self, obj):
        return pretty_print(obj.payload)

    pretty_payload.short_description = 'Payload'

    def jwt(self, obj):
        return obj.encode()

    jwt.short_description = 'JWT'

    def is_valid(self, obj):
        """Validate the time window and usage."""
        now = tz_now()
        return now > (obj.not_before_time or datetime.datetime.min) and now < (obj.expiration_time or datetime.datetime.max) and obj.used_to_date < obj.max_uses

    is_valid.boolean = True


admin.site.register(RequestToken, RequestTokenAdmin)