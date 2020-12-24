# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/notification.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 2432 bytes
__doc__ = 'PyAMS_security.notification module\n\nThis module handles notificaiton settings.\n'
from persistent import Persistent
from pyramid_mailer import IMailer
from zope.schema.fieldproperty import FieldProperty
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.notification import INotificationSettings
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

@factory_config(INotificationSettings)
class NotificationSettings(Persistent):
    """NotificationSettings"""
    enable_notifications = FieldProperty(INotificationSettings['enable_notifications'])
    mailer = FieldProperty(INotificationSettings['mailer'])
    service_name = FieldProperty(INotificationSettings['service_name'])
    service_owner = FieldProperty(INotificationSettings['service_owner'])
    sender_name = FieldProperty(INotificationSettings['sender_name'])
    sender_email = FieldProperty(INotificationSettings['sender_email'])
    subject_prefix = FieldProperty(INotificationSettings['subject_prefix'])
    confirmation_template = FieldProperty(INotificationSettings['confirmation_template'])
    registration_template = FieldProperty(INotificationSettings['registration_template'])
    signature = FieldProperty(INotificationSettings['signature'])

    def get_mailer(self):
        """Get mailer utility matching current selection"""
        if self.mailer is not None:
            return query_utility(IMailer, name=self.mailer)


NOTIFICATIONS_KEY = 'pyams_security.notifications'

@adapter_config(context=ISecurityManager, provides=INotificationSettings)
def security_notification_factory(context):
    """Security manager notifications factory adapter"""
    return get_annotation_adapter(context, NOTIFICATIONS_KEY, INotificationSettings, locate=False)