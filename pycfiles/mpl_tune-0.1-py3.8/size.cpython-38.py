# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpl_tune/size.py
# Compiled at: 2019-12-02 13:27:01
# Size of source mod 2**32: 12883 bytes


class FigSize(object):
    __doc__ = 'Helper to compute the size of matplotlib figures.\n\n\tThe idea is to perform conversion between absolute margin sizes (and spacing between rows and columns\n\tin case of multiple subplots) and their corresponding relative that are needed for matplotlib.\n\n\tAdditionnally, there is the possibility to reserve room on a plot to add a color bar.\n\t'
    SIZE_ALL = 1
    SIZE_NO_CBAR = 2
    SIZE_AXES = 3
    SIZE_AX = 4
    SIZE_RATIO_AX = 5

    def __init__(self, size_h=None, size_v=None, nrows=1, ncols=1, margin_left=None, margin_bottom=None, margin_right=None, margin_top=None):
        self.size_h = size_h
        self.type_h = self.SIZE_ALL
        self.size_v = size_v
        self.type_v = self.SIZE_ALL
        self.nrows = nrows
        self.ncols = ncols
        self.margin_left = margin_left
        self.margin_bottom = margin_bottom
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.spacing_h = None
        self.spacing_v = None
        self.cbar_loc = None
        self.cbar_width = None
        self.cbar_pad = None

    def set_size_h(self, size_h, type_h=None):
        """Set the horizontal size of the figure.

                Parameters
                ----------
                size_h : float
                        Horizontal size of the figure in inches, the meaning depends on the value of parameter `type_h`.

                type_h : int
                        Mode for the horizontal size, one of the SIZE_* constants.
                        - SIZE_ALL: `size_h` is the total size of the figure, including margins and color bar (default)
                        - SIZE_NO_CBAR: `size_h` is the size of the figure, without the potential color bar
                        - SIZE_AXES: `size_h` is the size of the axis region of the figure, without the margins and the potential color bar.
                        - SIZE_AX: `size_h` is the size of one of the axis.
                        - SIZE_RATIO_AX: `size_h` is the ratio of the vertical size of the axis region.
                """
        self.size_h = size_h
        if type_h is not None:
            self.type_h = type_h

    def set_size_v(self, size_v, type_v=None):
        """Set the vertical size of the figure.

                Parameters
                ----------
                size_v : float
                        Vertical size of the figure, the meaning depends on the value of parameter `type_v`.

                type_v : int
                        Mode for the vertical size, one of the SIZE_* constants.
                        - SIZE_ALL: `size_v` is the total size of the figure, including margins and color bar (default)
                        - SIZE_NO_CBAR: `size_v` is the size of the figure, without the potential color bar
                        - SIZE_AXES: `size_v` is the size of the axis region of the figure, without the margins and the potential color bar.
                        - SIZE_AX: `size_v` is the size of one of the axis.
                        - SIZE_RATIO_AX: `size_v` is the ratio of the horizontal size of the axis region.
                """
        self.size_v = size_v
        if type_v is not None:
            self.type_v = type_v

    def set_nrows(self, nrows):
        """Set the number of rows of subplots that will be inserted in the figure

                This is used to compute the vertical spacing between the rows.

                Parameters
                ----------
                nrows : int
                        Number of rows of subplots that will be inserted in the figure
                """
        self.nrows = nrows

    def set_ncols(self, ncols):
        """Set the number of columns of subplots that will be inserted in the figure

                This is used to compute the horizontal spacing between the rows.

                Parameters
                ----------
                ncols : int
                        Number of columns of subplots that will be inserted in the figure
                """
        self.ncols = ncols

    def get_margin_left(self):
        """Retrieve the left margin"""
        return self.margin_left

    def set_margin_left(self, margin_left):
        """Set the left margin

                Parameters
                ----------
                margin_left : float
                        Left margin, in inches
                """
        self.margin_left = margin_left

    def get_margin_bottom(self):
        """Retrieve the bottom margin"""
        return self.margin_bottom

    def set_margin_bottom(self, margin_bottom):
        """Set the bottom margin

                Parameters
                ----------
                margin_bottom : float
                        Bottom margin, in inches
                """
        self.margin_bottom = margin_bottom

    def get_margin_right(self):
        """Retrieve the right margin"""
        return self.margin_right

    def set_margin_right(self, margin_right):
        """Set the right margin

                Parameters
                ----------
                margin_right : float
                        Right margin, in inches
                """
        self.margin_right = margin_right

    def get_margin_top(self):
        """Retrieve the top margin"""
        return self.margin_top

    def set_margin_top(self, margin_top):
        """Set the top margin

                Parameters
                ----------
                margin_top : float
                        Top margin, in inches
                """
        self.margin_top = margin_top

    def set_spacing_h(self, spacing_h):
        """Set the horizontal spacing between panels.
                By default it is equal to the sum of the left and right margins.

                Parameters
                ----------
                spacing_h : float or None
                        Horizontal spacing in inches, or None to reset to default.
                """
        self.spacing_h = spacing_h

    def set_spacing_v(self, spacing_v):
        """Set the vertical spacing between panels.
                By default it is equal to the sum of the top and bottom margins.

                Parameters
                ----------
                spacing_v : float or None
                        Vertical spacing in inches, or None to reset to default.
                """
        self.spacing_v = spacing_v

    def set_cbar_loc(self, cbar_loc):
        """Set the location of the color bar

                Parameters
                ----------
                cbar_loc : "left", "bottom", "right" or "top"
                        Location of the color with respect to the plot area,
                        any other value will not reserve any room for the color bar on the figure.
                """
        self.cbar_loc = cbar_loc

    def set_cbar_width(self, cbar_width):
        """Set the width of the color bar

                Parameters
                ----------
                cbar_width : float
                        Set the width of the color bar plot area, in inches
                """
        self.cbar_width = cbar_width

    def set_cbar_pad(self, cbar_pad):
        """Set the padding between the color bar and the plot area.

                Parameters
                ----------
                cbar_loc : float
                        Set the width of the color bar axis area, in inches
                """
        self.cbar_pad = cbar_pad

    def get_figure_size--- This code section failed: ---

 L. 231         0  LOAD_FAST                'self'
                2  LOAD_ATTR                size_h
                4  STORE_FAST               'size_h'

 L. 232         6  LOAD_FAST                'self'
                8  LOAD_ATTR                size_v
               10  STORE_FAST               'size_v'

 L. 234        12  LOAD_FAST                'self'
               14  LOAD_ATTR                spacing_h
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    36  'to 36'

 L. 235        22  LOAD_FAST                'self'
               24  LOAD_ATTR                margin_left
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                margin_right
               30  BINARY_ADD       
               32  STORE_FAST               'spacing_h'
               34  JUMP_FORWARD         42  'to 42'
             36_0  COME_FROM            20  '20'

 L. 237        36  LOAD_FAST                'self'
               38  LOAD_ATTR                spacing_h
               40  STORE_FAST               'spacing_h'
             42_0  COME_FROM            34  '34'

 L. 239        42  LOAD_FAST                'self'
               44  LOAD_ATTR                spacing_v
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 240        52  LOAD_FAST                'self'
               54  LOAD_ATTR                margin_bottom
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                margin_top
               60  BINARY_ADD       
               62  STORE_FAST               'spacing_v'
               64  JUMP_FORWARD         72  'to 72'
             66_0  COME_FROM            50  '50'

 L. 242        66  LOAD_FAST                'self'
               68  LOAD_ATTR                spacing_v
               70  STORE_FAST               'spacing_v'
             72_0  COME_FROM            64  '64'

 L. 244        72  LOAD_FAST                'self'
               74  LOAD_ATTR                type_h
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                SIZE_RATIO_AX
               80  COMPARE_OP               ==
            82_84  POP_JUMP_IF_FALSE   304  'to 304'

 L. 245        86  LOAD_FAST                'self'
               88  LOAD_ATTR                type_v
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                SIZE_RATIO_AX
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L. 246        98  LOAD_GLOBAL              Exception
              100  LOAD_STR                 'type_h and type_v cannot be both SIZE_RATIO_AX at the same time.'
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
              106  JUMP_FORWARD        304  'to 304'
            108_0  COME_FROM            96  '96'

 L. 247       108  LOAD_FAST                'self'
              110  LOAD_ATTR                type_v
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                SIZE_AX
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 248       120  LOAD_FAST                'size_h'
              122  LOAD_FAST                'size_v'
              124  INPLACE_MULTIPLY 
              126  STORE_FAST               'size_h'
              128  JUMP_FORWARD        304  'to 304'
            130_0  COME_FROM           118  '118'

 L. 249       130  LOAD_FAST                'self'
              132  LOAD_ATTR                type_v
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                SIZE_AXES
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   172  'to 172'

 L. 250       142  LOAD_FAST                'size_h'
              144  LOAD_FAST                'size_v'
              146  LOAD_FAST                'spacing_v'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                nrows
              152  LOAD_CONST               1
              154  BINARY_SUBTRACT  
              156  BINARY_MULTIPLY  
              158  BINARY_SUBTRACT  
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                nrows
              164  BINARY_TRUE_DIVIDE
              166  INPLACE_MULTIPLY 
              168  STORE_FAST               'size_h'
              170  JUMP_FORWARD        304  'to 304'
            172_0  COME_FROM           140  '140'

 L. 251       172  LOAD_FAST                'self'
              174  LOAD_ATTR                type_v
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                SIZE_NO_CBAR
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   226  'to 226'

 L. 252       184  LOAD_FAST                'size_h'
              186  LOAD_FAST                'size_v'
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                margin_bottom
              192  BINARY_SUBTRACT  
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                margin_top
              198  BINARY_SUBTRACT  
              200  LOAD_FAST                'spacing_v'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                nrows
              206  LOAD_CONST               1
              208  BINARY_SUBTRACT  
              210  BINARY_MULTIPLY  
              212  BINARY_SUBTRACT  
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                nrows
              218  BINARY_TRUE_DIVIDE
              220  INPLACE_MULTIPLY 
              222  STORE_FAST               'size_h'
              224  JUMP_FORWARD        304  'to 304'
            226_0  COME_FROM           182  '182'

 L. 254       226  LOAD_FAST                'size_h'
              228  LOAD_FAST                'size_v'
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                cbar_loc
              234  LOAD_STR                 'bottom'
              236  COMPARE_OP               ==
              238  POP_JUMP_IF_TRUE    252  'to 252'
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                cbar_loc
              244  LOAD_STR                 'top'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   264  'to 264'
            252_0  COME_FROM           238  '238'
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                cbar_width
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                cbar_pad
              260  BINARY_ADD       
              262  JUMP_FORWARD        266  'to 266'
            264_0  COME_FROM           248  '248'
              264  LOAD_CONST               0.0
            266_0  COME_FROM           262  '262'
              266  BINARY_SUBTRACT  
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                margin_bottom
              272  BINARY_SUBTRACT  
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                margin_top
              278  BINARY_SUBTRACT  
              280  LOAD_FAST                'spacing_v'
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                nrows
              286  LOAD_CONST               1
              288  BINARY_SUBTRACT  
              290  BINARY_MULTIPLY  
              292  BINARY_SUBTRACT  
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                nrows
              298  BINARY_TRUE_DIVIDE
              300  INPLACE_MULTIPLY 
              302  STORE_FAST               'size_h'
            304_0  COME_FROM           224  '224'
            304_1  COME_FROM           170  '170'
            304_2  COME_FROM           128  '128'
            304_3  COME_FROM           106  '106'
            304_4  COME_FROM            82  '82'

 L. 256       304  LOAD_FAST                'self'
              306  LOAD_ATTR                type_v
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                SIZE_RATIO_AX
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   546  'to 546'

 L. 257       318  LOAD_FAST                'self'
              320  LOAD_ATTR                type_h
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                SIZE_RATIO_AX
              326  COMPARE_OP               ==
          328_330  POP_JUMP_IF_FALSE   342  'to 342'

 L. 259       332  LOAD_GLOBAL              Exception
              334  LOAD_STR                 'type_h and type_v cannot be both SIZE_RATIO_AX at the same time.'
              336  CALL_FUNCTION_1       1  ''
              338  RAISE_VARARGS_1       1  'exception instance'
              340  JUMP_FORWARD        546  'to 546'
            342_0  COME_FROM           328  '328'

 L. 260       342  LOAD_FAST                'self'
              344  LOAD_ATTR                type_h
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                SIZE_AX
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   366  'to 366'

 L. 261       356  LOAD_FAST                'size_v'
              358  LOAD_FAST                'size_h'
              360  INPLACE_MULTIPLY 
              362  STORE_FAST               'size_v'
              364  JUMP_FORWARD        546  'to 546'
            366_0  COME_FROM           352  '352'

 L. 262       366  LOAD_FAST                'self'
              368  LOAD_ATTR                type_h
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                SIZE_AXES
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   410  'to 410'

 L. 263       380  LOAD_FAST                'size_v'
              382  LOAD_FAST                'size_h'
              384  LOAD_FAST                'spacing_h'
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                ncols
              390  LOAD_CONST               1
              392  BINARY_SUBTRACT  
              394  BINARY_MULTIPLY  
              396  BINARY_SUBTRACT  
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                ncols
              402  BINARY_TRUE_DIVIDE
              404  INPLACE_MULTIPLY 
              406  STORE_FAST               'size_v'
              408  JUMP_FORWARD        546  'to 546'
            410_0  COME_FROM           376  '376'

 L. 264       410  LOAD_FAST                'self'
              412  LOAD_ATTR                type_h
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                SIZE_NO_CBAR
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   466  'to 466'

 L. 265       424  LOAD_FAST                'size_v'
              426  LOAD_FAST                'size_h'
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                margin_left
              432  BINARY_SUBTRACT  
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                margin_right
              438  BINARY_SUBTRACT  
              440  LOAD_FAST                'spacing_h'
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                ncols
              446  LOAD_CONST               1
              448  BINARY_SUBTRACT  
              450  BINARY_MULTIPLY  
              452  BINARY_SUBTRACT  
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                ncols
              458  BINARY_TRUE_DIVIDE
              460  INPLACE_MULTIPLY 
              462  STORE_FAST               'size_v'
              464  JUMP_FORWARD        546  'to 546'
            466_0  COME_FROM           420  '420'

 L. 267       466  LOAD_FAST                'size_v'
              468  LOAD_FAST                'size_h'
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                cbar_loc
              474  LOAD_STR                 'left'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_TRUE    494  'to 494'
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                cbar_loc
              486  LOAD_STR                 'right'
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_FALSE   506  'to 506'
            494_0  COME_FROM           478  '478'
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                cbar_width
              498  LOAD_FAST                'self'
              500  LOAD_ATTR                cbar_pad
              502  BINARY_ADD       
              504  JUMP_FORWARD        508  'to 508'
            506_0  COME_FROM           490  '490'
              506  LOAD_CONST               0.0
            508_0  COME_FROM           504  '504'
              508  BINARY_SUBTRACT  
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                margin_left
              514  BINARY_SUBTRACT  
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                margin_right
              520  BINARY_SUBTRACT  
              522  LOAD_FAST                'spacing_h'
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                ncols
              528  LOAD_CONST               1
              530  BINARY_SUBTRACT  
              532  BINARY_MULTIPLY  
              534  BINARY_SUBTRACT  
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                ncols
              540  BINARY_TRUE_DIVIDE
              542  INPLACE_MULTIPLY 
              544  STORE_FAST               'size_v'
            546_0  COME_FROM           464  '464'
            546_1  COME_FROM           408  '408'
            546_2  COME_FROM           364  '364'
            546_3  COME_FROM           340  '340'
            546_4  COME_FROM           314  '314'

 L. 269       546  LOAD_FAST                'self'
              548  LOAD_ATTR                type_h
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                SIZE_AX
              554  COMPARE_OP               ==
          556_558  POP_JUMP_IF_TRUE    574  'to 574'
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                type_h
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                SIZE_RATIO_AX
              568  COMPARE_OP               ==
          570_572  POP_JUMP_IF_FALSE   602  'to 602'
            574_0  COME_FROM           556  '556'

 L. 270       574  LOAD_FAST                'size_h'
              576  LOAD_FAST                'self'
              578  LOAD_ATTR                ncols
              580  INPLACE_MULTIPLY 
              582  STORE_FAST               'size_h'

 L. 271       584  LOAD_FAST                'size_h'
              586  LOAD_FAST                'spacing_h'
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                ncols
              592  LOAD_CONST               1
              594  BINARY_SUBTRACT  
              596  BINARY_MULTIPLY  
              598  INPLACE_ADD      
              600  STORE_FAST               'size_h'
            602_0  COME_FROM           570  '570'

 L. 273       602  LOAD_FAST                'self'
              604  LOAD_ATTR                type_v
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                SIZE_AX
              610  COMPARE_OP               ==
          612_614  POP_JUMP_IF_TRUE    630  'to 630'
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                type_v
              620  LOAD_FAST                'self'
              622  LOAD_ATTR                SIZE_RATIO_AX
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   658  'to 658'
            630_0  COME_FROM           612  '612'

 L. 274       630  LOAD_FAST                'size_v'
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                nrows
              636  INPLACE_MULTIPLY 
              638  STORE_FAST               'size_v'

 L. 275       640  LOAD_FAST                'size_v'
              642  LOAD_FAST                'spacing_v'
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                nrows
              648  LOAD_CONST               1
              650  BINARY_SUBTRACT  
              652  BINARY_MULTIPLY  
              654  INPLACE_ADD      
              656  STORE_FAST               'size_v'
            658_0  COME_FROM           626  '626'

 L. 277       658  LOAD_FAST                'self'
              660  LOAD_ATTR                type_h
              662  LOAD_FAST                'self'
              664  LOAD_ATTR                SIZE_AXES
              666  COMPARE_OP               ==
          668_670  POP_JUMP_IF_TRUE    700  'to 700'
              672  LOAD_FAST                'self'
              674  LOAD_ATTR                type_h
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                SIZE_AX
              680  COMPARE_OP               ==
          682_684  POP_JUMP_IF_TRUE    700  'to 700'
              686  LOAD_FAST                'self'
              688  LOAD_ATTR                type_h
              690  LOAD_FAST                'self'
              692  LOAD_ATTR                SIZE_RATIO_AX
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   716  'to 716'
            700_0  COME_FROM           682  '682'
            700_1  COME_FROM           668  '668'

 L. 278       700  LOAD_FAST                'size_h'
              702  LOAD_FAST                'self'
              704  LOAD_ATTR                margin_left
              706  LOAD_FAST                'self'
              708  LOAD_ATTR                margin_right
              710  BINARY_ADD       
              712  INPLACE_ADD      
              714  STORE_FAST               'size_h'
            716_0  COME_FROM           696  '696'

 L. 279       716  LOAD_FAST                'self'
              718  LOAD_ATTR                type_v
              720  LOAD_FAST                'self'
              722  LOAD_ATTR                SIZE_AXES
              724  COMPARE_OP               ==
          726_728  POP_JUMP_IF_TRUE    758  'to 758'
              730  LOAD_FAST                'self'
              732  LOAD_ATTR                type_v
              734  LOAD_FAST                'self'
              736  LOAD_ATTR                SIZE_AX
              738  COMPARE_OP               ==
          740_742  POP_JUMP_IF_TRUE    758  'to 758'
              744  LOAD_FAST                'self'
              746  LOAD_ATTR                type_v
              748  LOAD_FAST                'self'
              750  LOAD_ATTR                SIZE_RATIO_AX
              752  COMPARE_OP               ==
          754_756  POP_JUMP_IF_FALSE   774  'to 774'
            758_0  COME_FROM           740  '740'
            758_1  COME_FROM           726  '726'

 L. 280       758  LOAD_FAST                'size_v'
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                margin_bottom
              764  LOAD_FAST                'self'
              766  LOAD_ATTR                margin_top
              768  BINARY_ADD       
              770  INPLACE_ADD      
              772  STORE_FAST               'size_v'
            774_0  COME_FROM           754  '754'

 L. 282       774  LOAD_FAST                'self'
              776  LOAD_ATTR                type_h
              778  LOAD_FAST                'self'
              780  LOAD_ATTR                SIZE_NO_CBAR
              782  COMPARE_OP               ==
          784_786  POP_JUMP_IF_TRUE    830  'to 830'
              788  LOAD_FAST                'self'
              790  LOAD_ATTR                type_h
              792  LOAD_FAST                'self'
              794  LOAD_ATTR                SIZE_AXES
              796  COMPARE_OP               ==
          798_800  POP_JUMP_IF_TRUE    830  'to 830'
              802  LOAD_FAST                'self'
              804  LOAD_ATTR                type_h
              806  LOAD_FAST                'self'
              808  LOAD_ATTR                SIZE_AX
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_TRUE    830  'to 830'
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                type_h
              820  LOAD_FAST                'self'
              822  LOAD_ATTR                SIZE_RATIO_AX
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_FALSE   870  'to 870'
            830_0  COME_FROM           812  '812'
            830_1  COME_FROM           798  '798'
            830_2  COME_FROM           784  '784'
              830  LOAD_FAST                'self'
              832  LOAD_ATTR                cbar_loc
              834  LOAD_STR                 'left'
              836  COMPARE_OP               ==
          838_840  POP_JUMP_IF_TRUE    854  'to 854'
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                cbar_loc
              846  LOAD_STR                 'right'
              848  COMPARE_OP               ==
          850_852  POP_JUMP_IF_FALSE   870  'to 870'
            854_0  COME_FROM           838  '838'

 L. 283       854  LOAD_FAST                'size_h'
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                cbar_width
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                cbar_pad
              864  BINARY_ADD       
              866  INPLACE_ADD      
              868  STORE_FAST               'size_h'
            870_0  COME_FROM           850  '850'
            870_1  COME_FROM           826  '826'

 L. 284       870  LOAD_FAST                'self'
              872  LOAD_ATTR                type_v
              874  LOAD_FAST                'self'
              876  LOAD_ATTR                SIZE_NO_CBAR
              878  COMPARE_OP               ==
          880_882  POP_JUMP_IF_TRUE    926  'to 926'
              884  LOAD_FAST                'self'
              886  LOAD_ATTR                type_v
              888  LOAD_FAST                'self'
              890  LOAD_ATTR                SIZE_AXES
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_TRUE    926  'to 926'
              898  LOAD_FAST                'self'
              900  LOAD_ATTR                type_v
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                SIZE_AX
              906  COMPARE_OP               ==
          908_910  POP_JUMP_IF_TRUE    926  'to 926'
              912  LOAD_FAST                'self'
              914  LOAD_ATTR                type_v
              916  LOAD_FAST                'self'
              918  LOAD_ATTR                SIZE_RATIO_AX
              920  COMPARE_OP               ==
          922_924  POP_JUMP_IF_FALSE   966  'to 966'
            926_0  COME_FROM           908  '908'
            926_1  COME_FROM           894  '894'
            926_2  COME_FROM           880  '880'
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                cbar_loc
              930  LOAD_STR                 'bottom'
              932  COMPARE_OP               ==
          934_936  POP_JUMP_IF_TRUE    950  'to 950'
              938  LOAD_FAST                'self'
              940  LOAD_ATTR                cbar_loc
              942  LOAD_STR                 'top'
              944  COMPARE_OP               ==
          946_948  POP_JUMP_IF_FALSE   966  'to 966'
            950_0  COME_FROM           934  '934'

 L. 285       950  LOAD_FAST                'size_v'
              952  LOAD_FAST                'self'
              954  LOAD_ATTR                cbar_width
              956  LOAD_FAST                'self'
              958  LOAD_ATTR                cbar_pad
              960  BINARY_ADD       
              962  INPLACE_ADD      
              964  STORE_FAST               'size_v'
            966_0  COME_FROM           946  '946'
            966_1  COME_FROM           922  '922'

 L. 287       966  LOAD_FAST                'size_h'
              968  LOAD_FAST                'size_v'
              970  BUILD_TUPLE_2         2 
              972  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 972

    def get_figure_args(self):
        """
                Get the size arguments for when creating a figure.

                Returns
                -------
                dict
                        Arguments for the matplotlib.pyplot.figure() function.
                """
        return {'figsize': self.get_figure_size()}

    def get_subplots_args(self):
        """
                Get the arguments for the location of the subplots.

                Returns
                -------
                dict
                        Arguments for the Figure.subplots_adjust() function.
                """
        size_h, size_v = self.get_figure_size()
        left = self.margin_left
        bottom = self.margin_bottom
        right = self.margin_right
        top = self.margin_top
        if self.cbar_loc == 'left':
            left += self.cbar_width + self.cbar_pad
        else:
            if self.cbar_loc == 'right':
                right += self.cbar_width + self.cbar_pad
            else:
                if self.cbar_loc == 'bottom':
                    bottom += self.cbar_width + self.cbar_pad
                if self.cbar_loc == 'top':
                    top += self.cbar_width + self.cbar_pad
                if self.spacing_h is None:
                    spacing_h = self.margin_left + self.margin_right
                else:
                    spacing_h = self.spacing_h
            if self.spacing_v is None:
                spacing_v = self.margin_bottom + self.margin_top
            else:
                spacing_v = self.spacing_v
        if self.ncols > 1 and spacing_h > 0.0:
            wspace = self.ncols / ((size_h - right - left) / spacing_h - (self.ncols - 1))
        else:
            wspace = 0.0
        if self.nrows > 1 and spacing_v > 0.0:
            hspace = self.nrows / ((size_v - top - bottom) / spacing_v - (self.nrows - 1))
        else:
            hspace = 0.0
        return {'left':left / size_h,  'bottom':bottom / size_v,  'right':1.0 - right / size_h,  'top':1.0 - top / size_v,  'wspace':wspace,  'hspace':hspace}

    def has_cbar(self):
        """Retrieve whether room has been reserved for the color bar.

                Returns
                -------
                bool
                        Whether room is reserved for the color bar.
                """
        return self.cbar_loc == 'left' or self.cbar_loc == 'right' or self.cbar_loc == 'bottom' or self.cbar_loc == 'top'

    def get_cbar_ax_spec(self):
        """Retrieve the location of the color bar in the figure.

                Returns
                -------
                list
                        Location of the area for the color bar, which can be used as an argument to Figure.add_axes().
                """
        size_h, size_v = self.get_figure_size()
        if self.cbar_loc == 'left':
            return [
             self.margin_left / size_h, self.margin_bottom / size_v, self.cbar_width / size_h, 1.0 - (self.margin_bottom + self.margin_top) / size_v]
        if self.cbar_loc == 'right':
            return [
             1.0 - (self.cbar_width + self.cbar_pad) / size_h, self.margin_bottom / size_v, self.cbar_width / size_h, 1.0 - (self.margin_bottom + self.margin_top) / size_v]
        if self.cbar_loc == 'bottom':
            return [
             self.margin_left / size_h, self.margin_bottom / size_v, 1.0 - (self.margin_left + self.margin_right) / size_h, self.cbar_width / size_v]
        if self.cbar_loc == 'top':
            return [
             self.margin_left / size_h, 1.0 - (self.cbar_width + self.margin_top) / size_v, 1.0 - (self.margin_left + self.margin_right) / size_h, self.cbar_width / size_v]

    def get_cbar_orientation(self):
        """Retrieve the orientation of the color bar.

                Returns
                -------
                "vertical", "horizontal" or None
                        Orientation of the color bar, which can be provided as the value of the "orientation" parameter of Figure.colorbar(), or None if disabled.
                """
        if self.cbar_loc == 'left' or self.cbar_loc == 'right':
            return 'vertical'
        if self.cbar_loc == 'bottom' or self.cbar_loc == 'top':
            return 'horizontal'