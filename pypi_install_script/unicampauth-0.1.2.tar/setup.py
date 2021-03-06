import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='unicampauth',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description="A simple Django app to manage auth for unicamp students",
    long_description=README,
    author='Gustavo Maronato',
    author_email='gustavomaronato@gmail.com',
    install_requires=[
        'google-api-python-client==1.6.7'
    ],
    url='https://github.com/VotaUnicamp/UnicampAuth',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
