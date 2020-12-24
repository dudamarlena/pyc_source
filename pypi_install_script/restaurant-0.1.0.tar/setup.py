from distutils.core import setup
setup(
    name = 'restaurant',
    version = '0.1.0',
    description = 'Restaurant in CLI, change your control of it',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['restaurant'],
    entry_points='''
[console_scripts]
restaurant=restaurant:cli
''',
)