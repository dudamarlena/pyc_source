#!/usr/bin/env python3

from setuptools import find_packages, setup


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('test-requirements.txt') as requirements:
    test_required = requirements.read().splitlines()

with open("README.rst") as readme:
    long_description = readme.read()


if __name__ == "__main__":
    setup(name='bear_installation_tool',
          version='0.0.5',
          description='Installation tool for coala-bears',
          author="Adrian Zatreanu",
          maintainer="Adrian Zatreanu",
          maintainer_email='adrianzatreanu1@gmail.com',
          platforms='any',
          packages=find_packages(exclude=["build.*", "tests", "tests.*"]),
          install_requires=required,
          tests_require=test_required,
          license="AGPL-3.0",
          long_description=long_description,
          entry_points={
              "console_scripts": [
                  "coala-install = bear_installation_tool.installation_tool:main"]},
          classifiers=[
              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications :: Gnome',

              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',

              'License :: OSI Approved :: GNU Affero General Public License '
              'v3 or later (AGPLv3+)',

              'Operating System :: OS Independent',

              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3 :: Only',

              'Topic :: Scientific/Engineering :: Information Analysis',
              'Topic :: Software Development :: Quality Assurance',
              'Topic :: Text Processing :: Linguistic'])
