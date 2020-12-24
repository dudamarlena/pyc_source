# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/serialize/yaml.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
try:
    import yaml
except ImportError:
    raise ImportError(b'You must install the yaml package before you can serialize data this way.')

__all__ = [
 b'render']

def render(data, template=None, i18n=None, **kw):
    """Serialize data using PyYAML.
    
    Accepts the same extended arguments as the PyYAML dump() function, see:
    
        http://pyyaml.org/wiki/PyYAMLDocumentation#DumpingYAML
    
    """
    return (
     b'application/x-yaml', yaml.dump(data, **kw))