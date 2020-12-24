from distutils.core import setup
setup(
    name = 'soup',
    version = '0.1.0',
    description = 'A Python package - soup',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['soup'],
    entry_points='''
        [console_scripts]
        soup=soup:cli
    ''',
)
