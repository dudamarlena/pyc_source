# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mustafa/Repos/django-latexify/latexify/settings.py
# Compiled at: 2017-05-28 23:32:59
from django.conf import settings
LATEX_TEXT_CSS_CLASS = getattr(settings, 'LATEX_TEXT_CSS_CLASS', 'django-latexify text')
LATEX_MATH_INLINE_CSS_CLASS = getattr(settings, 'LATEX_MATH_INLINE_CSS_CLASS', 'django-latexify math inline')
LATEX_MATH_BLOCK_CSS_CLASS = getattr(settings, 'LATEX_MATH_BLOCK_CSS_CLASS', 'django-latexify math block')