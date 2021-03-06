# -*- coding: utf-8 -*-

# system imports
import sys
import os.path as osp
from setuptools import setup, find_packages
import importlib.util

# local imports (must not depend on 3rd party packages)
from maestral import __version__, __author__, __url__
from maestral.utils.appdirs import get_runtime_path, get_old_runtime_path
from maestral.config.base import list_configs


# abort install if there are running daemons
running_daemons = []

for config in list_configs():
    pid_file = get_runtime_path('maestral', config + '.pid')
    old_pid_file = get_old_runtime_path('maestral', config + '.pid')
    if osp.exists(pid_file) or osp.exists(old_pid_file):
        running_daemons.append(config)

if running_daemons:
    sys.stderr.write(f"""
Maestral daemons with the following configs are running:

{', '.join(running_daemons)}

Please stop the daemons before updating to ensure a clean upgrade
of config files and compatibility been the CLI and daemon.
    """)
    sys.exit(1)


# proceed with actual install
install_requires = [
    'atomicwrites>=1.0.0',
    'bugsnag>=3.4.0',
    'click>=7.1.1',
    'dropbox>=10.0.0',
    'importlib_metadata;python_version<"3.8"',
    'jeepney;sys_platform=="linux"',
    'keyring>=19.0.0',
    'keyrings.alt>=3.1.0',
    'lockfile>=0.12.0',
    'packaging',
    'pathspec>=0.5.8',
    'Pyro5>=5.7',
    'requests',
    'rubicon-objc>=0.3.1;sys_platform=="darwin"',
    'sdnotify',
    'setuptools',
    'watchdog>=0.10.0',
]

gui_requires = [
    'maestral_qt>=1.0.0;sys_platform=="linux"',
    'maestral_cocoa>=1.0.0;sys_platform=="darwin"',
]

syslog_requires = ['systemd-python']

# if GUI is installed, always update it as well
if importlib.util.find_spec('maestral_qt') or importlib.util.find_spec('maestral_cocoa'):
    install_requires.extend(gui_requires)


setup(
    name='maestral',
    version=__version__,
    description='Open-source Dropbox client for macOS and Linux.',
    url=__url__,
    author=__author__,
    author_email='ss2151@cam.ac.uk',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'maestral': [
            'resources/*',
        ],
    },
    setup_requires=['wheel'],
    install_requires=install_requires,
    extras_require={
        'gui': gui_requires,
        'syslog': syslog_requires,
    },
    zip_safe=False,
    entry_points={
        'console_scripts': ['maestral=maestral.cli:main'],
    },
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    data_files=[
        ('share/icons/hicolor/512x512/apps', ['maestral/resources/maestral.png'])
    ],
)
