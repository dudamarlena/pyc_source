# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['vidtag']
install_requires = \
['numpy>=1.16,<2.0',
 'opencv-python>=4.1,<5.0',
 'tensorflow>=2.0,<3.0',
 'tqdm>=4.40,<5.0']

entry_points = \
{'console_scripts': ['vidtag = entry:main']}

setup_kwargs = {
    'name': 'vidtag',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Oskar',
    'author_email': 'oskar.alund@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
