# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/outputhandler.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import bz2, collections, datetime, io, os, threading, time, sys
from xml.dom import minidom
from xml.etree import ElementTree as ET
import zipfile, benchexec
from benchexec.model import MEMLIMIT, TIMELIMIT, SOFTTIMELIMIT, CORELIMIT
from benchexec import filewriter
from benchexec import intel_cpu_energy
from benchexec import result
from benchexec import util
RESULT_XML_PUBLIC_ID = b'+//IDN sosy-lab.org//DTD BenchExec result 1.18//EN'
RESULT_XML_SYSTEM_ID = b'https://www.sosy-lab.org/benchexec/result-1.18.dtd'
COLOR_GREEN = b'\x1b[32;1m{0}\x1b[m'
COLOR_RED = b'\x1b[31;1m{0}\x1b[m'
COLOR_ORANGE = b'\x1b[33;1m{0}\x1b[m'
COLOR_MAGENTA = b'\x1b[35;1m{0}\x1b[m'
COLOR_DEFAULT = b'{0}'
UNDERLINE = b'\x1b[4m{0}\x1b[0m'
COLOR_DIC = collections.defaultdict(lambda : COLOR_DEFAULT)
TERMINAL_TITLE = b''
if sys.stdout.isatty():
    COLOR_DIC.update({result.CATEGORY_CORRECT: COLOR_GREEN, 
       result.CATEGORY_WRONG: COLOR_RED, 
       result.CATEGORY_UNKNOWN: COLOR_ORANGE, 
       result.CATEGORY_ERROR: COLOR_MAGENTA, 
       result.CATEGORY_MISSING: COLOR_DEFAULT})
    _term = os.environ.get(b'TERM', b'')
    if _term.startswith((b'xterm', b'rxvt')):
        TERMINAL_TITLE = b'\x1b]0;Task {0}\x07'
    elif _term.startswith(b'screen'):
        TERMINAL_TITLE = b'\x1bkTask {0}\x1b\\'
LEN_OF_STATUS = 22
TIME_PRECISION = 2
_BYTE_FACTOR = 1000

class OutputHandler(object):
    """
    The class OutputHandler manages all outputs to the terminal and to files.
    """
    print_lock = threading.Lock()

    def __init__(self, benchmark, sysinfo, compress_results):
        """
        The constructor of OutputHandler collects information about the benchmark and the computer.
        """
        self.compress_results = compress_results
        self.all_created_files = set()
        self.benchmark = benchmark
        self.statistics = Statistics()
        version = self.benchmark.tool_version
        memlimit = None
        timelimit = None
        corelimit = None
        if MEMLIMIT in self.benchmark.rlimits:
            memlimit = str(self.benchmark.rlimits[MEMLIMIT]) + b'B'
        if SOFTTIMELIMIT in self.benchmark.rlimits:
            timelimit = str(self.benchmark.rlimits[SOFTTIMELIMIT]) + b's'
        elif TIMELIMIT in self.benchmark.rlimits:
            timelimit = str(self.benchmark.rlimits[TIMELIMIT]) + b's'
        if CORELIMIT in self.benchmark.rlimits:
            corelimit = str(self.benchmark.rlimits[CORELIMIT])
        os.makedirs(benchmark.log_folder, exist_ok=True)
        self.store_header_in_xml(version, memlimit, timelimit, corelimit)
        self.write_header_to_log(sysinfo)
        if sysinfo:
            self.store_system_info(sysinfo.os, sysinfo.cpu_model, sysinfo.cpu_number_of_cores, sysinfo.cpu_max_frequency, sysinfo.memory, sysinfo.hostname, environment=sysinfo.environment, cpu_turboboost=sysinfo.cpu_turboboost)
        self.xml_file_names = []
        if compress_results:
            self.log_zip = zipfile.ZipFile(benchmark.log_zip, mode=b'w', compression=zipfile.ZIP_DEFLATED)
            self.log_zip_lock = threading.Lock()
            self.all_created_files.add(benchmark.log_zip)
        return

    def store_system_info(self, opSystem, cpu_model, cpu_number_of_cores, cpu_max_frequency, memory, hostname, runSet=None, environment={}, cpu_turboboost=None):
        for systemInfo in self.xml_header.findall(b'systeminfo'):
            if systemInfo.attrib[b'hostname'] == hostname:
                return

        osElem = ET.Element(b'os', {b'name': opSystem})
        cpuElem = ET.Element(b'cpu', {b'model': cpu_model, 
           b'cores': cpu_number_of_cores, 
           b'frequency': str(cpu_max_frequency) + b'Hz'})
        if cpu_turboboost is not None:
            cpuElem.set(b'turboboostActive', str(cpu_turboboost).lower())
        ramElem = ET.Element(b'ram', {b'size': str(memory) + b'B'})
        systemInfo = ET.Element(b'systeminfo', {b'hostname': hostname})
        systemInfo.append(osElem)
        systemInfo.append(cpuElem)
        systemInfo.append(ramElem)
        env = ET.SubElement(systemInfo, b'environment')
        for var, value in sorted(environment.items()):
            ET.SubElement(env, b'var', name=var).text = value

        self.xml_header.append(systemInfo)
        if runSet:
            i = None
            for i, elem in enumerate(runSet.xml):
                if elem.tag == b'run':
                    break

            if i is None:
                runSet.xml.append(systemInfo)
            else:
                runSet.xml.insert(i, systemInfo)
        return

    def set_error(self, msg, runSet=None):
        """
        Mark the benchmark as erroneous, e.g., because the benchmarking tool crashed.
        The message is intended as explanation for the user.
        """
        self.xml_header.set(b'error', msg if msg else b'unknown error')
        if runSet:
            runSet.xml.set(b'error', msg if msg else b'unknown error')

    def store_header_in_xml(self, version, memlimit, timelimit, corelimit):
        self.xml_header = ET.Element(b'result', {b'benchmarkname': self.benchmark.name, 
           b'date': self.benchmark.start_time.strftime(b'%Y-%m-%d %H:%M:%S %Z'), 
           b'starttime': self.benchmark.start_time.isoformat(), 
           b'tool': self.benchmark.tool_name, 
           b'version': version, 
           b'toolmodule': self.benchmark.tool_module, 
           b'generator': b'BenchExec ' + benchexec.__version__})
        if self.benchmark.display_name:
            self.xml_header.set(b'displayName', self.benchmark.display_name)
        if memlimit is not None:
            self.xml_header.set(MEMLIMIT, memlimit)
        if timelimit is not None:
            self.xml_header.set(TIMELIMIT, timelimit)
        if corelimit is not None:
            self.xml_header.set(CORELIMIT, corelimit)
        if self.benchmark.description:
            description_tag = ET.Element(b'description')
            description_tag.text = self.benchmark.description
            self.xml_header.append(description_tag)
        columntitlesElem = ET.Element(b'columns')
        columntitlesElem.append(ET.Element(b'column', {b'title': b'status'}))
        columntitlesElem.append(ET.Element(b'column', {b'title': b'cputime'}))
        columntitlesElem.append(ET.Element(b'column', {b'title': b'walltime'}))
        for column in self.benchmark.columns:
            columnElem = ET.Element(b'column', {b'title': column.title})
            columntitlesElem.append(columnElem)

        self.xml_header.append(columntitlesElem)
        return

    def write_header_to_log(self, sysinfo):
        """
        This method writes information about benchmark and system into txt_file.
        """
        runSetName = None
        run_sets = [ runSet for runSet in self.benchmark.run_sets if runSet.should_be_executed() ]
        if len(run_sets) == 1:
            runSetName = run_sets[0].name
        columnWidth = 25
        simpleLine = b'-' * 60 + b'\n\n'

        def format_line(key, value):
            if value is None:
                return b''
            else:
                return (key + b':').ljust(columnWidth) + str(value).strip() + b'\n'

        def format_byte(key, value):
            if value is None:
                return b''
            else:
                return format_line(key, str(value / _BYTE_FACTOR / _BYTE_FACTOR) + b' MB')

        def format_time(key, value):
            if value is None:
                return b''
            else:
                return format_line(key, str(value) + b' s')

        header = b'   BENCHMARK INFORMATION\n' + (self.benchmark.display_name + b'\n' if self.benchmark.display_name else b'') + format_line(b'benchmark definition', self.benchmark.benchmark_file) + format_line(b'name', self.benchmark.name) + format_line(b'run sets', (b', ').join(run_set.name for run_set in run_sets)) + format_line(b'date', self.benchmark.start_time.strftime(b'%a, %Y-%m-%d %H:%M:%S %Z')) + format_line(b'tool', self.benchmark.tool_name + b' ' + self.benchmark.tool_version) + format_line(b'tool executable', self.benchmark.executable) + format_line(b'options', (b' ').join(map(util.escape_string_shell, self.benchmark.options))) + format_line(b'property file', util.text_or_none(self.benchmark.propertytag))
        if self.benchmark.num_of_threads > 1:
            header += format_line(b'parallel runs', self.benchmark.num_of_threads)
        header += b'resource limits:\n' + format_byte(b'- memory', self.benchmark.rlimits.get(MEMLIMIT)) + format_time(b'- time', self.benchmark.rlimits.get(SOFTTIMELIMIT) or self.benchmark.rlimits.get(TIMELIMIT)) + format_line(b'- cpu cores', self.benchmark.rlimits.get(CORELIMIT))
        header += b'hardware requirements:\n' + format_line(b'- cpu model', self.benchmark.requirements.cpu_model) + format_line(b'- cpu cores', self.benchmark.requirements.cpu_cores) + format_byte(b'- memory', self.benchmark.requirements.memory) + simpleLine
        if sysinfo:
            header += b'   SYSTEM INFORMATION\n' + format_line(b'host', sysinfo.hostname) + format_line(b'os', sysinfo.os) + format_line(b'cpu', sysinfo.cpu_model) + format_line(b'- cores', sysinfo.cpu_number_of_cores) + format_line(b'- max frequency', str(sysinfo.cpu_max_frequency / 1000 / 1000) + b' MHz') + format_line(b'- turbo boost enabled', sysinfo.cpu_turboboost) + format_byte(b'ram', sysinfo.memory) + simpleLine
        self.description = header
        txt_file_name = self.get_filename(runSetName, b'txt')
        self.txt_file = filewriter.FileWriter(txt_file_name, self.description)
        self.all_created_files.add(txt_file_name)
        return

    def output_before_run_set(self, runSet, start_time=None):
        """
        The method output_before_run_set() calculates the length of the
        first column for the output in terminal and stores information
        about the runSet in XML.
        @param runSet: current run set
        """
        xml_file_name = self.get_filename(runSet.name, b'xml')
        identifier_names = [ run.identifier for run in runSet.runs ]
        runSet.common_prefix = util.common_base_dir(identifier_names)
        if runSet.common_prefix:
            runSet.common_prefix += os.path.sep
        runSet.max_length_of_filename = max(len(file) for file in identifier_names) if identifier_names else 20
        runSet.max_length_of_filename = max(20, runSet.max_length_of_filename - len(runSet.common_prefix))
        numberOfFiles = len(runSet.runs)
        numberOfFilesStr = b'     (1 file)' if numberOfFiles == 1 else (b'     ({0} files)').format(numberOfFiles)
        util.printOut(b'\nexecuting run set' + (b" '" + runSet.name + b"'" if runSet.name else b'') + numberOfFilesStr + TERMINAL_TITLE.format(runSet.full_name))
        self.writeRunSetInfoToLog(runSet)
        for run in runSet.runs:
            run.resultline = self.format_sourcefile_name(run.identifier, runSet)
            if run.sourcefiles:
                adjusted_identifier = util.relative_path(run.identifier, xml_file_name)
            else:
                adjusted_identifier = run.identifier
            run_attributes = {b'name': adjusted_identifier}
            if run.sourcefiles:
                adjusted_sourcefiles = [ util.relative_path(s, xml_file_name) for s in run.sourcefiles ]
                run_attributes[b'files'] = b'[' + (b', ').join(adjusted_sourcefiles) + b']'
            run.xml = ET.Element(b'run', run_attributes)
            if run.specific_options:
                run.xml.set(b'options', (b' ').join(run.specific_options))
            if run.properties:
                all_properties = [ prop_name for prop in run.properties for prop_name in prop.names ]
                run.xml.set(b'properties', (b' ').join(sorted(all_properties)))

        block_name = runSet.blocks[0].name if len(runSet.blocks) == 1 else None
        runSet.xml = self.runs_to_xml(runSet, runSet.runs, block_name)
        if start_time:
            runSet.xml.set(b'starttime', start_time.isoformat())
        elif not self.benchmark.config.start_time:
            runSet.xml.set(b'starttime', util.read_local_time().isoformat())
        self.txt_file.append(self.run_set_to_text(runSet), False)
        runSet.xml_file_name = xml_file_name
        self._write_rough_result_xml_to_file(runSet.xml, runSet.xml_file_name)
        runSet.xml_file_last_modified_time = util.read_monotonic_time()
        self.all_created_files.add(runSet.xml_file_name)
        self.xml_file_names.append(runSet.xml_file_name)
        return

    def output_for_skipping_run_set(self, runSet, reason=None):
        """
        This function writes a simple message to terminal and logfile,
        when a run set is skipped.
        There is no message about skipping a run set in the xml-file.
        """
        util.printOut(b'\nSkipping run set' + (b" '" + runSet.name + b"'" if runSet.name else b'') + (b' ' + reason if reason else b''))
        runSetInfo = b'\n\n'
        if runSet.name:
            runSetInfo += runSet.name + b'\n'
        runSetInfo += (b'Run set {0} of {1}: skipped {2}\n').format(runSet.index, len(self.benchmark.run_sets), reason or b'')
        self.txt_file.append(runSetInfo)

    def writeRunSetInfoToLog(self, runSet):
        """
        This method writes the information about a run set into the txt_file.
        """
        runSetInfo = b'\n\n'
        if runSet.name:
            runSetInfo += runSet.name + b'\n'
        runSetInfo += (b"Run set {0} of {1} with options '{2}' and propertyfile '{3}'\n\n").format(runSet.index, len(self.benchmark.run_sets), (b' ').join(runSet.options), util.text_or_none(runSet.propertytag))
        titleLine = self.create_output_line(runSet, b'inputfile', b'status', b'cpu time', b'wall time', b'host', self.benchmark.columns, True)
        runSet.simpleLine = b'-' * len(titleLine)
        runSetInfo += titleLine + b'\n' + runSet.simpleLine + b'\n'
        self.txt_file.append(runSetInfo)

    def output_before_run(self, run):
        """
        The method output_before_run() prints the name of a file to terminal.
        It returns the name of the logfile.
        @param run: a Run object
        """
        runSet = run.runSet
        try:
            OutputHandler.print_lock.acquire()
            try:
                runSet.started_runs += 1
            except AttributeError:
                runSet.started_runs = 1

            timeStr = time.strftime(b'%H:%M:%S', time.localtime()) + b'   '
            progressIndicator = (b' ({0}/{1})').format(runSet.started_runs, len(runSet.runs))
            terminalTitle = TERMINAL_TITLE.format(runSet.full_name + progressIndicator)
            if self.benchmark.num_of_threads == 1:
                util.printOut(terminalTitle + timeStr + self.format_sourcefile_name(run.identifier, runSet), b'')
            else:
                util.printOut(terminalTitle + timeStr + b'starting   ' + self.format_sourcefile_name(run.identifier, runSet))
        finally:
            OutputHandler.print_lock.release()

    def output_after_run(self, run):
        """
        The method output_after_run() prints filename, result, time and status
        of a run to terminal and stores all data in XML
        """
        cputime_str = util.format_number(run.values.get(b'cputime'), TIME_PRECISION)
        walltime_str = util.format_number(run.values.get(b'walltime'), TIME_PRECISION)
        for column in run.columns:
            if column.number_of_digits is not None:
                if not column.value.isdigit() and column.value[-2:-1].isdigit():
                    column.value = column.value[:-1]
                try:
                    floatValue = float(column.value)
                    column.value = util.format_number(floatValue, column.number_of_digits)
                except ValueError:
                    pass

        run.resultline = self.create_output_line(run.runSet, run.identifier, run.status, cputime_str, walltime_str, run.values.get(b'host'), run.columns)
        self.add_values_to_run_xml(run)
        statusStr = COLOR_DIC[run.category].format(run.status.ljust(LEN_OF_STATUS))
        try:
            OutputHandler.print_lock.acquire()
            valueStr = statusStr + cputime_str.rjust(8) + walltime_str.rjust(8)
            if self.benchmark.num_of_threads == 1:
                util.printOut(valueStr)
            else:
                timeStr = time.strftime(b'%H:%M:%S', time.localtime()) + b'              '
                util.printOut(timeStr + self.format_sourcefile_name(run.identifier, run.runSet) + valueStr)
            self.txt_file.append(self.run_set_to_text(run.runSet), False)
            self.statistics.add_result(run)
            currentTime = util.read_monotonic_time()
            if currentTime - run.runSet.xml_file_last_modified_time > 60:
                self._write_rough_result_xml_to_file(run.runSet.xml, run.runSet.xml_file_name)
                run.runSet.xml_file_last_modified_time = util.read_monotonic_time()
        finally:
            OutputHandler.print_lock.release()

        if self.compress_results:
            log_file_path = os.path.relpath(run.log_file, os.path.join(self.benchmark.log_folder, os.pardir))
            with self.log_zip_lock:
                self.log_zip.write(run.log_file, log_file_path)
            os.remove(run.log_file)
        else:
            self.all_created_files.add(run.log_file)
        if os.path.isdir(run.result_files_folder):
            self.all_created_files.add(run.result_files_folder)
        return

    def output_after_run_set(self, runSet, cputime=None, walltime=None, energy={}, cache={}, end_time=None):
        """
        The method output_after_run_set() stores the times of a run set in XML.
        @params cputime, walltime: accumulated times of the run set
        """
        self.add_values_to_run_set_xml(runSet, cputime, walltime, energy, cache)
        if end_time:
            runSet.xml.set(b'endtime', end_time.isoformat())
        elif not self.benchmark.config.start_time:
            runSet.xml.set(b'endtime', util.read_local_time().isoformat())
        self._write_pretty_result_xml_to_file(runSet.xml, runSet.xml_file_name)
        if len(runSet.blocks) > 1:
            for block in runSet.blocks:
                blockFileName = self.get_filename(runSet.name, block.name + b'.xml')
                block_xml = self.runs_to_xml(runSet, block.runs, block.name)
                block_xml.set(b'starttime', runSet.xml.get(b'starttime'))
                if runSet.xml.get(b'endtime'):
                    block_xml.set(b'endtime', runSet.xml.get(b'endtime'))
                self._write_pretty_result_xml_to_file(block_xml, blockFileName)

        self.txt_file.append(self.run_set_to_text(runSet, True, cputime, walltime, energy))

    def run_set_to_text(self, runSet, finished=False, cputime=0, walltime=0, energy={}):
        lines = []
        for run in runSet.runs:
            lines.append(run.resultline)

        lines.append(runSet.simpleLine)
        if finished:
            endline = (b'Run set {0}').format(runSet.index)
            cputime_str = b'None' if cputime is None else util.format_number(cputime, TIME_PRECISION)
            walltime_str = b'None' if walltime is None else util.format_number(walltime, TIME_PRECISION)
            lines.append(self.create_output_line(runSet, endline, b'done', cputime_str, walltime_str, b'-', []))
        return (b'\n').join(lines) + b'\n'

    def runs_to_xml(self, runSet, runs, blockname=None):
        """
        This function creates the XML structure for a list of runs
        """
        runsElem = util.copy_of_xml_element(self.xml_header)
        runsElem.set(b'options', (b' ').join(runSet.options))
        if blockname is not None:
            runsElem.set(b'block', blockname)
            runsElem.set(b'name', (runSet.real_name + b'.' if runSet.real_name else b'') + blockname)
        else:
            if runSet.real_name:
                runsElem.set(b'name', runSet.real_name)
            for run in runs:
                runsElem.append(run.xml)

        return runsElem

    def add_values_to_run_xml(self, run):
        """
        This function adds the result values to the XML representation of a run.
        """
        runElem = run.xml
        for elem in list(runElem):
            runElem.remove(elem)

        self.add_column_to_xml(runElem, b'status', run.status)
        self.add_column_to_xml(runElem, b'@category', run.category)
        self.add_column_to_xml(runElem, b'', run.values)
        for column in run.columns:
            self.add_column_to_xml(runElem, column.title, column.value)

        runElem[:] = sorted(runElem, key=lambda elem: (elem.get(b'hidden', b''), elem.get(b'title')))

    def add_values_to_run_set_xml(self, runSet, cputime, walltime, energy, cache):
        """
        This function adds the result values to the XML representation of a runSet.
        """
        self.add_column_to_xml(runSet.xml, b'cputime', cputime)
        self.add_column_to_xml(runSet.xml, b'walltime', walltime)
        energy = intel_cpu_energy.format_energy_results(energy)
        for energy_key, energy_value in energy.items():
            self.add_column_to_xml(runSet.xml, energy_key, energy_value)

        for cache_key, cache_value in cache.items():
            self.add_column_to_xml(runSet.xml, cache_key, cache_value)

    def add_column_to_xml(self, xml, title, value, prefix=b'', value_suffix=b''):
        if value is None:
            return
        else:
            if isinstance(value, dict):
                for key, value in value.items():
                    if prefix:
                        common_prefix = prefix + b'_' + title
                    else:
                        common_prefix = title
                    self.add_column_to_xml(xml, key, value, prefix=common_prefix)

                return
            if hasattr(value, b'__getitem__') and not isinstance(value, (str, bytes)):
                value = (b',').join(map(str, value))
            elif isinstance(value, datetime.datetime):
                value = value.isoformat()
            if prefix:
                title = prefix + b'_' + title
            if title[0] == b'@':
                hidden = True
                title = title[1:]
            else:
                hidden = False
            if not value_suffix and not isinstance(value, (str, bytes)):
                if title.startswith(b'cputime') or title.startswith(b'walltime'):
                    value_suffix = b's'
                elif title.startswith(b'cpuenergy'):
                    value_suffix = b'J'
                elif title.startswith(b'blkio-') or title.startswith(b'memory'):
                    value_suffix = b'B'
                elif title.startswith(b'llc'):
                    if not title.startswith(b'llc_misses'):
                        value_suffix = b'B'
                elif title.startswith(b'mbm'):
                    value_suffix = b'B/s'
            value = (b'{}{}').format(value, value_suffix)
            if hidden:
                attributes = {b'title': title, b'value': value, b'hidden': b'true'}
            else:
                attributes = {b'title': title, b'value': value}
            xml.append(ET.Element(b'column', attributes))
            return

    def create_output_line(self, runSet, sourcefile, status, cputime_delta, walltime_delta, host, columns, isFirstLine=False):
        """
        @param sourcefile: title of a sourcefile
        @param status: status of programm
        @param cputime_delta: time from running the programm
        @param walltime_delta: time from running the programm
        @param columns: list of columns with a title or a value
        @param isFirstLine: boolean for different output of headline and other lines
        @return: a line for the outputFile
        """
        lengthOfTime = 12
        minLengthOfColumns = 8
        outputLine = self.format_sourcefile_name(sourcefile, runSet) + status.ljust(LEN_OF_STATUS) + cputime_delta.rjust(lengthOfTime) + walltime_delta.rjust(lengthOfTime) + str(host).rjust(lengthOfTime)
        for column in columns:
            columnLength = max(minLengthOfColumns, len(column.title)) + 2
            if isFirstLine:
                value = column.title
            else:
                value = column.value
            outputLine = outputLine + str(value).rjust(columnLength)

        return outputLine

    def output_after_benchmark(self, isStoppedByInterrupt):
        stats = str(self.statistics)
        util.printOut(stats)
        self.txt_file.append(stats)
        if self.xml_file_names:

            def _find_file_relative(name):
                """
                Find a file with the given name in the same directory as this script.
                Returns a path relative to the current directory, or None.
                """
                path = os.path.join(os.path.dirname(sys.argv[0]), name)
                if not os.path.isfile(path):
                    path = os.path.join(os.path.dirname(__file__), os.path.pardir, name)
                    if not os.path.isfile(path):
                        return None
                if os.path.dirname(path) in os.environ[b'PATH'].split(os.pathsep):
                    return os.path.basename(path)
                else:
                    path = os.path.relpath(path)
                    if path == name:
                        path = b'./' + path
                    return path

            tableGeneratorPath = _find_file_relative(b'table-generator.py') or _find_file_relative(b'table-generator')
            if tableGeneratorPath:
                xml_file_names = [ file + b'.bz2' for file in self.xml_file_names ] if self.compress_results else self.xml_file_names
                util.printOut((b"In order to get HTML and CSV tables, run\n{0} '{1}'").format(tableGeneratorPath, (b"' '").join(xml_file_names)))
        if isStoppedByInterrupt:
            util.printOut(b'\nScript was interrupted by user, some runs may not be done.\n')

    def close(self):
        """Do all necessary cleanup."""
        if self.compress_results:
            with self.log_zip_lock:
                self.log_zip.close()

    def get_filename(self, runSetName, fileExtension):
        """
        This function returns the name of the file for a run set
        with an extension ("txt", "xml").
        """
        fileName = self.benchmark.output_base_name + b'.results.'
        if runSetName:
            fileName += runSetName + b'.'
        return fileName + fileExtension

    def format_sourcefile_name(self, fileName, runSet):
        """
        Formats the file name of a program for printing on console.
        """
        if fileName.startswith(runSet.common_prefix):
            fileName = fileName[len(runSet.common_prefix):]
        return fileName.ljust(runSet.max_length_of_filename + 4)

    def _write_rough_result_xml_to_file(self, xml, filename):
        """Write a rough string version of the XML (for temporary files)."""
        error = xml.get(b'error', None)
        xml.set(b'error', b'incomplete')
        temp_filename = filename + b'.tmp'
        with open(temp_filename, b'wb') as (file):
            ET.ElementTree(xml).write(file, encoding=b'utf-8', xml_declaration=True)
        os.rename(temp_filename, filename)
        if error is not None:
            xml.set(b'error', error)
        else:
            del xml.attrib[b'error']
        return

    def _write_pretty_result_xml_to_file(self, xml, filename):
        """Writes a nicely formatted XML file with DOCTYPE, and compressed if necessary."""
        if self.compress_results:
            actual_filename = filename + b'.bz2'
            open_func = bz2.BZ2File
        else:
            actual_filename = filename + b'.tmp'
            open_func = open
        with io.TextIOWrapper(open_func(actual_filename, b'wb'), encoding=b'utf-8') as (file):
            rough_string = ET.tostring(xml, encoding=b'unicode')
            reparsed = minidom.parseString(rough_string)
            doctype = minidom.DOMImplementation().createDocumentType(b'result', RESULT_XML_PUBLIC_ID, RESULT_XML_SYSTEM_ID)
            reparsed.insertBefore(doctype, reparsed.documentElement)
            reparsed.writexml(file, indent=b'', addindent=b'  ', newl=b'\n', encoding=b'utf-8')
        if self.compress_results:
            try:
                os.remove(filename)
            except OSError:
                pass

            self.all_created_files.discard(filename)
            self.all_created_files.add(actual_filename)
        else:
            os.rename(actual_filename, filename)
            self.all_created_files.add(filename)
        return filename


class Statistics(object):

    def __init__(self):
        self.dic = collections.defaultdict(int)
        self.counter = 0
        self.score = 0
        self.max_score = 0

    def add_result(self, run):
        self.counter += 1
        self.dic[run.category] += 1
        self.dic[(run.category, result.get_result_classification(run.status))] += 1
        for prop in run.properties:
            self.score += prop.compute_score(run.category, run.status)
            self.max_score += prop.max_score(run.expected_results.get(prop.filename))

    def __str__(self):
        correct = self.dic[result.CATEGORY_CORRECT]
        correct_true = self.dic[(result.CATEGORY_CORRECT, result.RESULT_CLASS_TRUE)]
        correct_false = correct - correct_true
        incorrect = self.dic[result.CATEGORY_WRONG]
        incorrect_true = self.dic[(result.CATEGORY_WRONG, result.RESULT_CLASS_TRUE)]
        incorrect_false = incorrect - incorrect_true
        width = 6
        output = [
         b'',
         b'Statistics:' + str(self.counter).rjust(width + 9) + b' Files',
         b'  correct:          ' + str(correct).rjust(width),
         b'    correct true:   ' + str(correct_true).rjust(width),
         b'    correct false:  ' + str(correct_false).rjust(width),
         b'  incorrect:        ' + str(incorrect).rjust(width),
         b'    incorrect true: ' + str(incorrect_true).rjust(width),
         b'    incorrect false:' + str(incorrect_false).rjust(width),
         b'  unknown:          ' + str(self.dic[result.CATEGORY_UNKNOWN] + self.dic[result.CATEGORY_ERROR]).rjust(width)]
        if self.max_score:
            output.append(b'  Score:            ' + str(self.score).rjust(width) + b' (max: ' + str(self.max_score) + b')')
        output.append(b'')
        return (b'\n').join(output)