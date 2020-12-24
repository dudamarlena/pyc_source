from setuptools import setup, find_packages
import os

version = '2.1.0'

setup(name='wildcard.cloudflare',
      version=version,
      description="",
      long_description="%s\n%s" % (
          open("README.rst").read(),
          open(os.path.join("docs", "HISTORY.txt")).read()),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone',
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.2",
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='plone caching purging cloudflare',
      author='Nathan Van Gheem',
      author_email='nathan@vangheem.us',
      url='https://github.com/collective/wildcard.cloudflare',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['wildcard'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.caching',
          'requests'
      ],
      extras_require={
          'test': ['plone.app.testing']
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """
      )
