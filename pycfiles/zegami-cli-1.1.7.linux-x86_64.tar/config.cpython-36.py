# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/config.py
# Compiled at: 2020-03-19 11:59:34
# Size of source mod 2**32: 1093 bytes
"""Collection commands."""
import os, sys
from jsonschema import validate
import yaml

def parse_args(args, log):
    if 'config' not in args:
        log.error('Configuration file path missing')
        sys.exit(1)
    configuration = parse_config(args.config)
    for attr in ('id', 'project', 'url'):
        if attr in args:
            configuration[attr] = getattr(args, attr)

    return configuration


def parse_config(path):
    """Parse yaml collection configuration."""
    configuration = load_config(path)
    validate_config(configuration)
    return configuration


def load_config(path):
    """Load yaml collection configuration."""
    with open(path, 'r') as (stream):
        return yaml.load(stream, Loader=(yaml.SafeLoader))


def validate_config(configuration):
    schema_path = os.path.join(os.path.dirname(__file__), 'schemata', 'spec.yaml')
    with open(schema_path, 'r') as (stream):
        schema = yaml.load(stream, Loader=(yaml.SafeLoader))
    validate(configuration, schema)