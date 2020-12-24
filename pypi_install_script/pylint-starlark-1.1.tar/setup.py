from distutils.core import setup

setup(
  name = 'pylint-starlark',         # How you named your package folder (MyLib)
  packages = ['pylint_starlark'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Run pylint on Starlark files.',   # Give a short description about your library
  long_description='''
Use pylint for Starlark files, by doing an AST transform of load() calls into python import statements.

Use it by running `pylint-starlark file.star`, which internally calls `pylint` with the `pylint-starlark-plugin` plugin enabled.
You may also run it `via python3 -m pylint_starlark file.star`.
''',
  long_description_content_type="text/markdown",
  author = 'Peter Hagen',                   # Type in your name
  author_email = 'peter@phgn.io',      # Type in your E-Mail
  url = 'https://github.com/phgn0/pylint-starlark',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/phgn0/pylint-starlark/archive/1.1.tar.gz',    # I explain this later on
  keywords = ['pylint', 'starlark', 'plugin'],   # Keywords that define your package best
  install_requires=[
    'pylint',
    'pylint-starlark-plugin',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  scripts=['pylint-starlark'],
)
