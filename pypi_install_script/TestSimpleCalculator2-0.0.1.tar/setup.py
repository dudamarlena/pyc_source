from setuptools import setup

setup(
    name = 'TestSimpleCalculator2',
    version = '0.0.1',
    author = 'Etienne Engel',
    packages = ['Package', 'Package/SubPackage'],
    description = '''TestSimpleCalculator is a simple package \
    in order to make some test on packaging principles in Python''',
    license = 'GNU GPLv3',
    python_requires = '>=3.4',
)
