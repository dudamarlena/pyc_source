from distutils.core import setup
setup(
    name = 'louisiana',
    version = '0.1.0',
    description = 'Louisiana statistics in the CLI',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['louisiana'],
    entry_points='''
[console_scripts]
louisiana=louisiana:cli
''',
)