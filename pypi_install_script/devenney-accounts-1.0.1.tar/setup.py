from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
  name='devenney-accounts',
  version='1.0.1',
  description='Elegant Django account management',
  long_description=readme(),
  author='Brendan Devenney',
  author_email='brendan@devenney.io',
  packages=['devenney.accounts'],
  package_dir = {
    'devenney.accounts': './accounts'
  },
  package_data={'devenney.accounts':['templates/*/*.html','templates/*/*/*.html']},
  url='https://github.com/devenney/django_accounts',
  license='MIT',
  install_requires=[
    "Django >= 2.0"
  ],
)
