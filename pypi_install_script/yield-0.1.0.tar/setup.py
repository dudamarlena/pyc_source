from distutils.core import setup
setup(
    name = 'yield',
    version = '0.1.0',
    description = 'A Python package - yield',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['yield'],
    entry_points='''
        [console_scripts]
        yield=yield:cli
    ''',
)
