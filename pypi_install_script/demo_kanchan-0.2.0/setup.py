from distutils.core import setup

setup(
    name = 'demo_kanchan',
    version = '0.1.0',
    description = 'A Python package example',
    author = 'Kanchan',
    author_email = 'kbartwal94@gmail.com',
    url = 'https://github.com',
    py_modules=['test'],
    install_requires=[
        # list of this package dependencies
    ],
    entry_points='''
        [console_scripts]
        demo=demo:code
    ''',
)