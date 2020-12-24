from distutils.core import setup
setup(
    name = 'lieutenant',
    version = '0.1.0',
    description = 'Leutenant package',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['lieutenant'],
    entry_points='''
[console_scripts]
lieutenant=lieutenant:cli
''',
)