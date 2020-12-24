"""
Flask-Outdated-Browser
---------------------


Links
`````

* `documentation <https://github.com/ondoheer/flask-outdated-browser>`_
* `development version
  <https://github.com/ondoheer/flask-outdated-browser>`_

"""
from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Flask-outdated-browser',
    version='0.01',
    packages=['flask_outdated_browser'],
    url='https://github.com/ondoheer/flask_outdated_browser',
    license='MIT',
    author='Pedro Baumann',
    author_email='ondoheer@gmail.com',
    description='Easily add outdated-browser project to your Flask project',
    long_description=read('README.rst'),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.8'
    ],
    classifiers=[

        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
