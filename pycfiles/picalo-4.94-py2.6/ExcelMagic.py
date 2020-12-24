# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/ExcelMagic.py
# Compiled at: 2008-03-17 12:58:02
__rev_id__ = '$Id: ExcelMagic.py,v 1.2 2005/10/26 07:44:24 rvk Exp $'
MAX_ROW = 65536
MAX_COL = 256
biff_records = {0: 'DIMENSIONS', 
   1: 'BLANK', 
   2: 'INTEGER', 
   3: 'NUMBER', 
   4: 'LABEL', 
   5: 'BOOLERR', 
   6: 'FORMULA', 
   7: 'STRING', 
   8: 'ROW', 
   9: 'BOF', 
   10: 'EOF', 
   11: 'INDEX', 
   12: 'CALCCOUNT', 
   13: 'CALCMODE', 
   14: 'PRECISION', 
   15: 'REFMODE', 
   16: 'DELTA', 
   17: 'ITERATION', 
   18: 'PROTECT', 
   19: 'PASSWORD', 
   20: 'HEADER', 
   21: 'FOOTER', 
   22: 'EXTERNCOUNT', 
   23: 'EXTERNSHEET', 
   24: 'NAME', 
   25: 'WINDOWPROTECT', 
   26: 'VERTICALPAGEBREAKS', 
   27: 'HORIZONTALPAGEBREAKS', 
   28: 'NOTE', 
   29: 'SELECTION', 
   30: 'FORMAT', 
   31: 'FORMATCOUNT', 
   32: 'COLUMNDEFAULT', 
   33: 'ARRAY', 
   34: '1904', 
   35: 'EXTERNNAME', 
   36: 'COLWIDTH', 
   37: 'DEFAULTROWHEIGHT', 
   38: 'LEFTMARGIN', 
   39: 'RIGHTMARGIN', 
   40: 'TOPMARGIN', 
   41: 'BOTTOMMARGIN', 
   42: 'PRINTHEADERS', 
   43: 'PRINTGRIDLINES', 
   47: 'FILEPASS', 
   49: 'FONT', 
   54: 'TABLE', 
   60: 'CONTINUE', 
   61: 'WINDOW1', 
   62: 'WINDOW2', 
   64: 'BACKUP', 
   65: 'PANE', 
   66: 'CODEPAGE', 
   67: 'XF', 
   68: 'IXFE', 
   69: 'EFONT', 
   77: 'PLS', 
   80: 'DCON', 
   81: 'DCONREF', 
   83: 'DCONNAME', 
   85: 'DEFCOLWIDTH', 
   86: 'BUILTINFMTCNT', 
   89: 'XCT', 
   90: 'CRN', 
   91: 'FILESHARING', 
   92: 'WRITEACCESS', 
   93: 'OBJ', 
   94: 'UNCALCED', 
   95: 'SAFERECALC', 
   96: 'TEMPLATE', 
   99: 'OBJPROTECT', 
   125: 'COLINFO', 
   126: 'RK', 
   127: 'IMDATA', 
   128: 'GUTS', 
   129: 'WSBOOL', 
   130: 'GRIDSET', 
   131: 'HCENTER', 
   132: 'VCENTER', 
   133: 'BOUNDSHEET', 
   134: 'WRITEPROT', 
   135: 'ADDIN', 
   136: 'EDG', 
   137: 'PUB', 
   140: 'COUNTRY', 
   141: 'HIDEOBJ', 
   142: 'BUNDLESOFFSET', 
   143: 'BUNDLEHEADER', 
   144: 'SORT', 
   145: 'SUB', 
   146: 'PALETTE', 
   147: 'STYLE', 
   148: 'LHRECORD', 
   149: 'LHNGRAPH', 
   150: 'SOUND', 
   152: 'LPR', 
   153: 'STANDARDWIDTH', 
   154: 'FNGROUPNAME', 
   155: 'FILTERMODE', 
   156: 'FNGROUPCOUNT', 
   157: 'AUTOFILTERINFO', 
   158: 'AUTOFILTER', 
   160: 'SCL', 
   161: 'SETUP', 
   169: 'COORDLIST', 
   171: 'GCW', 
   174: 'SCENMAN', 
   175: 'SCENARIO', 
   176: 'SXVIEW', 
   177: 'SXVD', 
   178: 'SXVI', 
   180: 'SXIVD', 
   181: 'SXLI', 
   182: 'SXPI', 
   184: 'DOCROUTE', 
   185: 'RECIPNAME', 
   188: 'SHRFMLA', 
   189: 'MULRK', 
   190: 'MULBLANK', 
   193: 'MMS', 
   194: 'ADDMENU', 
   195: 'DELMENU', 
   197: 'SXDI', 
   198: 'SXDB', 
   199: 'SXFIELD', 
   200: 'SXINDEXLIST', 
   201: 'SXDOUBLE', 
   205: 'SXSTRING', 
   206: 'SXDATETIME', 
   208: 'SXTBL', 
   209: 'SXTBRGITEM', 
   210: 'SXTBPG', 
   211: 'OBPROJ', 
   213: 'SXIDSTM', 
   214: 'RSTRING', 
   215: 'DBCELL', 
   218: 'BOOKBOOL', 
   220: 'SXEXT|PARAMQRY', 
   221: 'SCENPROTECT', 
   222: 'OLESIZE', 
   223: 'UDDESC', 
   224: 'XF', 
   225: 'INTERFACEHDR', 
   226: 'INTERFACEEND', 
   227: 'SXVS', 
   229: 'MERGEDCELLS', 
   233: 'BITMAP', 
   235: 'MSODRAWINGGROUP', 
   236: 'MSODRAWING', 
   237: 'MSODRAWINGSELECTION', 
   240: 'SXRULE', 
   241: 'SXEX', 
   242: 'SXFILT', 
   246: 'SXNAME', 
   247: 'SXSELECT', 
   248: 'SXPAIR', 
   249: 'SXFMLA', 
   251: 'SXFORMAT', 
   252: 'SST', 
   253: 'LABELSST', 
   255: 'EXTSST', 
   256: 'SXVDEX', 
   259: 'SXFORMULA', 
   290: 'SXDBEX', 
   311: 'CHTRINSERT', 
   312: 'CHTRINFO', 
   315: 'CHTRCELLCONTENT', 
   317: 'TABID', 
   320: 'CHTRMOVERANGE', 
   333: 'CHTRINSERTTAB', 
   351: 'LABELRANGES', 
   352: 'USESELFS', 
   353: 'DSF', 
   354: 'XL5MODIFY', 
   406: 'CHTRHEADER', 
   425: 'USERBVIEW', 
   426: 'USERSVIEWBEGIN', 
   427: 'USERSVIEWEND', 
   429: 'QSI', 
   430: 'SUPBOOK', 
   431: 'PROT4REV', 
   432: 'CONDFMT', 
   433: 'CF', 
   434: 'DVAL', 
   437: 'DCONBIN', 
   438: 'TXO', 
   439: 'REFRESHALL', 
   440: 'HLINK', 
   442: 'CODENAME', 
   443: 'SXFDBTYPE', 
   444: 'PROT4REVPASS', 
   446: 'DV', 
   448: 'XL9FILE', 
   449: 'RECALCID', 
   512: 'DIMENSIONS', 
   513: 'BLANK', 
   515: 'NUMBER', 
   516: 'LABEL', 
   517: 'BOOLERR', 
   518: 'FORMULA', 
   519: 'STRING', 
   520: 'ROW', 
   521: 'BOF', 
   523: 'INDEX', 
   536: 'NAME', 
   545: 'ARRAY', 
   547: 'EXTERNNAME', 
   549: 'DEFAULTROWHEIGHT', 
   561: 'FONT', 
   566: 'TABLE', 
   574: 'WINDOW2', 
   579: 'XF', 
   638: 'RK', 
   659: 'STYLE', 
   1030: 'FORMULA', 
   1033: 'BOF', 
   1054: 'FORMAT', 
   1091: 'XF', 
   1212: 'SHRFMLA', 
   2048: 'SCREENTIP', 
   2051: 'WEBQRYSETTINGS', 
   2052: 'WEBQRYTABLES', 
   2057: 'BOF', 
   2146: 'SHEETLAYOUT', 
   2151: 'SHEETPROTECTION', 
   4097: 'UNITS', 
   4098: 'ChartChart', 
   4099: 'ChartSeries', 
   4102: 'ChartDataformat', 
   4103: 'ChartLineformat', 
   4105: 'ChartMarkerformat', 
   4106: 'ChartAreaformat', 
   4107: 'ChartPieformat', 
   4108: 'ChartAttachedlabel', 
   4109: 'ChartSeriestext', 
   4116: 'ChartChartformat', 
   4117: 'ChartLegend', 
   4118: 'ChartSerieslist', 
   4119: 'ChartBar', 
   4120: 'ChartLine', 
   4121: 'ChartPie', 
   4122: 'ChartArea', 
   4123: 'ChartScatter', 
   4124: 'ChartChartline', 
   4125: 'ChartAxis', 
   4126: 'ChartTick', 
   4127: 'ChartValuerange', 
   4128: 'ChartCatserrange', 
   4129: 'ChartAxislineformat', 
   4130: 'ChartFormatlink', 
   4132: 'ChartDefaulttext', 
   4133: 'ChartText', 
   4134: 'ChartFontx', 
   4135: 'ChartObjectLink', 
   4146: 'ChartFrame', 
   4147: 'BEGIN', 
   4148: 'END', 
   4149: 'ChartPlotarea', 
   4154: 'Chart3D', 
   4156: 'ChartPicf', 
   4157: 'ChartDropbar', 
   4158: 'ChartRadar', 
   4159: 'ChartSurface', 
   4160: 'ChartRadararea', 
   4161: 'ChartAxisparent', 
   4163: 'ChartLegendxn', 
   4164: 'ChartShtprops', 
   4165: 'ChartSertocrt', 
   4166: 'ChartAxesused', 
   4168: 'ChartSbaseref', 
   4170: 'ChartSerparent', 
   4171: 'ChartSerauxtrend', 
   4174: 'ChartIfmt', 
   4175: 'ChartPos', 
   4176: 'ChartAlruns', 
   4177: 'ChartAI', 
   4187: 'ChartSerauxerrbar', 
   4189: 'ChartSerfmt', 
   4191: 'Chart3DDataFormat', 
   4192: 'ChartFbi', 
   4193: 'ChartBoppop', 
   4194: 'ChartAxcext', 
   4195: 'ChartDat', 
   4196: 'ChartPlotgrowth', 
   4197: 'ChartSiindex', 
   4198: 'ChartGelframe', 
   4199: 'ChartBoppcustom', 
   65535: ''}
std_func_by_name = {'ABS': (
         24, 1, 1, 'V', 'V', False), 
   'ACOS': (
          99, 1, 1, 'V', 'V', False), 
   'ACOSH': (
           233, 1, 1, 'V', 'V', False), 
   'ADDRESS': (
             219, 2, 5, 'V', 'V V V V V', False), 
   'AND': (
         36, 1, 30, 'V', 'R ...', False), 
   'ARCTAN': (
            18, 1, 1, 'V', 'V', False), 
   'AREAS': (
           75, 1, 1, 'V', 'R', False), 
   'ASC': (
         214, 1, 1, 'V', 'V', False), 
   'ASIN': (
          98, 1, 1, 'V', 'V', False), 
   'ASINH': (
           232, 1, 1, 'V', 'V', False), 
   'ATAN2': (
           97, 2, 2, 'V', 'V V', False), 
   'ATANH': (
           234, 1, 1, 'V', 'V', False), 
   'AVEDEV': (
            269, 1, 30, 'V', 'R ...', False), 
   'AVERAGE': (
             5, 1, 30, 'V', 'R ...', False), 
   'AVERAGEA': (
              361, 1, 30, 'V', 'R ...', False), 
   'BETADIST': (
              270, 3, 5, 'V', 'V V V V V', False), 
   'BETAINV': (
             272, 3, 5, 'V', 'V V V V V', False), 
   'BINOMDIST': (
               273, 4, 4, 'V', 'V V V V', False), 
   'CEILING': (
             288, 2, 2, 'V', 'V V', False), 
   'CELL': (
          125, 1, 2, 'V', 'V R', True), 
   'CHAR': (
          111, 1, 1, 'V', 'V', False), 
   'CHIDIST': (
             274, 2, 2, 'V', 'V V', False), 
   'CHIINV': (
            275, 2, 2, 'V', 'V V', False), 
   'CHITEST': (
             306, 2, 2, 'V', 'A A', False), 
   'CHOOSE': (
            100, 2, 30, 'R', 'V R ...', False), 
   'CLEAN': (
           162, 1, 1, 'V', 'V', False), 
   'CODE': (
          121, 1, 1, 'V', 'V', False), 
   'COLUMN': (
            9, 0, 1, 'V', 'R', False), 
   'COLUMNS': (
             77, 1, 1, 'V', 'R', False), 
   'COMBIN': (
            276, 2, 2, 'V', 'V V', False), 
   'CONCATENATE': (
                 336, 0, 30, 'V', 'V ...', False), 
   'CONFIDENCE': (
                277, 3, 3, 'V', 'V V V', False), 
   'CORREL': (
            307, 2, 2, 'V', 'A A', False), 
   'COS': (
         16, 1, 1, 'V', 'V', False), 
   'COSH': (
          230, 1, 1, 'V', 'V', False), 
   'COUNT': (
           0, 0, 30, 'V', 'R ...', False), 
   'COUNTA': (
            169, 0, 30, 'V', 'R ...', False), 
   'COUNTBLANK': (
                347, 1, 1, 'V', 'R', False), 
   'COUNTIF': (
             346, 2, 2, 'V', 'R V', False), 
   'COVAR': (
           308, 2, 2, 'V', 'A A', False), 
   'CRITBINOM': (
               278, 3, 3, 'V', 'V V V', False), 
   'DATE': (
          65, 3, 3, 'V', 'V V V', False), 
   'DATEDIF': (
             351, 3, 3, 'V', 'V V V', False), 
   'DATESTRING': (
                352, 1, 1, 'V', 'V', False), 
   'DATEVALUE': (
               140, 1, 1, 'V', 'V', False), 
   'DAVERAGE': (
              42, 3, 3, 'V', 'R R R', False), 
   'DAY': (
         67, 1, 1, 'V', 'V', False), 
   'DAYS360': (
             220, 2, 3, 'V', 'V V V', False), 
   'DB': (
        247, 4, 5, 'V', 'V V V V V', False), 
   'DBSC': (
          215, 1, 1, 'V', 'V', False), 
   'DCOUNT': (
            40, 3, 3, 'V', 'R R R', False), 
   'DCOUNTA': (
             199, 3, 3, 'V', 'R R R', False), 
   'DDB': (
         144, 4, 5, 'V', 'V V V V V', False), 
   'DEGREES': (
             343, 1, 1, 'V', 'V', False), 
   'DEVSQ': (
           318, 1, 30, 'V', 'R ...', False), 
   'DGET': (
          235, 3, 3, 'V', 'R R R', False), 
   'DMAX': (
          44, 3, 3, 'V', 'R R R', False), 
   'DMIN': (
          43, 3, 3, 'V', 'R R R', False), 
   'DOLLAR': (
            13, 1, 2, 'V', 'V V', False), 
   'DPRODUCT': (
              191, 3, 3, 'V', 'R R R', False), 
   'DSTDEV': (
            45, 3, 3, 'V', 'R R R', False), 
   'DSTDEVP': (
             195, 3, 3, 'V', 'R R R', False), 
   'DSUM': (
          41, 3, 3, 'V', 'R R R', False), 
   'DVAR': (
          47, 3, 3, 'V', 'R R R', False), 
   'DVARP': (
           196, 3, 3, 'V', 'R R R', False), 
   'ERROR.TYPE': (
                261, 1, 1, 'V', 'V', False), 
   'EVEN': (
          279, 1, 1, 'V', 'V', False), 
   'EXACT': (
           117, 2, 2, 'V', 'V V', False), 
   'EXP': (
         21, 1, 1, 'V', 'V', False), 
   'EXPONDIST': (
               280, 3, 3, 'V', 'V V V', False), 
   'FACT': (
          184, 1, 1, 'V', 'V', False), 
   'FALSE': (
           35, 0, 0, 'V', '-', False), 
   'FDIST': (
           281, 3, 3, 'V', 'V V V', False), 
   'FIND': (
          124, 2, 3, 'V', 'V V V', False), 
   'FINDB': (
           205, 2, 3, 'V', 'V V V', False), 
   'FINV': (
          282, 3, 3, 'V', 'V V V', False), 
   'FISHER': (
            283, 1, 1, 'V', 'V', False), 
   'FISHERINV': (
               284, 1, 1, 'V', 'V', False), 
   'FIXED': (
           14, 2, 3, 'V', 'V V V', False), 
   'FLOOR': (
           285, 2, 2, 'V', 'V V', False), 
   'FORECAST': (
              309, 3, 3, 'V', 'V A A', False), 
   'FREQUENCY': (
               252, 2, 2, 'A', 'R R', False), 
   'FTEST': (
           310, 2, 2, 'V', 'A A', False), 
   'FV': (
        57, 3, 5, 'V', 'V V V V V', False), 
   'GAMMADIST': (
               286, 4, 4, 'V', 'V V V V', False), 
   'GAMMAINV': (
              287, 3, 3, 'V', 'V V V', False), 
   'GAMMALN': (
             271, 1, 1, 'V', 'V', False), 
   'GEOMEAN': (
             319, 1, 30, 'V', 'R ...', False), 
   'GETPIVOTDATA': (
                  358, 2, 30, 'A', '-', False), 
   'GROWTH': (
            52, 1, 4, 'A', 'R R R V', False), 
   'HARMEAN': (
             320, 1, 30, 'V', 'R ...', False), 
   'HLOOKUP': (
             101, 3, 4, 'V', 'V R R V', False), 
   'HOUR': (
          71, 1, 1, 'V', 'V', False), 
   'HYPERLINK': (
               359, 1, 2, 'V', 'V V', False), 
   'HYPGEOMVERT': (
                 289, 4, 4, 'V', 'V V V V', False), 
   'IF': (
        1, 2, 3, 'R', 'V R R', False), 
   'INDEX': (
           29, 2, 4, 'R', 'R V V V', False), 
   'INDIRECT': (
              148, 1, 2, 'R', 'V V', True), 
   'INFO': (
          244, 1, 1, 'V', 'V', False), 
   'INT': (
         25, 1, 1, 'V', 'V', False), 
   'INTERCEPT': (
               311, 2, 2, 'V', 'A A', False), 
   'IPMT': (
          167, 4, 6, 'V', 'V V V V V V', False), 
   'IRR': (
         62, 1, 2, 'V', 'R V', False), 
   'ISBLANK': (
             129, 1, 1, 'V', 'V', False), 
   'ISERR': (
           126, 1, 1, 'V', 'V', False), 
   'ISERROR': (
             3, 1, 1, 'V', 'V', False), 
   'ISLOGICAL': (
               198, 1, 1, 'V', 'V', False), 
   'ISNA': (
          2, 1, 1, 'V', 'V', False), 
   'ISNONTEXT': (
               192, 1, 1, 'V', 'V', False), 
   'ISNUMBER': (
              128, 1, 1, 'V', 'V', False), 
   'ISPMT': (
           350, 4, 4, 'V', 'V V V V', False), 
   'ISREF': (
           105, 1, 1, 'V', 'R', False), 
   'ISTEXT': (
            127, 1, 1, 'V', 'V', False), 
   'KURT': (
          322, 1, 30, 'V', 'R ...', False), 
   'LARGE': (
           325, 2, 2, 'V', 'R V', False), 
   'LEFT': (
          115, 1, 2, 'V', 'V V', False), 
   'LEFTB': (
           208, 1, 2, 'V', 'V V', False), 
   'LEN': (
         32, 1, 1, 'V', 'V', False), 
   'LENB': (
          211, 1, 1, 'V', 'V', False), 
   'LINEST': (
            49, 1, 4, 'A', 'R R V V', False), 
   'LN': (
        22, 1, 1, 'V', 'V', False), 
   'LOG': (
         109, 1, 2, 'V', 'V V', False), 
   'LOG10': (
           23, 1, 1, 'V', 'V', False), 
   'LOGEST': (
            51, 1, 4, 'A', 'R R V V', False), 
   'LOGINV': (
            291, 3, 3, 'V', 'V V V', False), 
   'LOGNORMDIST': (
                 290, 3, 3, 'V', 'V V V', False), 
   'LOOKUP': (
            28, 2, 3, 'V', 'V R R', False), 
   'LOWER': (
           112, 1, 1, 'V', 'V', False), 
   'MATCH': (
           64, 2, 3, 'V', 'V R R', False), 
   'MAX': (
         7, 1, 30, 'V', 'R ...', False), 
   'MAXA': (
          362, 1, 30, 'V', 'R ...', False), 
   'MDETERM': (
             163, 1, 1, 'V', 'A', False), 
   'MEDIAN': (
            227, 1, 30, 'V', 'R ...', False), 
   'MID': (
         31, 3, 3, 'V', 'V V V', False), 
   'MIDB': (
          210, 3, 3, 'V', 'V V V', False), 
   'MIN': (
         6, 1, 30, 'V', 'R ...', False), 
   'MINA': (
          363, 1, 30, 'V', 'R ...', False), 
   'MINUTE': (
            72, 1, 1, 'V', 'V', False), 
   'MINVERSE': (
              164, 1, 1, 'A', 'A', False), 
   'MIRR': (
          61, 3, 3, 'V', 'R V V', False), 
   'MMULT': (
           165, 2, 2, 'A', 'A A', False), 
   'MNORMSINV': (
               296, 1, 1, 'V', 'V', False), 
   'MOD': (
         39, 2, 2, 'V', 'V V', False), 
   'MODE': (
          330, 1, 30, 'V', 'A ...', False), 
   'MONTH': (
           68, 1, 1, 'V', 'V', False), 
   'N': (
       131, 1, 1, 'V', 'R', False), 
   'NA': (
        10, 0, 0, 'V', '-', False), 
   'NEGBINOMDIST': (
                  292, 3, 3, 'V', 'V V V', False), 
   'NORMDIST': (
              293, 4, 4, 'V', 'V V V V', False), 
   'NORMINV': (
             295, 3, 3, 'V', 'V V V', False), 
   'NORMSDIST': (
               294, 1, 1, 'V', 'V', False), 
   'NOT': (
         38, 1, 1, 'V', 'V', False), 
   'NOW': (
         74, 0, 0, 'V', '-', True), 
   'NPER': (
          58, 3, 5, 'V', 'V V V V V', False), 
   'NPV': (
         11, 2, 30, 'V', 'V R ...', False), 
   'NUMBERSTRING': (
                  353, 2, 2, 'V', 'V V', False), 
   'ODD': (
         298, 1, 1, 'V', 'V', False), 
   'OFFSET': (
            78, 3, 5, 'R', 'R V V V V', True), 
   'OR': (
        37, 1, 30, 'V', 'R ...', False), 
   'PEARSON': (
             312, 2, 2, 'V', 'A A', False), 
   'PERCENTILE': (
                328, 2, 2, 'V', 'R V', False), 
   'PERCENTRANK': (
                 329, 2, 3, 'V', 'R V V', False), 
   'PERMUT': (
            299, 2, 2, 'V', 'V V', False), 
   'PHONETIC': (
              360, 1, 1, 'V', 'R', False), 
   'PI': (
        19, 0, 0, 'V', '-', False), 
   'PMT': (
         59, 3, 5, 'V', 'V V V V V', False), 
   'POISSON': (
             300, 3, 3, 'V', 'V V V', False), 
   'POWER': (
           337, 2, 2, 'V', 'V V', False), 
   'PPMT': (
          168, 4, 6, 'V', 'V V V V V V', False), 
   'PROB': (
          317, 3, 4, 'V', 'A A V V', False), 
   'PRODUCT': (
             183, 0, 30, 'V', 'R ...', False), 
   'PROPER': (
            114, 1, 1, 'V', 'V', False), 
   'PV': (
        56, 3, 5, 'V', 'V V V V V', False), 
   'QUARTILE': (
              327, 2, 2, 'V', 'R V', False), 
   'RADIANS': (
             342, 1, 1, 'V', 'V', False), 
   'RAND': (
          63, 0, 0, 'V', '-', True), 
   'RANK': (
          216, 2, 3, 'V', 'V R V', False), 
   'RATE': (
          60, 3, 6, 'V', 'V V V V V V', False), 
   'REPLACE': (
             119, 4, 4, 'V', 'V V V V', False), 
   'REPLACEB': (
              207, 4, 4, 'V', 'V V V V', False), 
   'REPT': (
          30, 2, 2, 'V', 'V V', False), 
   'RIGHT': (
           116, 1, 2, 'V', 'V V', False), 
   'RIGHTB': (
            209, 1, 2, 'V', 'V V', False), 
   'ROMAN': (
           354, 1, 2, 'V', 'V V', False), 
   'ROUND': (
           27, 2, 2, 'V', 'V V', False), 
   'ROUNDDOWN': (
               213, 2, 2, 'V', 'V V', False), 
   'ROUNDUP': (
             212, 2, 2, 'V', 'V V', False), 
   'ROW': (
         8, 0, 1, 'V', 'R', False), 
   'ROWS': (
          76, 1, 1, 'V', 'R', False), 
   'RSQ': (
         313, 2, 2, 'V', 'A A', False), 
   'SEARCH': (
            82, 2, 3, 'V', 'V V V', False), 
   'SEARCHB': (
             206, 2, 3, 'V', 'V V V', False), 
   'SECOND': (
            73, 1, 1, 'V', 'V', False), 
   'SIGN': (
          26, 1, 1, 'V', 'V', False), 
   'SIN': (
         15, 1, 1, 'V', 'V', False), 
   'SINH': (
          229, 1, 1, 'V', 'V', False), 
   'SKEW': (
          323, 1, 30, 'V', 'R ...', False), 
   'SLN': (
         142, 3, 3, 'V', 'V V V', False), 
   'SLOPE': (
           315, 2, 2, 'V', 'A A', False), 
   'SMALL': (
           326, 2, 2, 'V', 'R V', False), 
   'SQRT': (
          20, 1, 1, 'V', 'V', False), 
   'STANDARDIZE': (
                 297, 3, 3, 'V', 'V V V', False), 
   'STDEV': (
           12, 1, 30, 'V', 'R ...', False), 
   'STDEVA': (
            366, 1, 30, 'V', 'R ...', False), 
   'STDEVP': (
            193, 1, 30, 'V', 'R ...', False), 
   'STDEVPA': (
             364, 1, 30, 'V', 'R ...', False), 
   'STEYX': (
           314, 2, 2, 'V', 'A A', False), 
   'SUBSTITUTE': (
                120, 3, 4, 'V', 'V V V V', False), 
   'SUBTOTAL': (
              344, 2, 30, 'V', 'V R ...', False), 
   'SUM': (
         4, 0, 30, 'V', 'R ...', False), 
   'SUMIF': (
           345, 2, 3, 'V', 'R V R', False), 
   'SUMPRODUCT': (
                228, 1, 30, 'V', 'A ...', False), 
   'SUMSQ': (
           321, 0, 30, 'V', 'R ...', False), 
   'SUMX2MY2': (
              304, 2, 2, 'V', 'A A', False), 
   'SUMX2PY2': (
              305, 2, 2, 'V', 'A A', False), 
   'SUMXMY2': (
             303, 2, 2, 'V', 'A A', False), 
   'SYD': (
         143, 4, 4, 'V', 'V V V V', False), 
   'T': (
       130, 1, 1, 'V', 'R', False), 
   'TAN': (
         17, 1, 1, 'V', 'V', False), 
   'TANH': (
          231, 1, 1, 'V', 'V', False), 
   'TDIST': (
           301, 3, 3, 'V', 'V V V', False), 
   'TEXT': (
          48, 2, 2, 'V', 'V V', False), 
   'TIME': (
          66, 3, 3, 'V', 'V V V', False), 
   'TIMEVALUE': (
               141, 1, 1, 'V', 'V', False), 
   'TINV': (
          332, 2, 2, 'V', 'V V', False), 
   'TODAY': (
           221, 0, 0, 'V', '-', True), 
   'TRANSPOSE': (
               83, 1, 1, 'A', 'A', False), 
   'TREND': (
           50, 1, 4, 'A', 'R R R V', False), 
   'TRIM': (
          118, 1, 1, 'V', 'V', False), 
   'TRIMMEAN': (
              331, 2, 2, 'V', 'R V', False), 
   'TRUE': (
          34, 0, 0, 'V', '-', False), 
   'TRUNC': (
           197, 1, 2, 'V', 'V V', False), 
   'TTEST': (
           316, 4, 4, 'V', 'A A V V', False), 
   'TYPE': (
          86, 1, 1, 'V', 'V', False), 
   'UPPER': (
           113, 1, 1, 'V', 'V', False), 
   'USDOLLAR': (
              204, 1, 2, 'V', 'V V', False), 
   'VALUE': (
           33, 1, 1, 'V', 'V', False), 
   'VAR': (
         46, 1, 30, 'V', 'R ...', False), 
   'VARA': (
          367, 1, 30, 'V', 'R ...', False), 
   'VARP': (
          194, 1, 30, 'V', 'R ...', False), 
   'VARPA': (
           365, 1, 30, 'V', 'R ...', False), 
   'VDB': (
         222, 5, 7, 'V', 'V V V V V V V', False), 
   'VLOOKUP': (
             102, 3, 4, 'V', 'V R R V', False), 
   'WEEKDAY': (
             70, 1, 2, 'V', 'V V', False), 
   'WEIBULL': (
             302, 4, 4, 'V', 'V V V V', False), 
   'YEAR': (
          69, 1, 1, 'V', 'V', False), 
   'ZTEST': (
           324, 2, 3, 'V', 'R V V', False)}
std_func_by_num = {0: (
     'COUNT', 0, 30, 'V', 'R ...', False), 
   1: (
     'IF', 2, 3, 'R', 'V R R', False), 
   2: (
     'ISNA', 1, 1, 'V', 'V', False), 
   3: (
     'ISERROR', 1, 1, 'V', 'V', False), 
   4: (
     'SUM', 0, 30, 'V', 'R ...', False), 
   5: (
     'AVERAGE', 1, 30, 'V', 'R ...', False), 
   6: (
     'MIN', 1, 30, 'V', 'R ...', False), 
   7: (
     'MAX', 1, 30, 'V', 'R ...', False), 
   8: (
     'ROW', 0, 1, 'V', 'R', False), 
   9: (
     'COLUMN', 0, 1, 'V', 'R', False), 
   10: (
      'NA', 0, 0, 'V', '-', False), 
   11: (
      'NPV', 2, 30, 'V', 'V R ...', False), 
   12: (
      'STDEV', 1, 30, 'V', 'R ...', False), 
   13: (
      'DOLLAR', 1, 2, 'V', 'V V', False), 
   14: (
      'FIXED', 2, 3, 'V', 'V V V', False), 
   15: (
      'SIN', 1, 1, 'V', 'V', False), 
   16: (
      'COS', 1, 1, 'V', 'V', False), 
   17: (
      'TAN', 1, 1, 'V', 'V', False), 
   18: (
      'ARCTAN', 1, 1, 'V', 'V', False), 
   19: (
      'PI', 0, 0, 'V', '-', False), 
   20: (
      'SQRT', 1, 1, 'V', 'V', False), 
   21: (
      'EXP', 1, 1, 'V', 'V', False), 
   22: (
      'LN', 1, 1, 'V', 'V', False), 
   23: (
      'LOG10', 1, 1, 'V', 'V', False), 
   24: (
      'ABS', 1, 1, 'V', 'V', False), 
   25: (
      'INT', 1, 1, 'V', 'V', False), 
   26: (
      'SIGN', 1, 1, 'V', 'V', False), 
   27: (
      'ROUND', 2, 2, 'V', 'V V', False), 
   28: (
      'LOOKUP', 2, 3, 'V', 'V R R', False), 
   29: (
      'INDEX', 2, 4, 'R', 'R V V V', False), 
   30: (
      'REPT', 2, 2, 'V', 'V V', False), 
   31: (
      'MID', 3, 3, 'V', 'V V V', False), 
   32: (
      'LEN', 1, 1, 'V', 'V', False), 
   33: (
      'VALUE', 1, 1, 'V', 'V', False), 
   34: (
      'TRUE', 0, 0, 'V', '-', False), 
   35: (
      'FALSE', 0, 0, 'V', '-', False), 
   36: (
      'AND', 1, 30, 'V', 'R ...', False), 
   37: (
      'OR', 1, 30, 'V', 'R ...', False), 
   38: (
      'NOT', 1, 1, 'V', 'V', False), 
   39: (
      'MOD', 2, 2, 'V', 'V V', False), 
   40: (
      'DCOUNT', 3, 3, 'V', 'R R R', False), 
   41: (
      'DSUM', 3, 3, 'V', 'R R R', False), 
   42: (
      'DAVERAGE', 3, 3, 'V', 'R R R', False), 
   43: (
      'DMIN', 3, 3, 'V', 'R R R', False), 
   44: (
      'DMAX', 3, 3, 'V', 'R R R', False), 
   45: (
      'DSTDEV', 3, 3, 'V', 'R R R', False), 
   46: (
      'VAR', 1, 30, 'V', 'R ...', False), 
   47: (
      'DVAR', 3, 3, 'V', 'R R R', False), 
   48: (
      'TEXT', 2, 2, 'V', 'V V', False), 
   49: (
      'LINEST', 1, 4, 'A', 'R R V V', False), 
   50: (
      'TREND', 1, 4, 'A', 'R R R V', False), 
   51: (
      'LOGEST', 1, 4, 'A', 'R R V V', False), 
   52: (
      'GROWTH', 1, 4, 'A', 'R R R V', False), 
   56: (
      'PV', 3, 5, 'V', 'V V V V V', False), 
   57: (
      'FV', 3, 5, 'V', 'V V V V V', False), 
   58: (
      'NPER', 3, 5, 'V', 'V V V V V', False), 
   59: (
      'PMT', 3, 5, 'V', 'V V V V V', False), 
   60: (
      'RATE', 3, 6, 'V', 'V V V V V V', False), 
   61: (
      'MIRR', 3, 3, 'V', 'R V V', False), 
   62: (
      'IRR', 1, 2, 'V', 'R V', False), 
   63: (
      'RAND', 0, 0, 'V', '-', True), 
   64: (
      'MATCH', 2, 3, 'V', 'V R R', False), 
   65: (
      'DATE', 3, 3, 'V', 'V V V', False), 
   66: (
      'TIME', 3, 3, 'V', 'V V V', False), 
   67: (
      'DAY', 1, 1, 'V', 'V', False), 
   68: (
      'MONTH', 1, 1, 'V', 'V', False), 
   69: (
      'YEAR', 1, 1, 'V', 'V', False), 
   70: (
      'WEEKDAY', 1, 2, 'V', 'V V', False), 
   71: (
      'HOUR', 1, 1, 'V', 'V', False), 
   72: (
      'MINUTE', 1, 1, 'V', 'V', False), 
   73: (
      'SECOND', 1, 1, 'V', 'V', False), 
   74: (
      'NOW', 0, 0, 'V', '-', True), 
   75: (
      'AREAS', 1, 1, 'V', 'R', False), 
   76: (
      'ROWS', 1, 1, 'V', 'R', False), 
   77: (
      'COLUMNS', 1, 1, 'V', 'R', False), 
   78: (
      'OFFSET', 3, 5, 'R', 'R V V V V', True), 
   82: (
      'SEARCH', 2, 3, 'V', 'V V V', False), 
   83: (
      'TRANSPOSE', 1, 1, 'A', 'A', False), 
   86: (
      'TYPE', 1, 1, 'V', 'V', False), 
   97: (
      'ATAN2', 2, 2, 'V', 'V V', False), 
   98: (
      'ASIN', 1, 1, 'V', 'V', False), 
   99: (
      'ACOS', 1, 1, 'V', 'V', False), 
   100: (
       'CHOOSE', 2, 30, 'R', 'V R ...', False), 
   101: (
       'HLOOKUP', 3, 4, 'V', 'V R R V', False), 
   102: (
       'VLOOKUP', 3, 4, 'V', 'V R R V', False), 
   105: (
       'ISREF', 1, 1, 'V', 'R', False), 
   109: (
       'LOG', 1, 2, 'V', 'V V', False), 
   111: (
       'CHAR', 1, 1, 'V', 'V', False), 
   112: (
       'LOWER', 1, 1, 'V', 'V', False), 
   113: (
       'UPPER', 1, 1, 'V', 'V', False), 
   114: (
       'PROPER', 1, 1, 'V', 'V', False), 
   115: (
       'LEFT', 1, 2, 'V', 'V V', False), 
   116: (
       'RIGHT', 1, 2, 'V', 'V V', False), 
   117: (
       'EXACT', 2, 2, 'V', 'V V', False), 
   118: (
       'TRIM', 1, 1, 'V', 'V', False), 
   119: (
       'REPLACE', 4, 4, 'V', 'V V V V', False), 
   120: (
       'SUBSTITUTE', 3, 4, 'V', 'V V V V', False), 
   121: (
       'CODE', 1, 1, 'V', 'V', False), 
   124: (
       'FIND', 2, 3, 'V', 'V V V', False), 
   125: (
       'CELL', 1, 2, 'V', 'V R', True), 
   126: (
       'ISERR', 1, 1, 'V', 'V', False), 
   127: (
       'ISTEXT', 1, 1, 'V', 'V', False), 
   128: (
       'ISNUMBER', 1, 1, 'V', 'V', False), 
   129: (
       'ISBLANK', 1, 1, 'V', 'V', False), 
   130: (
       'T', 1, 1, 'V', 'R', False), 
   131: (
       'N', 1, 1, 'V', 'R', False), 
   140: (
       'DATEVALUE', 1, 1, 'V', 'V', False), 
   141: (
       'TIMEVALUE', 1, 1, 'V', 'V', False), 
   142: (
       'SLN', 3, 3, 'V', 'V V V', False), 
   143: (
       'SYD', 4, 4, 'V', 'V V V V', False), 
   144: (
       'DDB', 4, 5, 'V', 'V V V V V', False), 
   148: (
       'INDIRECT', 1, 2, 'R', 'V V', True), 
   162: (
       'CLEAN', 1, 1, 'V', 'V', False), 
   163: (
       'MDETERM', 1, 1, 'V', 'A', False), 
   164: (
       'MINVERSE', 1, 1, 'A', 'A', False), 
   165: (
       'MMULT', 2, 2, 'A', 'A A', False), 
   167: (
       'IPMT', 4, 6, 'V', 'V V V V V V', False), 
   168: (
       'PPMT', 4, 6, 'V', 'V V V V V V', False), 
   169: (
       'COUNTA', 0, 30, 'V', 'R ...', False), 
   183: (
       'PRODUCT', 0, 30, 'V', 'R ...', False), 
   184: (
       'FACT', 1, 1, 'V', 'V', False), 
   191: (
       'DPRODUCT', 3, 3, 'V', 'R R R', False), 
   192: (
       'ISNONTEXT', 1, 1, 'V', 'V', False), 
   193: (
       'STDEVP', 1, 30, 'V', 'R ...', False), 
   194: (
       'VARP', 1, 30, 'V', 'R ...', False), 
   195: (
       'DSTDEVP', 3, 3, 'V', 'R R R', False), 
   196: (
       'DVARP', 3, 3, 'V', 'R R R', False), 
   197: (
       'TRUNC', 1, 2, 'V', 'V V', False), 
   198: (
       'ISLOGICAL', 1, 1, 'V', 'V', False), 
   199: (
       'DCOUNTA', 3, 3, 'V', 'R R R', False), 
   204: (
       'USDOLLAR', 1, 2, 'V', 'V V', False), 
   205: (
       'FINDB', 2, 3, 'V', 'V V V', False), 
   206: (
       'SEARCHB', 2, 3, 'V', 'V V V', False), 
   207: (
       'REPLACEB', 4, 4, 'V', 'V V V V', False), 
   208: (
       'LEFTB', 1, 2, 'V', 'V V', False), 
   209: (
       'RIGHTB', 1, 2, 'V', 'V V', False), 
   210: (
       'MIDB', 3, 3, 'V', 'V V V', False), 
   211: (
       'LENB', 1, 1, 'V', 'V', False), 
   212: (
       'ROUNDUP', 2, 2, 'V', 'V V', False), 
   213: (
       'ROUNDDOWN', 2, 2, 'V', 'V V', False), 
   214: (
       'ASC', 1, 1, 'V', 'V', False), 
   215: (
       'DBSC', 1, 1, 'V', 'V', False), 
   216: (
       'RANK', 2, 3, 'V', 'V R V', False), 
   219: (
       'ADDRESS', 2, 5, 'V', 'V V V V V', False), 
   220: (
       'DAYS360', 2, 3, 'V', 'V V V', False), 
   221: (
       'TODAY', 0, 0, 'V', '-', True), 
   222: (
       'VDB', 5, 7, 'V', 'V V V V V V V', False), 
   227: (
       'MEDIAN', 1, 30, 'V', 'R ...', False), 
   228: (
       'SUMPRODUCT', 1, 30, 'V', 'A ...', False), 
   229: (
       'SINH', 1, 1, 'V', 'V', False), 
   230: (
       'COSH', 1, 1, 'V', 'V', False), 
   231: (
       'TANH', 1, 1, 'V', 'V', False), 
   232: (
       'ASINH', 1, 1, 'V', 'V', False), 
   233: (
       'ACOSH', 1, 1, 'V', 'V', False), 
   234: (
       'ATANH', 1, 1, 'V', 'V', False), 
   235: (
       'DGET', 3, 3, 'V', 'R R R', False), 
   244: (
       'INFO', 1, 1, 'V', 'V', False), 
   247: (
       'DB', 4, 5, 'V', 'V V V V V', False), 
   252: (
       'FREQUENCY', 2, 2, 'A', 'R R', False), 
   261: (
       'ERROR.TYPE', 1, 1, 'V', 'V', False), 
   269: (
       'AVEDEV', 1, 30, 'V', 'R ...', False), 
   270: (
       'BETADIST', 3, 5, 'V', 'V V V V V', False), 
   271: (
       'GAMMALN', 1, 1, 'V', 'V', False), 
   272: (
       'BETAINV', 3, 5, 'V', 'V V V V V', False), 
   273: (
       'BINOMDIST', 4, 4, 'V', 'V V V V', False), 
   274: (
       'CHIDIST', 2, 2, 'V', 'V V', False), 
   275: (
       'CHIINV', 2, 2, 'V', 'V V', False), 
   276: (
       'COMBIN', 2, 2, 'V', 'V V', False), 
   277: (
       'CONFIDENCE', 3, 3, 'V', 'V V V', False), 
   278: (
       'CRITBINOM', 3, 3, 'V', 'V V V', False), 
   279: (
       'EVEN', 1, 1, 'V', 'V', False), 
   280: (
       'EXPONDIST', 3, 3, 'V', 'V V V', False), 
   281: (
       'FDIST', 3, 3, 'V', 'V V V', False), 
   282: (
       'FINV', 3, 3, 'V', 'V V V', False), 
   283: (
       'FISHER', 1, 1, 'V', 'V', False), 
   284: (
       'FISHERINV', 1, 1, 'V', 'V', False), 
   285: (
       'FLOOR', 2, 2, 'V', 'V V', False), 
   286: (
       'GAMMADIST', 4, 4, 'V', 'V V V V', False), 
   287: (
       'GAMMAINV', 3, 3, 'V', 'V V V', False), 
   288: (
       'CEILING', 2, 2, 'V', 'V V', False), 
   289: (
       'HYPGEOMVERT', 4, 4, 'V', 'V V V V', False), 
   290: (
       'LOGNORMDIST', 3, 3, 'V', 'V V V', False), 
   291: (
       'LOGINV', 3, 3, 'V', 'V V V', False), 
   292: (
       'NEGBINOMDIST', 3, 3, 'V', 'V V V', False), 
   293: (
       'NORMDIST', 4, 4, 'V', 'V V V V', False), 
   294: (
       'NORMSDIST', 1, 1, 'V', 'V', False), 
   295: (
       'NORMINV', 3, 3, 'V', 'V V V', False), 
   296: (
       'MNORMSINV', 1, 1, 'V', 'V', False), 
   297: (
       'STANDARDIZE', 3, 3, 'V', 'V V V', False), 
   298: (
       'ODD', 1, 1, 'V', 'V', False), 
   299: (
       'PERMUT', 2, 2, 'V', 'V V', False), 
   300: (
       'POISSON', 3, 3, 'V', 'V V V', False), 
   301: (
       'TDIST', 3, 3, 'V', 'V V V', False), 
   302: (
       'WEIBULL', 4, 4, 'V', 'V V V V', False), 
   303: (
       'SUMXMY2', 2, 2, 'V', 'A A', False), 
   304: (
       'SUMX2MY2', 2, 2, 'V', 'A A', False), 
   305: (
       'SUMX2PY2', 2, 2, 'V', 'A A', False), 
   306: (
       'CHITEST', 2, 2, 'V', 'A A', False), 
   307: (
       'CORREL', 2, 2, 'V', 'A A', False), 
   308: (
       'COVAR', 2, 2, 'V', 'A A', False), 
   309: (
       'FORECAST', 3, 3, 'V', 'V A A', False), 
   310: (
       'FTEST', 2, 2, 'V', 'A A', False), 
   311: (
       'INTERCEPT', 2, 2, 'V', 'A A', False), 
   312: (
       'PEARSON', 2, 2, 'V', 'A A', False), 
   313: (
       'RSQ', 2, 2, 'V', 'A A', False), 
   314: (
       'STEYX', 2, 2, 'V', 'A A', False), 
   315: (
       'SLOPE', 2, 2, 'V', 'A A', False), 
   316: (
       'TTEST', 4, 4, 'V', 'A A V V', False), 
   317: (
       'PROB', 3, 4, 'V', 'A A V V', False), 
   318: (
       'DEVSQ', 1, 30, 'V', 'R ...', False), 
   319: (
       'GEOMEAN', 1, 30, 'V', 'R ...', False), 
   320: (
       'HARMEAN', 1, 30, 'V', 'R ...', False), 
   321: (
       'SUMSQ', 0, 30, 'V', 'R ...', False), 
   322: (
       'KURT', 1, 30, 'V', 'R ...', False), 
   323: (
       'SKEW', 1, 30, 'V', 'R ...', False), 
   324: (
       'ZTEST', 2, 3, 'V', 'R V V', False), 
   325: (
       'LARGE', 2, 2, 'V', 'R V', False), 
   326: (
       'SMALL', 2, 2, 'V', 'R V', False), 
   327: (
       'QUARTILE', 2, 2, 'V', 'R V', False), 
   328: (
       'PERCENTILE', 2, 2, 'V', 'R V', False), 
   329: (
       'PERCENTRANK', 2, 3, 'V', 'R V V', False), 
   330: (
       'MODE', 1, 30, 'V', 'A ...', False), 
   331: (
       'TRIMMEAN', 2, 2, 'V', 'R V', False), 
   332: (
       'TINV', 2, 2, 'V', 'V V', False), 
   336: (
       'CONCATENATE', 0, 30, 'V', 'V ...', False), 
   337: (
       'POWER', 2, 2, 'V', 'V V', False), 
   342: (
       'RADIANS', 1, 1, 'V', 'V', False), 
   343: (
       'DEGREES', 1, 1, 'V', 'V', False), 
   344: (
       'SUBTOTAL', 2, 30, 'V', 'V R ...', False), 
   345: (
       'SUMIF', 2, 3, 'V', 'R V R', False), 
   346: (
       'COUNTIF', 2, 2, 'V', 'R V', False), 
   347: (
       'COUNTBLANK', 1, 1, 'V', 'R', False), 
   350: (
       'ISPMT', 4, 4, 'V', 'V V V V', False), 
   351: (
       'DATEDIF', 3, 3, 'V', 'V V V', False), 
   352: (
       'DATESTRING', 1, 1, 'V', 'V', False), 
   353: (
       'NUMBERSTRING', 2, 2, 'V', 'V V', False), 
   354: (
       'ROMAN', 1, 2, 'V', 'V V', False), 
   358: (
       'GETPIVOTDATA', 2, 30, 'A', '-', False), 
   359: (
       'HYPERLINK', 1, 2, 'V', 'V V', False), 
   360: (
       'PHONETIC', 1, 1, 'V', 'R', False), 
   361: (
       'AVERAGEA', 1, 30, 'V', 'R ...', False), 
   362: (
       'MAXA', 1, 30, 'V', 'R ...', False), 
   363: (
       'MINA', 1, 30, 'V', 'R ...', False), 
   364: (
       'STDEVPA', 1, 30, 'V', 'R ...', False), 
   365: (
       'VARPA', 1, 30, 'V', 'R ...', False), 
   366: (
       'STDEVA', 1, 30, 'V', 'R ...', False), 
   367: (
       'VARA', 1, 30, 'V', 'R ...', False)}
ptgExp = 1
ptgTbl = 2
ptgAdd = 3
ptgSub = 4
ptgMul = 5
ptgDiv = 6
ptgPower = 7
ptgConcat = 8
ptgLT = 9
ptgLE = 10
ptgEQ = 11
ptgGE = 12
ptgGT = 13
ptgNE = 14
ptgIsect = 15
ptgUnion = 16
ptgRange = 17
ptgUplus = 18
ptgUminus = 19
ptgPercent = 20
ptgParen = 21
ptgMissArg = 22
ptgStr = 23
ptgExtend = 24
ptgAttr = 25
ptgSheet = 26
ptgEndSheet = 27
ptgErr = 28
ptgBool = 29
ptgInt = 30
ptgNum = 31
ptgArrayR = 32
ptgFuncR = 33
ptgFuncVarR = 34
ptgNameR = 35
ptgRefR = 36
ptgAreaR = 37
ptgMemAreaR = 38
ptgMemErrR = 39
ptgMemNoMemR = 40
ptgMemFuncR = 41
ptgRefErrR = 42
ptgAreaErrR = 43
ptgRefNR = 44
ptgAreaNR = 45
ptgMemAreaNR = 46
ptgMemNoMemNR = 47
ptgNameXR = 57
ptgRef3dR = 58
ptgArea3dR = 59
ptgRefErr3dR = 60
ptgAreaErr3dR = 61
ptgArrayV = 64
ptgFuncV = 65
ptgFuncVarV = 66
ptgNameV = 67
ptgRefV = 68
ptgAreaV = 69
ptgMemAreaV = 70
ptgMemErrV = 71
ptgMemNoMemV = 72
ptgMemFuncV = 73
ptgRefErrV = 74
ptgAreaErrV = 75
ptgRefNV = 76
ptgAreaNV = 77
ptgMemAreaNV = 78
ptgMemNoMemNV = 79
ptgFuncCEV = 88
ptgNameXV = 89
ptgRef3dV = 90
ptgArea3dV = 91
ptgRefErr3dV = 92
ptgAreaErr3dV = 93
ptgArrayA = 96
ptgFuncA = 97
ptgFuncVarA = 98
ptgNameA = 99
ptgRefA = 100
ptgAreaA = 101
ptgMemAreaA = 102
ptgMemErrA = 103
ptgMemNoMemA = 104
ptgMemFuncA = 105
ptgRefErrA = 106
ptgAreaErrA = 107
ptgRefNA = 108
ptgAreaNA = 109
ptgMemAreaNA = 110
ptgMemNoMemNA = 111
ptgFuncCEA = 120
ptgNameXA = 121
ptgRef3dA = 122
ptgArea3dA = 123
ptgRefErr3dA = 124
ptgAreaErr3dA = 125
PtgNames = {ptgExp: 'ptgExp', 
   ptgTbl: 'ptgTbl', 
   ptgAdd: 'ptgAdd', 
   ptgSub: 'ptgSub', 
   ptgMul: 'ptgMul', 
   ptgDiv: 'ptgDiv', 
   ptgPower: 'ptgPower', 
   ptgConcat: 'ptgConcat', 
   ptgLT: 'ptgLT', 
   ptgLE: 'ptgLE', 
   ptgEQ: 'ptgEQ', 
   ptgGE: 'ptgGE', 
   ptgGT: 'ptgGT', 
   ptgNE: 'ptgNE', 
   ptgIsect: 'ptgIsect', 
   ptgUnion: 'ptgUnion', 
   ptgRange: 'ptgRange', 
   ptgUplus: 'ptgUplus', 
   ptgUminus: 'ptgUminus', 
   ptgPercent: 'ptgPercent', 
   ptgParen: 'ptgParen', 
   ptgMissArg: 'ptgMissArg', 
   ptgStr: 'ptgStr', 
   ptgExtend: 'ptgExtend', 
   ptgAttr: 'ptgAttr', 
   ptgSheet: 'ptgSheet', 
   ptgEndSheet: 'ptgEndSheet', 
   ptgErr: 'ptgErr', 
   ptgBool: 'ptgBool', 
   ptgInt: 'ptgInt', 
   ptgNum: 'ptgNum', 
   ptgArrayR: 'ptgArrayR', 
   ptgFuncR: 'ptgFuncR', 
   ptgFuncVarR: 'ptgFuncVarR', 
   ptgNameR: 'ptgNameR', 
   ptgRefR: 'ptgRefR', 
   ptgAreaR: 'ptgAreaR', 
   ptgMemAreaR: 'ptgMemAreaR', 
   ptgMemErrR: 'ptgMemErrR', 
   ptgMemNoMemR: 'ptgMemNoMemR', 
   ptgMemFuncR: 'ptgMemFuncR', 
   ptgRefErrR: 'ptgRefErrR', 
   ptgAreaErrR: 'ptgAreaErrR', 
   ptgRefNR: 'ptgRefNR', 
   ptgAreaNR: 'ptgAreaNR', 
   ptgMemAreaNR: 'ptgMemAreaNR', 
   ptgMemNoMemNR: 'ptgMemNoMemNR', 
   ptgNameXR: 'ptgNameXR', 
   ptgRef3dR: 'ptgRef3dR', 
   ptgArea3dR: 'ptgArea3dR', 
   ptgRefErr3dR: 'ptgRefErr3dR', 
   ptgAreaErr3dR: 'ptgAreaErr3dR', 
   ptgArrayV: 'ptgArrayV', 
   ptgFuncV: 'ptgFuncV', 
   ptgFuncVarV: 'ptgFuncVarV', 
   ptgNameV: 'ptgNameV', 
   ptgRefV: 'ptgRefV', 
   ptgAreaV: 'ptgAreaV', 
   ptgMemAreaV: 'ptgMemAreaV', 
   ptgMemErrV: 'ptgMemErrV', 
   ptgMemNoMemV: 'ptgMemNoMemV', 
   ptgMemFuncV: 'ptgMemFuncV', 
   ptgRefErrV: 'ptgRefErrV', 
   ptgAreaErrV: 'ptgAreaErrV', 
   ptgRefNV: 'ptgRefNV', 
   ptgAreaNV: 'ptgAreaNV', 
   ptgMemAreaNV: 'ptgMemAreaNV', 
   ptgMemNoMemNV: 'ptgMemNoMemNV', 
   ptgFuncCEV: 'ptgFuncCEV', 
   ptgNameXV: 'ptgNameXV', 
   ptgRef3dV: 'ptgRef3dV', 
   ptgArea3dV: 'ptgArea3dV', 
   ptgRefErr3dV: 'ptgRefErr3dV', 
   ptgAreaErr3dV: 'ptgAreaErr3dV', 
   ptgArrayA: 'ptgArrayA', 
   ptgFuncA: 'ptgFuncA', 
   ptgFuncVarA: 'ptgFuncVarA', 
   ptgNameA: 'ptgNameA', 
   ptgRefA: 'ptgRefA', 
   ptgAreaA: 'ptgAreaA', 
   ptgMemAreaA: 'ptgMemAreaA', 
   ptgMemErrA: 'ptgMemErrA', 
   ptgMemNoMemA: 'ptgMemNoMemA', 
   ptgMemFuncA: 'ptgMemFuncA', 
   ptgRefErrA: 'ptgRefErrA', 
   ptgAreaErrA: 'ptgAreaErrA', 
   ptgRefNA: 'ptgRefNA', 
   ptgAreaNA: 'ptgAreaNA', 
   ptgMemAreaNA: 'ptgMemAreaNA', 
   ptgMemNoMemNA: 'ptgMemNoMemNA', 
   ptgFuncCEA: 'ptgFuncCEA', 
   ptgNameXA: 'ptgNameXA', 
   ptgRef3dA: 'ptgRef3dA', 
   ptgArea3dA: 'ptgArea3dA', 
   ptgRefErr3dA: 'ptgRefErr3dA', 
   ptgAreaErr3dA: 'ptgAreaErr3dA'}
error_msg_by_code = {0: '#NULL!', 
   7: '#DIV/0!', 
   15: '#VALUE!', 
   23: '#REF!', 
   29: '#NAME?', 
   36: '#NUM!', 
   42: '#N/A!'}