from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pituo',
    packages=['pituo'],
    version='0.0.2',
    license='MIT',
    description='Go-styled errors in Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ruyi Li',
    author_email='ruyili2002@gmail.com',
    url='https://github.com/RuyiLi/pituo',
    keywords=['go', 'error', 'exception'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
)
