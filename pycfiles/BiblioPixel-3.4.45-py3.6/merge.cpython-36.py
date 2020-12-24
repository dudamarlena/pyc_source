# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/merge.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2567 bytes
import collections
from . import construct, load
DEFAULT_PROJECT = collections.OrderedDict((
 (
  'aliases', {}),
 (
  'colors', {}),
 (
  'palettes', {}),
 ('path', ''),
 ('typename', 'bibliopixel.project.project.Project'),
 ('numbers', ''),
 ('maker', 'bibliopixel.project.data_maker.Maker'),
 (
  'driver', {}),
 (
  'drivers', []),
 (
  'shape', ()),
 (
  'layout', {}),
 (
  'run', {}),
 (
  'animation', {}),
 (
  'controls', [])))
NOT_MERGEABLE = ('controls', 'shape', 'drivers', 'numbers', 'path', 'typename')
SPECIAL_CASE = ('datatype', 'dimensions')
PROJECT_SECTIONS = tuple(DEFAULT_PROJECT.keys()) + SPECIAL_CASE
SECTION_ISNT_DICT_ERROR = 'Project section "%s" is %s, should be dictionary'
UNKNOWN_SECTION_ERROR = 'There is no Project section named "%s"'

def merge(*projects):
    """
    Merge zero or more dictionaries representing projects with the default
    project dictionary and return the result
    """
    result = {}
    for project in projects:
        for name, section in (project or {}).items():
            if name not in PROJECT_SECTIONS:
                raise ValueError(UNKNOWN_SECTION_ERROR % name)
            if section is None:
                result[name] = type(result[name])()
            elif name in NOT_MERGEABLE + SPECIAL_CASE:
                result[name] = section
            else:
                if section:
                    if not isinstance(section, (dict, str)):
                        cname = section.__class__.__name__
                        raise ValueError(SECTION_ISNT_DICT_ERROR % (name, cname))
                if name == 'animation':
                    adesc = load.load_if_filename(section)
                    if adesc:
                        section = adesc.get('animation', {})
                        section['run'] = adesc.get('run', {})
                result_section = result.setdefault(name, {})
                section = construct.to_type(section)
                for k, v in section.items():
                    if v is None:
                        result_section.pop(k, None)
                    else:
                        result_section[k] = v

    return result