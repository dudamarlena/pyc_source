from distutils.core import setup
setup(
    name = 'drug',
    version = '0.1.0',
    description = 'Drug is a name of package in russian, mean as Friend',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['drug'],
    entry_points='''
[console_scripts]
drug=drug:cli
''',
)