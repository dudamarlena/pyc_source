# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svdgraaf/Projects/nl.focusmedia/lib/python2.7/site-packages/eloqua/models.py
# Compiled at: 2013-03-01 07:45:03
from django.db import models
from eloqua.exceptions import ObjectNotFound
from eloqua import settings
from datetime import datetime, timedelta
import json
try:
    from django.contrib.auth import get_user_model
    user_model = django.contrib.auth.get_user_model()
except:
    from django.contrib.auth.models import User
    user_model = User

class Contact(models.Model):
    user = models.OneToOneField(user_model, related_name='eloqua_profile')
    contact_id = models.PositiveIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.TextField(null=True)
    _profile = None
    _contact_fields = {}

    def _fetch_profile(self):
        timeout = settings.PROFILE_TIMEOUT
        delta = timedelta(minutes=timeout)
        if self.data == None or datetime.now() - delta > self.updated_at:
            from eloqua.clients import EloquaClient
            e = EloquaClient()
            if self.contact_id == None:
                results = e.contacts.search(self.user.email)
                if len(results) > 0:
                    data = results['elements'][0]
            else:
                results = e.contacts.get(self.contact_id)
                data = results
            self.data = json.dumps(data)
            if 'contact_id' in data:
                self.contact_id = data['content_id']
            self.save()
        data = json.loads(self.data)
        self._profile = data
        fields = {}
        for field in data['fieldValues']:
            if 'value' in field:
                fields[int(field['id'])] = field['value']

        self._contact_fields = fields
        return self._profile

    @property
    def first_name(self):
        profile = self._fetch_profile()
        return profile['firstName']

    @property
    def last_name(self):
        profile = self._fetch_profile()
        return profile['lastName']

    def value_for_field(self, pk):
        self._fetch_profile()
        if pk in self._contact_fields:
            return self._contact_fields[pk]
        raise ObjectNotFound(pk)


user_model.eloqua_profile = property(lambda u: Contact.objects.get_or_create(user=u)[0])