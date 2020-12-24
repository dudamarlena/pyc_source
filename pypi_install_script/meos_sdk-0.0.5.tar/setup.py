# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path, environ


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


here = path.abspath(path.dirname(__file__))
install_reqs = parse_requirements('requirements.txt')

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


if environ.get('CI_COMMIT_TAG'):
    version = environ['CI_COMMIT_TAG']
elif environ.get('CI_JOB_ID'):
    version = environ['CI_JOB_ID']
else:
    version = 'dev'


setup(
    name='meos_sdk',  # Required
    version=version,  # Required
    description='Interact with the meos personal cloud environment',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='>=3.5, <4',
    install_requires=install_reqs,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'meos_sdk = meos_sdk.cli:meos_sdk',
        ],
    },
)
