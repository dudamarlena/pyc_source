from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='pycyberfusion',
    version='1.0.1',
    packages=find_packages(),
    install_requires=['requests'],
    url='https://cyberfusion.nl',
    license='MIT',
    author='Cyberfusion <support@cyberfusion.nl>, Yvan Watchman <ywatchman@cyberfusion.nl>, William Edwards <wedwards@cyberfusion.nl>',
    author_email='support@cyberfusion.nl',
    description='Python library for Cyberfusion API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['cyberfusion', 'api'],
    python_requires='>=3.5'
)
