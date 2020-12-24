from distutils.core import setup

setup(
    name = 'cldclr',
    version = '0.0.1',
    description = 'A Python package example by samvaran',
    author = 'samvaran kashyap rallabandi',
    author_email = 'samvaran.kashyap@gmail.com',
    url = '', 
    py_modules=['cldclr'],
    install_requires=[
    # list of this package dependencies
    ],
    entry_points='''
                 [console_scripts]
                 cldclr=cldclr:cli
                 ''',
    )
