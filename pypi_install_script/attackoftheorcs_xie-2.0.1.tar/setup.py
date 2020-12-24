from distutils.core import setup

with open('README') as file:
    readme = file.read()

# NOTE: change the 'name' field below with some unique package name.
# then update the url field accordingly.

setup(
    name = 'attackoftheorcs_xie',
    version = '2.0.1',
    packages = ['wargame'],
    url = 'https://test.pypi.org/manage/project/attackoftheorcs_xie/',
    license = 'LICENSE.txt',
    description = 'test attackoftheorcs ignore',
    long_description = readme,
    author = 'rsp8266',
    author_email = '1316547041@qq.com'
)