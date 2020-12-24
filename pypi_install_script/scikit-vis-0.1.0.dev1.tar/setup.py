from setuptools import setup, find_packages
import os

os.system('python gen_build.py')

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='scikit-vis',
    version='0.1.0dev1',
    description='stunning, one-line visualizations for scikit-learn',
    long_description=readme(),
    include_package_data = True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    keywords='scikit visualization ai',
    url='https://github.com/quantum-programmer/scikit-vis',
    author='Hans Musgrave',
    author_email='skvis@hans.codes',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'numpy',
        'matplotlib',
        'scipy',
        'wrapt>=1.10.0',
        ],
    setup_requires=[
        'scikit-learn',
        'numpy',
        'matplotlib',
        'scipy',
        'wrapt>=1.10.0',
        ],
    use_2to3=True,
)
