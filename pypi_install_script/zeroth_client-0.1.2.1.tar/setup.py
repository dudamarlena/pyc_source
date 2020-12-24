from setuptools import setup, find_packages
 
setup(
    name                = 'zeroth_client',
    version             = '0.1.2',
    description         = 'python client package for zeroth',
    author              = 'henry.kim',
    author_email        = 'henry@atlaslabs.ai',
    install_requires    =  [],
    packages            = find_packages(exclude = []),
    keywords            = ['pypi deploy'],
    python_requires     = '>=3',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    scripts=['bin/zeroth_client'],
)
