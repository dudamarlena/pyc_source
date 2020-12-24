# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_cli', 'aiogram_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=3.0.0-alpha.4,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'typer[all]>=0.2.1,<0.3.0']

entry_points = \
{'aiogram_cli.plugins': ['builtins = aiogram_cli.commands.builtin:setup'],
 'console_scripts': ['aiogram = aiogram_cli.main:main']}

setup_kwargs = {
    'name': 'aiogram-cli',
    'version': '0.0.1a1',
    'description': '',
    'long_description': None,
    'author': 'Alex Root Junior',
    'author_email': 'jroot.junior@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
