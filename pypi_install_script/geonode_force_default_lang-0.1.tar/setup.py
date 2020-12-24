from setuptools import setup

setup(name='geonode_force_default_lang',
      version='0.1',
      description='Overwrite browser HTTP_ACCEPT_LANGUAGE. Code taken from geonode docs.',
      url='http://docs.geonode.org/en/master/tutorials/admin/default_lang/',
      author='toni.schoenbuchner',
      author_email='toni.schoenbuchner@gmail.com',
      license='MIT',
      packages=['geonode_force_default_lang'],
      zip_safe=False)