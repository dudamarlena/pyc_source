# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/utils/template.py
# Compiled at: 2015-11-10 03:46:04
from coreinit.utils.exceptions import *
from coreinit.utils.installer import *
from coreinit import settings

def configure():
    try:
        import jinja2
    except:
        install_pip(['jinja2'])


def render(template, context):
    from jinja2 import Environment, FileSystemLoader
    if settings.TEMPLATE_PATH is None:
        raise ConfigurationException('TEMPLATE_PATH not configured')
    env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
    template = env.get_template(template)
    return template.render(**context)