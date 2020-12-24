from distutils.core import setup

setup(
    name='puffin-python-library',
    version='0.1.1',
    packages=['puffin'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    url='https://gitlab.com/nickgray1995/puffin-python-library',
    author='Nick Gray',
    author_email = 'nickgray@liv.ac.uk',
    install_requires=['pba>=0.3.4','numpy','antlr4-python3-runtime>=4.7.2','click>=7.0','mpmath','pyqt5'],

)
# RUN THIS CODE
'''
python3 setup.py sdist
python3 -m twine upload dist/*
'''
