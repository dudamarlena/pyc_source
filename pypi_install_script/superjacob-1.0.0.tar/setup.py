import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='superjacob',
    version='1.0.0',
    author='Benjamin Levy, Mark Miao, Zhenru Wang, Kidus Negesse',
    description='Yet another autodiff package (YAAP)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ADMonsters/cs207-FinalProject',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
