# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/context_processors.py
# Compiled at: 2012-07-20 05:27:44
from dress_blog.models import Config

def config(request):
    """
    Adds configuration information to the context.

    To employ, add the conf method reference to your project
    settings TEMPLATE_CONTEXT_PROCESSORS.

    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "dress_blog.context_processors.config",
        )
    """
    return {'dress_blog_config': Config.get_current()}