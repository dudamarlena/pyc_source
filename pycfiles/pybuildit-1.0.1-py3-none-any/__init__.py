# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pybuilder_smart_copy_resources\__init__.py
# Compiled at: 2017-07-10 12:44:04
import os, glob, shutil
from pybuilder.core import init, task
__author__ = 'Martin Grůber'
try:
    string_types = basestring
except NameError:
    string_types = str

@init
def init_smart_copy_plugin(project, logger):
    project.set_property_if_unset('smart_copy_resources', {})
    project.set_property_if_unset('smart_copy_resources_basedir', '')


@task
def package(project, logger):
    logger.info('Copying additional resource files')
    copy_source_dir = project.expand_path(project.get_property('smart_copy_resources_basedir'))
    resources_to_copy = project.get_property('smart_copy_resources')
    if not resources_to_copy:
        logger.warn('No resources to copy configured. Consider removing plugin.')
        return
    else:
        if not isinstance(resources_to_copy, dict):
            logger.warn('Invalid smart_copy_resources property, it shall be a dict-like object')
        for glob_to_copy, copy_settings in resources_to_copy.items():
            copy_as = None
            glob_to_copy = project.expand(glob_to_copy)
            if isinstance(copy_settings, dict):
                if 'destination' not in copy_settings:
                    logger.warn(("Missing 'destination' for resource: {}").format(glob_to_copy))
                    return
                destinations = copy_settings['destination']
                if 'copy_as' in copy_settings:
                    copy_as = copy_settings['copy_as']
            else:
                destinations = copy_settings
            if isinstance(destinations, string_types):
                destinations = [
                 destinations]
            else:
                if isinstance(destinations, list) or isinstance(destinations, tuple):
                    pass
                else:
                    logger.warn(('Invalid settings for resource: {}').format(glob_to_copy))
                    return
                all_files = glob.glob(os.path.join(copy_source_dir, glob_to_copy))
                if len(all_files) < 1:
                    logger.warn(('No files found to copy in smart_copy_resources for pattern: {}').format(glob_to_copy))
                    continue
                for file_to_copy in all_files:
                    for destination in destinations:
                        destination = project.expand(destination)
                        destination = os.path.abspath(destination)
                        smart_copy_resource(file_to_copy, os.path.basename(file_to_copy) if copy_as is None else copy_as, destination, logger, verbose=project.get_property('verbose'))

        return


def smart_copy_resource(absolute_filename, relative_filename, target_directory, logger, verbose=False):
    absolute_target_file_name = os.path.join(target_directory, relative_filename)
    if verbose:
        logger.info(('Copying resource {} to {}').format(absolute_filename, absolute_target_file_name))
    parent = os.path.dirname(absolute_target_file_name)
    if not os.path.exists(parent):
        os.makedirs(parent)
    shutil.copy(absolute_filename, absolute_target_file_name)