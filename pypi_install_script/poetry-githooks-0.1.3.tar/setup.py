# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_githooks']

package_data = \
{'': ['*']}

entry_points = \
{u'poetry_githooks': ['.git = poetry_githooks:main']}

setup_kwargs = {
    'name': 'poetry-githooks',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Thomas Thiebaud',
    'author_email': 'thiebaud.tom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
