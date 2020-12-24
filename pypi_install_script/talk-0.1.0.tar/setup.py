from distutils.core import setup
setup(
    name = 'talk',
    version = '0.1.0',
    description = 'Chat platform writen in Python',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['talk'],
    entry_points='''
[console_scripts]
talk=talk:cli
''',
)