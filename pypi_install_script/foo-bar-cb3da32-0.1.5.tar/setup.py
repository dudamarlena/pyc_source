# -*- coding: utf-8 -*-
from setuptools import setup

import sdist_upip
packages = \
['foo_bar_cb3da32']

package_data = \
{'': ['*'], 'foo_bar_cb3da32': ['foo_bar_cb3da32.egg-info/*']}

install_requires = \
['micropython-logging>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'foo-bar-cb3da32',
    'version': '0.1.5',
    'description': 'Foo bar library with alpha for beta.',
    'long_description': None,
    'author': 'George Hawkins',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'cmdclass': {'sdist': sdist_upip.sdist},
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


import sys
print(sys.argv)

setup(**setup_kwargs)
