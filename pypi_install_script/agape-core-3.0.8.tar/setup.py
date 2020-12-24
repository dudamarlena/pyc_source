import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()



# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='agape-core',
    version='3.0.8',
    packages=['agape'],
    include_package_data=True,
    license='All rights reserved.', 
    description='Agape Core libraries for application development.',
    long_description=README,
    long_description_content_type='text/markdown',
    url = 'https://gitlab.com/maverik.software/agape-django',
    author='Maverik Apollo Minett',
    author_email='maverik.apollo.minett@gmail.com',
    test_suite = "runtests.runtests",
    install_requires = [
        'Django>=2.2.9',
        'django-cors-headers>=2.5.3',
        'django-filter>=2.2.0',
        'djangorestframework>=3.11.0',
        'djangorestframework-jwt>=1.11.0',
        'simplejson>=0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
