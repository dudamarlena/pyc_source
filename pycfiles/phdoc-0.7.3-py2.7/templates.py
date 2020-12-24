# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/phdoc/templates.py
# Compiled at: 2013-09-24 11:14:27
import os.path as p, jinja2, phdoc
from phdoc.config import Config
Config.register_default('use-default-templates', True)

def build_template_env(config):
    """Build a Jinja2 template environment for a given config."""
    load_path = []
    if p.isdir(config.template_dir):
        load_path.append(config.template_dir)
    if config['use-default-templates']:
        load_path.append(phdoc.default_template_dir)
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(load_path))
    environment.globals['config'] = config
    return environment


def template_env(config):
    if not getattr(config, '_template_env', None):
        config._template_env = build_template_env(config)
    return config._template_env


Config.template_env = property(template_env)