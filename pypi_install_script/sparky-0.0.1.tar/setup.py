#!/usr/bin/env python
from setuptools import setup
import sparky

setup(
    name="sparky",
    version=sparky.__version__,
    url='https://github.com/citylive/sparky',
    license='BSD',
    description="Sparky Translation server",
    long_description=open('README.md', 'r').read(),
    author='Ingo Berben, VikingCo NV',
    author_email='ingo.berben@mobilevikings.com',
    packages=['sparky'],
    package_data={'sparky': [
        'static/*.js', 'static/*/*.js', 'static/*/*/*.js',
        'static/*.css', 'static/*/*.css', 'static/*/*/*.css',
        'static/*.png', 'static/*/*.png', 'static/*/*/*.png', 'static/*/*/*/*.png',
        'static/*.scss', 'static/*/*.scss', 'static/*/*/*.scss', 'static/*/*/*/*.scss',
        'templates/*.html', 'templates/*/*.html', 'templates/*/*/*.html', 'templates/*/*/*/*.html'
    ]},
    zip_safe=False,  # Don't create egg files, Django cannot find templates in egg files.
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Operating System :: Unix',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Localization',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Text Processing :: Linguistic'
    ],
)
