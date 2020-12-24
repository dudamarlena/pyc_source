# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact-setup/easy_contact_setup/models.py
# Compiled at: 2014-10-23 11:19:25
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fields.fields import EncryptedCharField

class Setup(models.Model):
    active = models.BooleanField(help_text=_('Activate or disable this settings object.'), verbose_name=_('Active'))
    slug = models.SlugField(verbose_name=_('Name'), unique=True, help_text=_('Give this setting an uniqe name. No spaces and special character allowed.'))
    mail_to = models.EmailField(max_length=50, verbose_name=_('Your email'), help_text=_(' This will be the email adress your mails are going to. If necessary the application also use it as sender adress.'))
    mail_host = EncryptedCharField(blank=True, max_length=50, verbose_name=_('Mail server'), help_text=_('Your smtp server, i.e.: mail.yourprovider.something or smtp.yourprovider.something. Make shure that the specified server belongs to the mail adress your specified above!'))
    mail_host_user = EncryptedCharField(blank=True, max_length=50, verbose_name=_('Username'), help_text=_('Smptp server user name. Mostly user or login name to your mail account. Usaly your email adress'))
    mail_host_pass = EncryptedCharField(blank=True, max_length=50, verbose_name=_('Password'), help_text=_('Smtp server password. Mostly the login password to your mail account.'))

    class Meta:
        verbose_name = _('Contact form setting')
        verbose_name_plural = _('Contact form settings')

    def __unicode__(self):
        return self.slug