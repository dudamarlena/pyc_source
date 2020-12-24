from distutils.core import setup
setup(
    name = 'assert',
    version = '0.1.0',
    description = 'Assert methods for Python',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['assert'],
    entry_points='''
[console_scripts]
assert=assert:cli
''',
)