#!/usr/bin/python
"""setup script for django_mojeid_connect."""
from __future__ import unicode_literals

from setuptools import find_packages, setup

import django_mojeid_connect

setup(name='django-mojeid-connect',
      version=django_mojeid_connect.__version__,
      description='Django application for login to mojeID using OpenID Connect',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Tomas Pazderka',
      author_email='tomas.pazderka@nic.cz',
      url='https://github.com/tpazderka/django-oidc-sub',
      packages=find_packages(),
      install_requires=['Django>=1.11', 'mozilla-django-oidc', 'django-oidc-sub'],
      extras_require={'quality': ['isort', 'flake8', 'pydocstyle']})
