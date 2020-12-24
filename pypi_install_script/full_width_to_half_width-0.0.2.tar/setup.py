"""
Convert full width UTF-8 characters to half width
Author: SF-Zhou
Date: 2018-08-28
"""

from setuptools import setup


name = 'full_width_to_half_width'
setup(
    name=name,
    version='0.0.2',
    description='Convert full width UTF-8 characters to half width',
    url=f'https://github.com/SF-Zhou/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='full width half utf-8',
    entry_points={
        'console_scripts': [f'{name}={name}:main'],
    },
    py_modules=[f'{name}']
)
