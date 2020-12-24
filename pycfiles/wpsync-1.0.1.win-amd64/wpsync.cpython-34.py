# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\wpsync\wpsync.py
# Compiled at: 2015-06-04 16:16:34
# Size of source mod 2**32: 9574 bytes
import os, json, tempfile, subprocess, shutil, re

class Composer:

    def __init__(self):
        self.main = 'composer.json'
        self.lock = 'composer.lock'
        self.json = json.loads(open(self.main).read())
        self.folder = 'vendor'
        self._Composer__check_folder()

    def __check_folder(self):
        if 'config' in self.json:
            if 'vendor-dir' in self.json['config']:
                self.folder = self.json['config']['vendor-dir']
            self.folder = os.path.normpath(self.folder)

    def update(self):
        if os.path.isfile(self.lock):
            os.remove(self.lock)
        if os.path.isdir(self.folder):
            shutil.rmtree(self.folder)
        subprocess.call('composer install', shell=True)


class Bower:

    def __init__(self):
        self.main = 'bower.json'
        self.cnf = '.bowerrc'
        self.json = json.loads(open(self.main).read())
        self.folder = 'bower_components'
        self.config = ''
        self._Bower__check_folder()

    def __check_folder(self):
        if os.path.isfile(self.cnf):
            self.config = json.loads(open(self.cnf).read())
            if 'directory' in self.config:
                self.folder = self.config['directory']
            self.folder = os.path.normpath(self.folder)

    def update(self):
        if os.path.isdir(self.folder):
            shutil.rmtree(self.folder)
        subprocess.call('bower install', shell=True)


class Git:

    def __init__(self):
        self.commit = ''
        self.tag = ''

    def update(self):
        subprocess.call('git add -A', shell=True)
        if self.tag is not '':
            subprocess.call('git tag ' + self.tag, shell=True)
        if self.commit is '':
            print("You haven't mentioned the commit message.")
            exit(1)
        subprocess.call("git commit -m '" + self.commit + "'", shell=True)
        subprocess.call('git push', shell=True)
        subprocess.call('git push --tags', shell=True)


class Svn:

    def __init__(self):
        self.commit = ''
        self.tag = ''

    def update(self):
        if self.tag is not '':
            repo = os.getcwd()
            trunk = os.path.join(repo, 'trunk')
            tags = os.path.join(repo, 'tags')
            new_tag = os.path.join(tags, self.tag)
            shutil.copytree(trunk, new_tag)
        if self.commit is '':
            print("You haven't mentioned the commit message.")
            exit(1)
        subprocess.call('svn add * --force', shell=True)
        subprocess.call("svn commit -m '" + self.commit + "'", shell=True)


class Plugin:

    def __init__(self):
        self.plugin_file = 'plugin.php'
        self.plugin_file_content = ''
        self.readme_file = 'readme.txt'
        self.readme_file_content = ''
        self.old_version = []
        self.new_version = []
        self.the_version = ''
        self.index = 2
        self.version_control = 'git'
        self.wordpress_svn = ''
        self.ignore_files = []

    def update(self):
        self._Plugin__get_plugin_file_content()
        self._Plugin__get_readme_content()
        self._Plugin__get_current_version()
        self._Plugin__get_new_version()
        try:
            input('Confirm you want to update your plugin to v' + self.the_version)
        except SyntaxError:
            pass

        self._Plugin__change_version_files()
        self._Plugin__update_this_repo()
        self._Plugin__update_wordpress_repo()

    def __get_current_version(self):
        match = re.search('Version:[ \t]*[\\d+\\.]+\\d', self.plugin_file_content)
        if match is None:
            print("We can't understand the version of your plugin :(")
            exit(1)
        version = match.group(0)
        version = re.search('[\\d+\\.]+\\d', version).group(0)
        version = version.split('.')
        self.old_version = list(map(int, version))

    def __get_plugin_file_content(self):
        self.plugin_file_content = open(self.plugin_file, 'r').read()

    def __get_readme_content(self):
        self.readme_file_content = open(self.readme_file, 'r').read()

    def __get_new_version_helper(self):
        if self.new_version[self.index] + 1 > 9 and self.index != 0:
            self.new_version[self.index] = 0
            self.index -= 1
            self._Plugin__get_new_version_helper()
        else:
            self.new_version[self.index] += 1

    def __get_new_version(self):
        index_list = {'major': 0, 
         'minor': 1, 
         'build': 2, 
         'revision': 3}
        self.index = index_list[self.index]
        self.new_version = self.old_version
        self._Plugin__get_new_version_helper()
        self.new_version = list(map(str, self.new_version))
        self.the_version = '.'.join(self.new_version)

    def __change_version_files(self):
        plugin_search = 'Version:[ \t]*[\\d+\\.]+\\d'
        plugin_replace = 'Version: ' + self.the_version
        self.plugin_file_content = re.sub(plugin_search, plugin_replace, self.plugin_file_content)
        with open(self.plugin_file, 'w') as (fs):
            fs.write(self.plugin_file_content)
        readme_search = 'Stable tag:[ \t]*[\\d+\\.]+\\d'
        readme_replace = 'Stable tag: ' + self.the_version
        self.readme_file_content = re.sub(readme_search, readme_replace, self.readme_file_content)
        with open(self.readme_file, 'w') as (fs):
            fs.write(self.readme_file_content)

    def __update_this_repo(self):
        if self.version_control == 'svn':
            svn = Svn()
            svn.tag = 'v' + self.the_version
            svn.commit = 'v' + self.the_version
            svn.update()
            return
        git = Git()
        git.tag = 'v' + self.the_version
        git.commit = 'v' + self.the_version
        git.update()

    def __update_wordpress_repo(self):
        main_path = os.getcwd()
        temp_path = tempfile.mkdtemp()
        ignore_files = shutil.ignore_patterns(*self.ignore_files)
        os.chdir(temp_path)
        subprocess.call('svn checkout ' + self.wordpress_svn + ' .', shell=True)
        trunk = os.path.join(temp_path, 'trunk')
        temporary_content = os.path.join(temp_path, 'contents_temp')
        shutil.copytree(main_path, temporary_content, False, ignore_files)
        shutil.rmtree(trunk)
        shutil.move(temporary_content, trunk)
        svn = Svn()
        svn.commit = 'v' + self.the_version
        svn.tag = self.the_version
        svn.update()
        os.chdir(main_path)
        shutil.rmtree(temp_path, True)


def main():
    config_file = 'wpsync.json'
    if not os.path.isfile(config_file):
        print('There is no configuration file.')
        exit(1)
    config = json.loads(open(config_file).read())
    if 'plugin' not in config:
        print('You have problems in the configuration file.')
        exit(1)
    if 'wordpress-svn' not in config:
        print("You haven't defined the WordPress SVN link.")
        exit(1)
    if 'trunk' in config['wordpress-svn']:
        print('Please remove "trunk" from the SVN link.')
        exit(1)
    if os.path.isfile('composer.json'):
        composer = Composer()
        composer.update()
    if os.path.isfile('bower.json'):
        bower = Bower()
        bower.update()
    plugin = Plugin()
    plugin.plugin_file = config['plugin']['main'] if 'main' in config['plugin'] else 'plugin.php'
    plugin.index = config['increase'] if 'increase' in config else 'build'
    if os.path.isdir('.svn'):
        plugin.version_control = 'svn'
    plugin.wordpress_svn = config['wordpress-svn']
    if 'ignore' in config:
        plugin.ignore_files = config['ignore']
    plugin.update()
    try:
        input('Press any key to continue...')
    except SyntaxError:
        pass