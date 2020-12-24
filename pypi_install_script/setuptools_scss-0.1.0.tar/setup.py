from setuptools import setup

import setuptools_scss


def main():
    setup(name='setuptools_scss',
          version=setuptools_scss.__version__,
          description='Plugin for setuptools to build and compile SCSS files',
          long_description=open('README.md').read(),
          author='Tomas Pazderka',
          author_email='tomas.pazderka@nic.cz',
          url='https://github.com/CZ-NIC/setuptools_scss',
          py_modules=['setuptools_scss'],
          entry_points={
              "distutils.commands": [
                  "build_scss = setuptools_scss:build_scss",
              ],
              "distutils.setup_keywords": [
                  "scss_files = setuptools_scss:validate_scss",
              ],
          },
          license='GPLv3',
          classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'Topic :: Software Development :: Build Tools',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
          ],
          )


if __name__ == '__main__':
    main()
