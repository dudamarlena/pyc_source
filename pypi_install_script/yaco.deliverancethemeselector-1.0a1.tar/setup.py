from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='yaco.deliverancethemeselector',
      version=version,
      description="Deliveranece theme selector",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Juan A. Diaz [nueces]',
      author_email='jdiaz@menttes.com',
      url='https://svn.plone.org/svn/collective/yaco.deliverancethemeselector',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['yaco'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
