# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/serialize/yaml_.py
# Compiled at: 2010-03-18 05:47:02
try:
    import yaml
except ImportError:
    raise ImportError('You must install the yaml package before you can serialize data this way.')

__all__ = [
 'render']

def render(data, template=None, **kw):
    """Serialize data using PyYAML.
    
    Accepts the same extended arguments as the PyYAML dump() function, see:
    
        http://pyyaml.org/wiki/PyYAMLDocumentation#DumpingYAML
    
    """
    return (
     'application/x-yaml', yaml.dump(data, **kw))