
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='obsh',
    version='3',
    url='https://github.com/bthate/obsh',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OBSH contains shell programs for the OB package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Public Domain',
    install_requires=["ob", "obot"],
    zip_safe=True,
    packages=["obsh"],
    scripts=["bin/ob", "bin/obot", "bin/obs", "bin/obd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
