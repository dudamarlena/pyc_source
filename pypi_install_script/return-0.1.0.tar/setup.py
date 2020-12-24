from distutils.core import setup
setup(
    name = 'return',
    version = '0.1.0',
    description = 'The return function in the steroids',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['return'],
    entry_points='''
[console_scripts]
return=return:cli
''',
)