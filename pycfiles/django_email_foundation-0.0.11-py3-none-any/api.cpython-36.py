# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/api.py
# Compiled at: 2019-03-27 04:19:31
# Size of source mod 2**32: 8732 bytes
import os, subprocess
from importlib import import_module
from shutil import which, copyfile, copytree
from typing import Union, List, Dict, Optional
from django.urls import reverse
from django_email_foundation import settings
from django_email_foundation.utils import get_relative_from_manage_path

class Checks:
    FOLDERS = ('pages', 'layouts', 'partials', 'helpers', 'assets', 'data')
    CHECKS = (('npm_or_yarn_installed', 'The "npm" or "yarn" is not installed or is not in your $PATH'),
              ('required_node_packages', 'Some of the required modules are not installed in "node_modules". Please run "./manage.py install_requires"'),
              ('templates_source_path', 'It is necessary to define DEF_TEMPLATES_SOURCE_PATH in your settings'),
              ('templates_dir_structure', 'The templates directory must have a valid structure. It must contain the pages, layouts, partials and helpers folders. You can run "./manage.py create_basic_structure" to build this structure, and to add a basic layout '),
              ('templates_target_path', 'It is necessary to define DEF_TEMPLATES_TARGET_PATH in your settings'),
              ('static_target_path', 'You must to set the DEF_STATIC_TARGET_PATH setting'),
              ('exists_pages', "You do not have any template in your 'pages' folder. Please, create one before run the email builder command"))

    def exists_pages(self) -> bool:
        """
        It checks if exists some template in the "pages" folder.
        :return:
        """
        if not self.templates_source_path():
            return True
        else:
            try:
                walk = os.listdir(os.path.join(self.get_templates_source_path(), 'pages'))
            except FileNotFoundError:
                return False

            return bool(walk)

    def npm_or_yarn_installed(self) -> bool:
        """
        It checks if the npm or yarn is installed in your system path.
        :return:
        """
        return bool(which(settings.DEF_NPM_OR_YARN))

    def required_node_packages(self) -> bool:
        """
        Iterate the required node packages list and check if are installed in your node_modules folder.
        :return:
        """
        for required_package in settings.DEF_NODE_PACKAGES_REQUIRED:
            name = required_package.split('@')[0]
            if not os.path.isdir('{}/node_modules/{}'.format(settings.DEF_NODE_MODULES_PATH, name)):
                return False

        return True

    def templates_source_path(self) -> bool:
        """
        Check if you have the source path in your settings.
        :return:
        """
        return bool(settings.DEF_TEMPLATES_SOURCE_PATH)

    def static_target_path(self) -> bool:
        """
        Check if the follow constance it's defined
        :return:
        """
        return bool(settings.DEF_STATIC_TARGET_PATH)

    def templates_target_path(self) -> bool:
        """
        Check if you have the target path in your settings.
        :return:
        """
        return bool(settings.DEF_TEMPLATES_TARGET_PATH)

    @staticmethod
    def get_templates_source_path() -> str:
        return get_relative_from_manage_path(settings.DEF_TEMPLATES_SOURCE_PATH)

    @staticmethod
    def get_templates_target_path() -> str:
        return get_relative_from_manage_path(settings.DEF_TEMPLATES_TARGET_PATH)

    def exists_folder(self, name: str) -> bool:
        """
        Check if exist the named folder in the source path folder.
        :param name:
        :return:
        """
        full_path = '{}/{}'.format(Checks.get_templates_source_path(), name)
        return os.path.isdir(full_path)

    def templates_dir_structure(self) -> bool:
        """
        Check if you have the right folders inside your source path folder.
        :return:
        """
        if not settings.DEF_TEMPLATES_SOURCE_PATH:
            return False
        else:
            for folder in self.FOLDERS:
                if not self.exists_folder(folder):
                    return False

            return True

    def start(self) -> List[str]:
        """
        Start to analyze all checks
        :return: A list of error text if exists...
        """
        errors = []
        for method, error_txt in self.CHECKS:
            if not getattr(self, method)():
                errors.append(error_txt)

        return errors


class DjangoEmailFoundation:
    __doc__ = '\n    Main API object for manage the library functionality.\n    '

    def perform_checks(self) -> Union[(bool, List[str])]:
        checks = Checks()
        return checks.start()

    def copy_gulpfile(self):
        """Copy the gulp file to the destination folder, where node_modules is installed"""
        current = os.path.dirname(os.path.realpath(__file__))
        copyfile(os.path.join(current, 'gulpfile.js'), os.path.join(settings.DEF_NODE_MODULES_PATH, 'gulpfile.js'))

    @property
    def install_required_packages(self) -> bool:
        """
        It install the required node packages from the DEF_NODE_PACKAGES_REQUIRED list, and return a True
        if everything went ok. Finally, copy the gulpfile.js file to the target folder.
        :return: Return the bool success value
        """
        command = [
         settings.DEF_NPM_OR_YARN,
         settings.DEF_NPM_YARN_INSTALL_COMMAND] + list(settings.DEF_NODE_PACKAGES_REQUIRED)
        exit_code = subprocess.call(command, cwd=(settings.DEF_NODE_MODULES_PATH))
        if exit_code != 0:
            return False
        else:
            self.copy_gulpfile()
            return True

    @property
    def preview_url(self) -> str:
        host = settings.DEF_RUNSERVER_HOST
        uri = reverse('django_email_foundation:index')
        return '{}{}'.format(host, uri)

    def run_watch(self):
        """
        Run the watch gulp task sending the right parameters, such as where is the source templates, the target, files
        to be ignored, etc.
        :return:
        """
        command = (
         './node_modules/.bin/gulp',
         'watch',
         '--templates_source={}'.format(settings.DEF_TEMPLATES_SOURCE_PATH),
         '--templates_target={}'.format(settings.DEF_TEMPLATES_TARGET_PATH),
         '--static_target={}'.format(settings.DEF_STATIC_TARGET_PATH),
         '--ignore_files={}'.format(','.join(settings.DEF_IGNORE_FILES)),
         '--preview_url={}'.format(self.preview_url))
        subprocess.call(command, cwd=(settings.DEF_NODE_MODULES_PATH))

    def create_basic_structure(self) -> Optional[str]:
        """
        It creates the basic foundation for emails (or panini) structure in your source path folder.
        :return: If some error occurs, the method return the description.
        """
        source_default_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'default_templates')
        for folder in Checks.FOLDERS:
            source_path = '{}/{}'.format(source_default_templates, folder)
            target_path = '{}/{}'.format(Checks.get_templates_source_path(), folder)
            if os.path.isdir(target_path):
                pass
            else:
                try:
                    if os.path.isdir(source_path):
                        copytree(source_path, target_path)
                    else:
                        os.mkdir(target_path)
                except FileNotFoundError as e:
                    return '{}. Please, check your DEF_TEMPLATES_SOURCE_PATH setting. The value must be start from the root project.'.format(str(e))

        self.copy_gulpfile()

    def get_build_files(self) -> Dict[(str, List[str])]:
        """
        Read the target folder and return the folders and build files. Useful for send in the preview view context.
        :return:
        """
        response = {}
        for root, dirs, files in os.walk(Checks.get_templates_target_path()):
            folder = root.split('/')[(-1)]
            if files:
                response[folder] = files

        return response

    def get_context(self) -> Optional[dict]:
        if not Checks.get_templates_source_path():
            return
        else:
            source_path = Checks.get_templates_source_path().replace('/', '.')
            module_path = '{}.data.context'.format(source_path)
            context = import_module(module_path).context
            return context