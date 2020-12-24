import setuptools

description = "weebhooks - A lib for interacting with Discord webhooks."
#long_description = open("README.md").read()
version = "1.0.0"

packages = ['weebhooks']

setuptools.setup(
    name='weebhooks',
    version=version,
    description=description,
    #long_description=long_description,
    url='https://github.com/bananaboy21/weebhooks',
    author='dat banana boi',
    author_email='kang.eric.hi@gmail.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    install_requires=['aiohttp>=2.0.0']
)
