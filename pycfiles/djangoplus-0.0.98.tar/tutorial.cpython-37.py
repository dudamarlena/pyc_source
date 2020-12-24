# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/opt/.virtualenvs/djangoplus/lib/python3.7/site-packages/djangoplus/docs/tutorial.py
# Compiled at: 2018-09-06 07:24:41
# Size of source mod 2**32: 3182 bytes
import os
from djangoplus.tools.http import HttpServer
from djangoplus.tools.terminal import Terminal
from djangoplus.tools.subtitle import Subtitle
from djangoplus.tools.browser import Browser
from djangoplus.tools.video import VideoRecorder
VIRTUALENV_PATH = '/var/opt/.virtualenvs/djangoplus'
VIRTUALENV_ACTIVATION_PATH = '{}/bin/activate'.format(VIRTUALENV_PATH)
PYTHON_PATH = '{}/bin/python'.format(VIRTUALENV_PATH)

class Tutorial(object):

    def __init__(self, project_path, devmode=False):
        self.project_path = project_path
        self.project_name = self.project_path.split(os.sep)[(-1)]
        self.base_dir = '/tmp/{}'.format(self.project_name)
        self.devmode = devmode
        self.subtitle = Subtitle()
        self.recorder = VideoRecorder()
        self.terminal = Terminal(python=PYTHON_PATH)
        self.server = HttpServer((self.base_dir), devmode, python=PYTHON_PATH)
        self.browser = Browser('http://localhost:8000', verbose=False, slowly=True, maximize=True)
        self.browser.get('https://www.google.com.br/')

    def start(self, create_project=True):
        try:
            self.terminal.hide()
            if create_project:
                self.delete_project()
                self.create_project()
            self.server.start()
            self.start_tutorial()
        finally:
            self.recorder.stop()
            self.server.stop()
            self.terminal.show()
            self.browser.close(5)

    def create_project(self):
        if self.devmode:
            os.system('clear')
        os.environ['DJANGO_SETTINGS_MODULE'] = '{}.settings'.format(self.project_name)
        command = 'source {} && cd /tmp && startproject {}'.format(VIRTUALENV_ACTIVATION_PATH, self.project_name)
        self.terminal.execute(command)

    def delete_project(self):
        os.system('rm -r {}'.format(self.base_dir))

    def start_tutorial(self):
        pass


class DevTutorial(Tutorial):

    def __init__(self, project_path):
        super(DevTutorial, self).__init__(project_path, devmode=True)

    def restart_server(self, sync=False):
        self.server.stop()
        if sync:
            self.terminal.execute('python manage.py sync', base_dir=(self.base_dir))
        self.server.start()

    def edit_models(self, step, file_name='models.py'):
        input_file_path = '{}/{}/{}'.format(self.project_path, self.project_name, file_name)
        output_file_path = '{}/{}/{}'.format(self.base_dir, self.project_name, file_name)
        print('Reading file {}'.format(input_file_path))
        input_file = open(input_file_path, 'r')
        file_content = input_file.read()
        input_file.close()
        print('Writing file {}'.format(output_file_path))
        output_file = open(output_file_path, 'w')
        output_file.write(file_content)
        output_file.close()
        self.restart_server(True)

    def edit_templates(self, step, file_name):
        pass

    def edit_formatters(self, file_name='formatters.py'):
        pass


class UserTutorial(Tutorial):

    def __init__(self, project_path):
        super(UserTutorial, self).__init__(project_path, devmode=False)