from distutils.core import setup
setup(
    name = 'weapon',
    version = '0.1.0',
    description = 'This package contains weapons..',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['weapon'],
    entry_points='''
[console_scripts]
weapon=weapon:cli
''',
)