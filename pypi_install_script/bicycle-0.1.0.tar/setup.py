from distutils.core import setup
setup(
    name = 'bicycle',
    version = '0.1.0',
    description = 'Methods and classes for men who ride many time on the bikes',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['bicycle'],
    entry_points='''
[console_scripts]
bicycle=bicycle:cli
''',
)