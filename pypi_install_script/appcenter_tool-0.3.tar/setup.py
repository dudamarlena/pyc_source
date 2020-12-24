#!/usr/bin/env python3

from setuptools import setup, find_packages


# Get long description about this python project.
with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setup(
    name='appcenter_tool',
    version='0.3',
    python_requires='>=3.6',
    url='https://bitbucket.org/celadonteam/appcenter-build',
    author='Celadon Developers',
    author_email='opensource@celadon.ae',
    description='Helper to trigger appcenterbuild',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    scripts=['appcenter_tool/__main__.py'],
    entry_points={
        'console_scripts': [
            'appcenter_tool=appcenter_tool.__main__:main',
        ],
    },
    zip_safe=False
)
