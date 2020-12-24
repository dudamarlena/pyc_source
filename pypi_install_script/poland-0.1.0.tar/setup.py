from distutils.core import setup
setup(
    name = 'poland',
    version = '0.1.0',
    description = 'Poland statistics in the CLI',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['poland'],
    entry_points='''
[console_scripts]
poland=poland:cli
''',
)