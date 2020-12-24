import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='turkish-suffix-library',
    version='0.2.0',
    packages=['tr_suffix'],
    include_package_data=False,
    license='BSD License',  # example license
    description='Turkish Suffix Library is a function for you to make suffixes according the Turkish grammatic rulues.',
    long_description=README,
    author='Cem YILDIZ',
    author_email='cem.yildiz@ya.ru',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)