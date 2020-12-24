from setuptools import setup


setup(
    name='yxwaiter',
    version=__import__('yxwaiter').__version__,
    description="YX waiter.",
    author='qx3501332',
    author_email='x.qiu@qq.com',
    license="MIT License",
    packages=['yxwaiter', 'yxwaiter.hivedata'],
    include_package_date=True,
    zip_safe=True,
    install_requires=['waiterdb', 'pymysql', 'grpcio', 'grpcio-tools', 'googleapis-common-protos'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
