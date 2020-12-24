# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Abe/Dropbox/work/library/fabric_common/fabriccommon/project.py
# Compiled at: 2013-01-23 12:05:05
import os

class ProjectInfo(object):
    """
    Manages common paths locally and remotely.
    """

    def __init__(self, project_name, local_top, remote_top='/opt', remote_temp_top='/tmp'):
        """
        Remote paths will contain 'remote_top' and 'project_name' usually.
        Only temporary files will be exluded from this.
        Temporary files will be created under 'remote_temp_top' remotely.

        Local paths will contain 'local_top' only.
        """
        self.project_name = project_name
        self.local_top = local_top
        self.remote_top = remote_top
        self.remote_temp_top = remote_temp_top
        self.temp_directory = self.remote_temp_top
        self.__subprojects = []

    @property
    def subprojects(self):
        if not self.__subprojects:
            root = self.local_project_directory
            self.__subprojects = filter(lambda x: not x.startswith('.'), map(lambda dirpath: os.path.basename(dirpath), filter(os.path.isdir, map(lambda filename: os.path.join(root, filename), os.listdir(root)))))
        return self.__subprojects

    @property
    def local_thirdparty_directory(self):
        """
        Location of thirdparty modules locally.
        """
        return '%s/thirdparty' % self.local_top

    @property
    def local_project_directory(self):
        return '%s/projects' % self.local_top

    @property
    def project_directory(self):
        """
        Location of project directory remotely.
        """
        return '%s/projects/%s' % (self.remote_top, self.project_name)

    @property
    def virtual_environment_top(self):
        """
        Location of virtual environments remotely.
        """
        return '/opt/virtualenvs'

    @property
    def virtual_environment(self):
        """
        Location of virtual environment remotely.
        """
        return os.path.join(self.virtual_environment_top, self.project_name)

    @property
    def virtual_environment_source_command(self):
        """
        Virtual environment source command.
        """
        return 'export VIRTUAL_ENV_HOME=%(virtual_environment)s && source %(virtual_environment)s/.virtualenvrc' % {'virtual_environment': self.virtual_environment_top}

    @property
    def virtual_environment_command(self):
        """
        Virtual environment command.
        """
        return 'virtualenv %s' % self.project_name

    @property
    def workon_command(self):
        """
        Workon command.
        """
        return 'workon %s' % self.project_name

    def get_subproject_directory(self, subproject):
        """
        Location of subproject directory remotely.
        """
        return '%s/%s' % (self.project_directory, subproject)