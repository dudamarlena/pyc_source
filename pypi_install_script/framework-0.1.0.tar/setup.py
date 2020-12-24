from distutils.core import setup
setup(
    name = 'framework',
    version = '0.1.0',
    description = 'The one framework of all frameworks',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['framework'],
    entry_points='''
[console_scripts]
framework=framework:cli
''',
)