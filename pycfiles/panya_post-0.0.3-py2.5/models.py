# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/post/models.py
# Compiled at: 2010-08-11 09:10:12
from django.core.urlresolvers import reverse
from panya.models import ModelBase
from ckeditor.fields import RichTextField

class Post(ModelBase):
    content = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        return reverse('post_object_detail', kwargs={'slug': self.slug})