from setuptools import setup, find_packages
from distutils.util import convert_path

def get_version():
    filepath = convert_path('enconf/version.py')
    namespace = {}
    with open(filepath) as version_file:
        exec(version_file.read(), namespace)

    return namespace['__version__']

setup(
    name='enconf',
    version=get_version(),
    description='Easy config setup from the environment',
    url='https://github.com/danielunderwood/enconf',
    author='Daniel Underwood',
    license='MIT',

    packages=find_packages(),

    extras_require={
        'test': ['pytest']
    },
)