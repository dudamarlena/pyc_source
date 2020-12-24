from os import path
from subprocess import check_output

from setuptools import setup, find_packages

git_version_command = 'git describe --tags --long --dirty'
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if path.exists(here + "/.git"):
    init_file = None
    with open(path.join(here, 'jivago_streams/__init__.py'), 'r', encoding='utf-8') as f:
        init_file = f.read()
    if "@@VERSION@@" in init_file:
        with open(path.join(here, 'jivago_streams/__init__.py'), 'w', encoding='utf-8') as f:
            f.write(init_file.replace("@@VERSION@@",
                                      check_output(git_version_command.split()).decode('utf-8').strip().split("-")[0]))

setup(
    name='jivago-streams',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    description='Chainable functional-style operations for Python3.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/jivago-python/jivago-streams',

    author='Kento A. Lauzon',
    author_email='kento.lauzon@ligature.ca',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(
        exclude=['tests', 'tests.*']),

    install_requires=[],
)
