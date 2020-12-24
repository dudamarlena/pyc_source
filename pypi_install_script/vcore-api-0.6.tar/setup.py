import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
try:
    import pypandoc

    README = pypandoc.convert(os.path.join(os.path.dirname(__file__), 'README.md'), 'rst')
except (ImportError, OSError, Exception):
    print("Can't build readme")
    README = ""
setup(
    name='vcore-api',
    version='0.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
    license='MIT License',
    description='Vcore python api',
    long_description=README,
    url='https://github.com/jonatanSh/vcore/',
    author='Jonathan Shimon',
    author_email='jonatanshimon@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
