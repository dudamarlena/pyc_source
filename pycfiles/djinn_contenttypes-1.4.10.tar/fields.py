# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/forms/fields.py
# Compiled at: 2014-04-22 08:31:13
from django.forms import CharField
from django.template.defaultfilters import removetags

class NoScriptCharField(CharField):
    """
    Specific CharField that filters out <script>-tags.
    """

    def to_python(self, value):
        """
        Strips <script>-tags from the field.
        """
        if value:
            value = value.replace('\r\n', '\n')
            return removetags(value, 'script')
        else:
            return
            return