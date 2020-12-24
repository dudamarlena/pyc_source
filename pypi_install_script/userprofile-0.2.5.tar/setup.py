import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from userprofile import __version__

setup(
    name='userprofile',
    version=__version__,
    packages=['userprofile'],
    include_package_data=True,
    license='MIT License',    # example license
    description='A packaged user application, leveraging python-social-auth.',
    long_description=README,
    url='https://angry-planet.com/user',
    author='Andreas.Neumeier',
    author_email='andreas@neumeier.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=1.9.0',
        'django-crispy-forms>=1.5.2',
        'python-social-auth>=0.2.2',
        'pyyaml',
    ],
)
