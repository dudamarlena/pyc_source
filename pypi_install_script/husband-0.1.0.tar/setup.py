from distutils.core import setup
setup(
    name = 'husband',
    version = '0.1.0',
    description = 'Great package for husbands',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['husband'],
    entry_points='''
[console_scripts]
husband=husband:cli
''',
)