from setuptools import setup, find_packages
setup(
    name='aliprojectlib',
    version=1.0,
    description=(
        'aliprojectlib'
    ),
    long_description=open('README.md').read(),
    author='aliblacken',
    author_email='ali.blacken@outlook.com',
    maintainer='Ali Blacken',
    maintainer_email='ali.blacken@outlook.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='http://www.ali-project.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)