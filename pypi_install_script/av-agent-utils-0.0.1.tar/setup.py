#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'av-agent-utils',
        version = '0.0.1',
        description = 'Some debugging tools for AV engineers to use',
        long_description = '',
        author = 'Rusty Brooks',
        author_email = 'rbrooks@alienvault.com',
        license = 'AlienVault Commercial',
        url = 'https://github.com/AlienVault-Engineering/agent-utils',
        scripts = [
            'scripts/agent-lookup-streams',
            'scripts/foo.config',
            'scripts/agent-validate-sts-tokens'
        ],
        packages = ['av_agent_utils'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'botocore',
            'boto3',
            'gimme_aws_creds'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '>=3.6.0',
        obsoletes = [],
    )
