# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chessmind/core/definitions.py
# Compiled at: 2008-04-25 20:06:43
ROWS = 3
COLS = 3
CHESS_ROWS = 8
CHESS_COLS = 8
PLAIN = 0
WHITE = 1
BLACK = -1
CHESS_BOARD = '\nrnbqkbnr\npppppppp\n........\n........\n........\n........\nPPPPPPPP\nRNBQKBNR\n'
EMPTY_CHESS_BOARD = '\n........\n........\n........\n........\n........\n........\n........\n........\n'
HINT_BOARD = '\nk.......\np..R....\n........\n........\n........\n........\n........\n.......K\n'
CASTLING_BOARD = '\nr...k..r\n.p......\n........\n........\n........\n........\n.P......\nR...K..R\n'
ENDGAME_BOARD = '\n....k..r\npp......\n.bN.....\n........\n........\n.q....P.\n......K.\nQ.......\n'
PROMOTION_BOARD = '\n.......r\nRpP..kP.\n...P..N.\n........\n........\n...p....\nP...p.K.\n........\n'
MATE_BOARD = '\n......rk\n......pp\n...p....\n....N...\n........\n......q.\nr.......\n.......K\n'
DEFEND_KING_BOARD = '\n..k..Qnr\nppp....p\n..nppq.B\n........\n.....P..\n..N.....\nPPP..PPP\nR....RK.\n'
CASTLE_PAIRS = ({'colour': WHITE, 'king_start': 'E1', 'king_middle': 'D1', 'king_end': 'C1', 'rook_start': 'A1', 'rook_end': 'D1'}, {'colour': WHITE, 'king_start': 'E1', 'king_middle': 'F1', 'king_end': 'G1', 'rook_start': 'H1', 'rook_end': 'F1'}, {'colour': BLACK, 'king_start': 'E8', 'king_middle': 'D8', 'king_end': 'C8', 'rook_start': 'A8', 'rook_end': 'D8'}, {'colour': BLACK, 'king_start': 'E8', 'king_middle': 'F8', 'king_end': 'G8', 'rook_start': 'H8', 'rook_end': 'F8'})