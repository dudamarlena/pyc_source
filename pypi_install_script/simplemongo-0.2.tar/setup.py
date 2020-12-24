from setuptools import setup

setup(name='simplemongo',
      version='0.2',
      description='Super simple ORM wrapper for MongoDB',
      url='http://github.com/stevenewey/simplemongo',
      author='Stephen Newey',
      author_email='python@s-n.me',
      license='Apache2',
      packages=['simplemongo'],
      install_requires=[
          'pymongo',
      ],
      zip_safe=False)
