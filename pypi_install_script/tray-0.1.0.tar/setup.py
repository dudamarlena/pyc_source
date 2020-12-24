from distutils.core import setup
setup(
    name = 'tray',
    version = '0.1.0',
    description = 'A Python package - tray',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['tray'],
    entry_points='''
        [console_scripts]
        tray=tray:cli
    ''',
)
