from setuptools import setup, find_packages


install_requires = [
    "fardel==1.3.0",
]

setup(
    name='fardel_auth_address',
    version='1.0.0',
    description='Address extension for FardelCMS users',
    author='Sepehr Hamzehlouy',
    author_email='s.hamzelooy@gmail.com',
    url='https://github.com/FardelCMS/fardel_auth_address',
    packages=find_packages(".", exclude=["tests", "tests.*"]),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.7',
    ],
)
