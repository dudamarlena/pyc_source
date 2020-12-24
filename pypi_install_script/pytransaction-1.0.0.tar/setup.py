from setuptools import setup

with open('README.md') as f:
    long_description = f.read().strip()


setup(
    name='pytransaction',
    description='run revert functions when exception occurs in context',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    version='1.0.0',
    author='thuhak',
    author_email='thuhak.zhou@nio.com',
    keywords='transaction',
    packages =['pytransaction'],
    url='https://github.com/thuhak/pytransaction.git',
    install_requires=[]
)
