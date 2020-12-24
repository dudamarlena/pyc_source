from distutils.core import setup
import setuptools

setup(
  name='mdal',
  packages=setuptools.find_packages(),
  version='0.0.3',
  license='MIT',
  description='Microscopic Data Access Layer for python',
  author='pbount',
  author_email='your.email@domain.com',
  url='https://github.com/pbount/mdal',
  download_url='https://github.com/pbount/mdal/archive/0.0.3§.tar.gz',
  keywords=['Persistence', 'SQL', 'Postgres', 'MySql', 'SQLite'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta", "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
