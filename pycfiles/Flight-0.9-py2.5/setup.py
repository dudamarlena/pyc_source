# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Flight/setup.py
# Compiled at: 2008-06-19 08:09:54
from setuptools import setup, find_packages
setup(name='Flight', version='0.4', packages=find_packages(), author='William Coleman', author_email='weecol@unlimitedmail.org', install_requires=[
 'setuptools', 'pyOpenGL'], package_data={'Flight': [
            '*.py']}, license='PSF', entry_points={'gui_scripts': [
                 'Flight_pilot = Flight.pilot']}, description='This is building towards a flight simulation')