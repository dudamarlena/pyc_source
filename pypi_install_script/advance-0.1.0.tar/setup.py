from distutils.core import setup
setup(
    name = 'advance',
    version = '0.1.0',
    description = 'Get advandes for good programming',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['advance'],
    entry_points='''
[console_scripts]
advance=advance:cli
''',
)