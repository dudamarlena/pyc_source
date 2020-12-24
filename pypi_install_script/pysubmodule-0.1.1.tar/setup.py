from setuptools import setup, find_packages


setup(
    name='pysubmodule',
    version='0.1.1',
    description='painless submodule manager',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/pysubmodule',
    packages=find_packages(),
    install_requires=[
        'structlog',
    ]
)
