# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/plugins/layers.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 734 bytes
import os

def _cp(context, source, destination):
    for root, dirs, files in os.walk(source):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.normpath(os.path.join(destination, os.path.relpath(root, source), f))
            context.cp(src, dst)


class PreBuildLayers:

    def pre_build(self, context):
        OUTPUT_ROOT = context.settings.OUTPUT_ROOT
        for layer in context.settings.PRE_BUILD_LAYERS:
            _cp(context, layer, OUTPUT_ROOT)


class PostBuildLayers:

    def post_build(self, context):
        OUTPUT_ROOT = context.settings.OUTPUT_ROOT
        for layer in context.settings.POST_BUILD_LAYERS:
            _cp(context, layer, OUTPUT_ROOT)