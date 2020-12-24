# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/model.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import collections, logging, os, re, time, sys, yaml
from xml.etree import ElementTree
from benchexec import BenchExecException
from benchexec import intel_cpu_energy
from benchexec import result
from benchexec import util
MEMLIMIT = b'memlimit'
TIMELIMIT = b'timelimit'
CORELIMIT = b'cpuCores'
SOFTTIMELIMIT = b'softtimelimit'
HARDTIMELIMIT = b'hardtimelimit'
WALLTIMELIMIT = b'walltimelimit'
_BYTE_FACTOR = 1000
_ERROR_RESULTS_FOR_TERMINATION_REASON = {b'memory': b'OUT OF MEMORY', 
   b'killed': b'KILLED', 
   b'failed': b'FAILED', 
   b'files-count': b'FILES-COUNT LIMIT', 
   b'files-size': b'FILES-SIZE LIMIT'}
_EXPECTED_RESULT_FILTER_VALUES = {True: b'true', False: b'false', None: b'unknown'}
_WARNED_ABOUT_UNSUPPORTED_EXPECTED_RESULT_FILTER = False

def substitute_vars(oldList, runSet=None, task_file=None):
    """
    This method replaces special substrings from a list of string
    and return a new list.
    """
    keyValueList = []
    if runSet:
        benchmark = runSet.benchmark
        keyValueList = [
         (
          b'benchmark_name', benchmark.name),
         (
          b'benchmark_date', benchmark.instance),
         (
          b'benchmark_path', benchmark.base_dir or b'.'),
         (
          b'benchmark_path_abs', os.path.abspath(benchmark.base_dir)),
         (
          b'benchmark_file', os.path.basename(benchmark.benchmark_file)),
         (
          b'benchmark_file_abs',
          os.path.abspath(os.path.basename(benchmark.benchmark_file))),
         (
          b'logfile_path', os.path.dirname(runSet.log_folder) or b'.'),
         (
          b'logfile_path_abs', os.path.abspath(runSet.log_folder)),
         (
          b'rundefinition_name', runSet.real_name if runSet.real_name else b''),
         (
          b'test_name', runSet.real_name if runSet.real_name else b'')]
    if task_file:
        var_prefix = b'taskdef_' if task_file.endswith(b'.yml') else b'inputfile_'
        keyValueList.append((var_prefix + b'name', os.path.basename(task_file)))
        keyValueList.append((var_prefix + b'path', os.path.dirname(task_file) or b'.'))
        keyValueList.append((
         var_prefix + b'path_abs', os.path.dirname(os.path.abspath(task_file))))
    assert len({key for key, value in keyValueList}) == len(keyValueList)
    return [ util.substitute_vars(s, keyValueList) for s in oldList ]


def load_task_definition_file(task_def_file):
    """Open and parse a task-definition file in YAML format."""
    try:
        with open(task_def_file) as (f):
            task_def = yaml.safe_load(f)
    except OSError as e:
        raise BenchExecException(b'Cannot open task-definition file: ' + str(e))
    except yaml.YAMLError as e:
        raise BenchExecException(b'Invalid task definition: ' + str(e))

    if str(task_def.get(b'format_version')) not in ('0.1', '1.0'):
        raise BenchExecException((b"Task-definition file {} specifies invalid format_version '{}'.").format(task_def_file, task_def.get(b'format_version')))
    return task_def


def load_tool_info(tool_name, config):
    """
    Load the tool-info class.
    @param tool_name: The name of the tool-info module.
    Either a full Python package name or a name within the benchexec.tools package.
    @return: A tuple of the full name of the used tool-info module and an instance of the tool-info class.
    """
    tool_module = tool_name if b'.' in tool_name else b'benchexec.tools.' + tool_name
    try:
        if config.container:
            from benchexec import containerized_tool
            tool = containerized_tool.ContainerizedTool(tool_module, config)
        else:
            tool = __import__(tool_module, fromlist=[b'Tool']).Tool()
            tool.close = lambda : None
    except ImportError as ie:
        logging.debug(b"Did not find module '%s'. Python probably looked for it in one of the following paths:\n  %s", tool_module, (b'\n  ').join(path or b'.' for path in sys.path))
        sys.exit((b'Unsupported tool "{0}" specified. ImportError: {1}').format(tool_name, ie))
    except AttributeError:
        sys.exit((b'The module "{0}" does not define the necessary class "Tool", it cannot be used as tool info for BenchExec.').format(tool_module))

    return (tool_module, tool)


def cmdline_for_run(tool, executable, options, sourcefiles, propertyfile, rlimits):
    working_directory = tool.working_directory(executable)

    def relpath(path):
        if os.path.isabs(path):
            return path
        return os.path.relpath(path, working_directory)

    rel_executable = relpath(executable)
    if os.path.sep not in rel_executable:
        rel_executable = os.path.join(os.curdir, rel_executable)
    args = tool.cmdline(rel_executable, list(options), list(map(relpath, sourcefiles)), relpath(propertyfile) if propertyfile else None, rlimits.copy())
    assert all(args), b'Tool cmdline contains empty or None argument: ' + str(args)
    args = [ os.path.expandvars(arg) for arg in args ]
    args = [ os.path.expanduser(arg) for arg in args ]
    return args


def get_propertytag(parent):
    tag = util.get_single_child_from_xml(parent, b'propertyfile')
    if tag is None:
        return
    else:
        expected_verdict = tag.get(b'expectedverdict')
        if expected_verdict is not None and expected_verdict not in _EXPECTED_RESULT_FILTER_VALUES.values() and not re.match(b'false(.*)', expected_verdict):
            raise BenchExecException((b"Invalid value '{}' for expectedverdict of <propertyfile> in tag <{}>: Only 'true', 'false', 'false(<subproperty>)' and 'unknown' are allowed!").format(expected_verdict, parent.tag))
        return tag


class Benchmark(object):
    """
    The class Benchmark manages the import of source files, options, columns and
    the tool from a benchmark_file.
    This class represents the <benchmark> tag.
    """

    def __init__(self, benchmark_file, config, start_time):
        """
        The constructor of Benchmark reads the source files, options, columns and the tool
        from the XML in the benchmark_file..
        """
        logging.debug(b"I'm loading the benchmark %s.", benchmark_file)
        self.config = config
        self.benchmark_file = benchmark_file
        self.base_dir = os.path.dirname(self.benchmark_file)
        self.name = os.path.basename(benchmark_file)[:-4]
        if config.name:
            self.name += b'.' + config.name
        self.description = None
        if config.description_file is not None:
            try:
                self.description = util.read_file(config.description_file)
            except (IOError, UnicodeDecodeError) as e:
                raise BenchExecException((b"File '{}' given for description could not be read: {}").format(config.description_file, e))

        self.start_time = start_time
        self.instance = start_time.strftime(b'%Y-%m-%d_%H%M')
        self.output_base_name = config.output_path + self.name + b'.' + self.instance
        self.log_folder = self.output_base_name + b'.logfiles' + os.path.sep
        self.log_zip = self.output_base_name + b'.logfiles.zip'
        self.result_files_folder = self.output_base_name + b'.files'
        try:
            rootTag = ElementTree.ElementTree().parse(benchmark_file)
        except ElementTree.ParseError as e:
            sys.exit((b'Benchmark file {} is invalid: {}').format(benchmark_file, e))

        if b'benchmark' != rootTag.tag:
            sys.exit((b"Benchmark file {} is invalid: It's root element is not named 'benchmark'.").format(benchmark_file))
        tool_name = rootTag.get(b'tool')
        if not tool_name:
            sys.exit(b'A tool needs to be specified in the benchmark definition file.')
        self.tool_module, self.tool = load_tool_info(tool_name, config)
        self.tool_name = self.tool.name()
        self.tool_version = None
        self.executable = None
        self.display_name = rootTag.get(b'displayName')

        def parse_memory_limit(value):
            try:
                value = int(value)
            except ValueError:
                return util.parse_memory_value(value)

            raise ValueError((b"Memory limit must have a unit suffix, e.g., '{} MB'").format(value))

        def handle_limit_value(name, key, cmdline_value, parse_fn):
            value = rootTag.get(key, None)
            if cmdline_value is not None:
                if cmdline_value.strip() == b'-1':
                    value = None
                else:
                    value = cmdline_value
            if value is not None:
                try:
                    self.rlimits[key] = parse_fn(value)
                except ValueError as e:
                    sys.exit((b'Invalid value for {} limit: {}').format(name.lower(), e))

                if self.rlimits[key] <= 0:
                    sys.exit((b'{} limit "{}" is invalid, it needs to be a positive number (or -1 on the command line for disabling it).').format(name, value))
            return

        self.rlimits = {}
        keys = list(rootTag.keys())
        handle_limit_value(b'Time', TIMELIMIT, config.timelimit, util.parse_timespan_value)
        handle_limit_value(b'Hard time', HARDTIMELIMIT, config.timelimit, util.parse_timespan_value)
        handle_limit_value(b'Wall time', WALLTIMELIMIT, config.walltimelimit, util.parse_timespan_value)
        handle_limit_value(b'Memory', MEMLIMIT, config.memorylimit, parse_memory_limit)
        handle_limit_value(b'Core', CORELIMIT, config.corelimit, int)
        if HARDTIMELIMIT in self.rlimits:
            hardtimelimit = self.rlimits.pop(HARDTIMELIMIT)
            if TIMELIMIT in self.rlimits:
                if hardtimelimit < self.rlimits[TIMELIMIT]:
                    logging.warning(b'Hard timelimit %d is smaller than timelimit %d, ignoring the former.', hardtimelimit, self.rlimits[TIMELIMIT])
                elif hardtimelimit > self.rlimits[TIMELIMIT]:
                    self.rlimits[SOFTTIMELIMIT] = self.rlimits[TIMELIMIT]
                    self.rlimits[TIMELIMIT] = hardtimelimit
            else:
                self.rlimits[TIMELIMIT] = hardtimelimit
        self.num_of_threads = int(rootTag.get(b'threads')) if b'threads' in keys else 1
        if config.num_of_threads is not None:
            self.num_of_threads = config.num_of_threads
        if self.num_of_threads < 1:
            logging.error(b'At least ONE thread must be given!')
            sys.exit()
        self.options = util.get_list_from_xml(rootTag)
        self.propertytag = get_propertytag(rootTag)
        self.columns = Benchmark.load_columns(rootTag.find(b'columns'))
        if rootTag.findall(b'sourcefiles'):
            sys.exit((b'Benchmark file {} has unsupported old format. Rename <sourcefiles> tags to <tasks>.').format(benchmark_file))
        globalSourcefilesTags = rootTag.findall(b'tasks')
        self._required_files = set()
        for required_files_tag in rootTag.findall(b'requiredfiles'):
            required_files = util.expand_filename_pattern(required_files_tag.text, self.base_dir)
            if not required_files:
                logging.warning(b'Pattern %s in requiredfiles tag did not match any file.', required_files_tag.text)
            self._required_files = self._required_files.union(required_files)

        self.requirements = Requirements(rootTag.findall(b'require'), self.rlimits, config)
        result_files_tags = rootTag.findall(b'resultfiles')
        if result_files_tags:
            self.result_files_patterns = [ os.path.normpath(p.text) for p in result_files_tags if p.text ]
            for pattern in self.result_files_patterns:
                if pattern.startswith(b'..'):
                    sys.exit((b"Invalid relative result-files pattern '{}'.").format(pattern))

        else:
            self.result_files_patterns = [
             b'.']
        self.run_sets = []
        for i, rundefinitionTag in enumerate(rootTag.findall(b'rundefinition')):
            self.run_sets.append(RunSet(rundefinitionTag, self, i + 1, globalSourcefilesTags))

        if not self.run_sets:
            logging.warning(b'Benchmark file %s specifies no runs to execute (no <rundefinition> tags found).', benchmark_file)
        if not any(runSet.should_be_executed() for runSet in self.run_sets):
            logging.warning(b'No <rundefinition> tag selected, nothing will be executed.')
            if config.selected_run_definitions:
                logging.warning(b'The selection %s does not match any run definitions of %s.', config.selected_run_definitions, [ runSet.real_name for runSet in self.run_sets ])
        elif config.selected_run_definitions:
            for selected in config.selected_run_definitions:
                if not any(util.wildcard_match(run_set.real_name, selected) for run_set in self.run_sets):
                    logging.warning(b'The selected run definition "%s" is not present in the input file, skipping it.', selected)

        return

    def required_files(self):
        assert self.executable is not None, b'executor needs to set tool executable'
        return self._required_files.union(self.tool.program_files(self.executable))

    def working_directory(self):
        assert self.executable is not None, b'executor needs to set tool executable'
        return self.tool.working_directory(self.executable)

    def environment(self):
        assert self.executable is not None, b'executor needs to set tool executable'
        return self.tool.environment(self.executable)

    @staticmethod
    def load_columns(columnsTag):
        """
        @param columnsTag: the columnsTag from the XML file
        @return: a list of Columns()
        """
        logging.debug(b"I'm loading some columns for the outputfile.")
        columns = []
        if columnsTag is not None:
            for columnTag in columnsTag.findall(b'column'):
                pattern = columnTag.text
                title = columnTag.get(b'title', pattern)
                number_of_digits = columnTag.get(b'numberOfDigits')
                column = Column(pattern, title, number_of_digits)
                columns.append(column)
                logging.debug(b'Column "%s" with title "%s" loaded from XML file.', column.text, column.title)

        return columns


class RunSet(object):
    """
    The class RunSet manages the import of files and options of a run set.
    """

    def __init__(self, rundefinitionTag, benchmark, index, globalSourcefilesTags=[]):
        """
        The constructor of RunSet reads run-set name and the source files from rundefinitionTag.
        Source files can be included or excluded, and imported from a list of
        names in another file. Wildcards and variables are expanded.
        @param rundefinitionTag: a rundefinitionTag from the XML file
        """
        self.benchmark = benchmark
        self.real_name = rundefinitionTag.get(b'name')
        self.index = index
        self.log_folder = benchmark.log_folder
        self.result_files_folder = benchmark.result_files_folder
        if self.real_name:
            self.log_folder += self.real_name + b'.'
            self.result_files_folder = os.path.join(self.result_files_folder, self.real_name)
        self.options = benchmark.options + util.get_list_from_xml(rundefinitionTag)
        self.propertytag = get_propertytag(rundefinitionTag)
        if self.propertytag is None:
            self.propertytag = benchmark.propertytag
        required_files_pattern = {tag.text for tag in rundefinitionTag.findall(b'requiredfiles')}
        if rundefinitionTag.findall(b'sourcefiles'):
            sys.exit((b'Benchmark file {} has unsupported old format. Rename <sourcefiles> tags to <tasks>.').format(benchmark.benchmark_file))
        self.blocks = self.extract_runs_from_xml(globalSourcefilesTags + rundefinitionTag.findall(b'tasks'), required_files_pattern)
        self.runs = [ run for block in self.blocks for run in block.runs ]
        names = [
         self.real_name]
        if len(self.blocks) == 1:
            names.append(self.blocks[0].real_name)
        self.name = (b'.').join(filter(None, names))
        self.full_name = self.benchmark.name + (b'.' + self.name if self.name else b'')
        if self.should_be_executed():
            sourcefilesSet = set()
            for run in self.runs:
                base = os.path.basename(run.identifier)
                if base in sourcefilesSet:
                    logging.warning(b"Input file with name '%s' appears twice in runset. This could cause problems with equal logfile-names.", base)
                else:
                    sourcefilesSet.add(base)

            del sourcefilesSet
        return

    def should_be_executed(self):
        return not self.benchmark.config.selected_run_definitions or any(util.wildcard_match(self.real_name, run_definition) for run_definition in self.benchmark.config.selected_run_definitions)

    def extract_runs_from_xml(self, sourcefilesTagList, global_required_files_pattern):
        """
        This function builds a list of SourcefileSets (containing filename with options).
        The files and their options are taken from the list of sourcefilesTags.
        """
        base_dir = self.benchmark.base_dir
        blocks = []
        for index, sourcefilesTag in enumerate(sourcefilesTagList):
            sourcefileSetName = sourcefilesTag.get(b'name')
            matchName = sourcefileSetName or str(index)
            if self.benchmark.config.selected_sourcefile_sets and not any(util.wildcard_match(matchName, sourcefile_set) for sourcefile_set in self.benchmark.config.selected_sourcefile_sets):
                continue
            required_files_pattern = global_required_files_pattern.union({tag.text for tag in sourcefilesTag.findall(b'requiredfiles')})
            task_def_files = self.get_task_def_files_from_xml(sourcefilesTag, base_dir)
            fileOptions = util.get_list_from_xml(sourcefilesTag)
            local_propertytag = get_propertytag(sourcefilesTag)
            appendFileTags = sourcefilesTag.findall(b'append')
            currentRuns = []
            for identifier in task_def_files:
                if identifier.endswith(b'.yml'):
                    if appendFileTags:
                        raise BenchExecException(b'Cannot combine <append> and task-definition files in the same <tasks> tag.')
                    run = self.create_run_from_task_definition(identifier, fileOptions, local_propertytag, required_files_pattern)
                else:
                    run = self.create_run_for_input_file(identifier, fileOptions, local_propertytag, required_files_pattern, appendFileTags)
                if run:
                    currentRuns.append(run)

            for run in sourcefilesTag.findall(b'withoutfile'):
                currentRuns.append(Run(run.text, [], fileOptions, self, local_propertytag, required_files_pattern))

            blocks.append(SourcefileSet(sourcefileSetName, index, currentRuns))

        if self.benchmark.config.selected_sourcefile_sets:
            for selected in self.benchmark.config.selected_sourcefile_sets:
                if not any(util.wildcard_match(sourcefile_set.real_name, selected) for sourcefile_set in blocks):
                    logging.warning(b'The selected tasks "%s" are not present in the input file, skipping them.', selected)

        return blocks

    def get_task_def_files_from_xml(self, sourcefilesTag, base_dir):
        """Get the task-definition files from the XML definition. Task-definition files are files
        for which we create a run (typically an input file or a YAML task definition).
        """
        sourcefiles = []
        for includedFiles in sourcefilesTag.findall(b'include'):
            sourcefiles += self.expand_filename_pattern(includedFiles.text, base_dir)

        for includesFilesFile in sourcefilesTag.findall(b'includesfile'):
            for file in self.expand_filename_pattern(includesFilesFile.text, base_dir):
                if util.is_code(file):
                    logging.error(b"'%s' seems to contain code instead of a set of source file names.\nPlease check your benchmark definition file or remove bracket '{' from this file.", file)
                    sys.exit()
                fileWithList = open(file, b'rt')
                for line in fileWithList:
                    line = line.strip()
                    if not util.is_comment(line):
                        sourcefiles += self.expand_filename_pattern(line, os.path.dirname(file))

                fileWithList.close()

        for excludedFiles in sourcefilesTag.findall(b'exclude'):
            excludedFilesList = self.expand_filename_pattern(excludedFiles.text, base_dir)
            for excludedFile in excludedFilesList:
                sourcefiles = util.remove_all(sourcefiles, excludedFile)

        for excludesFilesFile in sourcefilesTag.findall(b'excludesfile'):
            for file in self.expand_filename_pattern(excludesFilesFile.text, base_dir):
                fileWithList = open(file, b'rt')
                for line in fileWithList:
                    line = line.strip()
                    if not util.is_comment(line):
                        excludedFilesList = self.expand_filename_pattern(line, os.path.dirname(file))
                        for excludedFile in excludedFilesList:
                            sourcefiles = util.remove_all(sourcefiles, excludedFile)

                fileWithList.close()

        return sourcefiles

    def create_run_for_input_file(self, input_file, options, local_propertytag, required_files_pattern, append_file_tags):
        """Create a Run from a direct definition of the main input file (without task definition)"""
        global _WARNED_ABOUT_UNSUPPORTED_EXPECTED_RESULT_FILTER
        input_files = [
         input_file]
        base_dir = os.path.dirname(input_file)
        for append_file in append_file_tags:
            input_files.extend(self.expand_filename_pattern(append_file.text, base_dir, sourcefile=input_file))

        run = Run(input_file, util.get_files(input_files), options, self, local_propertytag, required_files_pattern)
        if not run.propertyfile:
            return run
        prop = result.Property.create(run.propertyfile, allow_unknown=False)
        run.properties = [prop]
        expected_results = result.expected_results_of_file(input_file)
        if prop.name in expected_results:
            run.expected_results[prop.filename] = expected_results[prop.name]
        if run.propertytag.get(b'expectedverdict'):
            if not _WARNED_ABOUT_UNSUPPORTED_EXPECTED_RESULT_FILTER:
                _WARNED_ABOUT_UNSUPPORTED_EXPECTED_RESULT_FILTER = True
                logging.warning(b'Ignoring filter based on expected verdict for tasks without task-definition file. Expected verdicts for such tasks will be removed in BenchExec 3.0 (cf. https://github.com/sosy-lab/benchexec/issues/439).')
        return run

    def create_run_from_task_definition(self, task_def_file, options, local_propertytag, required_files_pattern):
        """Create a Run from a task definition in yaml format"""
        task_def = load_task_definition_file(task_def_file)

        def expand_patterns_from_tag(tag):
            result = []
            patterns = task_def.get(tag, [])
            if isinstance(patterns, str) or not isinstance(patterns, collections.Iterable):
                patterns = [
                 patterns]
            for pattern in patterns:
                expanded = util.expand_filename_pattern(str(pattern), os.path.dirname(task_def_file))
                if not expanded:
                    raise BenchExecException((b"Pattern '{}' in task-definition file {} did not match any paths.").format(pattern, task_def_file))
                expanded.sort()
                result.extend(expanded)

            return result

        input_files = expand_patterns_from_tag(b'input_files')
        if not input_files:
            raise BenchExecException((b'Task-definition file {} does not define any input files.').format(task_def_file))
        required_files = expand_patterns_from_tag(b'required_files')
        run = Run(task_def_file, input_files, options, self, local_propertytag, required_files_pattern, required_files)
        if not run.propertyfile:
            return run
        else:
            prop = result.Property.create(run.propertyfile, allow_unknown=True)
            run.properties = [prop]
            for prop_dict in task_def.get(b'properties', []):
                if not isinstance(prop_dict, dict) or b'property_file' not in prop_dict:
                    raise BenchExecException((b'Missing property file for property in task-definition file {}.').format(task_def_file))
                expanded = util.expand_filename_pattern(prop_dict[b'property_file'], os.path.dirname(task_def_file))
                if len(expanded) != 1:
                    raise BenchExecException((b"Property pattern '{}' in task-definition file {} does not refer to exactly one file.").format(prop_dict[b'property_file'], task_def_file))
                if prop.filename == expanded[0] or os.path.samefile(prop.filename, expanded[0]):
                    expected_result = prop_dict.get(b'expected_verdict')
                    if expected_result is not None and not isinstance(expected_result, bool):
                        raise BenchExecException((b"Invalid expected result '{}' for property {} in task-definition file {}.").format(expected_result, prop_dict[b'property_file'], task_def_file))
                    run.expected_results[prop.filename] = result.ExpectedResult(expected_result, prop_dict.get(b'subproperty'))

            if not run.expected_results:
                logging.debug(b"Ignoring run '%s' because it does not have the property from %s.", run.identifier, run.propertyfile)
                return
            if len(run.expected_results) > 1:
                raise BenchExecException((b"Property '{}' specified multiple times in task-definition file {}.").format(prop.filename, task_def_file))
            assert len(run.expected_results) == 1
            expected_result_filter = run.propertytag.get(b'expectedverdict')
            if expected_result_filter is not None:
                expected_result = next(iter(run.expected_results.values()))
                expected_result_str = _EXPECTED_RESULT_FILTER_VALUES[expected_result.result]
                if expected_result.result == False and expected_result.subproperty and b'(' in expected_result_filter:
                    expected_result_str += b'(' + expected_result.subproperty + b')'
                if expected_result_str != expected_result_filter:
                    logging.debug(b"Ignoring run '%s' because it does not have the expected verdict '%s' for %s.", run.identifier, expected_result_filter, prop)
                    return
            return run

    def expand_filename_pattern(self, pattern, base_dir, sourcefile=None):
        """
        The function expand_filename_pattern expands a filename pattern to a sorted list
        of filenames. The pattern can contain variables and wildcards.
        If base_dir is given and pattern is not absolute, base_dir and pattern are joined.
        """
        expandedPattern = substitute_vars([pattern], self, sourcefile)
        if not len(expandedPattern) == 1:
            raise AssertionError
            expandedPattern = expandedPattern[0]
            if expandedPattern != pattern:
                logging.debug(b'Expanded variables in expression %r to %r.', pattern, expandedPattern)
            fileList = util.expand_filename_pattern(expandedPattern, base_dir)
            fileList.sort()
            fileList or logging.warning(b'No files found matching %r.', pattern)
        return fileList


class SourcefileSet(object):
    """
    A SourcefileSet contains a list of runs and a name.
    """

    def __init__(self, name, index, runs):
        self.real_name = name
        self.name = name or str(index)
        self.runs = runs


_logged_missing_property_files = set()

class Run(object):
    """
    A Run contains some sourcefile, some options, propertyfiles and some other stuff, that is needed for the Run.
    """

    def __init__(self, identifier, sourcefiles, fileOptions, runSet, local_propertytag=None, required_files_patterns=[], required_files=[], expected_results={}):
        assert identifier
        self.identifier = identifier
        self.sourcefiles = sourcefiles
        self.runSet = runSet
        self.specific_options = fileOptions
        self.log_file = runSet.log_folder + os.path.basename(self.identifier) + b'.log'
        self.result_files_folder = os.path.join(runSet.result_files_folder, os.path.basename(self.identifier))
        self.expected_results = expected_results or {}
        self.required_files = set(required_files)
        rel_sourcefile = os.path.relpath(self.identifier, runSet.benchmark.base_dir)
        for pattern in required_files_patterns:
            this_required_files = runSet.expand_filename_pattern(pattern, runSet.benchmark.base_dir, rel_sourcefile)
            if not this_required_files:
                logging.warning(b'Pattern %s in requiredfiles tag did not match any file for task %s.', pattern, self.identifier)
            self.required_files.update(this_required_files)

        self.options = runSet.options + fileOptions if fileOptions else runSet.options
        substitutedOptions = substitute_vars(self.options, runSet, self.identifier)
        if substitutedOptions != self.options:
            self.options = substitutedOptions
        self.propertytag = local_propertytag if local_propertytag is not None else runSet.propertytag
        self.propertyfile = util.text_or_none(self.propertytag)
        self.properties = []

        def log_property_file_once(msg):
            if self.propertyfile not in _logged_missing_property_files:
                _logged_missing_property_files.add(self.propertyfile)
                logging.warning(msg)

        if self.propertyfile is None:
            log_property_file_once(b'No propertyfile specified. Score computation will ignore the results.')
        else:
            expandedPropertyFiles = util.expand_filename_pattern(self.propertyfile, self.runSet.benchmark.base_dir)
            substitutedPropertyfiles = substitute_vars([
             self.propertyfile], runSet, self.identifier)
            assert len(substitutedPropertyfiles) == 1
            if expandedPropertyFiles:
                if len(expandedPropertyFiles) > 1:
                    log_property_file_once((b'Pattern {0} for input file {1} in propertyfile tag matches more than one file. Only {2} will be used.').format(self.propertyfile, self.identifier, expandedPropertyFiles[0]))
                self.propertyfile = expandedPropertyFiles[0]
            elif substitutedPropertyfiles and os.path.isfile(substitutedPropertyfiles[0]):
                self.propertyfile = substitutedPropertyfiles[0]
            else:
                log_property_file_once((b'Pattern {0} for input file {1} in propertyfile tag did not match any file. It will be ignored.').format(self.propertyfile, self.identifier))
                self.propertyfile = None
        if self.propertyfile:
            self.required_files.add(self.propertyfile)
        self.required_files = list(self.required_files)
        self.columns = [ Column(c.text, c.title, c.number_of_digits) for c in self.runSet.benchmark.columns
                       ]
        self.values = {}
        self.status = b''
        self.category = result.CATEGORY_UNKNOWN
        return

    def cmdline(self):
        assert self.runSet.benchmark.executable is not None, b'executor needs to set tool executable'
        return cmdline_for_run(self.runSet.benchmark.tool, self.runSet.benchmark.executable, self.options, self.sourcefiles or [self.identifier], self.propertyfile, self.runSet.benchmark.rlimits)

    def set_result(self, values, visible_columns={}):
        """Set the result of this run.
        @param values: a dictionary with result values as returned by RunExecutor.execute_run(),
            may also contain arbitrary additional values
        @param visible_columns: a set of keys of values that should be visible by default
            (i.e., not marked as hidden), apart from those that BenchExec shows by default anyway
        """
        exitcode = values.pop(b'exitcode', None)
        if exitcode is not None:
            if exitcode.signal:
                self.values[b'@exitsignal'] = exitcode.signal
            else:
                self.values[b'@returnvalue'] = exitcode.value
        for key, value in values.items():
            if key == b'cpuenergy' and not isinstance(value, (str, bytes)):
                energy = intel_cpu_energy.format_energy_results(value)
                for energy_key, energy_value in energy.items():
                    if energy_key != b'cpuenergy':
                        energy_key = b'@' + energy_key
                    self.values[energy_key] = energy_value

            elif key in ('walltime', 'cputime', 'memory', 'cpuenergy'):
                self.values[key] = value
            elif key in visible_columns:
                self.values[key] = value
            else:
                self.values[b'@' + key] = value

        termination_reason = values.get(b'terminationreason')
        isTimeout = termination_reason in ('cputime', 'cputime-soft', 'walltime') or self._is_timeout()
        try:
            with open(self.log_file, b'rt', errors=b'ignore') as (outputFile):
                output = outputFile.readlines()
                output = output[6:]
        except IOError as e:
            logging.warning(b'Cannot read log file: %s', e.strerror)
            output = []

        self.status = self._analyze_result(exitcode, output, isTimeout, termination_reason)
        self.category = result.get_result_category(self.expected_results, self.status, self.properties)
        for column in self.columns:
            substitutedColumnText = substitute_vars([
             column.text], self.runSet, self.sourcefiles[0])[0]
            column.value = self.runSet.benchmark.tool.get_value_from_output(output, substitutedColumnText)

        return

    def _analyze_result(self, exitcode, output, isTimeout, termination_reason):
        """Return status according to result and output of tool."""
        tool_status = None
        if exitcode is not None:
            logging.debug(b'My subprocess returned %s.', exitcode)
            tool_status = self.runSet.benchmark.tool.determine_result(exitcode.value or 0, exitcode.signal or 0, output, isTimeout)
            if tool_status in result.RESULT_LIST_OTHER:
                if exitcode.signal == 6:
                    tool_status = b'ABORTED'
                elif exitcode.signal == 11:
                    tool_status = b'SEGMENTATION FAULT'
                elif exitcode.signal == 15:
                    tool_status = b'KILLED'
                elif exitcode.signal:
                    tool_status = b'KILLED BY SIGNAL ' + str(exitcode.signal)
                elif exitcode.value:
                    tool_status = (b'{} ({})').format(result.RESULT_ERROR, exitcode.value)
        status = None
        if isTimeout:
            status = b'TIMEOUT'
        elif termination_reason:
            status = _ERROR_RESULTS_FOR_TERMINATION_REASON.get(termination_reason, termination_reason)
        if not status:
            status = tool_status
        elif tool_status and tool_status not in result.RESULT_LIST_OTHER + [status, b'KILLED', b'KILLED BY SIGNAL 9']:
            status = (b'{} ({})').format(status, tool_status)
        return status

    def _is_timeout(self):
        """ try to find out whether the tool terminated because of a timeout """
        if self.values.get(b'cputime') is None:
            is_cpulimit = False
        else:
            rlimits = self.runSet.benchmark.rlimits
            if SOFTTIMELIMIT in rlimits:
                limit = rlimits[SOFTTIMELIMIT]
            elif TIMELIMIT in rlimits:
                limit = rlimits[TIMELIMIT]
            else:
                limit = float(b'inf')
            is_cpulimit = self.values[b'cputime'] > limit
        if self.values.get(b'walltime') is None:
            is_walllimit = False
        else:
            rlimits = self.runSet.benchmark.rlimits
            if WALLTIMELIMIT in rlimits:
                limit = rlimits[WALLTIMELIMIT]
            else:
                limit = float(b'inf')
            is_walllimit = self.values[b'walltime'] > limit
        return is_cpulimit or is_walllimit


class Column(object):
    """
    The class Column contains text, title and number_of_digits of a column.
    """

    def __init__(self, text, title, numOfDigits):
        self.text = text
        self.title = title
        self.number_of_digits = numOfDigits
        self.value = b''


class Requirements(object):
    """
    This class wrappes the values for the requirements.
    It parses the tags from XML to get those values.
    If no values are found, at least the limits are used as requirements.
    If the user gives a cpu_model in the config, it overrides the previous cpu_model.
    """

    def __init__(self, tags, rlimits, config):
        self.cpu_model = None
        self.memory = None
        self.cpu_cores = None
        for requireTag in tags:
            cpu_model = requireTag.get(b'cpuModel', None)
            if cpu_model:
                if self.cpu_model is None:
                    self.cpu_model = cpu_model
                else:
                    raise Exception(b'Double specification of required CPU model.')
            cpu_cores = requireTag.get(b'cpuCores', None)
            if cpu_cores:
                if self.cpu_cores is None:
                    if cpu_cores is not None:
                        self.cpu_cores = int(cpu_cores)
                else:
                    raise Exception(b'Double specification of required CPU cores.')
            memory = requireTag.get(b'memory', None)
            if memory:
                if self.memory is None:
                    if memory is not None:
                        try:
                            self.memory = int(memory) * _BYTE_FACTOR * _BYTE_FACTOR
                            logging.warning(b'Value "%s" for memory requirement interpreted as MB for backwards compatibility, specify a unit to make this unambiguous.', memory)
                        except ValueError:
                            self.memory = util.parse_memory_value(memory)

                else:
                    raise Exception(b'Double specification of required memory.')

        if self.cpu_cores is None:
            self.cpu_cores = rlimits.get(CORELIMIT, None)
        if self.memory is None:
            self.memory = rlimits.get(MEMLIMIT, None)
        if hasattr(config, b'cpu_model') and config.cpu_model is not None:
            self.cpu_model = config.cpu_model
        if self.cpu_cores is not None and self.cpu_cores <= 0:
            raise Exception((b'Invalid value {} for required CPU cores.').format(self.cpu_cores))
        if self.memory is not None and self.memory <= 0:
            raise Exception((b'Invalid value {} for required memory.').format(self.memory))
        return

    def __str__(self):
        s = b''
        if self.cpu_model:
            s += b" CPU='" + self.cpu_model + b"'"
        if self.cpu_cores:
            s += b' Cores=' + str(self.cpu_cores)
        if self.memory:
            s += b' Memory=' + str(self.memory / _BYTE_FACTOR / _BYTE_FACTOR) + b' MB'
        return b'Requirements:' + (s if s else b' None')