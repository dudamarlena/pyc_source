# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/andaluh/defs.py
# Compiled at: 2019-02-19 15:10:53
VOWELS_ALL_NOTILDE = 'aeiouâêîôûAEIOUÂÊÎÔÛ'
VOWELS_ALL_TILDE = 'áéíóúâêîôûÁÉÍÓÚÂÊÎÔÛ'
VAF = 'ç'
VVF = 'h'
DIGRAPHS = [
 'bb', 'bc', 'bç', 'bÇ', 'bd', 'bf', 'bg', 'bh', 'bm', 'bn', 'bp', 'bq', 'bt', 'bx', 'by', 'cb', 'cc',
 'cç', 'cÇ', 'cd', 'cf', 'cg', 'ch', 'cm', 'cn', 'cp', 'cq', 'ct', 'cx', 'cy',
 'db', 'dc', 'dç', 'dÇ', 'dd', 'df', 'dg', 'dh', 'dl', 'dm', 'dn', 'dp', 'dq', 'dt', 'dx', 'dy',
 'fb', 'fc', 'fç', 'fÇ', 'fd', 'ff', 'fg', 'fh', 'fm', 'fn', 'fp', 'fq', 'ft', 'fx', 'fy',
 'gb', 'gc', 'gç', 'gÇ', 'gd', 'gf', 'gg', 'gh', 'gm', 'gn', 'gp', 'gq', 'gt', 'gx', 'gy',
 'jb', 'jc', 'jç', 'jÇ', 'jd', 'jf', 'jg', 'jh', 'jl', 'jm', 'jn', 'jp', 'jq', 'jr', 'jt', 'jx', 'jy',
 'lb', 'lc', 'lç', 'lÇ', 'ld', 'lf', 'lg', 'lh', 'll', 'lm', 'ln', 'lp', 'lq', 'lr', 'lt', 'lx', 'ly',
 'mm', 'mn',
 'nm', 'nn',
 'pb', 'pc', 'pç', 'pÇ', 'pd', 'pf', 'pg', 'ph', 'pm', 'pn', 'pp', 'pq', 'pt', 'px', 'py',
 'rn',
 'sb', 'sc', 'sç', 'sÇ', 'sd', 'sf', 'sg', 'sh', 'sk', 'sl', 'sm', 'sn', 'sñ', 'sp', 'sq', 'sr', 'st', 'sx', 'sy',
 'tb', 'tc', 'tç', 'tÇ', 'td', 'tf', 'tg', 'th', 'tl', 'tm', 'tn', 'tp', 'tq', 'tt', 'tx', 'ty',
 'xb', 'xc', 'xç', 'xÇ', 'xd', 'xf', 'xg', 'xh', 'xl', 'xm', 'xn', 'xp', 'xq', 'xr', 'xt', 'xx', 'xy',
 'zb', 'zc', 'zç', 'zÇ', 'zd', 'zf', 'zg', 'zh', 'zl', 'zm', 'zn', 'zp', 'zq', 'zr', 'zt', 'zx', 'zy']
H_RULES_EXCEPT = {'haz': 'âh', 
   'hez': 'êh', 'hoz': 'ôh', 'oh': 'ôh', 
   'yihad': 'yihá', 
   'h': 'h'}
GJ_RULES_EXCEPT = {'gin': 'yin', 
   'jazz': 'yâh', 'jet': 'yêh'}
V_RULES_EXCEPT = {'vis': 'bî', 
   'ves': 'bêh'}
LL_RULES_EXCEPT = {'grill': 'grîh'}
WORDEND_D_RULES_EXCEPT = {'çed': 'çêh'}
WORDEND_S_RULES_EXCEPT = {'bies': 'biêh', 
   'bis': 'bîh', 'blues': 'blû', 'bus': 'bûh', 'dios': 'diôh', 
   'dos': 'dôh', 'gas': 'gâh', 
   'gres': 'grêh', 'gris': 'grîh', 'luis': 'luîh', 
   'mies': 'miêh', 
   'mus': 'mûh', 'os': 'ô', 
   'pis': 'pîh', 
   'plus': 'plûh', 'pus': 'pûh', 'ras': 'râh', 
   'res': 'rêh', 'tos': 'tôh', 
   'tres': 'trêh', 'tris': 'trîh'}
WORDEND_CONST_RULES_EXCEPT = {'al': 'al', 
   'cual': 'cuâ', 'del': 'del', 'dél': 'dél', 'el': 'el', 'él': 'èl', 'tal': 'tal', 'bil': 'bîl', 'por': 'por', 
   'uir': 'huîh', 'çic': 'çic', 
   'tac': 'tac', 'yak': 'yak', 
   'stop': 'êttôh', 
   'bip': 'bip'}
WORDEND_D_INTERVOWEL_RULES_EXCEPT = {'fado': 'fado', 
   'cado': 'cado', 'nado': 'nado', 'priado': 'priado', 'fabada': 'fabada', 
   'fabadas': 'fabadas', 'fada': 'fada', 'ada': 'ada', 'lada': 'lada', 'rada': 'rada', 'adas': 'adas', 
   'radas': 'radas', 'nadas': 'nadas', 'aikido': 'aikido', 
   'bûççido': 'bûççido', 'çido': 'çido', 'cuido': 'cuido', 'cupido': 'cupido', 'descuido': 'descuido', 'despido': 'despido', 
   'eido': 'eido', 'embido': 'embido', 'fido': 'fido', 'hido': 'hido', 'ido': 'ido', 'infido': 'infido', 'laido': 'laido', 
   'libido': 'libido', 'nido': 'nido', 'nucleido': 'nucleido', 'çonido': 'çonido', 'çuido': 'çuido'}
ENDING_RULES_EXCEPTION = {'biêmmandao': 'bienmandao', 
   'biêmmeçabe': 'bienmeçabe', 'buêmmoço': 'buenmoço', 'çiêmmiléçima': 'çienmiléçima', 'çiêmmiléçimo': 'çienmiléçimo', 'çiêmmilímetro': 'çienmilímetro', 'çiêmmiyonéçima': 'çienmiyonéçima', 'çiêmmiyonéçimo': 'çienmiyonéçimo', 'çiêmmirmiyonéçima': 'çienmirmiyonéçima', 'çiêmmirmiyonéçimo': 'çienmirmiyonéçimo', 'marrotadôh': 'mârrotadôh', 
   'marrotâh': 'mârrotâh', 'mirrayâ': 'mîrrayâ', 'herôççiquiatría': 'heroçiquiatría', 
   'herôççiquiátrico': 'heroçiquiátrico', 'farmacôççiquiatría': 'farmacoçiquiatría', 'metempçícoçî': 'metemçícoçî', 'necróçico': 'necróççico', 'pampçiquîmmo': 'pamçiquîmmo', 'antîççerôttármico': 'antiçerôttármico', 
   'eclampçia': 'eclampçia', 'pôttoperatorio': 'pôççoperatorio', 'çáccrito': 'çánccrito', 'manbîh': 'mambîh', 'cômmelináçeo': 'commelináçeo', 'dîmmneçia': 'dînneçia', 'todo': 'tó', 'todô': 'tôh', 'toda': 'toa', 'todâ': 'toâ', 'as': 'âh', 
   'clown': 'claun', 'crack': 'crâh', 'down': 'daun', 'es': 'êh', 'ex': 'êh', 'ir': 'îh', 'miss': 'mîh', 'muy': 'mu', 'ôff': 'off', 'os': 'ô', 'para': 'pa', 'ring': 'rin', 'rock': 'rôh', 'spray': 'êppray', 'sprint': 'êpprín', 'wau': 'guau'}