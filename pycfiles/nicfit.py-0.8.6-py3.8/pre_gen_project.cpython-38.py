# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cookiecutter/hooks/pre_gen_project.py
# Compiled at: 2019-09-28 20:42:58
# Size of source mod 2**32: 2539 bytes
import re, sys
MODULE_REGEX = '^[_a-zA-Z][_a-zA-Z0-9]+$'
module_name = '{{ cookiecutter.py_module }}'
if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project slug (%s) is not a valid.' % module_name)
    sys.exit(1)
user_config = '\ndefault_context:\n    add_docs: "{{ cookiecutter.add_docs }}"\n    bitbucket_repo: "{{ cookiecutter.bitbucket_repo }}"\n    bitbucket_url: "{{ cookiecutter.bitbucket_url }}"\n    bitbucket_username: "{{ cookiecutter.bitbucket_username }}"\n    default_locale: "{{ cookiecutter.default_locale }}"\n    email: "{{ cookiecutter.email }}"\n    full_name: "{{ cookiecutter.full_name }}"\n    gettext_domain: "{{ cookiecutter.gettext_domain }}"\n    github_repo: "{{ cookiecutter.github_repo }}"\n    github_url: "{{ cookiecutter.github_url }}"\n    github_username: "{{ cookiecutter.github_username }}"\n    intended_audience: "{{ cookiecutter.intended_audience }}"\n    license: "{{ cookiecutter.license }}"\n    project_long_description: "{{ cookiecutter.project_long_description }}"\n    project_name: "{{ cookiecutter.project_name }}"\n    project_short_description: "{{ cookiecutter.project_short_description }}"\n    project_slug: "{{ cookiecutter.project_slug }}"\n    py26: "{{ cookiecutter.py26 }}"\n    py27: "{{ cookiecutter.py27 }}"\n    py33: "{{ cookiecutter.py33 }}"\n    py34: "{{ cookiecutter.py34 }}"\n    py35: "{{ cookiecutter.py35 }}"\n    py36: "{{ cookiecutter.py36 }}"\n    py37: "{{ cookiecutter.py37 }}"\n    py_module: "{{ cookiecutter.py_module }}"\n    pyapp_type: "{{ cookiecutter.pyapp_type }}"\n    pypi_repo_name: "{{ cookiecutter.pypi_repo_name }}"\n    pypi_username: "{{ cookiecutter.pypi_username }}"\n    pypy: "{{ cookiecutter.pypy }}"\n    pypy3: "{{ cookiecutter.pypy3 }}"\n    release_date: "{{ cookiecutter.release_date }}"\n    requirements_yaml: "{{ cookiecutter.requirements_yaml }}"\n    src_dir: "{{ cookiecutter.src_dir }}"\n    use_bitbucket: "{{ cookiecutter.use_bitbucket }}"\n    use_github: "{{ cookiecutter.use_github }}"\n    use_make: "{{ cookiecutter.use_make }}"\n    use_paver: "{{ cookiecutter.use_paver }}"\n    use_pypi_deployment_with_travis: "{{ cookiecutter.use_pypi_deployment_with_travis }}"\n    use_pytest: "{{ cookiecutter.use_pytest }}"\n    use_rtd: "{{ cookiecutter.use_rtd }}"\n    use_travis_ci: "{{ cookiecutter.use_travis_ci }}"\n    version: "{{ cookiecutter.version }}"\n    web: "{{ cookiecutter.web }}"\n    year: "{{ cookiecutter.year }}"\n'
with open('.cookiecutter.yml', 'w') as (fp):
    fp.write(user_config)