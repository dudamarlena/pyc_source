import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='mkstool',
    version='1.0.3',
    description='mkstool API',
    long_description=README,
    long_description_content_type="text/markdown",
    author='atosystem',
    author_email='atosystem@hotmail.com',
    url='https://github.com/atosystem/mkstool',
    keywords=['makerspace', 'API'],
    entry_points={'console_scripts': 
        ['mkstool = mkstool.__main__:main']
    },
    install_requires=[
        # Restriction that urllib3's version is less than 1.25 needed to avoid
        # requests dependency problem.
        'urllib3 >= 1.21.1, < 1.25',
        'requests',
        'Click',
        'tabulate'
    ],
    packages=find_packages(),
    license="MIT")