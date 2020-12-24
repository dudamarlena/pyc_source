import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='flipfloperator',
    version='0.1.2',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    description='Sorry.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['flipfloperator'],
)
