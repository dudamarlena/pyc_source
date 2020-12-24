from distutils.core import setup
setup(
    name = 'sort',
    version = '0.1.0',
    description = 'All variants of sorts',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['sort'],
    entry_points='''
[console_scripts]
sort=sort:cli
''',
)