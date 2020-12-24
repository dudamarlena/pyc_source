# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/strategies/spiral.py
# Compiled at: 2016-05-02 03:44:35


def generate_spiral_stream(card, posX, posY):
    """Generate spiral from a selected location on the card"""
    x = y = 0
    dx, dy = (0, -1)
    data = []
    matrix = card.m.tolist()
    for i in range(max(card.rows, card.columns) ** 2):
        if -card.rows / 2 < x <= card.rows / 2 and -card.columns / 2 < y <= card.columns / 2:
            row = y + posX
            column = x + posY
            if row == -1 or column == -1 or row == card.rows or column == card.columns:
                return ('').join(data)
            data.append(str(matrix[row][column]))
        if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
            dx, dy = -dy, dx
        x, y = x + dx, y + dy


def spiral(card):
    """If the password is read in a spiral shape from the card"""
    results = []
    for i in range(0, card.rows):
        for j in range(0, card.columns):
            stream = generate_spiral_stream(card, i, j)
            results.append(stream)

    return results