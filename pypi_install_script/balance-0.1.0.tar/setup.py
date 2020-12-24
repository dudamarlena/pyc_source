from distutils.core import setup
setup(
    name = 'balance',
    version = '0.1.0',
    description = 'Check you balances anywhere',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['balance'],
    entry_points='''
[console_scripts]
balance=balance:cli
''',
)