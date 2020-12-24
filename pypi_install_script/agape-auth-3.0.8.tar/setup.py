import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='agape-auth',
    version='3.0.8',
    packages=['agape.auth'],
    include_package_data=True,
    license='MIT License', 
    description='Agape Authentication library.',
    long_description_content_type='text/markdown',
    long_description=README,
    url = 'https://gitlab.com/maverik.software/agape',
    author='Jeffrey Hallock',
    author_email='maverik.software@gmail.com',
    test_suite = "runtests.runtests",
    install_requires = [
        'Django>=2.0.0',
        'django-cors-headers>=2.1.0',
        'django-filter>=1.1.0',
        'djangorestframework>=3.6.4',
        'djangorestframework-jwt>=1.11.0',
        'agape-core>=2.0.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
