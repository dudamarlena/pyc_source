import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py check -r -s', 'setup.py sdist']):
    raise ImportError('Placeholder for pipeformer')

setup(
    author='Amazon Web Services',
    author_email='aws-cryptools@amazon.com',
    classifiers=['Development Status :: 7 - Inactive'],
    description='Placeholder for pipeformer',
    long_description='\nThis is a placeholder to hold the pypi name for pipeformer.\nhttps://github.com/awslabs/pipeformer',
    name='pipeformer',
    url='https://github.com/awslabs/pipeformer',
    version='0.0.2'
)
