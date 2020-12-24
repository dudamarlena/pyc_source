from distutils.core import setup
setup(
    name = 'relevant',
    version = '0.1.0',
    description = 'Show relevant items',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['relevant'],
    entry_points='''
[console_scripts]
relevant=relevant:cli
''',
)