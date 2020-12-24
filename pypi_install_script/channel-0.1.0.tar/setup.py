from distutils.core import setup
setup(
    name = 'channel',
    version = '0.1.0',
    description = 'My AMQP service',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['channel'],
    entry_points='''
[console_scripts]
channel=channel:cli
''',
)