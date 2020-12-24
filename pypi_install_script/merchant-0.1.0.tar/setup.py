from distutils.core import setup
setup(
    name = 'merchant',
    version = '0.1.0',
    description = 'Great package for merchants, for business',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['merchant'],
    entry_points='''
[console_scripts]
merchant=merchant:cli
''',
)