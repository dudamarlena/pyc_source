from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='biodatagraph',
      version='0.0.6',
      description='Download data from biomedical databases and store in Neo4j.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/kaiserpreusse/biodatagraph',
      author='Martin Preusse',
      author_email='martin.preusse@gmail.com',
      license='Apache License 2.0',
      packages=find_packages(),
      install_requires=[
          'urllib3<1.25,>=1.23', 'py2neo', 'neo4j<4.0', 'pandas', 'xlrd', 'requests', 'ftputil',
          'psycopg2-binary', 'pronto', 'graphio'
      ],
      keywords=['NEO4J', 'Biology'],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License'
      ],
      )
