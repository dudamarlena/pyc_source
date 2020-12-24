# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/cwl/runtime_actions.py
# Compiled at: 2018-04-20 03:19:42
import json, os, shutil
from galaxy.util import safe_makedirs
from .cwltool_deps import ref_resolver
from .parser import JOB_JSON_FILE, load_job_proxy
from .util import SECONDARY_FILES_INDEX_PATH, STORE_SECONDARY_FILES_WITH_BASENAME

class FileDescription(object):
    pass


class PathFileDescription(object):

    def __init__(self, path):
        self.path = path

    def write_to(self, destination):
        shutil.copy(self.path, destination)


class LiteralFileDescription(object):

    def __init__(self, content):
        self.content = content

    def write_to(self, destination):
        with open(destination, 'wb') as (f):
            f.write(self.content.encode('UTF-8'))


def _possible_uri_to_path(location):
    if location.startswith('file://'):
        path = ref_resolver.uri_file_path(location)
    else:
        path = location
    return path


def file_dict_to_description(file_dict):
    assert file_dict['class'] == 'File', file_dict
    location = file_dict['location']
    if location.startswith('_:'):
        return LiteralFileDescription(file_dict['contents'])
    else:
        return PathFileDescription(_possible_uri_to_path(location))


def handle_outputs(job_directory=None):
    if job_directory is None:
        job_directory = os.path.join(os.getcwd(), os.path.pardir)
    cwl_job_file = os.path.join(job_directory, JOB_JSON_FILE)
    if not os.path.exists(cwl_job_file):
        return
    else:
        job_proxy = load_job_proxy(job_directory, strict_cwl_validation=False)
        tool_working_directory = os.path.join(job_directory, 'working')
        outputs = job_proxy.collect_outputs(tool_working_directory)
        provided_metadata = {}

        def move_directory(output, target_path, output_name=None):
            assert output['class'] == 'Directory'
            output_path = _possible_uri_to_path(output['location'])
            if output_path.startswith('_:'):
                safe_makedirs(target_path)
                for listed_file in output['listing']:
                    assert listed_file['class'] == 'File'
                    file_description = file_dict_to_description(listed_file)
                    file_description.write_to(os.path.join(target_path, listed_file['basename']))

            else:
                shutil.move(output_path, target_path)
            return {'cwl_filename': output['basename']}

        def move_output(output, target_path, output_name=None):
            assert output['class'] == 'File'
            file_description = file_dict_to_description(output)
            file_description.write_to(target_path)
            secondary_files = output.get('secondaryFiles', [])
            if secondary_files:
                order = []
                index_contents = {'order': order}
                for secondary_file in secondary_files:
                    if output_name is None:
                        raise NotImplementedError('secondaryFiles are unimplemented for dynamic list elements')
                    secondary_file_description = file_dict_to_description(secondary_file)
                    secondary_file_basename = secondary_file['basename']
                    if not STORE_SECONDARY_FILES_WITH_BASENAME:
                        output_basename = output['basename']
                        prefix = ''
                        while True:
                            if secondary_file_basename.startswith(output_basename):
                                secondary_file_name = prefix + secondary_file_basename[len(output_basename):]
                                break
                            prefix = '^%s' % prefix
                            if '.' not in output_basename:
                                secondary_file_name = prefix + secondary_file_name
                                break
                            else:
                                output_basename = output_basename.rsplit('.', 1)[0]

                    else:
                        secondary_file_name = secondary_file_basename
                    secondary_files_dir = job_proxy.output_secondary_files_dir(output_name, create=True)
                    extra_target = os.path.join(secondary_files_dir, secondary_file_name)
                    secondary_file_description.write_to(extra_target)
                    order.append(secondary_file_name)

                with open(os.path.join(secondary_files_dir, '..', SECONDARY_FILES_INDEX_PATH), 'w') as (f):
                    json.dump(index_contents, f)
            return {'cwl_filename': output['basename']}

        def handle_known_output(output, output_key, output_name):
            assert output_name
            if output['class'] == 'File':
                target_path = job_proxy.output_path(output_name)
                file_metadata = move_output(output, target_path, output_name=output_name)
            elif output['class'] == 'Directory':
                target_path = job_proxy.output_directory_contents_dir(output_name)
                file_metadata = move_directory(output, target_path, output_name=output_name)
            else:
                raise Exception('Unknown output type [%s] encountered' % output)
            provided_metadata[output_name] = file_metadata

        for output_name, output in outputs.items():
            if isinstance(output, dict) and 'location' in output:
                handle_known_output(output, output_name, output_name)
            elif isinstance(output, dict):
                prefix = '%s|__part__|' % output_name
                for record_key, record_value in output.items():
                    record_value_output_key = '%s%s' % (prefix, record_key)
                    handle_known_output(record_value, record_value_output_key, output_name)

            elif isinstance(output, list):
                elements = []
                for index, el in enumerate(output):
                    if isinstance(el, dict) and el['class'] == 'File':
                        output_path = _possible_uri_to_path(el['location'])
                        elements.append({'name': str(index), 'filename': output_path, 'cwl_filename': el['basename']})
                    else:
                        target_path = '%s____%s' % (output_name, str(index))
                        with open(target_path, 'w') as (f):
                            f.write(json.dumps(el))
                        elements.append({'name': str(index), 'filename': target_path, 'ext': 'expression.json'})

                provided_metadata[output_name] = {'elements': elements}
            else:
                target_path = job_proxy.output_path(output_name)
                with open(target_path, 'w') as (f):
                    f.write(json.dumps(output))
                provided_metadata[output_name] = {'ext': 'expression.json'}

        with open('galaxy.json', 'w') as (f):
            json.dump(provided_metadata, f)
        return


__all__ = ('handle_outputs', )