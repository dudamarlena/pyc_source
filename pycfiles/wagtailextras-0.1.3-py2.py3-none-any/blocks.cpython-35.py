# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nutz/JetBrains/wagtailextras/build/lib/wagtailextras/blocks.py
# Compiled at: 2016-10-07 06:58:55
# Size of source mod 2**32: 563 bytes
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.blocks import Block

class EmptyBlock(Block):

    def render_form(self, value, prefix='', errors=None):
        return render_to_string('wagtailextras/empty_block.html', {'name': self.name, 
         'classes': self.meta.classname, 
         'placeholder': mark_safe(self.meta.placeholder)})

    def get_default(self):
        return ''

    def value_from_datadict(self, data, files, prefix):
        return ''