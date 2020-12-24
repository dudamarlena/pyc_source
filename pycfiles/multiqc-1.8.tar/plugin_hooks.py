# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/utils/plugin_hooks.py
# Compiled at: 2019-11-01 10:12:16
""" MultiQC plugin hooks. Enables MultiQC plugins
to run their own custom subroutines at predefined
trigger points during MultiQC execution. """
import pkg_resources
hook_functions = {}
for entry_point in pkg_resources.iter_entry_points('multiqc.hooks.v1'):
    nicename = str(entry_point).split('=')[0].strip()
    try:
        hook_functions[nicename].append(entry_point.load())
    except KeyError:
        hook_functions[nicename] = [
         entry_point.load()]

def mqc_trigger(trigger):
    for hook in hook_functions.get(trigger, []):
        hook()