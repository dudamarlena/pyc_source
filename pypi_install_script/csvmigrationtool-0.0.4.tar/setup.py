from setuptools import setup

setup(name='csvmigrationtool',
      version='0.0.4',
      author='Tong Wang',
      author_email='wangtong4348@gmail.com',
      license='MIT',
      packages=['csvmigrationtool'],
      install_requires=['atlassian-python-api','PyYAML'],
      zip_safe=False)