# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lektor_htmlmin.py
# Compiled at: 2020-01-23 10:51:58
# Size of source mod 2**32: 2151 bytes
import os, codecs, chardet, sys, htmlmin
from lektor.pluginsystem import Plugin
import lektor.reporter as reporter

class HTMLMinPlugin(Plugin):
    name = 'Lektor HTMLmin'
    description = 'HTML minifier for Lektor. Based on htmlmin.'

    def __init__(self, *args, **kwargs):
        (Plugin.__init__)(self, *args, **kwargs)
        self.options = {'remove_empty_space':True, 
         'remove_all_empty_space':True, 
         'reduce_empty_attributes':True, 
         'reduce_boolean_attributes':False, 
         'remove_optional_attribute_quotes':False, 
         'keep_pre':False, 
         'pre_attr':'pre', 
         'remove_comments':True}

    def is_enabled(self, build_flags):
        return bool(build_flags.get('htmlmin'))

    def find_html_files(self, destination):
        """
        Finds all html files in the given destination.
        """
        for root, dirs, files in os.walk(destination):
            for f in files:
                if f.endswith('.html'):
                    yield os.path.join(root, f)

    def minify_file(self, target):
        """
        Minifies the target html file.
        """
        html = open(target, 'rb')
        enc = chardet.detect(html.read())['encoding']
        html.close()
        with codecs.open(target, 'r+', enc) as (f):
            result = (htmlmin.minify)((f.read()), **self.options)
            f.seek(0)
            f.write(result)
            f.truncate()

    def on_after_build_all(self, builder, **extra):
        """
        after-build-all lektor event
        """
        try:
            is_enabled = self.is_enabled(builder.build_flags)
        except AttributeError:
            is_enabled = self.is_enabled(builder.extra_flags)

        if not is_enabled:
            return
        reporter.report_generic('HTML minification started')
        for htmlfile in self.find_html_files(builder.destination_path):
            self.minify_file(htmlfile)

        reporter.report_generic('HTML minification finished')