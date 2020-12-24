import os
from setuptools import setup, find_packages
version = open('VERSION.txt').read().strip()


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = read('README.rst') + '\n'

setup(name='buildout.recipe.download',
      version=version,
      description="Download with multiple threads",
      classifiers=[

          'Development Status :: 3 - Alpha',
          'Environment :: Plugins',
          'Intended Audience :: System Administrators',
          'Framework :: Buildout',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'License :: Other/Proprietary License',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='development buildout recipe',
      author='Jagadeesh N Malakannavar',
      author_email='mnjagadeesh@gmail.com',
      license='BSD 3',
      long_description=long_description,
      packages=find_packages('src'),
      package_dir={"": "src"},
      namespace_packages=['buildout', 'buildout.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['zc.buildout', 'setuptools', 'ConfigParser'],
      entry_points={"zc.buildout": [
          "default=buildout.recipe.download:Download_eggs"]},
      )
