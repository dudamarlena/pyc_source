# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/decorators.py
# Compiled at: 2017-06-19 17:22:36
# Size of source mod 2**32: 2097 bytes
from functools import wraps
from ovp_organizations.models import Organization
from ovp_projects import models

def hide_address(func):
    """ Used to decorate Serializer.to_representation method.
      It hides the address field if the Project has 'hidden_address' == True
      and the request user is neither owner or member of the organization """

    @wraps(func)
    def _impl(self, instance):
        if instance.hidden_address:
            for i, field in enumerate(self._readable_fields):
                if field.field_name == 'address':
                    address = self._readable_fields.pop(i)

            ret = func(self, instance)
            self._readable_fields.insert(i, address)
            request = self.context['request']
            is_organization_member = False
            try:
                if instance.organization is not None:
                    is_organization_member = request.user in instance.organization.members.all()
            except Organization.DoesNotExist:
                pass

            if request.user == instance.owner or is_organization_member:
                ret['address'] = self.fields['address'].to_representation(instance.address)
            else:
                ret['address'] = None
        else:
            ret = func(self, instance)
        return ret

    return _impl


def add_current_user_is_applied_representation(func):
    """ Used to decorate Serializer.to_representation method.
      It sets the field "current_user_is_applied" if the user is applied to the project
  """

    @wraps(func)
    def _impl(self, instance):
        ret = func(self, instance)
        user = self.context['request'].user
        applied = False
        if not user.is_anonymous():
            try:
                applied = models.Apply.objects.filter(user=user, project=instance).count() > 0
            except:
                pass

        ret['current_user_is_applied'] = applied
        return ret

    return _impl