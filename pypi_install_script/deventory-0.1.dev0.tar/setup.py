# -*- coding: utf-8 -*-


"""Deventory setup module"""

from setuptools import setup

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '0.1dev0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'garaje@glezseoane.es'
__status__ = 'Development'


setup(
    name='deventory',
    version='0.1dev0',
    packages=['deventory'],
    entry_points={
        'console_scripts': [
            'deventory=deventory.__main__:main',
        ],
    },
    python_requires='>=3',
    url='https://github.com/glezseoane/deventory',
    download_url='https://github.com/glezseoane/deventory/archive/v'
                 '0.1dev0.tar.gz',
    license='LICENSE',
    author='Borja González Seoane',
    author_email='garaje@glezseoane.es',
    description='The development project inventory manager',
    long_description='The purpose of this tool is to become a local project '
                     'manager that automates certain processes and '
                     'facilitates the control of all the archived '
                     'repositories, respecting the idiosyncrasies of each '
                     'developer with storing preferences.',
    data_files=[("", ["LICENSE"])],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
        'Topic :: Software Development'
    ],
)
