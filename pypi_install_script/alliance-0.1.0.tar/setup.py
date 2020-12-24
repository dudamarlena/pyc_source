from distutils.core import setup
setup(
    name = 'alliance',
    version = '0.1.0',
    description = 'Alliance package for unite modules and packages',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['alliance'],
    entry_points='''
[console_scripts]
alliance=alliance:cli
''',
)