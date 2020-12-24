# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qgispluginci/parameters.py
# Compiled at: 2020-04-03 13:53:03
# Size of source mod 2**32: 4831 bytes
import os, re
from slugify import slugify
import datetime, warnings

class Parameters:
    __doc__ = "\n    Attributes\n    ----------\n    plugin_path: str\n        The directory of the source code in the repository.\n        Defaults to: `slugify(plugin_name, separator='_')`\n\n    github_organization_slug: str\n        The organization slug on SCM host (e.g. Github) and translation platform (e.g. Transifex).\n        Not required when running on Travis since deduced from `$TRAVIS_REPO_SLUG`environment variable.\n        \n    project_slug: str\n        The project slug on SCM host (e.g. Github) and translation platform (e.g. Transifex).\n        Not required when running on Travis since deduced from `$TRAVIS_REPO_SLUG`environment variable.\n\n    transifex_coordinator: str\n        The username of the coordinator in Transifex.\n        Required to create new languages.\n\n    transifex_organization: str\n        The organization name in Transifex\n        Defaults to: the GitHub organization slug\n\n    transifex_project: str\n        The project on Transifex, which can be different from the one on GitHub.\n        Defaults to: the project_slug\n\n    transifex_resource: str\n        The resource name in transifex\n        Defaults to: the project_slug\n\n    translation_source_language:\n        The source language for translations.\n        Defaults to: 'en'\n\n    translation_languages:\n        List of languages.\n\n    create_date: datetime.date\n        The date of creation of the plugin.\n        The would be used in the custom repository XML.\n        Format: YYYY-MM-DD\n\n    lrelease_path: str\n        The path of lrelease executable\n\n    pylupdate5_path: str\n        The path of pylupdate executable\n\n\n    "

    def __init__(self, definition: dict):
        self.plugin_path = definition['plugin_path']
        self.plugin_name = self._Parameters__get_from_metadata('name')
        self.plugin_slug = slugify(self.plugin_name)
        self.project_slug = definition.get('project_slug', os.environ.get('TRAVIS_REPO_SLUG', '.../{}'.format(self.plugin_slug)).split('/')[1])
        self.github_organization_slug = definition.get('github_organization_slug', os.environ.get('TRAVIS_REPO_SLUG', '').split('/')[0])
        self.transifex_coordinator = definition.get('transifex_coordinator', '')
        self.transifex_organization = definition.get('transifex_organization', self.github_organization_slug)
        self.translation_source_language = definition.get('translation_source_language', 'en')
        self.translation_languages = definition.get('translation_languages', {})
        self.transifex_project = definition.get('transifex_project', self.project_slug)
        self.transifex_resource = definition.get('transifex_resource', self.project_slug)
        self.create_date = datetime.datetime.strptime(str(definition.get('create_date', datetime.date.today())), '%Y-%m-%d')
        self.lrelease_path = definition.get('lrelease_path', 'lrelease')
        self.pylupdate5_path = definition.get('pylupdate5_path', 'pylupdate5')
        self.author = self._Parameters__get_from_metadata('author', '')
        self.description = self._Parameters__get_from_metadata('description')
        self.qgis_minimum_version = self._Parameters__get_from_metadata('qgisMinimumVersion')
        self.icon = self._Parameters__get_from_metadata('icon', '')
        self.tags = self._Parameters__get_from_metadata('tags', '')
        self.experimental = self._Parameters__get_from_metadata('experimental', False)
        self.deprecated = self._Parameters__get_from_metadata('deprecated', False)
        self.issue_tracker = self._Parameters__get_from_metadata('tracker')
        self.homepage = self._Parameters__get_from_metadata('homepage', '')
        if self.homepage == '':
            warnings.warn('Homepage is not given in the metadata. It is a requirement to publish the plugin on the repository')
        self.repository_url = self._Parameters__get_from_metadata('repository')

    def archive_name(self, release_version: str) -> str:
        """
        Returns the archive file name
        """
        return '{zipname}.{release_version}.zip'.format(zipname=(self.plugin_slug), release_version=release_version)

    def __get_from_metadata(self, key: str, default_value: any=None) -> str:
        metadata_file = '{}/metadata.txt'.format(self.plugin_path)
        with open(metadata_file) as (f):
            for line in f:
                m = re.match('{}\\s*=\\s*(.*)$'.format(key), line)
                if m:
                    return m.group(1)

        if default_value is None:
            raise Exception('missing key in metadata: {}'.format(key))
        return default_value