from distutils.core import setup
setup(
    name = 'wife',
    version = '0.1.0',
    description = 'Control your wife. ;)',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['wife'],
    entry_points='''
[console_scripts]
wife=wife:cli
''',
)