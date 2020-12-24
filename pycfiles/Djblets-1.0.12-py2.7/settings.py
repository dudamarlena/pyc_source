# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/settings.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import os
from djblets.staticbundles import PIPELINE_JAVASCRIPT, PIPELINE_STYLESHEETS
SECRET_KEY = b'47157c7ae957f904ab809d8c5b77e0209221d4c0'
USE_I18N = True
DEBUG = False
DJBLETS_ROOT = os.path.abspath(os.path.dirname(__file__))
HTDOCS_ROOT = os.path.join(DJBLETS_ROOT, b'htdocs')
STATIC_ROOT = os.path.join(HTDOCS_ROOT, b'static')
STATIC_URL = b'/'
LOGIN_LIMIT_RATE = b'5/m'
STATICFILES_DIRS = (
 os.path.join(DJBLETS_ROOT, b'static'),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', )
STATICFILES_STORAGE = b'pipeline.storage.PipelineCachedStorage'
NODE_PATH = os.path.join(DJBLETS_ROOT, b'..', b'node_modules')
os.environ[b'NODE_PATH'] = NODE_PATH
PIPELINE = {b'PIPELINE_ENABLED': not DEBUG or os.getenv(b'FORCE_BUILD_MEDIA'), 
   b'COMPILERS': [
                b'djblets.pipeline.compilers.es6.ES6Compiler',
                b'djblets.pipeline.compilers.less.LessCompiler'], 
   b'CSS_COMPRESSOR': None, 
   b'JS_COMPRESSOR': b'pipeline.compressors.uglifyjs.UglifyJSCompressor', 
   b'JAVASCRIPT': PIPELINE_JAVASCRIPT, 
   b'STYLESHEETS': PIPELINE_STYLESHEETS, 
   b'BABEL_BINARY': os.path.join(NODE_PATH, b'babel-cli', b'bin', b'babel.js'), 
   b'BABEL_ARGUMENTS': [
                      b'--presets', b'es2015', b'--plugins', b'dedent',
                      b'-s', b'true'], 
   b'LESS_BINARY': os.path.join(NODE_PATH, b'less', b'bin', b'lessc'), 
   b'LESS_ARGUMENTS': [
                     b'--no-color',
                     b'--source-map',
                     b'--js',
                     b'--autoprefix=> 2%, ie >= 9'], 
   b'UGLIFYJS_BINARY': os.path.join(NODE_PATH, b'uglify-js', b'bin', b'uglifyjs')}
INSTALLED_APPS = [
 b'django.contrib.staticfiles',
 b'djblets.auth',
 b'djblets.datagrid',
 b'djblets.extensions',
 b'djblets.feedview',
 b'djblets.gravatars',
 b'djblets.log',
 b'djblets.pipeline',
 b'djblets.siteconfig',
 b'djblets.testing',
 b'djblets.util',
 b'djblets.webapi']