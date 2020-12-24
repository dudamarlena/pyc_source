from distutils.core import setup
setup(
    name = 'beef',
    version = '0.1.0',
    description = 'Beef consumption statistic by Suroegin',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['beef'],
    entry_points='''
[console_scripts]
beef=beef:cli
''',
)