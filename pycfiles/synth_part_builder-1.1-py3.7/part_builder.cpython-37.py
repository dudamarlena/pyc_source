# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/synth_part_builder/part_builder.py
# Compiled at: 2019-06-18 17:02:09
# Size of source mod 2**32: 19559 bytes
"""
    Builds the docker-compose file using modular
    components specified by the user

    Also builds the NGINX router default.conf
    containing the routing for desired services

    Functions primarily do text appending,
    CLI logic is enclosed in synth.py
"""
import os
from part_builder import PartBuilderException

class PartBuilder:
    __doc__ = '\n        Part builder class for use with building the compose file\n        and nginx router file\n    '
    allowed_frontends = ['static', 'dynamic', 'react', 'reactjs']
    allowed_backends = ['node', 'flask', 'django']
    allowed_databases = ['mongo', 'postgres', 'mysql', 'mariadb']
    allowed_caches = ['redis', 'memcached']

    def __init__(self, parts_root=None, project_name=None, front_enabled=False, back_enabled=False):
        """
            Init method for class, sets important path information
        """
        self.str_check(parts_root, 'root to parts directory must be of type string in PartBuilder init function')
        self.str_check(project_name, 'default.conf file for NGINX router must be of type string in PartBuilder init function')
        nginx_file = '{}/nginx_router/nginx_conf/default.conf'.format(project_name)
        compose_file = '{}/docker-compose.yml'.format(project_name)
        if not os.path.isfile(nginx_file):
            raise PartBuilderException('{} is not a file or does not exist'.format(nginx_file))
        if not os.path.isfile(compose_file):
            raise PartBuilderException('{} is not a file or does not exist'.format(compose_file))
        self.parts_root = parts_root
        self.project_name = project_name
        self.nginx_file = nginx_file
        self.compose_file = compose_file
        self.allowed_master = []
        self.allowed_master.extend(self.allowed_frontends)
        self.allowed_master.extend(self.allowed_backends)
        self.allowed_master.extend(self.allowed_databases)
        self.allowed_master.extend(self.allowed_caches)
        self.compose_router_update(front_enabled=front_enabled,
          back_enabled=back_enabled)

    @staticmethod
    def str_check(param=None, err_msg='Path Error'):
        """
            Checks that variables passed to PartBuilder functions
            are not None and exist

            Based on:
                param: variable to check
                err_msg: error message to output
        """
        if param is None:
            raise PartBuilderException(err_msg)
        else:
            if type(param) != str:
                raise PartBuilderException(err_msg)

    def build_pipeline(self, name, pipeline, parts={}):
        """
            builds the config file for the ci / cd selected by user for the parts provided

            Based on:
                name: name of the project, used for tagging docker builds
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts for project
        """
        if len(parts) == 0 or parts.values() == [None for tmp in range(len(parts.values()))]:
            raise PartBuilderException('PartBuilder cannot build CI/CD pipeline with no parts provided')
        else:
            parts_path = '{}/pipeline/{}'.format(self.parts_root, pipeline)
            base_part_path = '{}/base.part'.format(parts_path)
            config_path = None
            if pipeline == 'travis':
                config_path = '{}/.travis.yml'.format(self.project_name)
            else:
                raise PartBuilderException('Pipeline ({}) is not yet configured for synth!')
        with open(base_part_path, 'r') as (base_part):
            part_data = base_part.readlines()
        with open(config_path, 'w') as (new_config):
            new_config.writelines(part_data)
        self.build_pipeline_section_pre_tests(pipeline, parts, parts_path, config_path)
        self.build_pipeline_section_tests(pipeline, parts, parts_path, config_path)
        self.build_pipeline_section_deploy(pipeline, parts, parts_path, config_path)
        with open(config_path, 'r') as (cur_config):
            conf_data = cur_config.readlines()
        new_data = []
        for line in conf_data:
            line = line.format(self.project_name)
            new_data.append(line)

        with open(config_path, 'w') as (new_config):
            new_config.writelines(new_data)

    def build_pipeline_section_pre_tests(self, pipeline, parts, parts_path, config_path):
        """
            builds the before_install section to build containers for testing

            Base on:
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts to test
                parts_path: path to pipeline parts location
                config_path: path to config file for pipeline
                             e.g: .travis.yml
        """
        parts_path += '/pre_tests'
        config_data = []
        with open(config_path, 'r') as (base_config):
            config_data = base_config.readlines()
        with open('{}/base.part'.format(parts_path), 'r') as (base_part):
            part_data = base_part.readlines()
            config_data.extend(part_data)
        for part_name, part in parts.items():
            if not part is None:
                if part_name == 'cache' or part_name == 'database' or part in ('dynamic',
                                                                               'static'):
                    continue
                if not os.path.isfile('{}/{}.part'.format(parts_path, part_name)):
                    continue
                with open('{}/{}.part'.format(parts_path, part_name), 'r') as (file):
                    part_data = file.readlines()
                    config_data.extend(part_data)

        with open(config_path, 'w') as (new_config):
            new_config.writelines(config_data)

    def build_pipeline_section_tests(self, pipeline, parts, parts_path, config_path):
        """
            builds the before_install section to build containers for testing

            Base on:
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts to test
                parts_path: path to pipeline parts location
                config_path: path to config file for pipeline
                             e.g: .travis.yml
        """
        parts_path += '/tests'
        config_data = []
        with open(config_path, 'r') as (base_config):
            config_data = base_config.readlines()
        with open('{}/base.part'.format(parts_path), 'r') as (base_part):
            part_data = base_part.readlines()
            config_data.extend(part_data)
        for part_name, part in parts.items():
            if not part is None:
                if part_name == 'cache' or part_name == 'database':
                    continue
                if not os.path.isfile('{}/{}.part'.format(parts_path, part)):
                    continue
                with open('{}/{}.part'.format(parts_path, part), 'r') as (file):
                    part_data = file.readlines()
                    config_data.extend(part_data)

        with open(config_path, 'w') as (new_config):
            new_config.writelines(config_data)

    def build_pipeline_section_deploy(self, pipeline, parts, parts_path, config_path):
        """
            builds the before_install section to build containers for testing

            Base on:
                pipeline: pipeline being used (travis or CircleCI)
                parts: list of parts to test
                parts_path: path to pipeline parts location
                config_path: path to config file for pipeline
                             e.g: .travis.yml
        """
        parts_path += '/deploy'
        config_data = []
        with open(config_path, 'r') as (base_config):
            config_data = base_config.readlines()
        with open('{}/base.part'.format(parts_path), 'r') as (base_part):
            part_data = base_part.readlines()
            config_data.extend(part_data)
        build_dir = parts_path + '/build'
        with open('{}/router.part'.format(build_dir), 'r') as (router_part):
            part_data = router_part.readlines()
            config_data.extend(part_data)
        for part_name, part in parts.items():
            if not part is None:
                if part_name == 'cache' or part_name == 'database':
                    continue
                if not os.path.isfile('{}/{}.part'.format(build_dir, part_name)):
                    continue
                with open('{}/{}.part'.format(build_dir, part_name), 'r') as (file):
                    part_data = file.readlines()
                    config_data.extend(part_data)

        push_dir = parts_path + '/push'
        with open('{}/router.part'.format(push_dir), 'r') as (router_part):
            part_data = router_part.readlines()
            config_data.extend(part_data)
        for part_name, part in parts.items():
            if not part is None:
                if part_name == 'cache' or part_name == 'database':
                    continue
                if not os.path.isfile('{}/{}.part'.format(push_dir, part_name)):
                    continue
                with open('{}/{}.part'.format(push_dir, part_name), 'r') as (file):
                    part_data = file.readlines()
                    config_data.extend(part_data)

        with open(config_path, 'w') as (new_config):
            new_config.writelines(config_data)

    def add_part(self, part=None, database=None, cache=None):
        """
            adds a part to compose and nginx files based on a string passed

            Based on:
                part: string representing part to add,
                    e.g: static
        """
        self.str_check(part, 'PartBuilder cannot add part of type {}'.format(type(part)))
        part = part.lower()
        if part in self.allowed_master:
            self.upstream_add(self.parts_root + '/nginx/upstream/{}.part'.format(part), self.nginx_file)
            self.location_add(self.parts_root + '/nginx/location/{}.part'.format(part), self.nginx_file)
            self.compose_add(self.parts_root + '/compose/{}.part'.format(part), self.compose_file)
            if not part in self.allowed_backends or database is not None or cache is not None:
                self.backend_compose_update(database, cache)
        else:
            raise PartBuilderException('part provided to PartBuilder ({}) is not in allowed_master'.format(part))

    def compose_router_update(self, front_enabled=False, back_enabled=False):
        """
        must be run before all other things dealing with compose building
        due to relating with the router
        """
        if not front_enabled:
            if not back_enabled:
                return
        self.compose_add(self.parts_root + '/compose/depends/base.part', self.compose_file)
        if front_enabled:
            self.compose_add(self.parts_root + '/compose/depends/frontend.part', self.compose_file)
        if back_enabled:
            self.compose_add(self.parts_root + '/compose/depends/backend.part', self.compose_file)

    def backend_compose_update(self, database, cache):
        """
            updates the compose file after adding a part if its a backend by adding
            neccessary environmental variables and depends_on sections
        """
        if database not in self.allowed_databases:
            if cache not in self.allowed_caches:
                raise PartBuilderException('backend_compose_update failed because database or cache not in allowed services')
        self.compose_add(self.parts_root + '/compose/depends/base.part', self.compose_file)
        if database in self.allowed_databases:
            self.compose_add(self.parts_root + '/compose/depends/{}.part'.format(database), self.compose_file)
        if cache in self.allowed_caches:
            self.compose_add(self.parts_root + '/compose/depends/{}.part'.format(cache), self.compose_file)
        self.compose_add(self.parts_root + '/compose/env/base.part', self.compose_file)
        if database in self.allowed_databases:
            self.compose_add(self.parts_root + '/compose/env/{}.part'.format(database), self.compose_file)
        if cache in self.allowed_caches:
            self.compose_add(self.parts_root + '/compose/env/{}.part'.format(cache), self.compose_file)

    def compose_add(self, part_path=None, config_path=None):
        """
            Adds a part to the master docker-compose file

            Based on:
                part_path: path to the part to add
                compose_path: path to master compose file to add to
        """
        path_err = 'Path to compose service part (part_path) must be of string type'
        config_err = 'Path to docker-compose file (config_path) must be of string type'
        self.str_check(part_path, path_err)
        self.str_check(config_path, config_err)
        if os.path.isfile(part_path) is False:
            raise PartBuilderException('{} is not a file or did not exist.'.format(part_path))
        with open(part_path, 'r') as (part_file):
            part_data = part_file.readlines()
        with open(config_path, 'r') as (file):
            cur_config = file.readlines()
        cur_config.extend(part_data)
        with open(config_path, 'w') as (new_config):
            new_config.writelines(cur_config)

    def upstream_add(self, part_path=None, config_path=None):
        """
            Adds an upstream to the NGINX router default.conf file

            ONLY needed for frontend and backend portions

            Based on:
                part_path: path to the part containing the upstream
                config_path: path to the NGINX router default.conf file
        """
        path_err = 'Path to upstream part (part_path) must be of string type'
        config_err = 'Path to NGINX router file (config_path) must be of string type'
        self.str_check(part_path, path_err)
        self.str_check(config_path, config_err)
        if os.path.isfile(part_path) is False:
            return
        with open(part_path, 'r') as (part_file):
            part_data = part_file.readlines()
        with open(config_path, 'r') as (file):
            cur_config = file.readlines()
        part_data.extend(cur_config)
        with open(config_path, 'w') as (new_config):
            new_config.writelines(part_data)

    def location_add(self, part_path=None, config_path=None):
        """
            Adds a location block to the server block in the NGINX router
            default.conf file
            This is needed for routing requests to the upstream

            Based on:
                part_path: path to the part containing the location
                config_path: path to the NGINX router default.conf file
        """
        path_err = 'Path to location part (part_path) must be of string type'
        config_err = 'Path to NGINX router file (config_path) must be of string type'
        self.str_check(part_path, path_err)
        self.str_check(config_path, config_err)
        if os.path.isfile(part_path) is False:
            return
        with open(part_path, 'r') as (part_file):
            part_data = part_file.readlines()
        with open(config_path, 'r') as (file):
            cur_config = file.readlines()
        del cur_config[-1]
        cur_config.extend(part_data)
        cur_config.append('}')
        with open(config_path, 'w') as (new_config):
            new_config.writelines(cur_config)