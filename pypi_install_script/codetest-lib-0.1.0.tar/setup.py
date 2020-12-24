from setuptools import find_packages,setup
setup(
    name = 'codetest-lib',
    version = '0.1.0',
    author = 'xes',
    description = '学而思库',
    packages = find_packages(),
    install_requires = ["requests", "pypinyin"],
    url = 'https://code.xueersi.com'
)