
from distutils.core import setup

setup(
    name = 'small',
    version = '0.1.0',
    description = 'A Python package - small',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com', 
    py_modules=['small'],
    entry_points='''
        [console_scripts]
        small=small:cli
    ''',
)
