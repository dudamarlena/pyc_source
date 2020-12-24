'Just increment the number and create a new lib. Never fix the original one.'
from distutils.core import setup
setup(name='urllib5', version='5.0.0', author='Thomas Perl <m@thp.io>',
        description=__doc__, py_modules=['urllib5'])
