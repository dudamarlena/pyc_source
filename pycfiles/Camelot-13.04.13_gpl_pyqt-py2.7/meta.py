# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/bin/meta.py
# Compiled at: 2013-04-11 17:47:52
"""
Utility functions and classes to start a new Camelot project, this
could be the start of MetaCamelot
"""
import os, logging
from camelot.core.conf import settings
from camelot.core.utils import ugettext_lazy as _
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.object_admin import ObjectAdmin
from camelot.admin.action import Action
from camelot.view.controls import delegates
from camelot.view.main import Application
LOGGER = logging.getLogger('camelot.bin.meta')

class MetaSettings(object):
    """settings target to be used within MetaCamelot, when no real
    settings are available yet"""
    CAMELOT_MEDIA_ROOT = '.'

    def ENGINE(self):
        return 'sqlite:///'

    def setup_model(self):
        pass


class MetaCamelotAdmin(ApplicationAdmin):
    """ApplicationAdmin class to be used within meta camelot"""
    name = 'Meta Camelot'


def launch_meta_camelot():
    import sys
    from camelot.view.model_thread import construct_model_thread, get_model_thread
    from camelot.admin.action import GuiContext
    from PyQt4 import QtGui
    app = QtGui.QApplication([ a for a in sys.argv if a ])
    construct_model_thread()
    mt = get_model_thread()
    mt.start()
    settings.append(MetaSettings())
    new_project = CreateNewProject()
    gui_context = GuiContext()
    admin = MetaCamelotAdmin()
    admin.get_stylesheet()
    gui_context.admin = admin
    new_project.gui_run(gui_context)
    return app


class MetaCamelotApplication(Application):
    """A Camelot application to build new Camelot
    projects."""

    def initialization(self):
        new_project = CreateNewProject('New Camelot Project')
        new_project.run()


features = [
 (
  'source', '.', delegates.LocalFileDelegate, 'The directory in which to create<br/>the sources of the new project '),
 (
  'name', 'My Application', delegates.PlainTextDelegate, 'The name of the application<br/>as it will appear in the main window and<br/>will be used to store settings in the<br/>registry.'),
 (
  'author', 'My Company', delegates.PlainTextDelegate, 'The author of the application, this<br/>will be used to store settings in the<br/>registry.'),
 (
  'module', 'myapplication', delegates.PlainTextDelegate, 'The name of the python module that<br/>will contain the application'),
 (
  'domain', 'mydomain.com', delegates.PlainTextDelegate, 'The domain name of the author, this will<br/>be used to store settings in the registry'),
 (
  'application_url', 'http://www.python-camelot.com', delegates.PlainTextDelegate, 'Url of the application, this url should be<br/>unique for the application, as it will be used<br/>to uniquely identify the application in Windows'),
 (
  'help_url', 'http://www.python-camelot.com/docs.html', delegates.PlainTextDelegate, 'Part of the website with online help'),
 (
  'installer', False, delegates.BoolDelegate, 'Build a windows installer')]
templates = [
 ('{{options.module}}/application_admin.py', "\nfrom camelot.view.art import Icon\nfrom camelot.admin.application_admin import ApplicationAdmin\nfrom camelot.admin.section import Section\nfrom camelot.core.utils import ugettext_lazy as _\n\nclass MyApplicationAdmin(ApplicationAdmin):\n  \n    name = '{{options.name}}'\n    application_url = '{{options.application_url}}'\n    help_url = '{{options.help_url}}'\n    author = '{{options.author}}'\n    domain = '{{options.domain}}'\n    \n    def get_sections(self):\n        from camelot.model.memento import Memento\n        from camelot.model.i18n import Translation\n        return [ Section( _('My classes'),\n                          self,\n                          Icon('tango/22x22/apps/system-users.png'),\n                          items = [] ),\n                 Section( _('Configuration'),\n                          self,\n                          Icon('tango/22x22/categories/preferences-system.png'),\n                          items = [Memento, Translation] )\n                ]\n    "),
 ('__init__.py', ''),
 ('{{options.module}}/__init__.py', ''),
 ('{{options.module}}/test.py', "\n#\n# Default unittests for a camelot application.  These unittests will create\n# screenshots of all the views in the application.  Run them with this command :\n#\n# python -m nose.core -v -s {{options.module}}/test.py\n#\n\nimport os\n\nfrom camelot.test import EntityViewsTest\n\n# screenshots will be put in this directory\nstatic_images_path = os.path.join( os.path.dirname( __file__ ), 'images' )\n\nclass MyApplicationViewsTest( EntityViewsTest ):\n\n    images_path = static_images_path\n    "),
 ('main.py', '\nimport logging\nfrom camelot.core.conf import settings, SimpleSettings\n\nlogging.basicConfig( level = logging.ERROR )\nlogger = logging.getLogger( \'main\' )\n\n# begin custom settings\nclass MySettings( SimpleSettings ):\n\n    # add an ENGINE or a CAMELOT_MEDIA_ROOT method here to connect\n    # to another database or change the location where files are stored\n    #\n    # def ENGINE( self ):\n    #     from sqlalchemy import create_engine\n    #     return create_engine( \'postgresql://user:passwd@127.0.0.1/database\' )\n    \n    def setup_model( self ):\n        """This function will be called at application startup, it is used to \n        setup the model"""\n        from camelot.core.sql import metadata\n        from camelot.core.orm import setup_all\n        metadata.bind = self.ENGINE()\n        import camelot.model.authentication\n        import camelot.model.i18n\n        import camelot.model.memento\n        import {{options.module}}.model\n        setup_all()\n        metadata.create_all()\n\nmy_settings = MySettings( \'{{options.author}}\', \'{{options.name}}\' ) \nsettings.append( my_settings )\n# end custom settings\n\ndef start_application():\n    from camelot.view.main import main\n    from {{options.module}}.application_admin import MyApplicationAdmin\n    main(MyApplicationAdmin())\n\nif __name__ == \'__main__\':\n    start_application()\n    '),
 ('{{options.module}}/model.py', '\nfrom sqlalchemy.schema import Column\nimport sqlalchemy.types\n    \nfrom camelot.admin.entity_admin import EntityAdmin\nfrom camelot.core.orm import Entity\nimport camelot.types\n    '),
 ('excludes.txt', '\nvtk*\nsphinx*\n\nLib\\site-packages\\cvxopt*\nLib\\site-packages\\IPython*\nLib\\site-packages\\logilab*\nLib\\site-packages\\nose*\nLib\\site-packages\\PIL*\nLib\\site-packages\\py2exe*\nLib\\site-packages\\pyflakes*\nLib\\site-packages\\pylint*\nLib\\site-packages\\pytz\\zoneinfo\\*\nLib\\site-packages\\rope*\nLib\\site-packages\\Sphinx*\nLib\\site-packages\\spyder*\nLib\\site-packages\\virtualenv*\nLib\\site-packages\\VTK*\nLib\\site-packages\\docutils*\nLib\\site-packages\\pyreadline*\nLib\\site-packages\\Bio*\nLib\\site-packages\\vitables*\nLib\\site-packages\\sympy*\nLib\\site-packages\\Cython*\nLib\\site-packages\\sympy*\nLib\\site-packages\\PyOpenGL*\nLib\\site-packages\\tables*\nLib\\site-packages\\zmq*\n\ninclude\nlicense\nlibs   \n    '),
 ('setup.py', "\n#\n# Default setup file for a Camelot application\n#\n# To build a windows installer, execute this file with :\n#\n#     python setup.py egg_info bdist_cloud wininst_cloud\n#\n# Running from the Python SDK command line\n#\n\nimport datetime\nimport logging\n\nfrom setuptools import setup, find_packages\n\nlogging.basicConfig( level=logging.INFO )\n\nsetup(\n    name = '{{options.name}}',\n    version = '1.0',\n    author = '{{options.author}}',\n    url = '{{options.application_url}}',\n    include_package_data = True,\n    packages = find_packages(),\n    py_modules = ['settings', 'main'],\n    entry_points = {'gui_scripts':[\n                     'main = main:start_application',\n                    ],},\n    options = {\n        'bdist_cloud':{'revision':'0',\n                       'branch':'master',\n                       'uuid':'{{uuid}}',\n                       'update_before_launch':False,\n                       'default_entry_point':('gui_scripts','main'),\n                       'changes':[],\n                       'timestamp':datetime.datetime.now(),\n                       },\n        'wininst_cloud':{ 'excludes':'excludes.txt',\n                          'uuid':'{{uuid}}', },\n    }, \n\n  )\n\n    ")]

class NewProjectOptions(object):

    def __init__(self):
        for feature in features:
            setattr(self, feature[0], feature[1])

    class Admin(ObjectAdmin):
        verbose_name = _('New project')
        form_display = [ feature[0] for feature in features ]
        field_attributes = dict((feature[0], {'editable': True, 'delegate': feature[2], 'nullable': False, 'tooltip': feature[3]}) for feature in features)
        field_attributes['source']['directory'] = True


class CreateNewProject(Action):
    """Action to create a new project, based on a form with
    options the user fills in."""

    def model_run(self, context=None):
        from PyQt4 import QtGui
        from camelot.view import action_steps
        options = NewProjectOptions()
        yield action_steps.UpdateProgress(text='Request information')
        yield action_steps.ChangeObject(options)
        yield action_steps.UpdateProgress(text='Creating new project')
        self.start_project(options)
        project_path = os.path.abspath(options.source)
        if options.installer:
            cloudlaunch_found = False
            try:
                import cloudlaunch
                cloudlaunch_found = True
            except Exception:
                yield action_steps.MessageBox('To build a Windows installer, you need to be using<br/>the Conceptive Python SDK, please visit<br/><a href="http://www.conceptive.be/python-sdk.html">www.conceptive.be/python-sdk.html</a><br/>for more information')

            if cloudlaunch_found:
                LOGGER.debug('%s imported' % cloudlaunch.__name__)
                yield action_steps.UpdateProgress(text='Building windows installer')
                import distutils.core
                current_dir = os.getcwd()
                os.chdir(project_path)
                setup_path = os.path.join('setup.py')
                distribution = distutils.core.run_setup(setup_path, script_args=[
                 'egg_info', 'bdist_cloud', 'wininst_cloud'])
                os.chdir(current_dir)
                for command, _python_version, filename in distribution.dist_files:
                    if command == 'wininst_cloud':
                        yield action_steps.MessageBox('Use Inno Setup to process the file<br/><b>%s</b><br/> to build the installer executable' % os.path.join(project_path, filename), standard_buttons=QtGui.QMessageBox.Ok)

        yield action_steps.MessageBox('All files for the new project<br/>were created in <b>%s</b>' % project_path, standard_buttons=QtGui.QMessageBox.Ok)
        yield action_steps.OpenFile(project_path)

    def start_project(self, options):
        from jinja2 import Template
        import uuid
        context = {'options': options, 'uuid': str(uuid.uuid4())}
        if not os.path.exists(os.path.join(options.source, options.module)):
            os.makedirs(os.path.join(options.source, options.module))
        for filename_template, code_template in templates:
            filename = Template(filename_template).render(context)
            code = Template(code_template).render(context)
            fp = open(os.path.join(options.source, filename), 'w')
            fp.write(code)
            fp.close()