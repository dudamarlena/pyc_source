from distutils.core import setup
setup(
    name = 'legend',
    version = '0.1.0',
    description = 'Work with legends in plots from matplotlib',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['legend'],
    entry_points='''
[console_scripts]
legend=legend:cli
''',
)