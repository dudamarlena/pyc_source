# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/common/runtime_template.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3837 bytes
"""
All-in-one metadata about runtimes
"""
import itertools, os, pathlib
_init_path = str(pathlib.Path(os.path.dirname(__file__)).parent)
_templates = os.path.join(_init_path, 'init', 'templates')
RUNTIME_DEP_TEMPLATE_MAPPING = {'python':[
  {'runtimes':[
    'python3.8', 'python3.7', 'python3.6', 'python2.7'], 
   'dependency_manager':'pip', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-python'), 
   'build':True}], 
 'ruby':[
  {'runtimes':[
    'ruby2.5', 'ruby2.7'], 
   'dependency_manager':'bundler', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-ruby'), 
   'build':True}], 
 'nodejs':[
  {'runtimes':[
    'nodejs12.x', 'nodejs10.x'], 
   'dependency_manager':'npm', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-nodejs'), 
   'build':True}], 
 'dotnet':[
  {'runtimes':[
    'dotnetcore2.1', 'dotnetcore2.0', 'dotnetcore1.0'], 
   'dependency_manager':'cli-package', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-dotnet'), 
   'build':True}], 
 'go':[
  {'runtimes':[
    'go1.x'], 
   'dependency_manager':'mod', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-golang'), 
   'build':False}], 
 'java':[
  {'runtimes':[
    'java11', 'java8'], 
   'dependency_manager':'maven', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-java-maven'), 
   'build':True},
  {'runtimes':[
    'java11', 'java8'], 
   'dependency_manager':'gradle', 
   'init_location':os.path.join(_templates, 'cookiecutter-aws-sam-hello-java-gradle'), 
   'build':True}]}
RUNTIME_TO_DEPENDENCY_MANAGERS = {'python3.8':[
  'pip'], 
 'python3.7':[
  'pip'], 
 'python3.6':[
  'pip'], 
 'python2.7':[
  'pip'], 
 'ruby2.5':[
  'bundler'], 
 'ruby2.7':[
  'bundler'], 
 'nodejs12.x':[
  'npm'], 
 'nodejs10.x':[
  'npm'], 
 'dotnetcore2.1':[
  'cli-package'], 
 'dotnetcore2.0':[
  'cli-package'], 
 'dotnetcore1.0':[
  'cli-package'], 
 'go1.x':[
  'mod'], 
 'java8':[
  'maven', 'gradle'], 
 'java11':[
  'maven', 'gradle']}
SUPPORTED_DEP_MANAGERS = {c['dependency_manager'] for c in list((itertools.chain)(*RUNTIME_DEP_TEMPLATE_MAPPING.values())) if c['dependency_manager'] if c['dependency_manager']}
RUNTIMES = set((itertools.chain)(*[c['runtimes'] for c in list((itertools.chain)(*RUNTIME_DEP_TEMPLATE_MAPPING.values()))]))
INIT_RUNTIMES = [
 'nodejs12.x',
 'python3.8',
 'ruby2.7',
 'go1.x',
 'java11',
 'dotnetcore2.1',
 'nodejs10.x',
 'python3.7',
 'python3.6',
 'python2.7',
 'ruby2.5',
 'java8',
 'dotnetcore2.0',
 'dotnetcore1.0']
SAM_RUNTIME_TO_SCHEMAS_CODE_LANG_MAPPING = {'java8':'Java8', 
 'java11':'Java8', 
 'python3.7':'Python36', 
 'python3.6':'Python36', 
 'python3.8':'Python36'}