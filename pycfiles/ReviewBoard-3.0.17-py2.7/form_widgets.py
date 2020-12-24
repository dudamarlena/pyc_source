# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/form_widgets.py
# Compiled at: 2020-02-11 04:03:56
"""Admin-specific form widgets."""
from __future__ import unicode_literals
import logging
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.template.loader import render_to_string
from django.utils import six
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from reviewboard.avatars import avatar_services
logger = logging.getLogger(__name__)

class RelatedUserWidget(HiddenInput):
    """A form widget to allow people to select one or more User relations.

    It's not unheard of to have a server with thousands or tens of thousands of
    registered users. In this case, the existing Django admin widgets fall down
    hard. The filtered select widgets can actually crash the webserver due to
    trying to pre-populate an enormous ``<select>`` element, and the raw ID
    widget is basically a write-only field.

    This field does much better, offering both the ability to see who's already
    in the list, as well as interactive search and filtering.
    """
    is_hidden = False

    def __init__(self, local_site_name=None, multivalued=True):
        """Initalize the RelatedUserWidget.

        Args:
            local_site_name (unicode, optional):
                The name of the LocalSite where the widget is being rendered.

            multivalued (bool, optional):
                Whether or not the widget should allow selecting multiple
                values.
        """
        super(RelatedUserWidget, self).__init__()
        self.local_site_name = local_site_name
        self.multivalued = multivalued

    def render(self, name, value, attrs=None):
        """Render the widget.

        Args:
            name (unicode):
                The name of the field.

            value (list or None):
                The current value of the field.

            attrs (dict):
                Attributes for the HTML element.

        Returns:
            django.utils.safestring.SafeText:
            The rendered HTML.
        """
        if value:
            if not self.multivalued:
                value = [
                 value]
            value = [ v for v in value if v ]
            input_value = (b',').join(force_text(v) for v in value)
            existing_users = User.objects.filter(pk__in=value).order_by(b'first_name', b'last_name', b'username')
        else:
            input_value = None
            existing_users = []
        final_attrs = self.build_attrs(attrs, name=name)
        input_html = super(RelatedUserWidget, self).render(name, input_value, attrs)
        use_avatars = avatar_services.avatars_enabled
        user_data = []
        for user in existing_users:
            data = {b'fullname': user.get_full_name(), 
               b'id': user.pk, 
               b'username': user.username}
            if use_avatars:
                try:
                    data[b'avatarHTML'] = avatar_services.for_user(user).render(request=None, user=user, size=20)
                except Exception as e:
                    logger.exception(b'Error rendering avatar for RelatedUserWidget: %s', e)
                    data[b'avatarHTML'] = None

            user_data.append(data)

        extra_html = render_to_string(b'admin/related_user_widget.html', {b'input_id': final_attrs[b'id'], 
           b'local_site_name': self.local_site_name, 
           b'multivalued': self.multivalued, 
           b'use_avatars': use_avatars, 
           b'users': user_data})
        return mark_safe(input_html + extra_html)

    def value_from_datadict(self, data, files, name):
        """Unpack the field's value from a datadict.

        Args:
            data (dict):
                The form's data.

            files (dict):
                The form's files.

            name (unicode):
                The name of the field.

        Returns:
            list:
            The list of PKs of User objects.
        """
        value = data.get(name)
        if self.multivalued:
            if isinstance(value, list):
                return value
            else:
                if isinstance(value, six.string_types):
                    return [ v for v in value.split(b',') if v ]
                return

        else:
            if value:
                return value
            else:
                return

        return