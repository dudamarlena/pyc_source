from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import find_packages, setup

pfile = Project(chdir=False).parsed_pipfile

setup(
    name='avantage',
    version='0.1.0',
    url='https://github.com/decached/avantage',
    author='Akash Kothawale',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=convert_deps_to_pip(pfile['packages'], r=False),
    tests_require=convert_deps_to_pip(pfile['dev-packages'], r=False),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
