from distutils.core import setup
setup(
    name = 'give',
    version = '0.1.0',
    description = 'A Python package - give',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['give'],
    entry_points='''
        [console_scripts]
        give=give:cli
    ''',
)
