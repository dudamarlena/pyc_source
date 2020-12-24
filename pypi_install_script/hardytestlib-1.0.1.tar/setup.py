from setuptools import setup

with open(file=r'README.md', encoding='utf-8') as fd:
    desc = fd.read()


setup(
    name='hardytestlib',
    version='1.0.1',
    description='this is a very niubi lib',
    packages=['hardy_lib'],
    py_modules=['my_module'],
    author='hardy9sap',
    author_email='hardy9sap@163.com',
    long_description=desc,
    url='https://github.com/hardy9sap',
    license='MIT'
)
