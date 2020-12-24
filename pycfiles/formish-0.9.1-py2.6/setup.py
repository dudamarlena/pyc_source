# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/tests/testish/setup.py
# Compiled at: 2009-01-06 08:44:47
from setuptools import setup, find_packages
version = '0.0'
setup(name='testish', version=version, description='', long_description='', classifiers=[], keywords='', author='', author_email='', url='', license='', packages=find_packages(exclude=['ez_setup', 'examples', 'tests']), include_package_data=True, zip_safe=False, install_requires=[
 'restish'], entry_points='\n      # -*- Entry points: -*-\n      [paste.app_factory]\n      main = testish.wsgiapp:make_app\n      ')