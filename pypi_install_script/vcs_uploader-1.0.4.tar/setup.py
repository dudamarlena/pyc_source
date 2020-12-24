#!/usr/bin/env python3

from setuptools import setup

from vcs_uploader import consts

setup(
    name=consts.name,
    version=consts.version,
    author=consts.author,
    author_email=consts.author_email,
    url='https://github.com/gen-iot/vcs-uploader',
    description=consts.description,
    license='MIT License',
    packages=[consts.name],
    platforms=['all'],
    python_requires='>=3.4',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    classifiers=['Programming Language :: Python :: 3.0',
                 'Topic :: Software Development :: Code Generators',
                 'Operating System :: OS Independent'],
    install_requires=[
        'requests>=2.22.0'
    ],
    entry_points={
        'console_scripts': [
            'vcsup = vcs_uploader.__main__:main '
        ]
    }

)
