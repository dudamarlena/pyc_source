# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/env.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 14788 bytes
__doc__ = '\nEnv subcommand\n'
import io, logging, os, tempfile, warnings
from functools import lru_cache
from compose_flow import docker, errors, utils
from compose_flow.commands.subcommands import BaseSubcommand
from compose_flow.config import get_config
from compose_flow.environment.backends import get_backend
DOCKER_IMAGE_VAR = 'DOCKER_IMAGE'
VERSION_VAR = 'VERSION'
RUNTIME_PLACEHOLDER = 'runtime://'
ENV_EXTENDS_BASENAME = 'CF_ENV_EXTENDS_BASENAME'

class Env(BaseSubcommand):
    """Env"""
    setup_profile = False

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, *kwargs)
        self._config = None
        self._docker_image = None
        self._data = None
        self._data_modified = False
        self._persistable_keys = []
        self._rendered_config = {}

    def _get_default_backend(self, remote):
        app_config = self.workflow.app_config
        remote_section = app_config.get('remotes', {}).get(remote, {})
        if 'environment' in remote_section.keys():
            warning_msg = 'The environment subsection of .compose/config.yml has been deprecated! Please flatten your remotes to just the backend field.'
            warnings.warn(warning_msg)
            remote_section = remote_section.get('environment', {})
        return remote_section.get('backend')

    @property
    def backend(self):
        """
        Returns the environment backend to use
        """
        return self.get_backend()

    def get_backend(self, remote=None):
        backend_name = 'local'
        remote = remote or self.workflow.args.remote
        project_config = get_config(self.workflow)
        if remote is not None:
            project_backend_name = project_config.get('remotes', {}).get(remote, {}).get('backend')
            default_backend_name = self._get_default_backend(remote)
            if project_backend_name:
                backend_name = project_backend_name
            elif default_backend_name:
                backend_name = default_backend_name
        backend = get_backend(backend_name, workflow=(self.workflow))
        self.logger.debug(f"backend_name={backend_name}, backend={backend}")
        return backend

    def edit(self) -> None:
        """
        Open the current backend data in an editor and write changes back
        """
        with tempfile.NamedTemporaryFile('w') as (fh):
            path = fh.name
            self.render_buf(fh, runtime_config=False)
            fh.flush()
            editor = os.environ.get('EDITOR', os.environ.get('VISUAL', 'vi'))
            self.execute(f"{editor} {path}", _fg=True)
            self.backend.write(self.workflow.config_name, path)

    def write(self) -> None:
        """
        Writes the environment into the backend
        """
        with tempfile.NamedTemporaryFile('w+') as (fh):
            self.render_buf(fh, runtime_config=False)
            fh.flush()
            self.backend.write(self.workflow.config_name, fh.name)

    @classmethod
    def fill_subparser(cls, parser, subparser):
        subparser.add_argument('action')
        subparser.add_argument('path', nargs='*')
        subparser.add_argument('-f',
          '--force', action='store_true', help='edit even if no config found')
        subparser.add_argument('--variables',
          action='store_true',
          help='show runtime variables instead of values')

    def cat(self) -> str:
        """
        Prints the loaded config to stdout
        """
        print(self.render())

    @property
    def cf_env(self):
        """
        Returns defaults for the environment
        """
        args = self.workflow.args
        return {'CF_ENV':args.environment or '', 
         'CF_PROJECT':self.workflow.project_name, 
         'CF_ENV_NAME':self.workflow.project_name}

    @property
    def data(self) -> dict:
        """
        Returns the loaded config as a dictionary
        """
        if self._data is not None:
            return self._data
        else:
            data = self.load()
            for k, v in data.items():
                if not v.startswith(RUNTIME_PLACEHOLDER):
                    pass
                else:
                    location, location_ref = v.split('://', 1)
                    location_ref = location_ref or k
                    if k not in self._rendered_config:
                        self._rendered_config[k] = v
                    new_val = os.environ.get(location_ref)
                    if new_val is None:
                        if hasattr(self.workflow.args, 'action'):
                            if self.is_env_modification_action():
                                new_val = RUNTIME_PLACEHOLDER
                        else:
                            raise errors.RuntimeEnvError(f"runtime substitution for {k}={v} not found")
                    data[k] = new_val

            sub_count = True
            while sub_count:
                sub_count = 0
                for k, v in data.items():
                    rendered = utils.render(v, env=data)
                    if rendered != v:
                        sub_count += 1
                        if k not in self._rendered_config:
                            self._rendered_config[k] = v
                        data[k] = rendered

            if self.workflow.subcommand.update_version_env_vars:
                self._docker_image = None
                data.update({DOCKER_IMAGE_VAR: self.set_docker_tag(self.docker_image), 
                 VERSION_VAR: self.version})
            self._data = data
            return self._data

    @property
    def docker_image(self) -> str:
        """
        Generates a docker image name for this action
        """
        if self._docker_image:
            return self._docker_image
        else:
            registry_domain = self.workflow.docker_image_prefix
            project_name = self.workflow.project_name
            env = self.workflow.environment_name
            docker_image = f"{registry_domain}/{project_name}:{env}"
            self._docker_image = self.set_docker_tag(docker_image)
            return self._docker_image

    def set_docker_tag(self, docker_image: str) -> str:
        """
        Sets the docker image tag based on the current version
        """
        if ':' not in docker_image:
            raise EnvironmentError('compose-flow enforces image versioning; DOCKER_IMAGE must contain a colon')
        return f"{docker_image.split(':', 1)[0]}:{self.version}"

    def update(self, new_data: dict, persistable: bool=True):
        """
        Updates the environment data with the new given data

        When persistable is True, the values being set are flagged for persisting into the backend
        and the _data_modified flag is set
        """
        data = self._data or {}
        data.update(new_data)
        if persistable:
            self._persistable_keys.extend(list(new_data.keys()))
            self._data_modified = True
        self._data = data

    def is_dirty_working_copy_okay(self, exc):
        is_dirty_working_copy_okay = super().is_dirty_working_copy_okay(exc)
        return is_dirty_working_copy_okay or self.is_env_modification_action()

    def is_env_error_okay(self, exc):
        return self.workflow.args.action in ('push', )

    def is_env_runtime_error_okay(self):
        return self.is_env_modification_action()

    def is_missing_config_okay(self, exc):
        args = self.workflow.args
        subcommand = self.workflow.subcommand
        force = 'force' in args and args.force
        try:
            action = self.workflow.args.action
        except AttributeError:
            action = None

        return action in ('edit', ) and force

    def is_env_modification_action(self):
        return self.workflow.args.action in ('cat', 'edit', 'push')

    def is_write_profile_error_okay(self, exc):
        return self.is_env_modification_action()

    def load(self, basename: str=None, post_process: bool=True) -> dict:
        """
        Loads an environment from the backend

        Args:
            basename: the config basename to load
            post_process: whether to perform post-processing upon reading data
        """
        data = {}
        environment = self.workflow.environment_name
        if not environment:
            return data
        else:
            config_name = self.workflow.config_name
            if basename:
                config_name = f"{self.workflow.args.environment}-{basename}"
            try:
                backend = self.get_backend(remote=(self.workflow.args.config_remote))
                content = backend.read(config_name)
            except errors.NoSuchConfig as exc:
                if not self.is_missing_config_okay(exc):
                    raise
                content = ''

            for idx, line in enumerate(content.splitlines()):
                if line.strip() == '':
                    pass
                else:
                    if line.strip().startswith('#'):
                        pass
                    else:
                        try:
                            line_split = line.split('=', 1)
                            if len(line_split) == 1:
                                line_split.append('')
                            key, value = line_split
                        except ValueError as exc:
                            self.logger.error(f"ERROR: unable to parse line number {idx}, edit your env: {line}")
                            raise

                        data[key] = value

            if post_process:
                self.update(data)
                self._docker_image = data.get('DOCKER_IMAGE')
            return data

    @property
    def logger(self):
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def render(self, data: dict=None) -> str:
        """
        Returns a rendered file in .env file format
        """
        buf = io.StringIO()
        try:
            runtime_config = not self.args.variables
        except AttributeError:
            runtime_config = True

        self.render_buf(buf, data=data, runtime_config=runtime_config)
        return buf.getvalue()

    def render_buf(self, buf, data: dict=None, runtime_config: bool=True):
        data = data or self.data
        if runtime_config:
            extended_configs = []
            _data, data = data, {}
            while True:
                extended_configs.insert(0, _data)
                extends_env = _data.get(ENV_EXTENDS_BASENAME)
                if not extends_env:
                    break
                self.logger.info(f"extending current env with {extends_env}")
                _data = self.load(basename=extends_env, post_process=False)

            for extended_config in extended_configs:
                data.update(extended_config)

            for k, v in self.cf_env.items():
                if k not in data:
                    data[k] = v

        else:
            data.update(self._rendered_config)
        lines = []
        for k, v in data.items():
            lines.append(f"{k}={v}")

        buf.write('\n'.join(sorted(lines)))

    def rm(self) -> None:
        """
        Removes an environment from the backend
        """
        self.backend.rm(self.workflow.config_name)

    def update_workflow_env(self):
        """
        Overwrites the cf environment in the data dictionary

        Even if values are already set, overwrite them with current values
        """
        self.data.update(self.cf_env)

    @property
    @lru_cache()
    def version(self):
        """
        Returns a version string for the current version of code
        """
        tag_version = self.workflow.args.tag_version
        if tag_version:
            return tag_version
        else:
            tag_version = self.workflow.environment_name
            try:
                tag_version = utils.get_tag_version(default=tag_version)
            except Exception as exc:
                subcommand = self.workflow.subcommand
                if not subcommand.is_dirty_working_copy_okay(exc):
                    raise errors.TagVersionError(f"Warning: unable to run tag-version ({exc})\n",
                      shell_exception=exc,
                      tag_version=tag_version)

            return tag_version