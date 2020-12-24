# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/utils/create_file_list.py
# Compiled at: 2012-09-24 08:16:34
"""
The backup script for the system.

It accepts a ``project`` name and an ``output_path`` which is the output of 
the filtered files.

The system creates filter rules to be used with ``rsync`` command and then calls
the ``rsync`` command on the server.

Because the pipeline ends at a Nuke file, all the source files which needs to
be backed up are listed in this nuke (*.nk) file. So the script searches for the
latest versions of nuke files, and if a ``-nv n`` parameters is also passed, 
then the last ``n`` versions will be investigated for source files.

Script will search for, Read, ReadGeo, ReadGeo2, Write, WriteGeo nodes and will
use the path value listed in the ``file`` attribute of those nodes.

If the file path is relative and a project_dir is present in the nuke file 
than the path will be converted to an absolute path.

:arg --project, -p: The name of the project. It should match the exact project 
  name otherwise it will raise a ValueError.

:arg --extra_filter_rules, -ef: a file which is holding extra filter rules 
  Can be skipped.

:arg --number_of_versions, -nv: the number of versions to be used in backup 
  process. Default value is 1.

:arg --output, -o: the output of the backed up files.

Examples::
  
  backup -p ProjectName -o /mnt/M/JOBs_Backup
  # creates a backup_filter file in the path that the script is executed
  
  # No output will raise RuntimeError:
  backup -p ProjectName
  # raises RuntimeError
"""
import glob, os, re

class BackUp(object):
    """Holds information about the backup process.
    
    :param project: The name of the project to be backed up or the
      :class:`~oyProjectManager.models.project.Project` instance showing the 
      project to be backed up. None or empty string will raise TypeError and
      ValueError respectively. If given as string a new
      :class:`~oyProjectManager.models.project.Project` instance will be
      created and hold in the
      :attr:`~oyProjectManager.utils.backup.BackUp.project` attribute.
    
    :param extra_filter_rules: A path of a text file which holds the extra 
      filter rules. Can be skipped.
    
    :param number_of_versions: The number of latest Nuke script version to be
      searched for inputs. Setting the number_of_versions to a negative value
      will result all the versions of the Nuke files to be used. Default value
      is 1.
    
    :param output: The output of the backed up files. If skipped a ValueError
      will be raised
    """

    def __init__(self, project_name=None, output=None, number_of_versions=None, extra_filter_rules=None):
        self.projects_path = os.path.expanduser('~/M/JOBs')
        self._project_name = self._validate_project(project_name)
        self._extra_filter_rules = self._validate_extra_filter_rules(extra_filter_rules)
        self._output = self._validate_output(output)
        self._number_of_versions = self._validate_number_of_versions(number_of_versions)

    def doBackup(self):
        """Does the backup process.
        
        Calls ``rsync`` with the appropriate filters. Creates the output path
        if it doesn't exists.
        """
        project_full_path = os.path.join(self.projects_path, self._project_name)
        seqs_folders = glob.glob(project_full_path + '/*')
        files_to_backup = []
        for seq_folder in seqs_folders:
            if not os.path.isdir(seq_folder):
                continue
            comp_files = []
            comp_folders = glob.glob(seq_folder + '/*COMP*')
            for comp_folder in comp_folders:
                if not os.path.isdir(comp_folder):
                    continue
                for current_dir, dirs, files in os.walk(comp_folder):
                    for file in files:
                        if file.endswith('.nk'):
                            comp_files.append(current_dir + '/' + file)

            shot_containers = []
            for comp_file in comp_files:
                match_obj = re.match('(.*?[0-9]+)_([a-zA-Z0-9]+).*v([0-9]+)', comp_file)
                if match_obj:
                    name = match_obj.groups()[0]
                    sub_name = match_obj.groups()[1]
                    version_number = match_obj.groups()[2]
                    appended = False
                    if len(shot_containers) > 0:
                        for shot_container in shot_containers:
                            if shot_container.name == name and shot_container.sub_name == sub_name:
                                shot_container.versions.append(comp_file)
                                appended = True
                                break

                    if not appended:
                        new_shot_container = ShotContainer()
                        new_shot_container.name = name
                        new_shot_container.sub_name = sub_name
                        new_shot_container.versions.append(comp_file)
                        shot_containers.append(new_shot_container)

            for shot_container in shot_containers:
                for version in shot_container.versions[-1:]:
                    last_version_file_path = version
                    content = open(last_version_file_path).read()
                    temp_data = re.findall('project_directory (.*?[\\w%#./:]*)', content)
                    project_directory = temp_data[0] if len(temp_data) > 0 else ''
                    for file_path in re.findall('file (.*?[\\w%#./:]*)', content):
                        if not os.path.isabs(file_path):
                            file_path = project_directory + '/' + file_path
                        file_path = os.path.normpath(file_path)
                        file_path = file_path.replace('\\', '/')
                        file_path = file_path.replace('M:/', '/home/Administrator/M/')
                        file_path = file_path.replace('/mnt/M/', '/home/Administrator/M/')
                        file_path = file_path.replace('//', '/')
                        file_path = os.path.expanduser(file_path)
                        file_path = os.path.normpath(file_path)
                        if seq_folder in file_path:
                            files_to_backup.append(file_path)

        new_file_list = []
        new_file_list.append('#!/bin/sh\n')
        for i, file_ in enumerate(files_to_backup):
            file_ = re.sub('[#]+', '*', file_)
            file_ = re.sub('%0[0-9]+d', '*', file_)
            new_file_list.append('echo ' + str(i + 1) + '/' + str(len(files_to_backup)) + ' copying ' + file_.replace('*', '\\*') + '\n')
            new_file_list.append('mkdir -p ' + os.path.dirname(file_.replace(project_full_path + '/', os.path.join(self.output, self.project + '/'))) + '/\n')
            new_file_list.append('cp ' + file_ + ' ' + os.path.dirname(file_.replace(project_full_path + '/', os.path.join(self.output, self.project + '/'))) + '/\n')

        rule_file = open('python_file_list', 'w')
        rule_file.writelines(new_file_list)
        rule_file.close()
        os.chmod('python_file_list', 511)

    def __repr__(self):
        return super(BackUp, self).__repr__()

    def _validate_project(self, project):
        """validates the given project value
        """
        if not isinstance(project, str):
            raise TypeError('BackUp.project should be an instance ofstring instance')
        if project == '':
            raise ValueError
        return project

    def _validate_extra_filter_rules(self, extra_filter_rules):
        """validates the given extra_filter_rules
        """
        if extra_filter_rules is None:
            extra_filter_rules = ''
        if not isinstance(extra_filter_rules, (str, unicode)):
            raise TypeError('extra_filter_rules should be a string showing the path of the extra filter rules')
        return extra_filter_rules

    def _validate_output(self, output):
        """validates the given output value
        """
        if output is None:
            raise TypeError('output argument can not be None')
        if output == '':
            raise ValueError('output argument can not be empty string')
        if not isinstance(output, (str, unicode)):
            raise TypeError('output argument should be a string')
        return output

    def _validate_number_of_versions(self, number_of_versions):
        """validates the given number_of_versions value
        """
        if number_of_versions is None:
            number_of_versions = 1
        if not isinstance(number_of_versions, int):
            raise TypeError('number_of_versions should be an integer')
        return number_of_versions

    @property
    def project(self):
        """The project to be backed up.
        
        It is an instance of :class:`~oyProjectManager.models.project.Project`.
        """
        return self._project_name

    @project.setter
    def project(self, project):
        """setter of the project attribute
        """
        self._project_name = self._validate_project(project)

    @property
    def extra_filter_rules(self):
        """a string showing the file path of the extra filter rules which is
        going to be used with the rsync
        """
        return self._extra_filter_rules

    @extra_filter_rules.setter
    def extra_filter_rules(self, extra_filter_rules):
        """setter for the extra_filter_rules
        """
        self._extra_filter_rules = self._validate_extra_filter_rules(extra_filter_rules)

    @property
    def num_of_versions(self):
        """the number of versions of latest Nuke files.
        
        It is an integer.
        """
        return self._number_of_versions

    @num_of_versions.setter
    def num_of_versions(self, num_of_versions):
        """the setter for the number of versions attribute
        """
        self._number_of_versions = self._validate_number_of_versions(num_of_versions)

    @property
    def output(self):
        """A string showing the output of the backed up files.
        
        If it is set to None a TypeError will be raised and if it is set to 
        an empty string a ValueError will be raised.
        """
        return self._output

    @output.setter
    def output(self, output):
        """the output setter
        """
        self._output = self._validate_output(output)


class ShotContainer(object):

    def __init__(self):
        self.name = None
        self.sub_name = None
        self.versions = []
        return


import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=str)
    parser.add_argument('--output', type=str, default='~/M/JOBs_BACKUP')
    args = parser.parse_args()
    backup_obj = BackUp(project_name=args.project, output=args.output)
    backup_obj.doBackup()