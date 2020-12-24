# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/djangomako/middleware.py
# Compiled at: 2008-09-28 17:34:52
from mako.lookup import TemplateLookup
import tempfile

class MakoMiddleware(object):

    def __init__(self):
        """Setup mako variables and lookup object"""
        global encoding_errors
        global lookup
        global module_directory
        global output_encoding
        from django.conf import settings
        directories = getattr(settings, 'MAKO_TEMPLATE_DIRS', settings.TEMPLATE_DIRS)
        module_directory = getattr(settings, 'MAKO_MODULE_DIR', tempfile.mkdtemp())
        output_encoding = getattr(settings, 'MAKO_OUTPUT_ENCODING', 'utf-8')
        encoding_errors = getattr(settings, 'MAKO_ENCODING_ERRORS', 'replace')
        lookup = TemplateLookup(directories=directories, module_directory=module_directory, output_encoding=output_encoding, encoding_errors=encoding_errors)
        import djangomako
        djangomako.lookup = lookup