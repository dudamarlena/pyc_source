from distutils.core import setup

setup(
    name = 'gummybears',
    version = '0.0.3',
    description = 'A Python package example by samvaran',
    author = 'samvaran kashyap rallabandi',
    author_email = 'samvaran.kashyap@gmail.com',
    url = '', 
    py_modules=['gummybears'],
    install_requires=[
    # list of this package dependencies
    ],
    entry_points='''
                 [console_scripts]
                 gummybears=gummybears:cli
                 ''',
    )
