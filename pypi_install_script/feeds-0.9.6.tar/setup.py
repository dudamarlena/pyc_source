import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from feeds import __version__

setup(
    name = 'feeds',
    version = __version__,
    packages = ['feeds'],
    include_package_data = True,
    license = 'BSD License', # example license
    description = 'A feedburner replacement built on Django.',
    long_description = README,
    url = 'https://angry-planet.com/feeds',
    author = 'Andreas.Neumeier',
    author_email = 'andreas@neumeier.org',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
