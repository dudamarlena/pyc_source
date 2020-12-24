from distutils.core import setup
setup(
    name = 'welcome',
    version = '0.0.1',
    description = 'A Python package - welcome',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['welcome'],
    entry_points='''
        [console_scripts]
        welcome=welcome:cli
    ''',
)
