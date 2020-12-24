from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2b'
name='betahaus.openmember'

long_description = (
    read('docs','README.rst')
    + '\n' +
    'Change history\n'
    '==============\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Known Issues\n'
    '============\n'
    + '\n' +
    read('KNOWN_ISSUES.txt')

    )

setup(name=name,
      version=version,
      description="A member database to track membership over time",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone',
      author='Betahaus',
      author_email='robin@betahaus.net',
      url='http://www.betahaus.net',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['betahaus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
