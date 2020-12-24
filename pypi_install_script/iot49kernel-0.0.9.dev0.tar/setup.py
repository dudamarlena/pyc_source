#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup

# from setuptools import setup
import sys
from iot49kernel.version import __version__

if sys.version_info < (3, 6):
    print('Python 3.6 or later requied')
    # sys.exit(1)

repl_server_req = [
    'pyserial',
    'selectors',
    'selectors2',
    'pyopenssl',
    'termcolor',
    'argparse'
]

repl_client_req = [
    'jupyter_client',
    'IPython',
    'ipykernel',
]

setup(
    name = 'iot49kernel',
    packages = ['iot49kernel'],
    version = __version__,
    description = 'Jupyter Kernel for IoT Python',
    license = 'MIT',
    author = 'Bernhard Boser',
    author_email = 'boser@berkeley.edu',
    url = 'https://iot49.github.io/',
    download_url = 'https://github.com/iot49/iot49kernel.git',
    keywords = ['micropython', 'iotpython'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    install_requires=repl_server_req,
    entry_points = {
        'console_scripts': [
            'iot49server=iot49kernel.serial2net:main',
            'iot49client=iot49kernel.net_repl:main',
        ],
    },
)
