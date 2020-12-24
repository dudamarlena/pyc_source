from distutils.core import setup
setup(
    name = 'client',
    version = '0.0.1',
    description = 'A Python package - client',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['client'],
    entry_points='''
        [console_scripts]
        client=client:cli
    ''',
)
