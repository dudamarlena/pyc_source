from distutils.core import setup
setup(
    name = 'theme',
    version = '0.1.0',
    description = 'Themes for popular web-frameworks',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['theme'],
    entry_points='''
[console_scripts]
theme=theme:cli
''',
)