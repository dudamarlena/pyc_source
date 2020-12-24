# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mack/mack.py
# Compiled at: 2017-08-19 20:39:16
from argparse import ArgumentParser
from time import sleep
import os

def build_structure(structure):
    for key, value in structure.items():
        os.mkdir(key)
        print ('\x1b[1;37m[OK]\x1b[0m Created directory {0} ').format(key)
        sleep(0.3)
        if type(value) == dict:
            os.chdir(key)
            build_structure(value)
            os.chdir('..')


abspath = os.path.abspath(os.path.dirname(__file__))

class Initialize(object):

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.target = os.path.join(self.directory, self.name)
        self.local_path = os.path.join(abspath, 'project')

    def create_dir(self):
        if os.path.exists(self.target):
            print '[ERROR] Project already exists in directory!'
            exit(1)
        os.mkdir(self.target)
        os.chdir(self.target)
        return 0

    def make_app(self, dirs, dir_map, env):
        os.system('git init >> /dev/null')
        with open('.gitignore', 'wa') as (g):
            g.write('*.pyc\nvenv\n*.db')
        g.close()
        os.system(("touch README.md && echo '# {0}' >> README.md").format(self.name))
        print '\n\x1b[1;37m[OK]\x1b[0mInitialized Git repo!\n'
        build_structure(dirs)
        dir_map = dict(dir_map)
        for a in dir_map:
            os.system(('cp {0}/{1} {2}/{3}').format(self.local_path, a, self.target, dir_map[a]))
            print ('\x1b[1;37m[OK]\x1b[0m Created file {0}').format(dir_map[a])
            sleep(0.3)

        if env is None:
            os.system('virtualenv venv')
        else:
            os.system('virtualenv {0}')
        print '\n\x1b[1;37m[OK]\x1b[0mInitialized virtualenv!\n'
        sleep(0.3)
        return


structure = {'static': {'css': None, 'js': None, 'img': None}, 'templates': {'layouts': None}}
local_map = [
 ('Procfile', 'Procfile'),
 ('requirements.txt', 'requirements.txt'),
 ('app.py', 'app.py'),
 ('templates/404.html', 'templates/404.html'),
 ('templates/index.html', 'templates/index.html'),
 ('templates/layout.html', 'templates/layouts/layout.html'),
 ('static/style.css', 'static/css/style.css')]
directory = os.getcwd()

def main():
    parser = ArgumentParser(description='Generate incredibly lightweight Flask projects')
    parser.add_argument('name', type=str, help='Name of project')
    parser.add_argument('-s, --sandbox', dest='sandbox', type=str, help='Name of virtualenv sandbox environment')
    args = parser.parse_args()
    name = args.name
    env = args.sandbox
    a = Initialize(name, directory)
    a.create_dir()
    a.make_app(structure, local_map, env)


if __name__ == '__main__':
    main()