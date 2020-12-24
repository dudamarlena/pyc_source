from distutils.core import setup

setup(
    name='rbk',
    version='0.1',
    packages=['mysql'],
    url='https://richardkeller.net',
    description='MySQL class wrapper for PyMySQL',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    install_requires=[
        'PyMySQL >= 0.7.11'
    ]
)
