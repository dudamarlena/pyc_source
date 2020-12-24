# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nemo_annotator_plugin/__init__.py
# Compiled at: 2016-07-21 13:21:17
# Size of source mod 2**32: 673 bytes
from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename

class AnnotatorPlugin(PluginPrototype):
    HAS_AUGMENT_RENDER = True
    TEMPLATES = {'annotator': resource_filename('nemo_annotator_plugin', 'data/templates')}
    ROUTES = PluginPrototype.ROUTES

    def __init__(self, *args, **kwargs):
        super(AnnotatorPlugin, self).__init__(*args, **kwargs)

    def render(self, **kwargs):
        update = kwargs
        if 'template' in kwargs and kwargs['template'] == 'main::text.html':
            update['template'] = 'annotator::text.html'
        return update