# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ansible_readme/ansible_readme.py
# Compiled at: 2019-10-30 11:00:10
# Size of source mod 2**32: 10083 bytes
__doc__ = 'The AnsibleReadme core module.\n\nAll documentation context is stored within the AnsibleReadme object along with\nany file system locations, configurations and other information relevant to\naiding in documenting roles.\n'
import os, pathlib, typing, attr, click, yaml
from jinja2 import Environment, FileSystemLoader
from ansible_readme.filters import listify, quicklistify
from ansible_readme.logger import get_logger, red_text
log = get_logger(__name__)

@attr.s(auto_attribs=True)
class AnsibleReadme:
    """AnsibleReadme"""
    path = attr.ib()
    path: pathlib.Path
    is_single_role = attr.ib(default=False)
    is_single_role: bool
    is_multiple_role = attr.ib(default=False)
    is_multiple_role: bool
    role_paths = attr.ib(default=(attr.Factory(list)))
    role_paths: typing.List[pathlib.Path]
    role_docs = attr.ib(default=(attr.Factory(dict)))
    role_docs: typing.Dict[(str, typing.Any)]
    role_readmes = attr.ib(default=(attr.Factory(dict)))
    role_readmes: typing.Dict[(str, str)]
    STANDARD_ROLE_PATHS = [
     'defaults',
     'files',
     'meta',
     'molecule',
     'tasks',
     'templates',
     'vars']
    STANDARD_ROLE_PATHS: typing.List[str]
    should_force = attr.ib(default=False)
    should_force: bool
    template = attr.ib(default=(pathlib.Path(__file__).parent.absolute() / 'data' / 'readme.md.j2'))
    template: pathlib.Path
    readme_name = attr.ib(default='README.md')
    readme_name: str
    debug = attr.ib(default=False)
    debug: bool
    context = attr.ib(default=None)
    context: typing.Any

    def __attrs_post_init__(self):
        """Initalise state after validation has run through."""
        self.path = pathlib.Path(self.path).absolute()
        self.role_paths = self.gather_role_paths()
        if self.debug:
            paths = ', '.join(map(str, self.role_paths))
            log.info('Role paths are {}'.format(paths))

    @path.validator
    def __check_path(self, attribute: attr.Attribute, value: pathlib.Path) -> typing.Optional[Exception]:
        """Ensure 'value' does indeed contain a role or roles."""
        path = pathlib.Path(value).absolute()
        if self.is_role_path(path) or self.is_roles_path(path):
            if self.debug:
                msg = 'a single role' if self.is_single_role else 'multiple roles'
                log.info(f"{path} contains {msg}")
            return
        raise click.ClickException(red_text(f"{path} does not contain any Ansible roles?"))

    def has_standard_role_paths(self, path: pathlib.Path) -> bool:
        """Does 'path' contain standard role paths?"""
        _dirs = [_dir for _dir in os.listdir(path) if os.path.isdir(path / _dir)]
        if not any((_dir in self.STANDARD_ROLE_PATHS for _dir in _dirs)):
            return False
        else:
            main_yml_paths = [path / _dir / 'main.yml' for _dir in self.STANDARD_ROLE_PATHS]
            return any((os.path.exists(main_yml) for main_yml in main_yml_paths)) or False
        return True

    def is_role_path(self, path: pathlib.Path) -> bool:
        """Does 'path' contain a role?"""
        if self.has_standard_role_paths(path):
            self.is_single_role = True
        else:
            self.is_single_role = False
        return self.is_single_role

    def is_roles_path(self, path: pathlib.Path) -> bool:
        """Does 'path' contain at least one role?"""
        if self.is_single_role:
            self.is_multiple_role = False
            return self.is_multiple_role
        _dirs = [path / _dir for _dir in os.listdir(path) if os.path.isdir(path / _dir)]
        for _dir in _dirs:
            if self.has_standard_role_paths(_dir):
                self.is_multiple_role = True

        return self.is_multiple_role

    def gather_role_paths(self) -> typing.List[pathlib.Path]:
        """Retrieve a list of valid role paths after validation."""
        if self.is_single_role:
            return [self.path]
        return [pathlib.Path(self.path / role_path) for role_path in os.listdir(self.path) if os.path.isdir(self.path / role_path)]

    def do_gathering(self, path: pathlib.Path) -> typing.Dict[(str, typing.Any)]:
        """Do actual gathering of information specifed at path."""
        contents = {}
        if os.path.exists(path):
            with open(path) as (file):
                loaded = yaml.load((file.read()), Loader=(yaml.SafeLoader))
                contents = loaded if loaded else {}
        return contents

    def gather_meta(self, path: pathlib.Path) -> typing.Dict[(str, typing.Any)]:
        """Gather all meta for a role."""
        contents = self.do_gathering(path / 'meta' / 'main.yml')
        if 'galaxy_info' not in contents:
            contents['galaxy_info'] = {}
        return contents

    def gather_docs(self, path: pathlib.Path) -> typing.Dict[(str, typing.Any)]:
        """Gather docs/ path documentation for a role."""
        return self.do_gathering(path / 'docs' / 'main.yml')

    def gather_defaults(self, path: pathlib.Path) -> typing.Dict[(str, typing.Any)]:
        """Gather all defaults for a role."""
        return self.do_gathering(path / 'defaults' / 'main.yml')

    def gather_extras(self, path: pathlib.Path) -> typing.Dict[(str, typing.Any)]:
        """Gather extra context documentation for a role."""
        contents = {}
        contents['role_name'] = os.path.basename(path)
        return contents

    def gather_all(self) -> typing.Dict[(str, typing.Any)]:
        """Gather all documentation for roles."""
        for path in self.role_paths:
            role_name = os.path.basename(path)
            self.role_docs[role_name] = {'meta':self.gather_meta(path), 
             'defaults':self.gather_defaults(path), 
             'extras':self.gather_extras(path), 
             'docs':self.gather_docs(path)}

        if self.debug:
            log.info(f"Gathered role documentation: {self.role_docs}")
        return self.role_docs

    def render_readmes(self) -> typing.Dict[(str, str)]:
        """Render README file templates using Jinja2 with gathered docs."""
        template_path = str(pathlib.Path(self.template).parent.absolute())
        jinja_env = Environment(loader=(FileSystemLoader(template_path)),
          trim_blocks=True,
          lstrip_blocks=True)
        jinja_env.filters['listify'] = listify
        jinja_env.filters['quicklistify'] = quicklistify
        template = jinja_env.get_template(os.path.basename(self.template))
        for role_doc in self.role_docs:
            self.role_readmes[role_doc] = (template.render)(**self.role_docs[role_doc])

        return self.role_readmes

    def write_readmes(self) -> None:
        """Write README files from rendered templates."""
        for path in self.role_paths:
            role_name = os.path.basename(path)
            readme_path = path / self.readme_name
            if self.debug:
                log.info('README will look like:\n\n{}'.format(self.role_readmes[role_name]))
            if os.path.exists(readme_path):
                if not self.should_force:
                    msg = 'Discovered {} which already exists, refusing to overwrite (pass --force to override this)'.format(readme_path)
                    raise click.ClickException(red_text(msg))
            with open(readme_path, 'w') as (readme_handle):
                readme_handle.write(self.role_readmes[role_name])

    def generate_readmes(self) -> None:
        """Generate READMEs for discovered roles."""
        self.init_docs()
        self.gather_all()
        self.render_readmes()
        self.write_readmes()

    def init_docs(self) -> None:
        """Generate docs/ folders with defaults."""
        for role_path in self.role_paths:
            docs = {'defaults': {}}
            docs_path = role_path / 'docs'
            is_init_without_force = self.context.command.name == 'init' and os.path.exists(docs_path) and not self.should_force
            another_cmd = self.context.command.name != 'init' and os.path.exists(docs_path)
            if not is_init_without_force:
                if another_cmd:
                    log.info(f"{docs_path} already exists, skipping (use init command with --force to override)")
                    continue
                if not os.path.exists(docs_path):
                    os.mkdir(docs_path)
                defaults = self.gather_defaults(role_path)
                for default in defaults:
                    docs['defaults'].update({default: {'help': 'TODO.'}})

                with open(docs_path / 'main.yml', 'w') as (docs_file):
                    yaml.dump(docs,
                      docs_file,
                      explicit_start=True,
                      default_flow_style=False)