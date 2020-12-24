# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/mcli/shell.py
# Compiled at: 2019-02-12 12:07:18
# Size of source mod 2**32: 2292 bytes
import logging, colorama
from mercury_sdk.rpc.job import SimpleJob
LOG = logging.getLogger(__name__)
PROMPT = f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}(♀)︎{colorama.Fore.MAGENTA}~>{colorama.Style.RESET_ALL} "

class MercuryShell:
    __doc__ = ' Ridiculously simple shell (no readline support) '

    def __init__(self, rpc_client, prompt=PROMPT, initial_query=None, raw=False, quiet=False):
        self.rpc_client = rpc_client
        self.prompt = prompt
        self.query = initial_query
        self.raw = raw
        self.quiet = quiet

    def run_job(self, instruction):
        instruction = 'bash -c "{}"'.format(instruction)
        s = SimpleJob((self.rpc_client), (self.query), 'run', job_args=[
         instruction])
        s.start()
        s.join(poll_interval=0.2)
        for t in s.tasks['tasks']:
            if not self.quiet:
                if not self.raw:
                    co = colorama.Fore.CYAN if t['message']['returncode'] == 0 else colorama.Fore.LIGHTRED_EX
                    print(f"{co}{t['mercury_id']}{colorama.Style.RESET_ALL}\n")
                stdout = t['message']['stdout']
                if stdout:
                    print(stdout)
                stderr = t['message']['stderr']
                if stderr:
                    print(stderr)

    def input_loop(self):
        while True:
            try:
                instruction = input(self.prompt)
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                print()
                break

            if not instruction:
                continue
            if instruction == 'exit':
                break
            if instruction.strip()[0] == '!':
                if not len(instruction) > 1:
                    print('Shell command missing')
                print('THIS IS A SHELL ESCAPE: {}'.format(instruction[1:]))
            else:
                self.run_job(instruction)


if __name__ == '__main__':
    from mercury_sdk.http.rpc import JobInterfaceBase
    ib = JobInterfaceBase('http://localhost:9005')
    _s = MercuryShell(ib, initial_query={})
    _s.input_loop()