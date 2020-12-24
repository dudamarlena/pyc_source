#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 
    'Jinja2==2.10.3',
    'MarkupSafe==1.1.1'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Marcel Neidinger",
    author_email='marcel.neidinger@nlogn.org',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Simple python module to generate configurations from templates",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='config_templater',
    name='config_templater',
    packages=find_packages(include=['config_templater', 'config_templater.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/squ4rks/config_templater',
    version='0.1.1',
    zip_safe=False,
)
