from setuptools import setup, find_packages

setup(
    name='dict_to_obj',
    version='0.0.2',
    packages=find_packages(exclude=['tests*']),
    description='Convert nested Python dict to object',
    long_description='''
    Convert nested Python dict to object
    https://github.com/alon710/DictToObj''',
    install_requires=[],
    url='https://github.com/alon710/DictToObj',
    author='Alon Barad',
    author_email='Alon710@gmail.com'
)
