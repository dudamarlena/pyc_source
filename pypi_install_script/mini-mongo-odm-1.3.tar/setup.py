# encoding=utf8

from setuptools import setup

setup(name='mini-mongo-odm',
      version='1.3',
      description='Easy MongoDB Object Document Mapper for Flask',
      url='https://github.com/solo-framework/mini-mongo-odm',
      author='Andrey Filippov',
      author_email='a.fiwork@gmail.com',
      license='MIT',
      packages=['mini_mongo_odm'],
      install_requires=[
          'mongoengine',
          'flask-mongoengine'
      ],
      zip_safe=False)
