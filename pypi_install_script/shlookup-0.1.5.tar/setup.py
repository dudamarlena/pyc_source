# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shlookup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shlookup',
    'version': '0.1.5',
    'description': 'A tool to provide at a glance information about a given EVE Online character',
    'long_description': None,
    'author': 'Sapporo Jones',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
