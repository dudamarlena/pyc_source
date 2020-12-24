import setuptools
import os


def _get_modules():
    modules = []
    target_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'amanita_cli')
    for f in filter(lambda x: os.path.isdir(os.path.join(target_dir, x)),
                    os.listdir(target_dir)):
        if f !='__pycache__':
            modules.append(f)
    return modules


def _get_packages():
    packages = ['amanita_cli']
    for module in _get_modules():
        packages.append('amanita_cli.{}'.format(module))
    return packages


def _get_package_data():
    res = {'amanita_cli': ['conf.default.yml']}
    res.update({'': ['*.yml', '.module']})
    return res


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author='Max Lit',
    author_email='max.lit.mbox@gmail.com',
    name='amanita-cli',
    version='0.0.10',
    license='LGPL-3',
    description='Amanita Telefonica spawn',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://gitlab.com/amanita_telefonica',
    keywords = ['asterisk', 'odoo', 'amanita'],
    download_url='https://gitlab.com/amanita_telefonica/cli/-/archive/master/cli-master.tar.gz',
    packages = _get_packages(),
    package_data = _get_package_data(),
    install_requires=[
        'click', 'ansible', 'nameko', 'pyyaml>=5.1', 'odoorpc',
    ],
    entry_points='''
        [console_scripts]
        amanita=amanita_cli:cli
    ''',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
      ],    
)
