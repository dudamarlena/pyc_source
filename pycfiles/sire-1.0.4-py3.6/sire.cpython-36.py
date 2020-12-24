# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sire/sire.py
# Compiled at: 2019-07-07 17:27:54
# Size of source mod 2**32: 11550 bytes
"""
sire: create a new python3.7 project using all the extra stuff i like.
"""
import argparse, getpass, os, shutil, stat, subprocess, sys
PATHS = {
 '.bumpversion.cfg',
 '.coveragerc',
 '.flake8',
 '.travis.yml',
 'CHANGELOG.md',
 'LICENSE',
 'mypy.ini',
 'publish.sh',
 'README.md',
 'requirements.txt',
 'setup.py',
 'tests/tests.py',
 '{name}/__init__.py'}
EXCLUDE_TRANSLATIONS = dict(codecov='coveragerc',
  coverage='coveragerc',
  bump2version='bumpversion.cfg',
  rtd='readthedocs.cfg',
  readthedocs='readthedocs.cfg',
  venv='virtualenv',
  docs='readthedocs.cfg',
  test='tests.py')

class SafeDict(dict):
    __doc__ = '\n    Need a custom object to not error when formatting files that contain {str}\n    '

    def __missing__(self, key):
        return '{' + key + '}'


def _clean_kwargs(kwargs):
    """
    Turn exclude into a set of normalised strings, and translate
    exclude=git,virtualenv to git=False, virtualenv=False etc
    """
    exclude = kwargs['exclude']
    if not exclude:
        return kwargs
    else:
        exclude = {EXCLUDE_TRANSLATIONS.get(i, i) for i in exclude.split(',')}
        for special in frozenset({'virtualenv', 'mkdocs', 'git'}):
            if special in exclude:
                print(f"* Skipping {special} because it is in the exclude list.")
                kwargs[special] = False

        kwargs['exclude'] = exclude
        return kwargs


def _parse_cmdline_args():
    """
    Command line argument parsing. Doing it here means less duplication than
    would be the case in bin/
    """
    parser = argparse.ArgumentParser(description='sire a new Python 3.7 project.')
    extra = [os.path.basename(os.path.splitext(i)[0]).strip('.').lower() for i in PATHS]
    paths = '/'.join(sorted(extra))
    parser.add_argument('-e',
      '--exclude',
      nargs='?',
      type=str,
      required=False,
      help=f"Comma separated files/modules to exclude. Any of: {paths}")
    parser.add_argument('-m',
      '--mkdocs',
      default=False,
      action='store_true',
      required=False,
      help='Generate files for mkdocs/readthedocs')
    parser.add_argument('-i',
      '--interactive',
      default=False,
      action='store_true',
      required=False,
      help='Interactive prompt with a few extra fields to autofill')
    parser.add_argument('-v',
      '--virtualenv',
      default=False,
      action='store_true',
      required=False,
      help='Generate a virtualenv for this project')
    parser.add_argument('-g',
      '--git',
      default=False,
      action='store_true',
      required=False,
      help='Generate .git, .gitignore and hook(s)')
    parser.add_argument('project_name', help='Name of the new Python project')
    kwargs = vars(parser.parse_args())
    kwargs['name'] = kwargs.pop('project_name')
    return _clean_kwargs(kwargs)


def _locate_templates():
    """
    templates dir seems to move around depending on how you install!?
    """
    fpath = os.path.dirname(__file__)
    first = os.path.dirname(fpath)
    second = os.path.dirname(first)
    third = sys.prefix
    fourth = os.path.join(third, 'sire')
    dirs = [first, second, third, fourth]
    for path in dirs:
        if os.path.isdir(os.path.join(path, 'templates')):
            return os.path.join(path, 'templates')

    raise ValueError(f"No templates found in: {dirs}")


TEMPLATES = _locate_templates()

def _write(proj, outpath, formatters):
    """
    Get the filename from outpath
    read it from templates dir
    format any variables in the templates with projname/other formatters
    write to outpath
    """
    fname = os.path.basename(outpath)
    template = os.path.join(TEMPLATES, fname)
    with open(template, 'r') as (fo):
        formatted = fo.read().format_map(SafeDict(name=proj, **formatters))
    with open(os.path.join(proj, outpath.format(name=proj)), 'w') as (fo):
        fo.write(formatted.strip() + '\n')


def _make_todos(name, paths, mkdocs, git, github_username):
    """
    Make a formatted str of things to do from here. Mostly so the user can copy
    urls and so on (to quickly set up hooks, git remote)
    """
    todos = [
     f"Actually write some tests: {name}/tests.py"]
    if '.coveragerc' in paths:
        todos.append('Set up codecov and a git hook for it.')
    if mkdocs:
        rtd = 'https://readthedocs.org/dashboard/import'
        todos.append(f"Set up a readthedocs and a git hook for it: {rtd}")
    if git:
        url = f"git remote set-url origin https://github.com/{github_username}/{name}"
        todos.append(f"Set git remote: (e.g.) {url}")
    return '\n* '.join(todos)


def _filter_excluded(exclude):
    """
    Get just the subset of PATH strings that we need to process, based on the
    contents of exclude, which was already pre-processed during argument parsing
    """
    if not exclude:
        return PATHS
    else:
        filtered = set()
        for path in PATHS:
            no_pth = os.path.basename(path).lstrip('.')
            no_ext = os.path.splitext(no_pth)[0]
            possible = {path, no_pth, no_ext}
            if any(i in exclude for i in possible):
                print(f"* Skipping {path} because it is in the exclude list.")
            else:
                filtered.add(path)

        return filtered


def _build_virtualenv(name):
    """
    If the user wants, make a new virtualenv, install dependencies, and
    print some helpful copyable strings along the way
    """
    print('Making virtualenv and installing dependencies')
    subprocess.call(f"python3.7 -m venv {name}/venv-{name}".split())
    pip = os.path.abspath(f"{name}/venv-{name}/bin/pip")
    subprocess.call(f"{pip} install wheel".split())
    subprocess.call(f"{pip} install -r {name}/requirements.txt".split())
    vfile = os.path.join(os.path.dirname(pip), 'activate')
    print(f"\n* virtualenv created: activate with `source {vfile}`")


def _input_wrap(prompt, default=None):
    """
    Run input() with formatted prompt, and return
    The while loop can be used to ensure correct output
    """
    understood = False
    while not understood:
        result = input(prompt.format(default=default)).lower().strip()
        if result in frozenset({'yes', 'y'}):
            return True
        if result in frozenset({'no', 'n'}):
            return False
        if not result:
            return default
        if result in frozenset({'exit', 'quit', 'q'}):
            raise RuntimeError('User quit.')
        if not isinstance(default, bool):
            return result
        print("Error: answer not understood. You can 'quit' or hit ctrl+c to exit.")


def _interactive(name):
    """
    Interactive assistant. This will supercede any command line arguments, meaning
    that it is pointless to add any other arguments when using the -i argument.
    """
    prompt = "\n========================================================================\nThis is the interactive helper for *sire*. Details entered here will \ndetermine which files are included, and format them with the correct \ninformation. Leaving a field blank is OK, but can result in incompletely \nformatted files. Hit enter to begin, or type 'quit' to quit.\n========================================================================\n\n"
    _input_wrap(prompt)
    output = dict()
    usr = getpass.getuser()
    email = 'git config user.email'.split()
    email = subprocess.check_output(email).decode('utf-8').strip()
    real_name = 'git config user.name'.split()
    real_name = subprocess.check_output(real_name).decode('utf-8').strip()
    exes = 'Comma separated list of files to exclude (e.g. travis/mypy/bumpversion):  '
    prompts = [
     (
      'real_name', 'Real name (for license, setup.py) ({default}):  ', real_name),
     (
      'username', 'Username ({default}):  ', usr),
     (
      'email', 'Email ({default}):  ', email),
     (
      'github_username', 'GitHub username ({default}):  ', usr),
     ('description', 'Short project description:  ', None),
     ('mkdocs', 'Use mkdocs/readthedocs for documentation (y/N):  ', False),
     ('virtualenv', 'Generate a virtualenv for this project (y/N):  ', False),
     ('git', 'Initialise as a git repo (y/N):  ', False),
     (
      'exclude', exes, set())]
    for field, prompt, default in prompts:
        output[field] = _input_wrap(prompt, default)

    return output


def sire(name, mkdocs=True, virtualenv=True, git=True, exclude=None, interactive=False):
    """
    Generate a new Python 3.7 project, optionally with .git, virtualenv and
    mkthedocs basics present too.
    """
    formatters = dict() if not interactive else _interactive(name)
    if interactive:
        mkdocs = formatters.pop('mkdocs')
        virtualenv = formatters.pop('virtualenv')
        git = formatters.pop('git')
        exclude = formatters.pop('exclude')
    dirname = os.path.abspath(f"./{name}")
    print(f"\nGenerating new project at `{dirname}`...")
    os.makedirs(os.path.join(name, name))
    os.makedirs(os.path.join(name, 'tests'))
    paths = _filter_excluded(exclude)
    if git:
        subprocess.call(f"git init {name}".split())
        paths.update({'.gitignore', '.pre-commit-config.yaml'})
    if mkdocs:
        files = {
         'mkdocs.yml', 'docs/index.md', 'docs/about.md', '.readthedocs.yaml'}
        os.makedirs(os.path.join(name, 'docs'))
        paths.update(files)
    for path in paths:
        _write(name, path, formatters)

    st = os.stat(f"{name}/publish.sh")
    os.chmod(f"{name}/publish.sh", st.st_mode | stat.S_IEXEC)
    if virtualenv:
        _build_virtualenv(name)
    gh_username = formatters.get('github_username', '<username>')
    todos = _make_todos(name, paths, mkdocs, git, gh_username)
    final = f"\nAll done! `cd {name}` to check out your new project."
    if todos:
        final += f"\n\nTo do:\n\n* {todos}\n"
    print(final)


def wrapped_sire(**kwargs):
    """
    Make sure that the directory is deleted if there is an error during sire
    """
    try:
        sire(**kwargs)
    except KeyboardInterrupt:
        print('Process stopped by user. Aborting and cleaning up ...')
        shutil.rmtree((kwargs['name']), ignore_errors=True)
    except Exception:
        print('Error during project creation. Aborting and cleaning up ...')
        shutil.rmtree((kwargs['name']), ignore_errors=True)
        raise


if __name__ == '__main__':
    wrapped_sire(**_parse_cmdline_args())