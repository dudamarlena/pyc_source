# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/stard/development/cocoag/cocoag/configuration/config.py
# Compiled at: 2017-05-28 19:39:49
# Size of source mod 2**32: 1987 bytes
import configparser, logging, os
from pathlib import Path
current_file = os.path.realpath(__file__)
CONFIG_ROOT = Path(current_file).parent
CONFIG_TEMPLATE = os.path.join(CONFIG_ROOT, 'default_cocoag.cfg')
PACKAGE_ROOT = Path(CONFIG_ROOT).parent
COCOAG_ROOT = os.path.join(PACKAGE_ROOT, 'cocoag')
GENERATOR_ROOT = os.path.join(COCOAG_ROOT, 'generator')
S3_ROOT = os.path.join(COCOAG_ROOT, 's3')

class MyConfigParser(configparser.ConfigParser):

    def getlist(self, section, option):
        value = self.get(section, option)
        return list(filter(None, (x.strip() for x in value.splitlines())))

    def getlistint(self, section, option):
        return [int(x) for x in self.getlist(section, option)]


def expand_env_var(env_var):
    """
    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        env_var = interpolated


def generate_default_conf():
    with open(CONFIG_TEMPLATE) as (config_template):
        conf = config_template.read()
        return conf.format(PACKAGE_ROOT=PACKAGE_ROOT)


if 'COCOAG_CONF' not in os.environ:
    COCOAG_CONF = expand_env_var('~/.cocoag.cfg')
else:
    COCOAG_CONF = expand_env_var(os.environ['COCOAG_CONF'])
if not os.path.isfile(COCOAG_CONF):
    logging.info('Creating new Cocoag config file in: {}'.format(COCOAG_CONF))
    with open(COCOAG_CONF, 'w') as (f):
        f.write(generate_default_conf())
config = MyConfigParser()
config.read(COCOAG_CONF)