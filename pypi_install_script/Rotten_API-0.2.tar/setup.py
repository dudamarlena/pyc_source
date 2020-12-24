from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Rotten_API',
    version='0.2',
    packages=['RottenPy'],
    url='https://github.com/chyvn/Rotten_API',
    license='MIT',
    author='Avinash Tulasi',
    author_email='avinasht@iiitd.ac.in',
    description='Rotten Tomatoes API',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
