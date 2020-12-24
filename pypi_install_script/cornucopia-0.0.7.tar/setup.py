#!/usr/bin/env python

import os
from setuptools import setup

import cornucopia


# Find dependencies
filter_deps = lambda r: not r.startswith('#') and not r.startswith('-')
with open('requirements.txt') as f:
    requires = list(filter(filter_deps, [l.rstrip('\n') for l in f]))


# Find all the modules to include in the package
package_data = []
project_name = cornucopia.__name__
for dirname in os.listdir(cornucopia.__name__):
    if dirname == '__pycache__':
        continue

    # Loop over all the sub-modules within the main package, adding them
    # to be included in the install.
    for root, _, _ in os.walk(os.path.join(project_name, dirname)):
        package_data.append(os.path.join(root[len(project_name) + 1:], '**'))


# The actual package setup
setup(
    name=project_name,
    description=cornucopia.__doc__,
    version=cornucopia.__version__,
    license=cornucopia.__license__,
    author=cornucopia.__author__,
    install_requires=requires,
    extras_require={
        'develop': ['jedi', 'flake8', 'nose', 'ipython', 'coverage']},
    packages=[project_name],
    package_dir={project_name: project_name},
    package_data={project_name: package_data},
    entry_points={
        'console_scripts': [
            '{0} = {0}.cli:cli'.format(project_name)
        ],
    },
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython'])
