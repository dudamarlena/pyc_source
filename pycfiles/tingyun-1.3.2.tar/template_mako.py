# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/template_mako.py
# Compiled at: 2016-06-30 06:13:10
"""Define this module for basic armory for detect mako

"""
from tingyun.armoury.ammunition.function_tracker import wrap_function_trace

def detect_template(module):
    """
    :param module:
    :return:
    """

    def template_name(template, text, filename, *args):
        """
        :param template:
        :param text:
        :param filename:
        :param args: compatible with _compile_text and _compile_module_file
        :return:
        """
        return filename

    def template_name_in_render(instance, *args, **kwargs):
        return getattr(instance, 'filename', 'template')

    wrap_function_trace(module, '_compile_text', name=template_name, group='Template.compile')
    wrap_function_trace(module, '_compile_module_file', name=template_name, group='Template.compile')
    wrap_function_trace(module, 'Template.render', name=template_name_in_render, group='Template.render')