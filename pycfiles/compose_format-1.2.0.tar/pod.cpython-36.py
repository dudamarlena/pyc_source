# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/pod.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 3673 bytes
__doc__ = '\nSubcommand for working with pods\n\nThis subcommand provides one action:\n\n- exec\n\nThe `exec` action will execute the given command within the specified pod.\nFor example, the following command will launch an interactive shell in the `app`\ncontainer:\n\n```\ncompose-flow -e dev service exec web /bin/bash\n```\n'
import argparse, logging, os, re, time
from compose_flow.kube.mixins import KubeMixIn
from .base import BaseSubcommand
from compose_flow import errors, shell

class Pod(BaseSubcommand, KubeMixIn):
    command_name = 'pod'
    setup_environment = True
    setup_profile = False

    @property
    def namespace(self):
        return self.workflow.args.namespace or self.workflow.project_name

    @classmethod
    def fill_subparser(cls, parser, subparser):
        subparser.epilog = __doc__
        subparser.formatter_class = argparse.RawDescriptionHelpFormatter
        subparser.add_argument('--container',
          type=str,
          default=None,
          help='which container to exec into within a pod')
        subparser.add_argument('-i',
          '--container-index',
          type=int,
          default=0,
          help="exec into the i'th container")
        subparser.add_argument('--retries',
          type=int, default=30, help='number of times to retry')
        subparser.add_argument('--namespace',
          type=str,
          help='override the namespace. defaults to project name.')
        subparser.add_argument('action', help='action to run. options: [exec,]')
        subparser.add_argument('pod_name', help='name of desired pod, e.g. `web`')

    def action_exec(self):
        args = self.workflow.args
        self.switch_rancher_context()
        for i in range(args.retries):
            try:
                self.run_pod()
            except errors.NoContainer:
                time.sleep(1.0)
            else:
                break

    def format_pods_output(self, list_raw, include_header=False):
        list_raw = list_raw.split('\n')
        list_raw = [row_str.split(' ') for row_str in list_raw]
        if not include_header:
            list_raw = list_raw[1:]
        cleaned_output = []
        for row in list_raw:
            cleaned_row = [element for element in row if element]
            cleaned_output.append(cleaned_row)

        return [row for row in cleaned_output if row]

    def run_pod(self):
        args = self.workflow.args
        pod = self.select_pod()
        if args.container:
            target_container = f"--container {args.container}"
        else:
            target_container = ''
        command = f"{self.kubectl_command} -n {self.namespace} exec -it {pod} {target_container} -- {' '.join(self.workflow.args_remainder)}"
        logging.debug(f"command={command}")
        return shell.execute(command, (os.environ), _fg=True)

    def select_pod(self):
        args = self.workflow.args
        pods_list_raw = self.list_pods(namespace=(self.namespace))
        pods_list = self.format_pods_output(pods_list_raw)
        pod_name_re = f"^{args.pod_name}\\-.*\\-.*$"
        matched_pods = [p for p in pods_list if re.match(pod_name_re, p[0])]
        try:
            target_pod = matched_pods[args.container_index][0]
            return target_pod
        except IndexError:
            raise errors.PodNotFound(f"Could not find pod with index {args.container_index} matching regex {pod_name_re}")