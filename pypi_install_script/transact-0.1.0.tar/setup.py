
from distutils.core import setup

setup(
    name = 'transact',
    version = '0.1.0',
    description = 'A Python package - transact',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com', 
    py_modules=['transact'],
    entry_points='''
        [console_scripts]
        transact=transact:cli
    ''',
)
