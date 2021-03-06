"""
    Boilerplate-Python
    ~~~~~~~~~~~~~~~~~~

    Boilerplate-Python is an empty Python project.

    It is meant to be forked when starting a new Python project to inherit multiple DevOps functions.
"""

from os import path

from setuptools import setup


def read(file_name):
    try:
        return open(path.join(path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


setup(
    name='Boilerplate-Python',
    version='0.0.0',
    license=read('LICENSE.rst'),
    url='https://github.com/nmvalera/boilerplate-python',
    author='Nicolas Maurice',
    author_email='nicolas.maurice.valera@gmail.com',
    description='Boilerplate-Python is an empty Python project',
    packages=['boilerplate_python'],
    install_requires=[
    ],
    extras_require={
        'dev': [
            'autoflake',
            'autopep8',
            'coverage',
            'flake8',
            'pytest>=3',
            'tox',
            'sphinx',
        ],
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
