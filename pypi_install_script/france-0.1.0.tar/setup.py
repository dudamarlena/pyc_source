from distutils.core import setup
setup(
    name = 'france',
    version = '0.1.0',
    description = 'France statistics in the CLI',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['france'],
    entry_points='''
[console_scripts]
france=france:cli
''',
)