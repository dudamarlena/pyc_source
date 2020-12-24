#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, Command
from pip._internal.req import parse_requirements
import os

install_reqs = parse_requirements('requirements.txt', session='hack')
requires = [str(ir.req) for ir in install_reqs]


class PublishCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -rf dist/')
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')


setup(
    name='lamblackbox',
    description='This is a AWS Lambda function logging library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    use_scm_version=True,
    url='https://github.com/youyo/lamblackbox',
    author='youyo',
    author_email='1003ni2@gmail.com',
    install_requires=requires,
    license="MIT License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='aws lambda log logger logging',
    packages=['lamblackbox'],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/youyo/lamblackbox',
    },
    cmdclass={'publish': PublishCommand},
)
