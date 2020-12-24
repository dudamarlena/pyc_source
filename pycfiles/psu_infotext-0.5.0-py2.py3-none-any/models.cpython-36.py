# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mjg/git/django/psu/psu-infotext/psu_infotext/models.py
# Compiled at: 2019-07-29 18:37:11
# Size of source mod 2**32: 965 bytes
from django.db import models

class Infotext(models.Model):
    __doc__ = 'User-editable text'
    app_code = models.CharField(max_length=15,
      verbose_name='Application Code',
      help_text='Application that this text belongs to')
    text_code = models.CharField(max_length=80,
      verbose_name='Text Identifier',
      help_text='Unique identifier for this text instance')
    user_edited = models.CharField(max_length=1,
      help_text='Has this text been modified from its coded value?',
      default='N',
      choices=(('N', 'No'), ('Y', 'Yes')))
    content = models.TextField(verbose_name='Text Content')
    last_updated = models.DateTimeField(auto_now=True)

    def set_content(self, new_content):
        self.content = new_content
        self.user_edited = 'Y'
        self.save()

    def __str__(self):
        if self.text_code:
            return self.text_code
        else:
            return ''