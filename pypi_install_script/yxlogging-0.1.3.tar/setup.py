from distutils.core import setup


setup(
    name='yxlogging',
    version=__import__('yxlogging').__version__,
    description="formatted logs",
    author='qx3501332',
    author_email='x.qiu@qq.com',
    license="MIT License",
    packages=['yxlogging'],
    install_requires=[],
    include_package_date=True,
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
