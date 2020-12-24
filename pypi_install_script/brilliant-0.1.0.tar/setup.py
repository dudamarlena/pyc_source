from distutils.core import setup
setup(
    name = 'brilliant',
    version = '0.1.0',
    description = 'Brilliant package',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['brilliant'],
    entry_points='''
[console_scripts]
brilliant=brilliant:cli
''',
)