# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/clusterflow/clusterflow.py
# Compiled at: 2019-11-13 05:22:42
""" MultiQC module to parse output from Cluster Flow """
from __future__ import print_function
from collections import OrderedDict
import datetime, logging, re, os, time
from multiqc.plots import table
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """
    Cluster Flow module class, parses run logs.
    """

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Cluster Flow', anchor='clusterflow', href='http://clusterflow.io', info='is a simple and flexible bioinformatics pipeline tool.')
        self.clusterflow_commands = dict()
        self.clusterflow_runfiles = dict()
        for f in self.find_log_files('clusterflow/logs', filehandles=True):
            self.parse_clusterflow_logs(f)
            self.add_data_source(f, 'log')

        for f in self.find_log_files('clusterflow/runfiles', filehandles=True):
            parsed_data = self.parse_clusterflow_runfiles(f)
            if parsed_data is not None:
                self.clusterflow_runfiles[f['s_name']] = parsed_data
                self.add_data_source(f, 'runfile')

        self.clusterflow_commands = self.ignore_samples(self.clusterflow_commands)
        self.clusterflow_runfiles = self.ignore_samples(self.clusterflow_runfiles)
        if len(self.clusterflow_commands) == 0 and len(self.clusterflow_runfiles) == 0:
            raise UserWarning
        num_log_pipelines = len(self.clusterflow_commands)
        num_runfile_pipelines = len(set(d.get('pipeline_id', 'unknown') for d in self.clusterflow_runfiles.values()))
        log.info(('Found {} pipelines').format(max(num_log_pipelines, num_runfile_pipelines)))
        log.debug(('Found {} log pipelines').format(num_log_pipelines))
        log.debug(('Found {} runfile pipelines').format(num_runfile_pipelines))
        if len(self.clusterflow_runfiles) > 0:
            self.clusterflow_pipelines_section()
        if len(self.clusterflow_commands) > 0:
            self.clusterflow_commands_table()
        return

    def parse_clusterflow_logs(self, f):
        """ Parse Clusterflow logs """
        module = None
        job_id = None
        pipeline_id = None
        for l in f['f']:
            module_r = re.match('Module:\\s+(.+)$', l)
            if module_r:
                module = module_r.group(1)
            job_id_r = re.match('Job ID:\\s+(.+)$', l)
            if job_id_r:
                job_id = job_id_r.group(1)
                if module is not None:
                    pipeline_r = re.match('(cf_.+)_' + re.escape(module) + '_\\d+$', job_id)
                    if pipeline_r:
                        pipeline_id = pipeline_r.group(1)
            if l.startswith('###CFCMD'):
                if pipeline_id is None:
                    pipeline_id = 'unknown'
                if pipeline_id not in self.clusterflow_commands.keys():
                    self.clusterflow_commands[pipeline_id] = list()
                self.clusterflow_commands[pipeline_id].append(l[8:])

        return

    def clusterflow_commands_table(self):
        """ Make a table of the Cluster Flow commands """
        desc = 'Every Cluster Flow run will have many different commands.\n            MultiQC splits these by whitespace, collects by the tool name\n            and shows the first command found. Any terms not found in <em>all</em> subsequent\n            calls are replaced with <code>[variable]</code>\n            <em>(typically input and ouput filenames)</em>. Each column is for one Cluster Flow run.'
        tool_cmds = OrderedDict()
        headers = dict()
        for pipeline_id, commands in self.clusterflow_commands.items():
            headers[pipeline_id] = {'scale': False}
            self.var_html = '<span style="background-color:#dedede; color:#999;">[variable]</span>'
            tool_cmd_parts = OrderedDict()
            for cmd in commands:
                s = cmd.split()
                tool = self._guess_cmd_name(s)
                if tool not in tool_cmd_parts.keys():
                    tool_cmd_parts[tool] = list()
                tool_cmd_parts[tool].append(s)

            for tool, cmds in tool_cmd_parts.items():
                cons_cmd = self._replace_variable_chunks(cmds)
                variable_count = cons_cmd.count(self.var_html)
                if variable_count == len(cmds[0]) - 1 and len(cmds[0]) > 2:
                    for subcmd in set([ x[1] for x in cmds ]):
                        sub_cons_cmd = self._replace_variable_chunks([ cmd for cmd in cmds if cmd[1] == subcmd ])
                        tool = ('{} {}').format(tool, subcmd)
                        if tool not in tool_cmds:
                            tool_cmds[tool] = dict()
                        tool_cmds[tool][pipeline_id] = ('<code style="white-space:nowrap;">{}</code>').format((' ').join(sub_cons_cmd))

                else:
                    if tool not in tool_cmds:
                        tool_cmds[tool] = dict()
                    tool_cmds[tool][pipeline_id] = ('<code style="white-space:nowrap;">{}</code>').format((' ').join(cons_cmd))

        table_config = {'namespace': 'Cluster Flow', 
           'id': 'clusterflow-commands-table', 
           'table_title': 'Cluster Flow Commands', 
           'col1_header': 'Tool', 
           'sortRows': False, 
           'no_beeswarm': True}
        self.add_section(name='Commands', anchor='clusterflow-commands', description=desc, plot=table.plot(tool_cmds, headers, table_config))

    def _replace_variable_chunks(self, cmds):
        """ List through a list of command chunks. Return a single list
        with any variable bits blanked out. """
        cons_cmd = None
        while cons_cmd is None:
            for cmd in cmds:
                if cons_cmd is None:
                    cons_cmd = cmd[:]
                else:
                    for idx, s in enumerate(cons_cmd):
                        if s not in cmd:
                            cons_cmd[idx] = self.var_html

        return cons_cmd

    def _guess_cmd_name(self, cmd):
        """ Manually guess some known command names, where we can
        do a better job than the automatic parsing. """
        if cmd[0] == 'zcat' and 'bowtie' in cmd:
            return 'bowtie'
        if cmd[0] == 'samtools':
            return (' ').join(cmd[0:2])
        if cmd[0] == 'java':
            jars = [ s for s in cmd if '.jar' in s ]
            return os.path.basename(jars[0].replace('.jar', ''))
        return cmd[0]

    def parse_clusterflow_runfiles(self, f):
        """ Parse run files generated by Cluster Flow.
        Currently gets pipeline IDs and associated steps."""
        data = dict()
        in_comment = False
        seen_pipeline = False
        cf_file = False
        for l in f['f']:
            l = l.rstrip()
            if 'Cluster Flow' in l:
                cf_file = True
            if l.startswith('Pipeline: '):
                data['pipeline_name'] = l[10:]
            if l.startswith('Pipeline ID: '):
                data['pipeline_id'] = l[13:]
            if l.startswith('Created at '):
                data['pipeline_start'] = l[11:]
            if l.startswith('@'):
                s = l.split(None, 1)
                key = s[0].replace('@', '').strip()
                try:
                    data[key] = ('\t').join(s[1:])
                except IndexError:
                    data[key] = True

            if l.startswith('/*'):
                in_comment = True
            if l.startswith('*/'):
                in_comment = False
            if in_comment:
                if 'comment' not in data:
                    data['comment'] = ''
                data['comment'] += l + '\n'
            if l.strip().startswith('#'):
                if 'pipeline_steps' not in data:
                    data['pipeline_steps'] = []
                data['pipeline_steps'].append(l)
                seen_pipeline = True
            elif seen_pipeline:
                s = l.split('\t')
                if len(s) > 1:
                    if 'files' not in data:
                        data['files'] = OrderedDict()
                    if s[0] not in data['files']:
                        data['files'][s[0]] = []
                    data['files'][s[0]].append(s[1:])

        dt = None
        if 'pipeline_id' in data:
            s = data['pipeline_id'].split('_')
            dt = datetime.datetime.fromtimestamp(int(s[(-1)]))
        elif 'pipeline_start' in data:
            dt_r = re.match('(\\d{2}):(\\d{2}), (\\d{2})-(\\d{2})-(\\d{4})', data['pipeline_start'])
            if dt_r:
                dt = datetime.datetime(int(dt_r.group(5)), int(dt_r.group(4)), int(dt_r.group(3)), int(dt_r.group(1)), int(dt_r.group(2)))
        if not cf_file:
            return
        else:
            if dt is not None:
                data['pipeline_start_dateparts'] = {'year': dt.year, 'month': dt.month, 
                   'day': dt.day, 
                   'hour': dt.hour, 
                   'minute': dt.minute, 
                   'second': dt.second, 
                   'microsecond': dt.microsecond, 
                   'timestamp': time.mktime(dt.timetuple())}
            if 'pipeline_id' not in data:
                if 'pipeline_name' in data and 'pipeline_start_dateparts' in data:
                    log.debug(('Trying to guess pipeline ID for file "{}"').format(f['fn']))
                    data['pipeline_id'] = ('cf_{}_{}').format(data['pipeline_name'], data['pipeline_start_dateparts']['timestamp'])
            return data

    def clusterflow_pipelines_section(self):
        """ Generate HTML for section about pipelines, generated from
        information parsed from run files. """
        data = dict()
        pids_guessed = ''
        for f, d in self.clusterflow_runfiles.items():
            pid = d.get('pipeline_id', 'unknown')
            if d.get('pipeline_id_guess', False) is True:
                pid += '*'
                pids_guessed = ' Project IDs with an asterisk may be inaccurate.'
            num_starting_files = 0
            for step_name, files in d.get('files', {}).items():
                if step_name.startswith('start'):
                    num_starting_files += len(files)

            if 'pipeline_start_dateparts' in d:
                dt = d['pipeline_start_dateparts']
                d['pipeline_start'] = ('{}-{:02d}-{:02d} {:02d}:{:02d}').format(dt['year'], dt['month'], dt['day'], dt['hour'], dt['minute'])
            if pid not in data:
                data[pid] = d
                data[pid]['num_starting_files'] = int(num_starting_files)
            else:
                data[pid]['num_starting_files'] += int(num_starting_files)

        headers = OrderedDict()
        headers['pipeline_name'] = {'title': 'Pipeline Name'}
        headers['pipeline_start'] = {'title': 'Date Started', 'description': 'Date and time that pipeline was started (YYYY-MM-DD HH:SS)'}
        headers['genome'] = {'title': 'Genome ID', 'description': 'ID of reference genome used'}
        headers['num_starting_files'] = {'title': '# Starting Files', 'format': '{:,.0f}', 'description': 'Number of input files at start of pipeline run.'}
        table_config = {'namespace': 'Cluster Flow', 
           'id': 'clusterflow-pipelines-table', 
           'table_title': 'Cluster Flow Pipelines', 
           'col1_header': 'Pipeline ID', 
           'no_beeswarm': True, 
           'save_file': True}
        self.add_section(name='Pipelines', anchor='clusterflow-pipelines', description=('Information about pipelines is parsed from <code>*.run</code> files. {}').format(pids_guessed), plot=table.plot(data, headers, table_config), content=self.clusterflow_pipelines_printout())

    def clusterflow_pipelines_printout(self):
        """ Print the steps used in each Cluster Flow pipeline """
        data = dict()
        html = ''
        for f, d in self.clusterflow_runfiles.items():
            pid = d.get('pipeline_id', 'unknown')
            data[pid] = [
             d.get('pipeline_name'),
             ('\n').join(d.get('pipeline_steps', []))]

        for pid, d in data.items():
            html += ('\n                <div class="panel panel-default">\n                    <div class="panel-heading"><h3 class="panel-title">Pipeline Steps: {} (<code>{}</code>)</h3></div>\n                    <pre class="panel-body" style="border:0; background-color:transparent; padding:0 15px; margin:0; color:#666; font-size:90%;">{}</pre>\n                </div>\n                ').format(pid, d[0], d[1])

        return html