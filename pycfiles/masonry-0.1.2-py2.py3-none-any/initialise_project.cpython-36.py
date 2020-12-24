# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/stone-mason/package/src/stonemason/initialise_project.py
# Compiled at: 2017-06-20 17:14:22
# Size of source mod 2**32: 1637 bytes
from pathlib import Path
import json
from .resolution import create_dependency_graph, resolve
from .render import render_cookiecutter

def initialise_project(project, template=None, output_dir='.'):
    project_path = Path(project)
    if not template:
        meta_data_path = project_path / 'metadata.json'
        with meta_data_path.open() as (meta_data_file):
            meta_data = json.load(meta_data_file)
        template = meta_data['default']
    template_paths = {p.name:p for p in project_path.iterdir() if p.is_dir() if p.is_dir()}
    template_names = list(template_paths.keys())
    g = create_dependency_graph((project_path / 'metadata.json'), node_list=template_names)
    template_order = [n.name for n in resolve(g['package'])]
    print(f"Creating project from templates:\n\t{template_order}")
    content_variables = {}
    for name in template_order:
        template = template_paths[name].as_posix()
        project_dir, content = render_cookiecutter(template,
          extra_context=content_variables,
          output_dir=output_dir,
          overwrite_if_exists=True)
        print(f"Rendered: {template}")
        content_variables.update(content)

    mason_vars = Path(project_dir) / '.mason.json'
    with mason_vars.open('w') as (f):
        json.dump(content_variables, f)