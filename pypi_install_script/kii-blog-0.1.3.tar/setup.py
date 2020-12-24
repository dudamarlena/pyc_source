import os
from setuptools import setup, find_packages
import kii_blog as package

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='kii-blog',
    version=package.__version__,
    packages=find_packages(),
    include_package_data=True,
    license='BSD',  # example license
    description='Kii Blog',
    long_description=README,
    author='Eliot Berriot',
    author_email='contact@eliotberriot.com',
    install_requires=[
        'kii',
    ],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)