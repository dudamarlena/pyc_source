import os
from setuptools import setup, find_packages
import wxr_parser as package

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='wxr-parser',
    version=package.__version__,
    packages=find_packages(),
    include_package_data=True,
    license='BSD',  # example license
    description='A simple Worpdress eXtended RSS (WXR) parser',
    long_description=README,
    author='Eliot Berriot',
    author_email='contact@eliotberriot.com',
    url='https://code.eliotberriot.com/eliotberriot/wxr-parser',
    zip_safe=False,
    install_requires=[
        'lxml',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)