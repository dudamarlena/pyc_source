# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyle/fcms/flask-cms/flask_cms/settings.py
# Compiled at: 2016-01-26 17:48:16
"""
    settings
    ~~~~~~~~

    Global settings for project.
"""
import os
from local_settings import LocalConfig

class BaseConfig(LocalConfig):
    SYSTEM_MESSAGE_CATEGORIES = [
     'successinfo',
     'warning',
     'danger']
    ADMIN_PER_PAGE = 5
    CODEMIRROR_LANGUAGES = ['python', 'python2', 'python3', 'php', 'javascript', 'xml', 'jinja2']
    CODEMIRROR_THEME = 'blackboard'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    URL_MODULES = [
     'flask_cms.core.urls.routes',
     'flask_cms.admin.urls.routes',
     'flask_cms.auth.urls.routes',
     'flask_cms.blog.urls.routes',
     'flask_cms.member.urls.routes',
     'flask_cms.page.urls.routes',
     'flask_cms.fileviewer.urls.routes']
    BLUEPRINTS = [
     'core.core',
     'member.member',
     'admin.admin',
     'menu.menu',
     'blog.blog',
     'page.page',
     'auth.auth',
     'fileviewer.fileviewer']
    EXTENSIONS = [
     'ext.alembic']
    CONTEXT_PROCESSORS = [
     'core.context_processors.common_context',
     'menu.context_processors.frontend_nav',
     'menu.context_processors.admin_nav',
     'auth.context_processors.user_context',
     'core.context_processors.add_is_page',
     'core.context_processors.add_is_list',
     'core.context_processors.add_get_model',
     'core.context_processors.add_get_button',
     'core.context_processors.add_get_icon',
     'core.context_processors.get_context',
     'core.context_processors.add_get_block',
     'core.context_processors.add_urlfor',
     'core.context_processors.add_layouts',
     'core.context_processors.add_layout_mode',
     'menu.context_processors.get_navbar',
     'menu.context_processors._add_navbar',
     'make_base.base',
     'auth.context_processors.auth_context',
     'blog.context_processors.add_admin_head',
     'core.context_processors.add_size_converters']
    TEMPLATE_FILTERS = [
     'flask.ext.xxl.filters.date',
     'flask.ext.xxl.filters.date_pretty',
     'flask.ext.xxl.filters.datetime',
     'flask.ext.xxl.filters.pluralize',
     'flask.ext.xxl.filters.month_name',
     'flask.ext.xxl.filters.markdown',
     'core.context_processors.fix_body',
     'core.filters.split',
     'blog.filters.markdown']
    CONTACT_FORM_SETTINGS = {'HEADING': 'Send Us a message', 
       'SUBHEADING': 'Or a Comment', 
       'OPTIONS': (
                 ('test', 'opt1'),
                 ('test2', 'opt2'),
                 ('test3', 'opt3'),
                 ('test4', 'opt4'),
                 ('test5', 'opt5'),
                 ('test6', 'opt6')), 
       'SUBMIT_TEXT': 'Send to Us', 
       'COMPANY_TITLE': 'Level2designs', 
       'COMPANY_ADDRESS': {'NAME': 'level2designs', 
                           'STREET': '1045 w katella', 
                           'CITY': 'Orange', 
                           'STATE': 'CA', 
                           'ZIP': '92804'}, 
       'COMPANY_PHONE': '714-783-6369', 
       'CONTACT_NAME': 'Roux', 
       'CONTACT_EMAIL': 'kyle@level2designs.com'}
    NAVBAR_TEMPLATE_FILES = (
     ('bootstrap-std', 'navbars/bs_std.html'),
     ('bootstrap-inverse', 'navbars/bs_inverse.html'),
     ('blog', 'navbars/blog.html'),
     ('clean', 'navbars/clean.html'))
    DEFAULT_NAVBAR = 'clean'
    LAYOUT_FILES = {'blog': 'layouts/1col_leftsidebar.html', 
       'post_form': 'layouts/1col_rightsidebar.html', 
       'one_col_left': 'layouts/1col_leftsidebar.html', 
       'one_col_right': 'layouts/1col_rightsidebar.html', 
       'two_col_left': 'layouts/2col_leftsidebar.html', 
       'two_col_right': 'layouts/2col_rightsidebar.html', 
       'three_col_left': 'layouts/3col_leftsidebar.html'}
    BASE_TEMPLATE_FILES = [
     ('one_col_left', '1_col_left.html'),
     ('one_col_right', '1_col_right.html'),
     ('two_col_left', '2_col_left.html'),
     ('two_col_right', '2_col_right.html'),
     ('three_col', '3_col.html')]
    BLOG_SIDEBAR_LEFT = True
    BLOG_TITLE = 'Dynamic'
    BLOG_CONTENT = 'some text to put into my<br />Blog'
    DEFAULT_ICON_LIBRARY = 'octicon'


def get_choices():
    return BaseConfig.CONTACT_FORM_SETTINGS['OPTIONS']


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'mysql://test:test@174.140.227.137:3306/test_test5'