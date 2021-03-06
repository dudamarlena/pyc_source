# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qgispluginci/translation.py
# Compiled at: 2020-04-03 13:53:03
# Size of source mod 2**32: 6731 bytes
import glob, subprocess
from pytransifex import Transifex
from qgispluginci.parameters import Parameters
from qgispluginci.exceptions import TranslationFailed, TransifexNoResource, TransifexManyResources
from qgispluginci.utils import touch_file

class Translation:

    def __init__(self, parameters: Parameters, transifex_token: str, create_project: bool=True):
        """
        Parameters
        ----------
        parameters:

        transifex_token:
            Transifex API token

        create_project:
            if True, it will create the project, resource and language on Transifex

        """
        self.parameters = parameters
        self._t = Transifex(transifex_token, (parameters.transifex_organization), i18n_type='QT')
        if not self._t.ping():
            raise AssertionError
        else:
            self.ts_file = '{dir}/i18n/{res}_{lan}.ts'.format(dir=(self.parameters.plugin_path), res=(self.parameters.transifex_resource),
              lan=(self.parameters.translation_source_language))
            if self._t.project_exists(parameters.transifex_project):
                print('Project {o}/{p} exists on Transifex'.format(o=(self.parameters.transifex_organization), p=(self.parameters.transifex_project)))
            else:
                if create_project:
                    print('project does not exists on Transifex, creating one as {o}/{p}'.format(o=(self.parameters.transifex_organization), p=(self.parameters.transifex_project)))
                    self._t.create_project(slug=(self.parameters.transifex_project), repository_url=(self.parameters.repository_url),
                      source_language_code=(parameters.translation_source_language))
                    self.update_strings()
                    print('creating resource in {o}/{p}/{r} with {f}'.format(o=(self.parameters.transifex_organization), p=(self.parameters.transifex_project),
                      r=(self.parameters.transifex_resource),
                      f=(self.ts_file)))
                    self._t.create_resource(project_slug=(self.parameters.transifex_project), path_to_file=(self.ts_file),
                      resource_slug=(self.parameters.transifex_resource))
                    print('OK')
                else:
                    raise TranslationFailed('Project {o}/{p} does not exists on Transifex'.format(o=(self.parameters.transifex_organization),
                      p=(self.parameters.transifex_project)))

    def update_strings(self):
        """
        Update TS files from plugin source strings
        """
        cmd = [
         self.parameters.pylupdate5_path, '-noobsolete']
        for ext in ('py', 'ui'):
            for file in glob.glob('{dir}/**/*.{ext}'.format(dir=(self.parameters.plugin_path), ext=ext), recursive=True):
                cmd.append(file)

        touch_file(self.ts_file)
        cmd.append('-ts')
        cmd.append(self.ts_file)
        output = subprocess.run(cmd, capture_output=True, text=True)
        if output.returncode != 0:
            raise TranslationFailed(output.stderr)
        else:
            print('Successfully run pylupdate5: {}'.format(output.stdout))

    def compile_strings(self):
        """
        Compile TS file into QM files
        """
        cmd = [
         self.parameters.lrelease_path]
        for file in glob.glob('{dir}/i18n/*.ts'.format(dir=(self.parameters.plugin_path))):
            cmd.append(file)

        output = subprocess.run(cmd, capture_output=True, text=True)
        if output.returncode != 0:
            raise TranslationFailed(output.stderr)
        else:
            print('Successfully run lrelease: {}'.format(output.stdout))

    def pull(self):
        """
        Pull TS files from Transifex
        """
        resource = self._Translation__get_resource()
        existing_langs = self._t.list_languages(project_slug=(self.parameters.transifex_project),
          resource_slug=(resource['slug']))
        existing_langs.remove(self.parameters.translation_source_language)
        print('{c} languages found for resource {s} ({langs})'.format(s=(resource['slug']),
          c=(len(existing_langs)),
          langs=existing_langs))
        for lang in self.parameters.translation_languages:
            if lang not in existing_langs:
                print('creating missing language: {}'.format(lang))
                self._t.create_language(self.parameters.transifex_project, lang, [self.parameters.transifex_coordinator])
                existing_langs.append(lang)

        for lang in existing_langs:
            ts_file = '{dir}/i18n/{res}_{lan}.ts'.format(dir=(self.parameters.plugin_path), res=(self.parameters.transifex_resource),
              lan=lang)
            print('downloading translation file: {}'.format(ts_file))
            self._t.get_translation(self.parameters.transifex_project, resource['slug'], lang, ts_file)

    def push(self):
        resource = self._Translation__get_resource()
        print('pushing resource: {} with file {}'.format(self.parameters.transifex_resource, self.ts_file))
        result = self._t.update_source_translation(project_slug=(self.parameters.transifex_project),
          resource_slug=(resource['slug']),
          path_to_file=(self.ts_file))
        print('done: {}'.format(result))

    def __get_resource(self) -> dict:
        resources = self._t.list_resources(self.parameters.transifex_project)
        if len(resources) == 0:
            raise TransifexNoResource("project '{}' has no resource on Transifex".format(self.parameters.transifex_project))
        if len(resources) > 1:
            for resource in resources:
                if resource['name'] == self.parameters.transifex_resource:
                    return resource

            raise TransifexManyResources("project '{p}' has several resources on Transifex and none is named as the project slug.Specify one in the parameters with transifex_resource.These resources have been found: {r}".format(p=(self.parameters.transifex_project),
              r=(', '.join([r['name'] for r in resources]))))
        return resources[0]