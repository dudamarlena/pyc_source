from distutils.core import setup
setup(
    name = 'coffee',
    version = '0.1.0',
    description = 'A Python package - coffee',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['coffee'],
    entry_points='''
        [console_scripts]
        coffee=coffee:cli
    ''',
)
