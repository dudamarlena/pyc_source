# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/libsast/core_matcher/helpers.py
# Compiled at: 2020-04-14 22:39:36
# Size of source mod 2**32: 1580 bytes
"""Helper Functions."""
from pathlib import Path
from libsast.logger import init_logger
import yaml, requests
logger = init_logger(__name__)

def download_rule(url):
    """Download Pattern File."""
    try:
        with requests.get(url, allow_redirects=True) as (r):
            r.raise_for_status()
            return r.text
    except requests.exceptions.RequestException:
        logger.exception('Failed to download patterns from url: %s', url)

    return False


def read_yaml(file_obj, text=False):
    try:
        if text:
            return yaml.safe_load(file_obj)
        return yaml.safe_load(file_obj.read_text('utf-8', 'ignore'))
    except yaml.YAMLError:
        logger.error('Failed to parse YAML')
    except Exception:
        logger.exception('Error parsing YAML')


def get_rules(rule_loc):
    """Get pattern matcher rules."""
    if not rule_loc:
        logger.error('No rule directory, file or url specified')
        return
        if rule_loc.startswith(('http://', 'https://')):
            pat = download_rule(rule_loc)
            if not pat:
                return
            return read_yaml(pat, True)
    else:
        rule = Path(rule_loc)
        if rule.is_file():
            if rule.exists():
                return read_yaml(rule)
        if rule.is_dir() and rule.exists():
            patterns = []
            for yfile in rule.glob('**/*.yaml'):
                patterns.extend(read_yaml(yfile))

            return patterns
    logger.error('Not a valid file or directory: %s', rule)