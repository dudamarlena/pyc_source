# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/nanorc.py
# Compiled at: 2012-08-07 05:06:10
import os
_content1 = '\n## Nanorc files\ninclude "/usr/share/nano/nanorc.nanorc"\n\n## C/C++\ninclude "/usr/share/nano/c.nanorc"\n\n## Cascading Style Sheets\ninclude "/usr/share/nano/css.nanorc"\n\n## Debian files\ninclude "/usr/share/nano/debian.nanorc"\n\n## Gentoo files\ninclude "/usr/share/nano/gentoo.nanorc"\n\n## HTML\ninclude "/usr/share/nano/html.nanorc"\n\n## PHP\ninclude "/usr/share/nano/php.nanorc"\n\n## TCL\ninclude "/usr/share/nano/tcl.nanorc"\n\n## TeX\ninclude "/usr/share/nano/tex.nanorc"\n\n## Quoted emails (under e.g. mutt)\ninclude "/usr/share/nano/mutt.nanorc"\n\n## Patch files\ninclude "/usr/share/nano/patch.nanorc"\n\n## Manpages\ninclude "/usr/share/nano/man.nanorc"\n\n## Groff\ninclude "/usr/share/nano/groff.nanorc"\n\n## Perl\ninclude "/usr/share/nano/perl.nanorc"\n\n## Python\ninclude "/usr/share/nano/python.nanorc"\n\n## Ruby\ninclude "/usr/share/nano/ruby.nanorc"\n\n## Java\ninclude "/usr/share/nano/java.nanorc"\n\n## AWK\ninclude "/usr/share/nano/awk.nanorc"\n\n## Assembler\ninclude "/usr/share/nano/asm.nanorc"\n\n## Bourne shell scripts\ninclude "/usr/share/nano/sh.nanorc"\n\n## POV-Ray\ninclude "/usr/share/nano/pov.nanorc"\n\n## XML-type files\ninclude "/usr/share/nano/xml.nanorc"\n\n## Custom coloring for VHDL files.\nsyntax "vhdl" "\\.vhdl$"\nicolor brightblue "def [0-9A-Z_]+"\ncolor brightred "\\<(abs|access|after|alias|all|and|architecture|array|assert|attribute|begin|block|body|buffer|bus|case|component|configuration|constant|disconnect|downto|else|elsif|end|entity|exit|file|for|function|generate|generic|group|guarded|if|impure|in|inertial|inout|is|label|library|linkage|literal|loop|map|mod|nand|new|next|nor|not|null|of|on|open|or|others|out|package|port|postponed|procedure|process|pure|range|record|register|reject|rem|report|return|rol|ror|select|severity|signal|shared|sla|sll|sra|srl|subtype|then|to|transport|type|unaffected|units|until|use|variable|wait|when|while|with|xnor|xor)\\>"\ncolor green "\\<(std_logic|std_logic_vector|bit)\\>"\ncolor magenta "\\<(ieee|std_logic_1164|numeric_std|numeric_signed|numberic_unsigned|numeric_bit|math_real|math_complex|std_logic_arith|std_logic_unsigned|std_logic_signed)\\>"\ncolor brightgreen "[\'][^\']*[^\\][\']" "[\']{3}.*[^\\][\']{3}"\ncolor brightgreen "["][^"]*[^\\]["]" "["]{3}.*[^\\]["]{3}"\ncolor blue "--.*$"\n\n# set tab to spaces of size 4 spaces\nset tabstospaces\nset tabsize 4\n\n# enable mouse\nset mouse\n\n# use one additional line\nset morespace\n\n#set the line number indication in the status bar\n#set const\n\n# set autoindentation\nset autoindent\n\n'

def make():
    """ Create a nano configuration file named ".nanorc" in ~/
        IMPORTANT: if you already have this file NOTHING WILL BE DONE. 
    """
    if os.path.isfile(os.getenv('HOME') + '/.nanorc'):
        print 'WARNING. "~/.nanorc" file already exist. Nothing will be done.'
    else:
        with open(os.getenv('HOME') + '/.nanorc', 'w') as (fl):
            fl.write(_content1)
        print '"~/.nanorc" configuration file created.'
    return 0