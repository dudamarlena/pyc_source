from setuptools import setup, find_packages


setup(
    name="sweetest",
    version="1.1",
    author="tonglei",
    author_email="tonglei@qq.com",
    description="Web UI Autotest with Selenium & Excel",
    #long_description=open("README.rst").read(),
    license="Apache License, Version 2.0",
    url="https://github.com/tonglei100/sweetest",
    packages=['sweetest', 'sweetest.keywords', 'sweetest.lib', 'sweetest.example'],
    package_data={'sweetest': ['*.py', 'example\sweetest_example.zip']},
    install_requires=[
        'selenium',
        'xlrd',
        'xlsxwriter',
        'requests',
        'injson',
        'Appium-Python-Client',
        'Pillow'
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': [
            'sweetest=sweetest:sweetest'
        ]
    }
)
