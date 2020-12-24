# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\rgilmore\PycharmProjects\OrthoEvolution\OrthoEvol\Cookies\cookie_jar.py
# Compiled at: 2017-11-20 17:46:52
# Size of source mod 2**32: 13427 bytes
import os, pkg_resources, yaml
from cookiecutter.main import cookiecutter
from cookiecutter.prompt import prompt_for_config
from cookiecutter.generate import generate_context
from cookiecutter.hooks import run_script
from pathlib import Path
from OrthoEvol import Cookies
from OrthoEvol.Tools.logit import LogIt
from OrthoEvol.Manager.config import yml
from pkg_resources import resource_filename
from OrthoEvol.Cookies.utils import archive

class CookBook(object):
    _config_file = resource_filename(yml.__name__, 'cookie_recipes.yml')

    def __init__(self, config_file=_config_file, **new_recipes):
        """
        The Cookie Recipes are public attributes for accessing
        the paths to the various cookiecutter templates in the
        Cookies module.

        The Cookie Recipes are used for the Recipes attribute
        in the Oven class.

        New Recipes can also be added...
        """
        self.CookieJar = Path(pkg_resources.resource_filename(Cookies.__name__, ''))
        self.repo_cookie = self.CookieJar / Path('new_repository')
        self.user_cookie = self.CookieJar / Path('new_user')
        self.project_cookie = self.CookieJar / Path('new_project')
        self.basic_project_cookie = self.CookieJar / Path('new_basic_project')
        self.research_cookie = self.CookieJar / Path('new_research')
        self.app_cookie = self.CookieJar / Path('new_app')
        self.db_cookie = self.CookieJar / Path('new_database')
        self.website_cookie = self.CookieJar / Path('new_website')
        with open(config_file, 'r') as (ymlfile):
            configuration = yaml.safe_load(ymlfile)
            if configuration is not None:
                setattr(self, 'CONFIGURATION', configuration)
                for key, value in configuration.items():
                    setattr(self, key, value)

        if new_recipes:
            for cookie, path in new_recipes.items():
                setattr(self, cookie, path)

            configuration.update(new_recipes)
        with open(config_file, 'w') as (ymlfile):
            yaml.dump(configuration, ymlfile)


class Oven(object):

    def __init__(self, repo=None, user=None, project=None, basic_project=False, website=None, db_repo='databases', output_dir=os.getcwd(), recipes=CookBook()):
        """
        This class uses cookiecutter to deploy custom cookiecutter templates:

        The Oven uses the different Ingredients (parameters/attributes) and
        the Cook Book(cookiecutter templates) to bake_the_cookies
        in the Oven(class methods).

        After the cookies cool, they are put in the cookie_jar (output directory).

        :param repo (string):  An ingredient representing the repository name.
        :param user (string):  An ingredient representing the user name
        :param project (string):  An ingredient representing the project name.
        :param basic_project (bool):  A secret ingredient ONLY for the basic project cookie.
        :param db_config_file (list):  An ingredient representing a list of db_config_file.
        :param website (string):  An ingredient representing the website name.
        :param output_dir (path or pathlike):  The cookie jar for storing the cookies.
        :param recipes (pathlike):  An index for the different recipe templates.
        """
        self.cookielog = LogIt().default(logname='Cookies', logfile=None)
        self.cookie_jar = output_dir
        self.repo = repo
        self.user = user
        self.project = project
        self.basic_project = basic_project
        self.website = website
        self.db_repo = db_repo
        self.Recipes = recipes
        self.Ingredients = {'repo':self.repo,  'user':self.user, 
         'project':self.project, 
         'basic_project':self.basic_project, 
         'website':self.website, 
         'db_repo':self.db_repo, 
         'recipes':self.Recipes.__dict__}

    def bake_the_repo(self, cookie_jar=None):
        self.cookielog.warn('Creating directories from the Repository Cookie template.')
        if cookie_jar:
            self.cookie_jar = cookie_jar
        else:
            if self.repo:
                no_input = True
                e_c = {'repository_name': self.repo}
            else:
                no_input = False
                e_c = None
        cookiecutter((str(self.Recipes.repo_cookie)), no_input=no_input, extra_context=e_c,
          output_dir=(str(self.cookie_jar)))
        os.chmod((str(self.cookie_jar / Path(self.repo))), mode=511)
        self.cookielog.info('Repository directories have been created. ✔')

    def bake_the_user(self, cookie_jar=None):
        self.cookielog.warn('Creating directories from the User Cookie template.')
        if cookie_jar:
            self.cookie_jar = cookie_jar
        cookiecutter((str(self.Recipes.user_cookie)), no_input=True, extra_context={'user_name': self.user},
          output_dir=(str(self.cookie_jar)))
        os.chmod((str(self.cookie_jar / Path(self.user))), mode=511)
        self.cookielog.info('Directories have been created for the user, %s. ✔' % self.user)

    def bake_the_project(self, cookie_jar=None):
        self.cookielog.warn('Creating directories from the Project Cookie template.')
        if cookie_jar:
            self.cookie_jar = cookie_jar
        else:
            if self.project:
                no_input = True
                e_c = {'project_name': self.project}
                project_log_message = '(%s)' % self.project
            else:
                no_input = False
                e_c = None
                project_log_message = 'that has been named with user input'
            if not self.basic_project:
                self.cookielog.warn('A project linked to a user/repository is being created.')
                cookiecutter((str(self.Recipes.project_cookie)), extra_context=e_c, no_input=no_input, output_dir=(str(self.cookie_jar)))
                if self.user:
                    self.cookielog.info("Directories have been created for %s's project %s. ✔" % (self.user, project_log_message))
                else:
                    self.cookielog.info('Directories have been created for %s.' % project_log_message)
            else:
                self.cookielog.warn('A basic standalone project is being created.')
                cookiecutter((str(self.Recipes.basic_project_cookie)), extra_context=e_c, no_input=no_input, output_dir=(str(self.cookie_jar)))
                self.cookielog.info('Directories have been created for a standalone project %s. ✔' % project_log_message)
        os.chmod((str(self.cookie_jar / Path(self.project))), mode=511)

    def bake_the_db_repo(self, db_config_file, db_path, cookie_jar=None, archive_flag=False, delete=False):
        """
        :return: A new database inside the users database directory
        """
        if cookie_jar:
            self.cookie_jar = cookie_jar
            cookiecutter((str(self.Recipes.db_cookie)), extra_context=e_c, no_input=no_input, output_dir=(str(self.cookie_jar)))
            self.cookielog.info('Directories have been created for a database repository %s.' % str(self.cookie_jar / Path(self.db_repo)))
            os.chmod((str(self.cookie_jar / Path(self.db_repo))), mode=511)

    def bake_the_website(self, host, port, website_path, cookie_jar=None):
        self.cookielog.warn('Creating directories from the Website Cookie template.')
        if cookie_jar:
            self.cookie_jar = cookie_jar
        e_c = {'website_name':self.website,  'website_path':os.path.join(str(website_path), ''), 
         'website_host':host, 
         'website_port':port}
        cookiecutter((str(self.Recipes.website_cookie)), no_input=True, extra_context=e_c,
          output_dir=(str(self.cookie_jar)))
        os.chmod((str(self.cookie_jar / Path(self.website))), mode=511)
        script_path = website_path / Path('hooks') / Path('post_gen_project.sh')
        run_script(script_path=(str(script_path)), cwd=(str(website_path)))
        self.cookielog.info('Directories have been created for the Flask Web Server, %s. ✔' % self.website)
        self.cookielog.warn('The %s Flask Server should now be running on http://%s:%s' % (self.website, host, port))

    def bake_the_research(self, research_type, research, cookie_jar=None):
        self.cookielog.warn('Creating directories from the Research Cookie template.')
        if cookie_jar:
            self.cookie_jar = cookie_jar
        e_c = {'research_type':research_type,  'research_name':research}
        cookiecutter((str(self.Recipes.research_cookie)), no_input=True, extra_context=e_c,
          output_dir=(str(self.cookie_jar)))
        os.chmod((str(self.cookie_jar / Path(research_type))), mode=511)
        self.cookielog.info('Directories have been created for the %s research project, %s. ✔' % (research_type, research))

    def bake_the_app(self, app, cookie_jar=None):
        self.cookielog.warn('Creating directories from the App Cookie template.')
        if cookie_jar:
            self.cookie_jar = cookie_jar
        e_c = {'app_name': app}
        cookiecutter((str(self.Recipes.app_cookie)), no_input=True, extra_context=e_c,
          output_dir=(str(self.cookie_jar)))
        os.chmod((str(self.cookie_jar)), mode=511)
        self.cookielog.info('Directories have been created for an R-Shiny app, %s. ✔' % app)