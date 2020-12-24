# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/python_deploy.py
# Compiled at: 2014-03-23 22:59:33
"""
Command-line script and library to automate the steps involved to
deploy python packages automatically to pypi and github.
"""
import six, benchline.args, benchline.command, benchline.user_input, os.path

def validate_args(parser, options, args):
    pass


def run_tests(version_str):
    """
    Run the tests through setuptools
    :param version_str:
    :return:
    """
    benchline.command.run('python%s setup.py test' % version_str)


def get_version():
    """
    Returns the version from the setup.py file.

    >>> six.b(".") in get_version()
    True

    :return: string version of setup.py file
    """
    return benchline.command.output('python setup.py --version')[:-1]


def increment_revision():
    """
    Opens the setup.py file in vim for editing.
    :return:
    """
    benchline.command.run('vim setup.py')


def get_pypi_servers():
    """
    Returns all the pypi servers in the .pypirc file.
    :return: string
    """
    config = six.moves.configparser.SafeConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.pypirc'))
    return config.get('distutils', 'index-servers')[1:].split('\n')


def get_pypi_server():
    servers = get_pypi_servers()
    return benchline.user_input.select('Select the pypi server to deploy to', servers)


def main():
    benchline.args.go(__doc__, validate_args=validate_args)
    run_tests('2')
    run_tests('3')
    increment_revision()
    version = get_version()
    benchline.command.run('git commit -a -m "[Updating version to %s]"' % version)
    benchline.command.run('git tag %s' % version)
    benchline.command.run('git push')
    benchline.command.run('git push --tags')
    pypi_server = get_pypi_server()
    benchline.command.run('python setup.py sdist bdist_egg bdist_wheel upload -r %s' % pypi_server)
    benchline.command.run('python3 setup.py bdist_egg upload -r %s' % pypi_server)


if __name__ == '__main__':
    main()