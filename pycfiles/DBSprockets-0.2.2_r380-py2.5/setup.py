# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/dbmechanic/frameworks/tg2/test/TG2TestApp/setup.py
# Compiled at: 2008-06-30 11:43:47
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='TG2TestApp', version='', install_requires=[
 'TurboGears2'], packages=find_packages(exclude=['ez_setup']), include_package_data=True, test_suite='nose.collector', package_data={'tg2testapp': ['i18n/*/LC_MESSAGES/*.mo',
                'templates/*/*',
                'public/*/*']}, entry_points='\n    [paste.app_factory]\n    main = tg2testapp.config.middleware:make_app\n\n    [paste.app_install]\n    main = pylons.util:PylonsInstaller\n    ')