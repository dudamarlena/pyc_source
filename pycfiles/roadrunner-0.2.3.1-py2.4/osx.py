# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/roadrunner/platform/osx.py
# Compiled at: 2009-06-16 00:05:39
import sys

def avoid_core_functions():
    """
    http://hexsprite.lighthouseapp.com/projects/21973-roadrunner/tickets/4

    Using urllib under OSX triggers this error.

    This patch causes Python to skip using the ic module under OSX to avoid
    triggering this error.

     __THE_PROCESS_HAS_FORKED_AND_YOU_CANNOT_USE_THIS_COREFOUNDATION_FUNCTIONALITY___YOU_MUST_EXEC__()
    is the worst error name ever

    Who knows, maybe there's a better way to solve this?
    """
    import sys
    sys.modules['ic'] = None
    return


def patch_osx():
    avoid_core_functions()


if sys.platform == 'darwin':
    patch_osx()