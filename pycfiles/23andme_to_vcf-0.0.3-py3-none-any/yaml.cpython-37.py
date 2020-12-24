# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/steven/Documents/Projects/radio/EOR/OthersCodes/21cmFAST/21cmFAST/src/py21cmfast/yaml.py
# Compiled at: 2020-02-13 15:47:20
# Size of source mod 2**32: 1444 bytes
__doc__ = 'Modified YAML that can load/dump `astropy` quantities.\n\nA modification of the basic YAML and astropy.io.misc.yaml to be able to load/dump\nobjects with astropy quantities in them.\n'
import yaml
import astropy.io.misc as ayaml

class _NewDumper(yaml.Dumper, ayaml.AstropyDumper):
    pass


class _NewLoader(yaml.Loader, ayaml.AstropyLoader):
    pass


for k, v in yaml.Dumper.yaml_representers.items():
    _NewDumper.add_representer(k, v)

for k, v in yaml.Dumper.yaml_multi_representers.items():
    _NewDumper.add_multi_representer(k, v)

for k, v in ayaml.AstropyDumper.yaml_representers.items():
    _NewDumper.add_representer(k, v)

for k, v in ayaml.AstropyDumper.yaml_multi_representers.items():
    _NewDumper.add_multi_representer(k, v)

for k, v in yaml.Loader.yaml_constructors.items():
    _NewLoader.add_constructor(k, v)

for k, v in ayaml.AstropyLoader.yaml_constructors.items():
    _NewLoader.add_constructor(k, v)

for k, v in yaml.Loader.yaml_multi_constructors.items():
    _NewLoader.add_multi_constructor(k, v)

for k, v in ayaml.AstropyLoader.yaml_multi_constructors.items():
    _NewLoader.add_multi_constructor(k, v)

def load(stream):
    """Load an object from a YAML stream."""
    return yaml.load(stream, Loader=_NewLoader)


def dump(data, stream=None, **kwargs):
    """Dump an object into a YAML stream."""
    kwargs['Dumper'] = _NewDumper
    return (yaml.dump)(data, stream=stream, **kwargs)