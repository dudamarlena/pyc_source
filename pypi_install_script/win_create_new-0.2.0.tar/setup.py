#!/usr/bin/env python
# -*-coding:utf-8-*-


from setuptools import setup, find_packages
import win_create_new
import codecs

REQUIREMENTS = []



setup(
    name='win_create_new',
    version=win_create_new.__version__,
    description='create a new file with template in windows.',
    url='https://github.com/a358003542/win_create_new',
    long_description="create a new file with template in windows.",
    author='wanze',
    author_email='a358003542@gmail.com',
    maintainer='wanze',
    maintainer_email='a358003542@gmail.com',
    license='GPL 2',
    platforms='Linux',
    keywords=['skeleton', 'python'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                 'Programming Language :: Python :: 3.6'],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    setup_requires=REQUIREMENTS,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['win_create_new=win_create_new.__main__:main'],
    }
)
