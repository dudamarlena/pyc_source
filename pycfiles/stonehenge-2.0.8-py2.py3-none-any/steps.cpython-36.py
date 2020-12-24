# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rtownley/Projects/stonehenge/stonehenge/build_project/steps.py
# Compiled at: 2018-09-10 11:14:52
# Size of source mod 2**32: 6426 bytes
import os, psycopg2, shutil
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from subprocess import call
from stonehenge.utils import copy_from_template
from stonehenge.utils import copy_dir_from_template
from stonehenge.utils import generate_password
from stonehenge.utils import config
from stonehenge.utils import PROJECT_DIR
from stonehenge.utils import TEMPLATES_DIR
from stonehenge.utils import git_commit

def install_python_dependencies(project):
    """Installs Python requirements for a project"""
    copy_from_template(project, 'requirements.txt')
    call(['pip', 'install', '-r', 'requirements.txt'])


def configure_database(project):
    """Configures the PostgreSQL database for the project"""
    if not project.DATABASE_NAME:
        project.DATABASE_NAME = project.slug + 'db'
    elif not project.DATABASE_USER:
        project.DATABASE_USER = project.slug + 'dbuser'
    else:
        if not project.DATABASE_PASSWORD:
            project.DATABASE_PASSWORD = generate_password()
        else:
            postgres_password = getattr(config, 'POSTGRES_USER_PASSWORD', None)
            if not postgres_password:
                postgres_password = input('PostgreSQL user password: ')
            connection = psycopg2.connect(dbname='postgres',
              user='postgres',
              password=postgres_password)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            try:
                cursor.execute('CREATE USER {0};'.format(project.DATABASE_USER))
            except psycopg2.ProgrammingError:
                try:
                    cursor.execute('DROP USER {0};'.format(project.DATABASE_USER))
                    cursor.execute('CREATE USER {0};'.format(project.DATABASE_USER))
                except psycopg2.InternalError:
                    cursor.execute('DROP DATABASE {0};'.format(project.DATABASE_NAME))
                    cursor.execute('DROP USER {0};'.format(project.DATABASE_USER))
                    cursor.execute('CREATE USER {0};'.format(project.DATABASE_USER))

        cursor.execute("ALTER USER {0} WITH PASSWORD '{1}';".format(project.DATABASE_USER, project.DATABASE_PASSWORD))
        try:
            cursor.execute('CREATE DATABASE {0} OWNER {1};'.format(project.DATABASE_NAME, project.DATABASE_USER))
        except psycopg2.ProgrammingError:
            cursor.execute('DROP DATABASE {0};'.format(project.DATABASE_NAME))
            cursor.execute('CREATE DATABASE {0} OWNER {1};'.format(project.DATABASE_NAME, project.DATABASE_USER))


def setup_version_control(project):
    """Configures version control for the project"""
    if os.path.isdir(os.path.join(PROJECT_DIR, '.git')):
        shutil.rmtree(os.path.join(PROJECT_DIR, '.git'))
    if os.path.isfile(os.path.join(PROJECT_DIR, '.gitignore')):
        os.remove(os.path.join(PROJECT_DIR, '.gitignore'))
    call(['git', 'init'])
    call(['git', 'remote', 'add', 'origin', project.GIT_REPOSITORY])
    copy_from_template(project, '.gitignore')


def build_backend(project):
    """Build the backend project out

    Called after building frontend to accommodate create-react-app
    """
    call(['django-admin', 'startproject', project.slug, '.'])
    call('python manage.py startapp public'.split(' '))
    call('python manage.py startapp users'.split(' '))
    if os.path.isfile(os.path.join(PROJECT_DIR, project.slug, 'settings.py')):
        os.remove(os.path.join(PROJECT_DIR, project.slug, 'settings.py'))
    try:
        os.makedirs(os.path.join(PROJECT_DIR, project.slug, 'settings'))
    except FileExistsError:
        pass

    for settings_file in os.listdir(os.path.join(TEMPLATES_DIR, 'settings')):
        source = os.path.join('settings', settings_file)
        destination = os.path.join(PROJECT_DIR, project.slug, 'settings', settings_file)
        copy_from_template(project, source, dest=destination)

    destination = os.path.join(PROJECT_DIR, project.slug, 'urls.py')
    copy_from_template(project, 'urls.py', dest=destination)
    os.makedirs(os.path.join(PROJECT_DIR, 'templates'))
    destination = os.path.join(PROJECT_DIR, 'templates', 'index.html')
    copy_dir_from_template(project, 'public')
    copy_dir_from_template(project, 'users')
    call('python manage.py makemigrations'.split(' '))
    call('python manage.py migrate'.split(' '))


def build_frontend(project):
    """Build out the frontend"""
    call(['npx', 'create-react-app', 'frontend'])
    for filename in os.listdir(os.path.join(PROJECT_DIR, 'frontend')):
        if filename != project.slug:
            shutil.move(os.path.join(PROJECT_DIR, 'frontend', filename), os.path.join(PROJECT_DIR, filename))

    shutil.rmtree(os.path.join(PROJECT_DIR, 'frontend'))
    git_commit('Pre create-react-app ejection commit')
    call(['npm', 'run', 'eject'])
    FRONTEND_DEPENDENCIES = [
     'normalize.css']
    for dep in FRONTEND_DEPENDENCIES:
        call('npm install {0} --save'.format(dep).split(' '))

    FRONTEND_DEV_DEPENDENCIES = [
     'style-loader',
     'css-loader',
     'sass-loader',
     'node-sass']
    for dep in FRONTEND_DEV_DEPENDENCIES:
        call('npm install {0} --save-dev'.format(dep).split(' '))

    call('npm install webpack-bundle-tracker --save-dev'.split(' '))
    copy_from_template(project, 'config/paths.js')
    copy_from_template(project, 'config/webpack.config.dev.js')
    copy_from_template(project, 'config/webpackDevServer.config.js')
    call('mkdir -p assets/bundles'.split(' '))
    call('npm install --save react-router-dom'.split(' '))
    call('mkdir -p src/components/'.split(' '))
    copy_from_template(project, 'src/App.js')
    copy_dir_from_template(project, 'src')