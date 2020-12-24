try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

setup(
        name="inlinesas",
        version='0.1.3',
        description="Run SAS code from within a Python script.",
        author="Joe Dougherty",
        author_email="josepd@wharton.upenn.edu",
        url="https://wrds-web.wharton.upenn.edu/wrds/",
        packages=['inlinesas'],
        keywords=['SAS', 'etl'],
        install_requires=['sasrunner>=0.1.2',]
)
