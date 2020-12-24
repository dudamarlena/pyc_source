from distutils.core import setup
setup(
    name = 'hold',
    version = '0.1.0',
    description = 'Hold methods for effective works',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['hold'],
    entry_points='''
[console_scripts]
hold=hold:cli
''',
)