from distutils.core import setup
setup(
    name = 'portland',
    version = '0.1.0',
    description = 'Portland statistics in the CLI',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['portland'],
    entry_points='''
[console_scripts]
portland=portland:cli
''',
)