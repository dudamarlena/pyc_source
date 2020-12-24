import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mvm',
    version='0.1.1',
    author='Sean Drzewiecki',
    author_email='sean@drzewiecki.io',
    packages=['mvm'],
    url='http://pypi.python.org/pypi/mvm/',
    license='LICENSE',
    description='Minecraft Version Manager',
    long_description=long_description,
    install_requires=[
        'Click',
        'requests'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['mvm=mvm.__main__:main']
    }
)
