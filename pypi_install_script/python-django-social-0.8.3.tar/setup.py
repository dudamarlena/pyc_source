import os
from setuptools import setup
from social import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='python-django-social',
    version=__version__,
    packages=['social'],
    include_package_data=True,
    license='BSD License',    # example license
    description='Social scoring of URLs.',
    long_description=README,
    author='Andreas.Neumeier',
    author_email='andreas@neumeier.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',    # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'requests>=2.6',
    ],
)
