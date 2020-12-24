from setuptools import setup
import os

# Read in README.md for the long description
def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='simplenotifications',
    version='0.2.18',
    description='Cross-platform desktop notifications',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='desktop notifications',
    url='https://github.com/0Gitnick/simplenotifications',
    author='0Gitnick',
    author_email='36289298+0Gitnick@users.noreply.github.com',
    license='GPLv3-or-later',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python'
    ],
    install_requires=[
        'win10toast==0.9 ; platform_system=="Windows"'
    ],
    packages=['simplenotifications'],
    scripts=['bin/notify'],
    test_suite='simplenotifications',
    include_package_data=True,
    zip_safe=False)
