# -*- encoding: utf-8 -*-
"""
Python setup file for the asyncmailer app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
asyncmailer/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
import os
from setuptools import setup, find_packages
import asyncmailer as app


dev_requires = [
    'flake8',
]


def fetch_dependencies(file_name):
    deps = []
    for line in open(file_name).read().splitlines():
        if line.startswith("-r "):
            deps.append(fetch_dependencies(line[3:]))
        else:
            deps.append(line)
    return deps

install_requires = fetch_dependencies('requirements.txt')


def read(fname):
    try:
        print('read:{}'.format(fname))
        path = os.path.join(os.path.dirname(__file__), fname)
        return open(path, 'r').read()
    except IOError as e:
        print('read {} error.'.format(path))
        print(e)
        return ''

setup(
    name="django2-asyncmailer",
    version='0.0.4',
    description=read('DESCRIPTION'),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, async, email',
    author='Dong',
    author_email='choubaodxs@163.com',
    url="https://github.com/ChouBaoDxs/django2-asyncmailer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
)
