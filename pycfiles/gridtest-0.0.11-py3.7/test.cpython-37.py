# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/main/test.py
# Compiled at: 2020-05-07 19:46:42
# Size of source mod 2**32: 26847 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.defaults import GRIDTEST_WORKERS, GRIDTEST_RETURNTYPES
from gridtest.templates import copy_template
from gridtest.utils import read_yaml, write_yaml, write_json
from gridtest.logger import bot
from gridtest import __version__
from gridtest.main.generate import import_module, get_function_typing, extract_modulename
from gridtest.main.grids import get_grids
from gridtest.main.helpers import test_basic
from gridtest.main.workers import Workers
from gridtest.main.substitute import substitute_func, substitute_args, expand_args
from copy import deepcopy
import itertools, re, shutil, sys, os

class GridTest:

    def __init__(self, module, name, func=None, filename=None, params=None, verbose=False, cleanup=True, show_progress=True):
        self.name = name
        self.func = func
        self.module = module
        self.valid = False
        self.success = False
        self.filename = filename or ''
        self.verbose = verbose
        self.cleanup_temp = cleanup
        self.to_cleanup = set()
        self.show_progress = show_progress
        self.result = None
        self.raises = None
        self.out = []
        self.err = []
        self.metrics = {}
        self.set_params(params)

    def __repr__(self):
        return '[test|%s]' % self.name

    def __str__(self):
        return '[test|%s]' % self.name

    def set_params(self, params):
        """Given params with args that are loaded, making substitutions
           at the onset of generating the test. Also keep track of
           any directories / files defined by tmp_path and tmp_dir
           to clean up after the test is run.
        """
        self.params = params or {}
        for name, value in self.params.get('args', {}).items():
            new_value = self.substitute(value)
            self.params['args'][name] = new_value
            if isinstance(value, str) and re.sub('({%|%}| )', '', value) in ('tmp_dir',
                                                                             'tmp_path'):
                self.to_cleanup.add(new_value)

        self._params = deepcopy(self.params)

    def substitute(self, value):
        """Given an input value, return the appropriate substituted string for
           it. This means that {{ args.x }} references can reference arguments
           in params, or {% func %} can refer to a function in the gridtest
           helpers namespace.
        """
        value = self._substitute_args(value)
        value = self._substitute_func(value)
        return value

    def post_substitute(self):
        """After a run, sometimes we want to check the result (whatever it is)
        """
        for section in GRIDTEST_RETURNTYPES:
            if section in self.params:
                self.params[section] = self.substitute(self.params[section])

    def _substitute_args(self, value):
        """Given a value, determine if it has variable argument substitutions
           in the format of {{ args.<name> }} and if so, if the argument is present
           return the value with the substitution.
        """
        if not isinstance(value, str):
            return value
        else:
            if re.search('{{(\\s+)?returns(\\s)?}}', value):
                if 'returns' in self.params:
                    value = substitute_args(value, params=(self.params))
            if re.search('{{(\\s+)?result(\\s)?}}', value) and self.result:
                value = substitute_args(value, params={'result': self.result})
        value = re.sub('args[.]', '', value, 1)
        return substitute_args(value, params=(self.params.get('args', {})))

    def _substitute_func(self, value):
        """Given a value, determine if it contains a function substitution,
           and do it. See gridtest.main.helpers.substitute_func. for details.
        """
        return substitute_func(value)

    @property
    def summary(self):
        """print a summary of the test, including if it is supposed to
           return, raise, or check existance.
        """
        if self.success:
            return self.summary_success()
        return self.summary_failure()

    def get_func(self):
        """Get the function name, meaning we get the module first. This can
           also be used for one off (custom) function and module names.
        """
        sys.path.insert(0, os.path.dirname(self.filename))
        module = import_module(self.module)
        func = getattr(module, self.get_funcname())
        if func is None:
            bot.error('Cannot find function.')
        return func

    def get_funcname(self):
        """Get the function name, meaning we get the module first.
        """
        return re.sub('^%s[.]' % self.module, '', self.name)

    def run(self, interactive=False, cleanup=None):
        """run an isolated test, and store the return code and result with
           the tester here. 

           Arguments:
            - interactive (bool) : run interactively for shell to debug
            - cleanup (bool) : remove any temporary directories or files (True)
        """
        if not self.show_progress:
            bot.info(f"Running test {name}")
        if cleanup is not None:
            self.cleanup_temp = cleanup
        passed, result, out, err, raises = test_basic(funcname=(self.get_funcname()),
          module=(self.module),
          func=(self.func),
          filename=(self.filename),
          metrics=(self.params.get('metrics', [])),
          args=(self.params.get('args', {})),
          returns=(self.params.get('returns')),
          interactive=interactive)
        self.success = passed
        self.result = result
        self.out = out
        self.err = err
        self.raises = raises
        self.check_output()
        if self.cleanup_temp:
            self.cleanup()

    def check_output(self):
        """Given that self.result is defined, check final output for the test.
           This works (and is called) after self.run(), OR by the multiprocessing
           worker that has updated self.result. Each of the actions below
           does additional parsing of the result, and the client will update
           self.success to be False if there is an issue.
        """
        self.post_substitute()
        self.check_metrics()
        if 'returns' in self.params:
            self.check_returns(self.params['returns'])
        if 'raises' in self.params:
            self.check_raises(self.params['raises'])
        if 'exists' in self.params:
            self.check_exists(self.params['exists'])
        if 'istrue' in self.params:
            self.check_istrue(self.params['istrue'])
        if 'isfalse' in self.params:
            self.check_isfalse(self.params['isfalse'])
        if 'equals' in self.params:
            self.check_equals(self.params['equals'])
        if 'isinstance' in self.params:
            self.check_isinstance(self.params['isinstance'])
        if self.raises:
            if 'raises' not in self.params:
                self.err.append(f"Unexpected Exception: {self.raises}.")
                self.success = False
        if 'success' in self.params:
            if not self.params['success']:
                if not self.success:
                    self.out.append('success key set to false, expected failure.')
                    self.success = True

    def check_exists(self, filename):
        """check if a filename exists.
        """
        self.success = False
        if os.path.exists(filename):
            self.success = True

    def check_returns(self, value):
        """test that a function returns a particular value. The value might
           reference an input variable, so we use the args dictionary to
           substitute
        """
        self.success = False
        value = self.substitute(value)
        if value == self.result:
            self.success = True

    def check_raises(self, exception):
        """Ensure that running a function raises a particular error. If the
           function runs successfully, this is considered a failure.
        """
        self.success = False
        if not self.raises:
            self.success = False
            self.err.append(f"Expected exception {exception} not raised")
        else:
            if self.raises == exception:
                self.success = True
                self.out.append(f"Exception: {self.raises} raised as desired.")
            else:
                self.err.append(f"Expected exception {exception}, instead raised {self.raises}")

    def check_isinstance(self, instance):
        """check if the result is of a particular type
        """
        if not type(self.result).__name__ == instance:
            self.err.append(f"{type(self.result).__name__} is not instance of {instance}")
            self.success = False

    def check_istrue(self, statement):
        """check if a statement is true.
        """
        if not eval(str(statement)) == True:
            self.success = False

    def check_isfalse(self, statement):
        """check if a statement is false
        """
        if not eval(str(statement)) == False:
            self.success = False

    def check_equals(self, statement):
        """check if a result equals some statement.
        """
        if not eval(str(statement)) == self.result:
            self.success = False

    def check_metrics(self):
        """After runs are complete, given metrics defined in params, parse
           over the list and look for metric output in the output (and remove)
        """
        metrics = self.params.get('metrics')
        if metrics:
            regex = '^(%s)' % '|'.join(metrics)
            self.metrics = {k:[] for k in metrics}
            for line in self.out:
                for metric in metrics:
                    if line.startswith(metric):
                        self.metrics[metric].append(line.replace(metric, '', 1).strip())

            self.out = [x for x in self.out if not re.search(regex, x)]

    def cleanup(self):
        """Given a list of paths (files or folders) generated by gridtest,
           clean them up with shutil.rm
        """
        if self.cleanup_temp:
            bot.debug('Skipping cleanup.')
        else:
            for path in self.to_cleanup:
                if os.path.isfile(path):
                    bot.debug(f"Cleaning up file {path}")
                    os.remove(path)

    def reset(self):
        """reset a test to it's original state, meaning that original parameters,
           the result, raises, etc. are reset.
        """
        self.params = deepcopy(self._params)
        self.result = None
        self.raises = None
        self.valid = False
        self.success = False
        self.to_cleanup = set()
        self.out = []
        self.err = []

    def _summary(self, out):
        """return summary for specific output (or error) stream
        """
        output = ''.join(out) if self.verbose else ''
        for key in ('returns', 'raises', 'exists', 'istrue', 'isfalse', 'equals', 'isinstance'):
            if key in self.params:
                output += ' %s %s' % (key, self.params[key])

        return output.strip()

    def summary_success(self):
        return self._summary(self.out)

    def summary_failure(self):
        return self._summary(self.err)


class GridTestFunc(GridTest):
    __doc__ = 'a function can be loaded from within Python with GridTestFunc.\n    '

    def __init__(self, func, params=None, verbose=False, show_progress=True):
        super().__init__(module=(func.__module__),
          func=func,
          name=(func.__name__),
          params=params,
          verbose=verbose,
          show_progress=show_progress)


class GridRunner:

    def __init__(self, input_file, **kwargs):
        """the grid tester loads a gridtest specification file,
           and then deploys testing workers to run the tests.

           Arguments:

           input_file (str) : the watcher name, defaults to github
           kwargs: should include command line arguments from the client.
        """
        self.config = {}
        self._version = __version__
        self.load(input_file)
        self.set_name(kwargs.get('name'))
        self._fill_classes()
        self.show_progress = True
        self.grids = {}

    def load(self, input_file):
        """load a testing gridtest file.
        """
        input_file = os.path.abspath(input_file)
        if not os.path.exists(input_file):
            sys.exit(f"Cannot find gridtest file {input_file}")
        if not re.search('(yml|yaml)$', input_file):
            sys.exit('Please provide a yaml file (e.g., gridtest.yml) to test.')
        self.config = read_yaml(input_file)
        self.input_file = input_file
        self.input_dir = os.path.dirname(input_file)

    def set_name(self, name=None):
        """set a custom name. If the user provides a name to the GridRunner,
           this name will be used. Otherwise we use the basename of the input
           file.

           Arguments:
            - name (str): the name of the input file
        """
        self.name = name or os.path.basename(self.input_file)

    def iter_tests(self):
        for _, section in self.config.items():
            for name, tests in section.get('tests', {}).items():
                yield (
                 name, tests)

    def iter_grids(self):
        for name, grid in self.grids.items():
            yield (
             name, grid)

    def _fill_classes(self):
        """Read in a config, and create a lookup for any instance variables. Then
           substitute arguments (starting with instance) for these variables.
        """
        lookup = dict()
        for name, tests in self.iter_tests():
            for test in tests:
                if 'instance' in test:
                    lookup[test['instance']] = test['args']

        for name, tests in self.iter_tests():
            for test in tests:
                if 'self' in test.get('args', {}):
                    if not test['args']['self']:
                        sys.exit("%s: please define an instance to use with 'self: {{ instance.name }}'" % name)
                    if re.search('{{.+}}', test['args']['self']):
                        instance = re.sub('({{|}}|instance[.])', '', '{{ instance.thisone }}').strip()
                        if instance in lookup:
                            test['args']['self'] = lookup[instance]

    def run_tests(self, tests, nproc=9, parallel=True, interactive=False, name=None):
        """run tests. By default, we run them in parallel, unless serial
           is selected.

           Arguments:
            - parallel (bool) : run tasks in parallel that are able (default is True)
            - nproc (int) : number of processes to run
            - cleanup (bool) : clean up files/dir generated with tmp_path, tmp_dir
            - name (str) : the name of a test to interact with
            - interactive (bool) : run jobs interactively (for debugging)
              not available for parallel jobs.
        """
        if parallel:
            interactive or self._run_parallel(tests, nproc=nproc)
        else:
            total = len(tests)
            progress = 1
            for _, task in tests.items():
                prefix = '[%s:%s/%s]' % (task.name, progress, total)
                if self.show_progress:
                    bot.show_progress(progress, total, length=35, prefix=prefix)
                else:
                    bot.info('Running %s' % prefix)
                is_interactive = interactive
                if name is not None:
                    if interactive:
                        if not task.name.startswith(name):
                            is_interactive = False
                task.run(interactive=is_interactive)
                progress += 1

        return tests

    def _run_parallel(self, tests, nproc=GRIDTEST_WORKERS):
        """run tasks in parallel using the Workers class. Returns the same
           tests results, but after running.

           Arguments:
              - queue: the list of task objects to run
        """
        workers = Workers(show_progress=(self.show_progress), workers=nproc)
        workers.run(tests)
        for name, test in tests.items():
            test.check_output()
            if test.cleanup_temp:
                test.cleanup()

        return tests

    def run(self, regexp=None, parallel=True, nproc=None, show_progress=True, verbose=False, interactive=False, name=None, cleanup=True, save=None, save_report=None, report_template='report'):
        """run the grid runner, meaning that we turn each function and set of
           tests into a single test, and then run with multiprocessing. 
           This is the function called by the user that also does filtering
           of tests based on a regular expression before calling them.

           Arguments:
              - regexp (str) : if supplied, filter to this pattern 
              - parallel (bool) : use multiprocessing to run tasks (default True)
              - show_progress (bool) : show progress instead of task information
              - nproc (int) : number of processes to use for parallel testing
              - verbose (bool) : print success output too
              - interactive (bool) : interactively debug functions
              - name (str) : if specified, a name of a test to interact with
              - cleanup (bool) : cleanup files/directories generated with tmp_path tmp_dir
              - save (str) : a filepath to save results to (must be json)
              - save_report (str) : path to folder (not existing) to save a report to
              - report_template (str) : a template name of a report to generate
        """
        self.get_grids()
        tests = self.get_tests(regexp=regexp, verbose=verbose, cleanup=cleanup)
        self.show_progress = show_progress
        self.run_tests(tests=tests,
          parallel=parallel,
          nproc=(nproc or GRIDTEST_WORKERS),
          interactive=interactive,
          name=name)
        self.print_results(tests)
        if save_report:
            report_dir = self.save_report(save_report, report_template)
            save = os.path.join(report_dir, 'results.json')
        if save:
            self.save_results(save, tests)
        if self.failed(tests):
            return 1
        return 0

    def success(self, tests):
        """Given a test of tests, return True if all are successful.
        """
        return all([test.success for name, test in tests.items()])

    def failed(self, tests):
        """Given a test of tests, return True if any are not successful.
        """
        return not self.success(tests)

    def save(self, testfile):
        """Save the runner.config to an output yaml file.
        """
        bot.info(f"Writing {self} to {testfile}")
        write_yaml(self.config, testfile)

    def save_report(self, report_dir, report_template):
        """save a runner results to file.
        """
        report_dir = os.path.abspath(report_dir)
        if os.path.exists(report_dir):
            bot.exit(f"{report_dir} already exists, please remove before using.")
        dest = copy_template(report_template, report_dir)
        if not dest:
            bot.exit(f"Error writing to {dest}.")
        return dest

    def save_results(self, filename, tests):
        """save a runner results to file.
        """
        filename = os.path.abspath(filename)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            bot.exit(f"{dirname} does not exist, skipping save.")
        else:
            if not filename.endswith('.json'):
                bot.warning(f"{dirname} must be extension .json, skipping save.")
            else:
                results = []
                for key, test in tests.items():
                    results.append({'name':key, 
                     'function':test.name, 
                     'filename':test.filename, 
                     'out':test.out, 
                     'err':test.err, 
                     'result':test.result, 
                     'params':test.params, 
                     'raises':test.raises, 
                     'success':test.success, 
                     'metrics':test.metrics, 
                     'module':test.module})

                write_json(results, filename)
                return filename

    def print_results(self, tests):
        """print the results of the tests, meaning that success is in green,
           and non-success is in red.
        """
        total = 0
        success = 0
        failure = 0
        has_metrics = False
        print('{:<30} {:<30} {:<30}'.format('Name', 'Status', 'Summary'))
        print('{:_<120}'.format(''))
        for name, test in tests.items():
            total += 1
            if test.metrics:
                has_metrics = True
            if test.success:
                bot.success('{:<30} {:<30} {:<30}'.format(name, 'success', test.summary))
                success += 1
            else:
                bot.failure(f"failure: {name} {test.summary}")
                failure += 1

        if has_metrics:
            print('\n{:_<120}'.format(''))
        for name, test in tests.items():
            for metric, result in test.metrics.items():
                print('{:<30} {:<30} {:<30}'.format(name, metric, '|'.join(result)))

        print(f"\n{success}/{total} tests passed")

    def get_grids(self):
        """a grid is a specification under "grids" that can be run to
           parameterize a set of arguments, optionally run through a function
           or just generated to have combinations. If a count variable is
           included, we multiply by that many times.
        """
        for parent, section in self.config.items():
            filename = extract_modulename(section.get('filename', ''), self.input_dir)
            self.grids.update(get_grids((section.get('grids', {})), filename=filename))

        return self.grids

    def get_tests(self, regexp=None, verbose=False, cleanup=True):
        """get tests based on a regular expression.

           Arguments:
            - regexp (str) : if provided, only include those tests that match.
        """
        tests = {}
        for parent, section in self.config.items():
            for name, module in section.get('tests', {}).items():
                if regexp:
                    if not re.search(regexp, name):
                        continue
                if name.startswith(parent):
                    filename = extract_modulename(section.get('filename', ''), self.input_dir)
                    idx = 0
                    for entry in module:
                        if set(entry.get('args', {}).keys()).intersection(set(entry.get('grid', {}).keys())):
                            bot.exit(f"{name} has shared grid and args keys.")
                        for argset in expand_args(entry, lookup=(self.grids)):
                            updated = deepcopy(entry)
                            updated['args'] = argset
                            tests['%s.%s' % (name, idx)] = GridTest(module=parent,
                              name=name,
                              params=updated,
                              verbose=verbose,
                              cleanup=cleanup,
                              filename=filename,
                              show_progress=(self.show_progress))
                            idx += 1

        return tests

    def __repr__(self):
        return '[gridtest|%s]' % self.name

    def __str__(self):
        return '[gridtest|%s]' % self.name