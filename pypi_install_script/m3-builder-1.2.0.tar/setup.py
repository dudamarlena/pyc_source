# coding: utf-8
from setuptools import find_packages
from setuptools import setup


setup(
    name='m3-builder',
    author="BARS Group",
    author_email='bars@bars-open.ru',
    description='Сборщик пакетов',
    url='https://stash.bars-open.ru/projects/EDUBASE/repos/utils',
    version="1.2.0",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=(
        'six',
    ),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
    ],
    entry_points={
        'distutils.setup_keywords': [
            'set_build_info = m3_builder:set_build_info',
        ],
    },
)
