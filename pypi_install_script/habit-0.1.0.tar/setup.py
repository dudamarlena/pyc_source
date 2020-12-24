from distutils.core import setup
setup(
    name = 'habit',
    version = '0.1.0',
    description = 'Work with site visitor habits, detect bots and etc',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['habit'],
    entry_points='''
[console_scripts]
habit=habit:cli
''',
)