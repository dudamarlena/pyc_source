# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/internal/venom_yaml.py
# Compiled at: 2016-04-20 16:49:44
import os
from builtin_file import bfile
from index_yaml import IndexYaml, IndexYamlFromFile, IndexGenerator
__all__ = [
 'VenomIndexGenerator', 'VenomYamlFromFile']
__all__ += ['update_venom_yaml']

def update_venom_yaml(models):
    is_dev = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
    if not is_dev:
        return False
    index = ''
    if os.path.isfile('search.venom.yaml'):
        with open('search.venom.yaml', 'r') as (f):
            index = f.read()
    schemas = map(lambda model: model._schema, models)
    generator = VenomIndexGenerator(yaml=index, schemas=schemas)
    with bfile('search.venom.yaml', 'w+') as (f):
        f.write(generator.generate())
    return True


class VenomYamlFromFile(IndexYamlFromFile):
    venom_info = '\n# This search.yaml is automatically updated whenever the venom framework\n# detects a schema change. If you want to manage the search.yaml file\n# manually, remove the above marker line (the line saying "# VENOM INDEXES").\n# If you want to manage some indexes manually, move them above the marker line.\n# The search.yaml file is automatically uploaded to the admin console when\n# you next deploy your application using appcfg.py.\n'


class VenomIndexGenerator(IndexGenerator):
    yaml_parser = VenomYamlFromFile

    def _get_properties_from_schema(self, schema):
        return [ {'name': name} for name, prop_schema in schema.items() if prop_schema.search
               ]