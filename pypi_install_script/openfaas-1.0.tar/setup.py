from setuptools import setup
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
        return long_description

def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='openfaas',
    python_requires='>=3.4.0',
    version='1.0',
    description="High aviariable proxy pool client for crawlers.",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author="yujmo",
    author_email='yujmo94@gmail.com',
    url='https://github.com/yujmo/openfaas',
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    keywords=['proxy', 'client', 'openfaas'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
