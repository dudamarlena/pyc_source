# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/widgets.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 276 bytes


def add_styles(widget, styles):
    """ Helper function - adds CSS styles to widget

    """
    attrs = widget.attrs or {}
    if 'style' in attrs:
        attrs['style'] = '%s %s' % (attrs['style'], styles)
    else:
        attrs['style'] = styles
    widget.attrs = attrs