# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PackageMaster\PackageMaster.py
# Compiled at: 2020-03-30 12:36:52
# Size of source mod 2**32: 19551 bytes
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, NoSuchElementException, WebDriverException, ElementNotVisibleException
from tkinter import ttk, Tk, Label, Entry
import tkinter as tk, os, time, shutil, platform, subprocess, shaonutil, pipreqs
package_name = ''

def make_package_config():
    package_name = ''
    version = ''
    author_name = ''
    keywords = ''
    console_decision = ''
    github_user = ''
    github_pass = ''
    github_project_url = ''
    pypi_user = ''
    pypi_pass = ''
    window = Tk()
    window.title('Welcome to Package Config')
    window.geometry('400x400')
    window.configure(background='grey')
    package_name_ = tk.StringVar(window)
    version_ = tk.StringVar(window)
    author_name_ = tk.StringVar(window)
    keywords_ = tk.StringVar(window)
    console_decision_ = tk.StringVar(window)
    github_user_ = tk.StringVar(window)
    github_pass_ = tk.StringVar(window)
    github_project_url_ = tk.StringVar(window)
    pypi_user_ = tk.StringVar(window)
    pypi_pass_ = tk.StringVar(window)
    Label(window, text='Package Config').grid(row=0, column=0, columnspan=2)
    Label(window, text='Package Name').grid(row=1, column=0)
    Label(window, text='Version').grid(row=2, column=0)
    Label(window, text='Author Name').grid(row=3, column=0)
    Label(window, text='Keywords').grid(row=4, column=0)
    Label(window, text='Console Decision').grid(row=5, column=0)
    Label(window, text='Github User').grid(row=6, column=0)
    Label(window, text='Github Password').grid(row=7, column=0)
    Label(window, text='Github Project Url').grid(row=8, column=0)
    Label(window, text='PyPi User').grid(row=9, column=0)
    Label(window, text='PyPi Password').grid(row=10, column=0)
    Entry(window, textvariable=package_name_).grid(row=1, column=1)
    Entry(window, textvariable=version_).grid(row=2, column=1)
    Entry(window, textvariable=author_name_).grid(row=3, column=1)
    Entry(window, textvariable=keywords_).grid(row=4, column=1)
    Entry(window, textvariable=console_decision_).grid(row=5, column=1)
    Entry(window, textvariable=github_user_).grid(row=6, column=1)
    Entry(window, show='*', textvariable=github_pass_).grid(row=7, column=1)
    Entry(window, textvariable=github_project_url_).grid(row=8, column=1)
    Entry(window, textvariable=pypi_user_).grid(row=9, column=1)
    Entry(window, textvariable=pypi_pass_).grid(row=10, column=1)

    def clicked():
        package_nameT = package_name_.get()
        version = version_.get()
        author_name = author_name_.get()
        keywords = keywords_.get()
        console_decision = console_decision_.get()
        github_user = github_user_.get()
        github_pass = github_pass_.get()
        github_project_url = github_project_url_.get()
        pypi_user = pypi_user_.get()
        pypi_pass = pypi_pass_.get()
        strs = f"; github config\n[PACKAGE]\npackage_name = {package_nameT}\nversion = {version}\nauthor_name = {author_name}\nkeywords = {keywords}\nconsole_decision = {console_decision}\ngithub_project_url = {github_project_url}\ngithub_user = {github_user}\ngithub_pass = {github_pass}\npypi_user = {pypi_user}\npypi_pass = {pypi_pass}"
        shaonutil.file.write_file('private/package.config', strs)
        window.destroy()

    btn = ttk.Button(window, text='Submit', command=clicked).grid(row=11, column=0)
    window.mainloop()
    config = shaonutil.file.read_configuration_ini('private/package.config')
    package_name = config['PACKAGE']['package_name']


def get_package_name--- This code section failed: ---

 L. 110         0  LOAD_STR                 ''
                2  STORE_FAST               'vname'

 L. 111         4  LOAD_GLOBAL              shaonutil
                6  LOAD_ATTR                file
                8  LOAD_METHOD              read_file
               10  LOAD_STR                 'setup.py'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'lines'

 L. 112        16  LOAD_FAST                'lines'
               18  POP_JUMP_IF_FALSE   112  'to 112'

 L. 113        20  LOAD_CONST               0
               22  STORE_FAST               'i'

 L. 114        24  LOAD_FAST                'lines'
               26  GET_ITER         
               28  FOR_ITER            112  'to 112'
               30  STORE_FAST               'line'

 L. 115        32  LOAD_STR                 'name='
               34  LOAD_FAST                'line'
               36  LOAD_METHOD              replace
               38  LOAD_STR                 ' '
               40  LOAD_STR                 ''
               42  CALL_METHOD_2         2  ''
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE   102  'to 102'

 L. 116        48  LOAD_STR                 "'"
               50  STORE_FAST               'marker'

 L. 117        52  LOAD_FAST                'line'
               54  STORE_FAST               's'

 L. 118        56  LOAD_FAST                's'
               58  LOAD_METHOD              find
               60  LOAD_FAST                'marker'
               62  CALL_METHOD_1         1  ''
               64  LOAD_GLOBAL              len
               66  LOAD_FAST                'marker'
               68  CALL_FUNCTION_1       1  ''
               70  BINARY_ADD       
               72  STORE_FAST               'start'

 L. 119        74  LOAD_FAST                's'
               76  LOAD_METHOD              find
               78  LOAD_FAST                'marker'
               80  LOAD_FAST                'start'
               82  CALL_METHOD_2         2  ''
               84  STORE_FAST               'end'

 L. 120        86  LOAD_FAST                's'
               88  LOAD_FAST                'start'
               90  LOAD_FAST                'end'
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  STORE_FAST               'vname'

 L. 121        98  POP_TOP          
              100  JUMP_ABSOLUTE       112  'to 112'
            102_0  COME_FROM            46  '46'

 L. 122       102  LOAD_FAST                'i'
              104  LOAD_CONST               1
              106  INPLACE_ADD      
              108  STORE_FAST               'i'
              110  JUMP_BACK            28  'to 28'
            112_0  COME_FROM            18  '18'

 L. 123       112  LOAD_FAST                'vname'
              114  LOAD_STR                 ''
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 124       120  LOAD_GLOBAL              input
              122  LOAD_STR                 'Enter Package Name : '
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'vname'
            128_0  COME_FROM           118  '118'

 L. 126       128  LOAD_FAST                'vname'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 100


def initialize_git(project_github_url=''):
    if project_github_url == '':
        project_github_url = input('Give Project Github Url : ')
    commit_message = input('Give Commit Message : ')
    commands = f'git init\ngit remote add origin {project_github_url}.git\ngit add .\ngit commit -m "{commit_message}\ngit push -u origin master'
    commands = commands.split('\n')
    for command in commands:
        for path in execute_shell(command):
            print(path, end='')


def create_setup_py():
    config = shaonutil.file.read_configuration_ini('private/package.config')
    package_name = config['PACKAGE']['package_name']
    version = config['PACKAGE']['version']
    author_name = config['PACKAGE']['author_name']
    author_email = config['PACKAGE']['github_user']
    project_url = config['PACKAGE']['github_project_url']
    project_github_url = config['PACKAGE']['github_project_url']
    keywords = config['PACKAGE']['keywords']
    console_decision = config['PACKAGE']['console_decision']
    classifiers = []
    download_url = project_github_url + '/archive/' + version + '.tar.gz'
    keywords = keywords.split(',')
    dirs = [dir_ + '/*' for dir_ in shaonutil.file.get_all_dirs() if dir_ != 'private']
    dirs.append('*')
    if console_decision == 'y':
        StR = f"#from distutils.core import setup\nfrom setuptools import setup\nfrom os import path\n\n# read the contents of your README file\nthis_directory = path.abspath(path.dirname(__file__))\nwith open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:\n    long_description = f.read()\n\n\nsetup(\n    name = '{package_name}',\n    packages = ['{package_name}'],\n    version = '{version}',\n    long_description=long_description,\n    long_description_content_type='text/markdown',\n    author = '{author_name}',\n    author_email = '{author_email}',\n    url = '{project_url}',\n    download_url = '{download_url}',\n    keywords = {keywords},\n    classifiers = {classifiers},\n    setup_requires=['wheel'],\n    entry_points={{\n        'console_scripts': [\n            '{package_name}={package_name}.{package_name}:main',\n        ],\n    }},\n    package_data= {{'': {dirs}}}\n)"
    else:
        StR = f"#from distutils.core import setup\nfrom setuptools import setup\nfrom os import path\n\n# read the contents of your README file\nthis_directory = path.abspath(path.dirname(__file__))\nwith open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:\n    long_description = f.read()\n\n\nsetup(\n    name = '{package_name}',\n    packages = ['{package_name}'],\n    version = '{version}',\n    long_description=long_description,\n    long_description_content_type='text/markdown',\n    author = '{author_name}',\n    author_email = '{author_email}',\n    url = '{project_url}',\n    download_url = '{download_url}',\n    keywords = {keywords},\n    classifiers = {classifiers},\n    setup_requires=['wheel']\n)"
    shaonutil.file.write_file('setup.py', StR)


def execute_shell(cmd):
    popen = subprocess.Popen(cmd, stdout=(subprocess.PIPE), universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ''):
        yield stdout_line
    else:
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


def cleaning_before_commit(package_name):
    files = package_name + '.egg-info\nbuild\ndist\n.eggs\ngeckodriver.log\n'
    print('Cleaning files -', files)
    files = files.split('\n')
    for file in files:
        if os.path.exists(file):
            try:
                shutil.rmtree(file)
            except:
                os.remove(file)


def get_version_name--- This code section failed: ---

 L. 253         0  LOAD_STR                 ''
                2  STORE_FAST               'vname'

 L. 254         4  LOAD_GLOBAL              shaonutil
                6  LOAD_ATTR                file
                8  LOAD_METHOD              read_file
               10  LOAD_STR                 'setup.py'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'lines'

 L. 255        16  LOAD_FAST                'lines'
               18  POP_JUMP_IF_FALSE   114  'to 114'

 L. 256        20  LOAD_CONST               0
               22  STORE_FAST               'i'

 L. 257        24  LOAD_FAST                'lines'
               26  GET_ITER         
               28  FOR_ITER            112  'to 112'
               30  STORE_FAST               'line'

 L. 258        32  LOAD_STR                 'version='
               34  LOAD_FAST                'line'
               36  LOAD_METHOD              replace
               38  LOAD_STR                 ' '
               40  LOAD_STR                 ''
               42  CALL_METHOD_2         2  ''
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE   102  'to 102'

 L. 259        48  LOAD_STR                 "'"
               50  STORE_FAST               'marker'

 L. 260        52  LOAD_FAST                'line'
               54  STORE_FAST               's'

 L. 261        56  LOAD_FAST                's'
               58  LOAD_METHOD              find
               60  LOAD_FAST                'marker'
               62  CALL_METHOD_1         1  ''
               64  LOAD_GLOBAL              len
               66  LOAD_FAST                'marker'
               68  CALL_FUNCTION_1       1  ''
               70  BINARY_ADD       
               72  STORE_FAST               'start'

 L. 262        74  LOAD_FAST                's'
               76  LOAD_METHOD              find
               78  LOAD_FAST                'marker'
               80  LOAD_FAST                'start'
               82  CALL_METHOD_2         2  ''
               84  STORE_FAST               'end'

 L. 263        86  LOAD_FAST                's'
               88  LOAD_FAST                'start'
               90  LOAD_FAST                'end'
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  STORE_FAST               'vname'

 L. 264        98  POP_TOP          
              100  JUMP_ABSOLUTE       122  'to 122'
            102_0  COME_FROM            46  '46'

 L. 265       102  LOAD_FAST                'i'
              104  LOAD_CONST               1
              106  INPLACE_ADD      
              108  STORE_FAST               'i'
              110  JUMP_BACK            28  'to 28'
              112  JUMP_FORWARD        122  'to 122'
            114_0  COME_FROM            18  '18'

 L. 267       114  LOAD_GLOBAL              input
              116  LOAD_STR                 'Give Version Name : '
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'vname'
            122_0  COME_FROM           112  '112'

 L. 268       122  LOAD_FAST                'vname'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 100


def changing_version_name(prev_vname, new_vname):
    lines = shaonutil.file.read_file('setup.py')
    strs = '\n'.join(lines)
    strs = strs.replace(prev_vname, new_vname)
    shaonutil.file.write_file('setup.py', strs)


def changing_version_name_prev(new_vname):
    lines = shaonutil.file.read_file('setup.py')
    i = 0
    for line in lines:
        if '__version__' in line:
            marker = "'"
            s = line
            start = s.find(marker) + len(marker)
            end = s.find(marker, start)
            vname = s[start:end]
            s = s.replace(vname, new_vname)
            break
        i += 1
    else:
        lines[i] = s
        strs = '\n'.join(lines)
        shaonutil.file.write_file('setup.py', strs)


def check_necessary_resources(package_name_=''):
    if package_name_ == '':
        package_name = get_package_name()
    else:
        package_name = package_name_
    dirs = shaonutil.file.get_all_dirs()
    print('Checking the required files/folders ...')
    folders = f"private/\nprivate/package.config\nsetup.py\n{package_name}/\nREADME.md\nrequirements.txt\nLICENSE\n.gitignore\n.git"
    folders = folders.split('\n')
    for folder in folders:
        os.path.exists(folder) or print('Warning :', folder, 'does not exist.')
        if '.gitignore' in folder:
            input_ = input('Do u want to create ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                shaonutil.file.write_file('.gitignore', 'private/')
        elif 'private/package.config' in folder:
            input_ = input('Do u want to create package.config ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                make_package_config()
        elif 'private/' in folder:
            input_ = input('Do u want to create directory ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                os.mkdir('private')
        elif 'setup.py' in folder:
            input_ = input('Do u want to create ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                create_setup_py()
        elif '.git' in folder:
            input_ = input('Do u want to create ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                config = shaonutil.file.read_configuration_ini('private/package.config')
                initialize_git(config['PACKAGE']['github_project_url'])
        elif 'requirements.txt' in folder:
            input_ = input('Do u want to create ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                commands = 'pipreqs .'
                commands = commands.split('\n')
                for command in commands:
                    for path in execute_shell(command):
                        print(path, end='')

        elif 'README.md' in folder:
            input_ = input('Do u want to create ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                shaonutil.file.write_file('README.md', '')
        elif package_name in folder:
            input_ = input('Do u want to create ' + folder + ' (y/n) : ')
            if input_ == 'y' or input_ == 'Y':
                os.mkdir(package_name)
                folders[3] = package_name + '/'
                print(folders)

    for dir_ in shaonutil.file.get_all_files_dirs():
        print(dir_)
        if os.path.isdir(dir_):
            dir_ = dir_ + '/'
        if dir_ not in folders:
            dir_ = dir_.replace('/', '')
            print(dir_)
            shutil.move(dir_, os.path.join(package_name, dir_))


def check_necessary_packages():
    print('Checking the required modules ...')
    modules = 'setuptools\nwheel\ntwine\npipreqs'
    modules = modules.split('\n')
    for module in modules:
        found = shaonutil.file.package_exists(module)
        if not found:
            print(module, ' package is not installed.')
            print(module, ' package is installing.')
            if platform.system() == 'Linux':
                command = 'pip3 install ' + module
            else:
                if platform.system() == 'Windows':
                    command = 'pip3 install ' + module
        for path in execute_shell(command):
            print(path, end='')


def commit_push():
    commit_msg = input('Give Commit Message : ')
    if platform.system() == 'Linux':
        commands = 'git add .\ngit commit -m "' + commit_msg + '";\ngit push -u origin master'
    else:
        if platform.system() == 'Windows':
            commands = 'git add .\ngit commit -m "' + commit_msg + '";\ngit push -u origin master'
    commands = commands.split('\n')
    for command in commands:
        for path in execute_shell(command):
            print(path, end='')


def make_release--- This code section failed: ---

 L. 418         0  LOAD_FAST                'git_url'
                2  LOAD_STR                 '/releases/new'
                4  BINARY_ADD       
                6  STORE_FAST               'git_url'

 L. 419         8  LOAD_GLOBAL              print
               10  LOAD_STR                 'Making release ...'
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 422        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              dirname
               22  LOAD_GLOBAL              os
               24  LOAD_ATTR                path
               26  LOAD_METHOD              realpath
               28  LOAD_GLOBAL              __file__
               30  CALL_METHOD_1         1  ''
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'script_dir'

 L. 424        36  LOAD_GLOBAL              platform
               38  LOAD_METHOD              system
               40  CALL_METHOD_0         0  ''
               42  LOAD_STR                 'Linux'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    64  'to 64'

 L. 425        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              join
               54  LOAD_FAST                'script_dir'
               56  LOAD_STR                 'resources/geckodriver'
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'driver_path_firefox'
               62  JUMP_FORWARD         90  'to 90'
             64_0  COME_FROM            46  '46'

 L. 426        64  LOAD_GLOBAL              platform
               66  LOAD_METHOD              system
               68  CALL_METHOD_0         0  ''
               70  LOAD_STR                 'Windows'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L. 427        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'script_dir'
               84  LOAD_STR                 'resources/geckodriver.exe'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'driver_path_firefox'
             90_0  COME_FROM            74  '74'
             90_1  COME_FROM            62  '62'

 L. 430        90  LOAD_GLOBAL              Options
               92  CALL_FUNCTION_0       0  ''
               94  STORE_FAST               'options'

 L. 432        96  SETUP_FINALLY       116  'to 116'

 L. 433        98  LOAD_GLOBAL              webdriver
              100  LOAD_ATTR                Firefox
              102  LOAD_FAST                'driver_path_firefox'
              104  LOAD_FAST                'options'
              106  LOAD_CONST               ('executable_path', 'options')
              108  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              110  STORE_FAST               'driver'
              112  POP_BLOCK        
              114  JUMP_FORWARD        144  'to 144'
            116_0  COME_FROM_FINALLY    96  '96'

 L. 434       116  DUP_TOP          
              118  LOAD_GLOBAL              WebDriverException
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   142  'to 142'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 435       130  LOAD_GLOBAL              WebDriverException
              132  LOAD_STR                 "invalid argument: can't kill an exited process\n Check if Firefox version and geckodriver in resources folder is not matched"
              134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM           122  '122'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           114  '114'

 L. 437       144  LOAD_FAST                'driver'
              146  LOAD_METHOD              get
              148  LOAD_STR                 'https://github.com'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          

 L. 438       154  LOAD_FAST                'driver'
              156  LOAD_METHOD              find_element_by_xpath
              158  LOAD_STR                 '//a[@href="/login" and contains(@data-ga-click,"text:sign-in")]'
              160  CALL_METHOD_1         1  ''
              162  LOAD_METHOD              click
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          

 L. 439       168  LOAD_FAST                'driver'
              170  LOAD_METHOD              find_element_by_xpath
              172  LOAD_STR                 '//input[@type="text" and @name="login" and @id="login_field" and @autocomplete="username"]'
              174  CALL_METHOD_1         1  ''
              176  LOAD_METHOD              click
              178  CALL_METHOD_0         0  ''
              180  POP_TOP          

 L. 440       182  LOAD_FAST                'driver'
              184  LOAD_METHOD              find_element_by_xpath
              186  LOAD_STR                 '//input[@type="text" and @name="login" and @id="login_field" and @autocomplete="username"]'
              188  CALL_METHOD_1         1  ''
              190  LOAD_METHOD              send_keys
              192  LOAD_FAST                'github_user'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L. 441       198  LOAD_FAST                'driver'
              200  LOAD_METHOD              find_element_by_xpath
              202  LOAD_STR                 '//input[@type="password" and @name="password" and @id="password" and @autocomplete="current-password"]'
              204  CALL_METHOD_1         1  ''
              206  LOAD_METHOD              click
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          

 L. 442       212  LOAD_FAST                'driver'
              214  LOAD_METHOD              find_element_by_xpath
              216  LOAD_STR                 '//input[@type="password" and @name="password" and @id="password" and @autocomplete="current-password"]'
              218  CALL_METHOD_1         1  ''
              220  LOAD_METHOD              send_keys
              222  LOAD_FAST                'github_pass'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          

 L. 443       228  LOAD_FAST                'driver'
              230  LOAD_METHOD              find_element_by_xpath
              232  LOAD_STR                 '//input[@type="submit" and @name="commit" and @value="Sign in"]'
              234  CALL_METHOD_1         1  ''
              236  LOAD_METHOD              click
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          

 L. 444       242  LOAD_FAST                'driver'
              244  LOAD_METHOD              get
              246  LOAD_FAST                'git_url'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          

 L. 445       252  LOAD_FAST                'driver'
              254  LOAD_METHOD              find_element_by_xpath
              256  LOAD_STR                 '//input[@placeholder="Tag version" and @list="git-tags" and contains(@class,"release-tag-field") and contains(@class,"js-release-tag-field") and @aria-label="Enter tag name or version number" and @data-existing-id="none" and @type="text" and @name="release[tag_name]" and @id="release_tag_name"]'
              258  CALL_METHOD_1         1  ''
              260  LOAD_METHOD              click
              262  CALL_METHOD_0         0  ''
              264  POP_TOP          

 L. 446       266  LOAD_FAST                'driver'
              268  LOAD_METHOD              find_element_by_xpath
              270  LOAD_STR                 '//input[@placeholder="Tag version" and @list="git-tags" and contains(@class,"release-tag-field") and contains(@class,"js-release-tag-field") and @aria-label="Enter tag name or version number" and @data-existing-id="none" and @type="text" and @name="release[tag_name]" and @id="release_tag_name"]'
              272  CALL_METHOD_1         1  ''
              274  LOAD_METHOD              send_keys
              276  LOAD_FAST                'release_tag'
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          

 L. 447       282  LOAD_FAST                'driver'
              284  LOAD_METHOD              find_element_by_xpath
              286  LOAD_STR                 '//button[contains(@class,"js-publish-release") and @type="submit" and text()="Publish release"]'
              288  CALL_METHOD_1         1  ''
              290  LOAD_METHOD              click
              292  CALL_METHOD_0         0  ''
              294  POP_TOP          

 L. 449       296  SETUP_FINALLY       330  'to 330'

 L. 450       298  LOAD_FAST                'driver'
              300  LOAD_METHOD              find_element_by_xpath
              302  LOAD_STR                 '//a[contains(@href,"releases/tag/0.0.0.27.1") and text()="0.0.0.27.1"]'
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'link_release'

 L. 451       308  LOAD_FAST                'driver'
              310  LOAD_METHOD              close
              312  CALL_METHOD_0         0  ''
              314  POP_TOP          

 L. 452       316  LOAD_FAST                'driver'
              318  LOAD_METHOD              quit
              320  CALL_METHOD_0         0  ''
              322  POP_TOP          

 L. 453       324  POP_BLOCK        
              326  LOAD_CONST               True
              328  RETURN_VALUE     
            330_0  COME_FROM_FINALLY   296  '296'

 L. 454       330  POP_TOP          
              332  POP_TOP          
              334  POP_TOP          

 L. 455       336  LOAD_FAST                'driver'
              338  LOAD_METHOD              close
              340  CALL_METHOD_0         0  ''
              342  POP_TOP          

 L. 456       344  LOAD_FAST                'driver'
              346  LOAD_METHOD              quit
              348  CALL_METHOD_0         0  ''
              350  POP_TOP          

 L. 458       352  LOAD_GLOBAL              print
              354  LOAD_STR                 'Release was not created.'
              356  CALL_FUNCTION_1       1  ''
              358  POP_TOP          

 L. 459       360  POP_EXCEPT       
              362  LOAD_CONST               False
              364  RETURN_VALUE     
              366  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 328


def upload_to_pypi(pypi_user, pypi_pass):
    if platform.system() == 'Linux':
        commands = f"twine upload dist/* -u {pypi_user} -p {pypi_pass} --verbose"
    else:
        if platform.system() == 'Windows':
            commands = f"twine upload dist/* -u {pypi_user} -p {pypi_pass} --verbose"
    commands = commands.split('\n')
    for command in commands:
        for path in execute_shell(command):
            print(path, end='')


def create_dist():
    if platform.system() == 'Linux':
        commands = 'python3 setup.py sdist bdist_wheel'
    else:
        if platform.system() == 'Windows':
            commands = 'python setup.py sdist bdist_wheel'
    commands = commands.split('\n')
    for command in commands:
        for path in execute_shell(command):
            print(path, end='')


def locally_install():
    if platform.system() == 'Linux':
        commands = 'python3 setup.py install'
    else:
        if platform.system() == 'Windows':
            commands = 'python setup.py install'
    commands = commands.split('\n')
    for command in commands:
        for path in execute_shell(command):
            print(path, end='')


def main():
    check_necessary_packages()
    check_necessary_resources()
    config_path = os.path.join(os.getcwd(), 'private/package.config')
    config = shaonutil.file.read_configuration_ini(config_path)
    package_name = config['PACKAGE']['package_name']
    git_url = config['PACKAGE']['github_project_url']
    github_user = config['PACKAGE']['github_user']
    github_pass = config['PACKAGE']['github_pass']
    pypi_user = config['PACKAGE']['pypi_user']
    pypi_pass = config['PACKAGE']['pypi_pass']
    pre_vname = get_version_name()
    print('Showing Previous Version :', pre_vname)
    new_vname = input('Give    New Version Name : ')
    release_tag = input('Give New Release tag : ')
    config['PACKAGE']['version'] = new_vname
    shaonutil.file.write_configuration_ini(config, config_path)
    changing_version_name(pre_vname, new_vname)
    cleaning_before_commit(package_name)
    commit_push()
    make_release(release_tag, git_url, github_user, github_pass)
    create_dist()
    locally_install()
    upload_to_pypi(pypi_user, pypi_pass)
    cleaning_before_commit(package_name)


if __name__ == '__main__':
    main()