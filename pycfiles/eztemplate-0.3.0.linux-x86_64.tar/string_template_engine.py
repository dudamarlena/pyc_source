# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/eztemplate/engines/string_template_engine.py
# Compiled at: 2016-02-22 12:37:51
"""Provide the standard Python string.Template engine."""
from __future__ import absolute_import
from __future__ import print_function
from string import Template
from . import Engine

class StringTemplate(Engine):
    """String.Template engine."""
    handle = 'string.Template'

    def __init__(self, template, tolerant=False, **kwargs):
        """Initialize string.Template."""
        super(StringTemplate, self).__init__(**kwargs)
        self.template = Template(template)
        self.tolerant = tolerant

    def apply(self, mapping):
        """Apply a mapping of name-value-pairs to a template."""
        mapping = {name:self.str(value, tolerant=self.tolerant) for name, value in mapping.items() if value is not None or self.tolerant}
        if self.tolerant:
            return self.template.safe_substitute(mapping)
        return self.template.substitute(mapping)