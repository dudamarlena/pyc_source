# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/quick_start.py
# Compiled at: 2012-08-06 02:52:19
import os
from subprocess import call

def make_vhdl_counter_project(_where):
    """ make_vhdl_counter_project(_where):
        Create a _where folder and put in it two basic VHDL files as well as a
        constraints file. This is just to help beginners to get started 
        with boot.
    """
    call(('clear').split())
    content_fl1 = "--- ##### file: counter_top.vhdl #####\n-- This is the VHDL top-level design file. This file defines the top-level \n-- entity of your VHDL design.\n-- library\nlibrary ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all; \n \n-- entity\nentity counter_top is\nport (\n     cout     :out std_logic_vector (7 downto 0); -- Output signal (bus)\n     up_down  :in  std_logic;                     -- up down control for counter\n     fpga_clk :in  std_logic;                     -- Input clock\n     reset    :in  std_logic);                    -- Input reset\nend entity;\n\n-- architecture\narchitecture rtl of counter_top is\n    signal count :std_logic_vector (7 downto 0);\n    begin\n        process (fpga_clk, reset) begin \n            if (reset = '1') then  \n                count <= (others=>'0');\n            elsif (rising_edge(fpga_clk)) then\n                if (up_down = '1') then\n                    count <= std_logic_vector(unsigned(count) + 1);\n                else\n                    count <= std_logic_vector(unsigned(count) - 1);\n                end if;\n            end if;\n        end process;\n        cout <= count;\nend architecture;\n"
    content_fl2 = "--- ##### file: counter_tb.vhdl #####\n-- This is the test-bench file and is used to drive the simulation of \n-- your design. This file is not used during synthesis.\n-- library\nlibrary ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all;\n\n-- entity\nentity counter_tb is\nend entity;\n\n-- architecture\narchitecture TB of counter_tb is\n \n    component counter_top\n    port( cout:     out std_logic_vector(7 downto 0);\n          up_down:  in std_logic;\n          reset:    in std_logic;\n          fpga_clk: in std_logic);\n    end component;\n \n    signal cout:    std_logic_vector(7 downto 0);\n    signal up_down: std_logic; \n    signal reset:   std_logic; \n    signal cin:     std_logic; \n \nbegin\n \n    dut: counter_top port map (cout, up_down, reset, cin); \n \n    process\n    begin\n        cin <= '0';  \n        wait for 10 ns;\n        cin <= '1';\n        wait for 10 ns;\n    end process;\n\n    process\n    begin\n        up_down <= '1';\n        reset <= '1';\n        wait for 10 ns;\n        reset <= '0';\n        wait for 500 ns;\n \n        up_down <= '0';\n        wait for 500 ns;\n    end process;\nend;\n"
    content_fl3 = '##### file: board.ucf #####\n# This is a simplified version of a .ucf file that can be used\n# for the Xula-200 board. \n# The Xula-200 board has a Spartan3A XC3S200A, VQ100, speed grade: -4\n\n# used by counter_top.vhdl\nnet fpga_clk       loc = p43;\nnet cin            loc = p50;\nnet reset          loc = p52;\nnet up_down        loc = p56;\nnet cout<0>        loc = p57;\nnet cout<1>        loc = p61;\nnet cout<2>        loc = p62;\n\nnet sdram_clk      loc = p40;\nnet sdram_clk_fb   loc = p41;\nnet ras_n          loc = p59;\nnet cas_n          loc = p60;\nnet we_n           loc = p64;\nnet bs             loc = p53;\n\nnet a<0>           loc = p49;\nnet a<1>           loc = p48;\nnet a<2>           loc = p46;\nnet a<3>           loc = p31;\nnet a<4>           loc = p30;\nnet a<5>           loc = p29;\nnet a<6>           loc = p28;\nnet a<7>           loc = p27;\n\nnet fpga_clk       IOSTANDARD = LVTTL;\nnet sdram_clk      IOSTANDARD = LVTTL | SLEW=FAST | DRIVE=8;\nnet a*             IOSTANDARD = LVTTL | SLEW=SLOW | DRIVE=6;\nnet bs             IOSTANDARD = LVTTL | SLEW=SLOW | DRIVE=6;\nnet ras_n          IOSTANDARD = LVTTL | SLEW=SLOW | DRIVE=6;\nnet cas_n          IOSTANDARD = LVTTL | SLEW=SLOW | DRIVE=6;\nnet we_n           IOSTANDARD = LVTTL | SLEW=SLOW | DRIVE=6;\n\nNET "fpga_clk" TNM_NET = "fpga_clk";\nTIMESPEC "TS_fpga_clk" = PERIOD "fpga_clk" 83 ns HIGH 50%;\n\n'
    if not os.path.isdir(_where):
        try:
            os.path.os.mkdir(_where)
            os.path.os.mkdir(os.path.join(_where, 'build'))
        except:
            print 'Not able to create the directory:', _where, 'and its content.'
            return 1

    try:
        open(os.path.join(_where, 'counter_top.vhdl'), 'w').write(content_fl1)
        open(os.path.join(_where, 'counter_tb.vhdl'), 'w').write(content_fl2)
        open(os.path.join(_where, 'board.ucf'), 'w').write(content_fl3)
    except:
        print 'Problems in writing. You might have permission problems or\n',
        print 'the "src" folder already exists.\n'
        return 1

    print 'Building a basic VHDL working environment.'
    return 0