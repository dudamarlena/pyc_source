# -*- coding: UTF-8 -*-
from distutils.core import setup
setup(
    name = 'marmotas',
    packages = ['marmotas'], # this must be the same as the name above
    version = '0.1',
    description = 'Para hacerme la vida mas simple 👍',
    author = 'Franco Díaz',
    author_email = 'fraediaz@icloud.com',
    url = 'https://github.com/fraediaz/marmotas',
    download_url = 'https://github.com/fraediaz/marmotas/',
    license="GPLv3+",
    py_modules=['marmotas'],
    install_requires=[
        'termcolor',  
    ],
    entry_points='''
        [console_scripts]
        marmotas=marmotas:main
    ''',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    )
)