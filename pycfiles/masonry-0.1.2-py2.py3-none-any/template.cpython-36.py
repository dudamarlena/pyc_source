# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/masonry/package/src/masonry/template.py
# Compiled at: 2017-10-25 16:30:29
# Size of source mod 2**32: 9037 bytes
import json, shutil, sys, tempfile
from pathlib import Path
import git
from clint.textui import colored, prompt, puts, validators, indent
from .postprocess import combine_file_snippets
from .prompt import prompt_cookiecutter_variables
from .render import render_cookiecutter
from .resolution import create_dependency_graph, resolve
from .utils import load_application_data, save_application_data
STDOUT = sys.stdout.write

def initialise_project(project: Path, template=None, output_dir='.', interactive=True, stream=STDOUT):
    project_path = Path(project).resolve()
    meta_data_path = project_path / 'metadata.json'
    project_templates = load_application_data()
    if not meta_data_path.exists():
        raise IOError('Not a valid project directory. Missing metadata.json file')
    if not template:
        with meta_data_path.open() as (meta_data_file):
            meta_data = json.load(meta_data_file)
        template = meta_data['default']
    if project_path.name in project_templates:
        if project_templates[project_path.name] != project_path.as_posix():
            ans = prompt.query('Project with the same name already exists in another location. Overwrite? [y/n]',
              validators=[
             validators.RegexValidator('[yn]')])
            if ans == 'n':
                sys.exit()
    project_templates[project_path.name] = project_path.as_posix()
    save_application_data(project_templates)
    template_paths = {p.name:p for p in project_path.iterdir() if p.is_dir() if p.is_dir()}
    template_names = list(template_paths.keys())
    g = create_dependency_graph((project_path / 'metadata.json'), node_list=template_names)
    template_order = [n.name for n in resolve(g[template])]
    order_str = ' --> '.join(template_order)
    puts((colored.yellow(f"Creating new project from templates: {order_str}")), stream=stream)
    puts(stream=stream)
    project_state = {}
    project_state['templates'] = []
    project_state['variables'] = {}
    for name in template_order:
        template = template_paths[name].as_posix()
        if interactive:
            context_variables = prompt_cookiecutter_variables(template, project_state['variables'])
        else:
            context_variables_path = Path(template) / 'cookiecutter.json'
            context_variables = json.load(context_variables_path.open())
        puts(f'Rendering "{name}" ...', stream=stream)
        output_project_dir, content = safe_render(template,
          output_dir, context=context_variables, stream=stream)
        combine_file_snippets(output_project_dir, stream=stream)
        if not (Path(output_project_dir) / '.git').exists():
            if 'repo' not in vars():
                repo = git.Repo.init(output_project_dir)
        else:
            repo = git.Repo(output_project_dir)
        project_state['variables'].update(content)
        if name not in project_state['templates']:
            project_state['templates'].append(name)
        project_state['project'] = project_path.name
        mason_vars = Path(output_project_dir) / '.mason'
        with mason_vars.open('w') as (f):
            json.dump(project_state, f, indent=4)
        all_files = [p.as_posix() for p in Path(output_project_dir).iterdir() if p.is_file]
        repo.index.add(all_files)
        repo.index.commit(f"Add '{name}' template layer via stone mason.")

    return output_project_dir


def add_template(templates: list, project_dir: Path, interactive=True, stream=STDOUT):
    """ Add a template to an existing project """
    project_dir = Path(project_dir).resolve()
    repo = git.Repo(project_dir.as_posix())
    mason_vars = project_dir / '.mason'
    with mason_vars.open('r') as (f):
        project_state = json.load(f)
    project_template_data = load_application_data()
    project_root = Path(project_template_data[project_state['project']])
    previous_templates = project_state['templates']
    paths = project_root.iterdir()
    template_paths = {p.name:p for p in paths if p.is_dir() if p.is_dir()}
    templates_names = list(template_paths.keys())
    templates_names.sort()
    for t in templates:
        assert t in templates_names, f"{t} not in templates for this type of project"

    g = create_dependency_graph((project_root / 'metadata.json'), node_list=templates_names)
    template_orders = []
    for t in templates:
        order = [n.name for n in resolve(g[t]) if n.name not in previous_templates]
        if order:
            template_orders.append(order)
            previous_templates.extend(order)

    order_strs = [' --> '.join(order) for order in template_orders]
    puts((colored.yellow('Adding the following templates to project:')), stream=stream)
    with indent(4):
        for order in order_strs:
            puts((colored.yellow(order)), stream=stream)

    puts(stream=stream)
    for order_set in template_orders:
        for name in order_set:
            template = template_paths[name].as_posix()
            if interactive:
                context_variables = prompt_cookiecutter_variables(template, project_state['variables'])
            else:
                context_variables_path = Path(template) / 'cookiecutter.json'
                context_variables = json.load(context_variables_path.open())
            for k, v in context_variables.items():
                if k not in project_state['variables']:
                    project_state['variables'][k] = v

            puts(f'Rendering "{name}" ...', stream=stream)
            output_project_dir, content = safe_render(template,
              target_dir=(project_dir.parent),
              context=(project_state['variables']),
              stream=stream)
            combine_file_snippets(output_project_dir, stream=stream)
            project_state['variables'].update(content)
            if name not in project_state['templates']:
                project_state['templates'].append(name)
            with mason_vars.open('w') as (f):
                json.dump(project_state, f, indent=4)
            output_project_dir = Path(output_project_dir)
            repo.git.add((output_project_dir.as_posix()), force=False)
            repo.index.commit(f"Add '{name}' template layer via stone mason.")


def safe_render(template, target_dir, context, stream=STDOUT):
    """Safely Render a new template by first making a backup to roll back to if needed."""
    backup_dir = Path(tempfile.mkdtemp()) / 'backup'
    backup = shutil.copytree(target_dir, backup_dir)
    try:
        output_dir, content = render_cookiecutter(template,
          no_input=True, extra_context=context,
          output_dir=target_dir,
          overwrite_if_exists=True)
    except Exception as e:
        puts((colored.red('An error occured during templating, Rolling back to last stable state.')), stream=stream)
        shutil.rmtree(target_dir)
        shutil.copytree(backup, target_dir)
        with indent(4):
            puts(f"Restored {backup_dir} to {target_dir}", stream=stream)
            puts((colored.red(f"Traceback: \n{e}")), stream=stream)
        raise e
        sys.exit()

    return (
     output_dir, content)