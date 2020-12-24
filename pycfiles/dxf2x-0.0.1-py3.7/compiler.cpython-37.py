# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dxf2x/compiler.py
# Compiled at: 2019-10-10 04:01:34
# Size of source mod 2**32: 2309 bytes


def syntax(tokens):
    ast = {'blocks':[],  'entities':[]}
    pointer = ast
    for token in tokens:
        if token == {'0':'SECTION',  '2':'BLOCKS'} or token['0'] == 'ENDBLK':
            pointer = ast['blocks']
        elif token == {'0':'SECTION',  '2':'ENTITIES'}:
            pointer = ast['entities']
        elif token['0'] == 'BLOCK':
            pointer.append(token)
            pointer = token['entities'] = []
        elif token['0'] == 'POLYLINE':
            pointer.append(token)
            pointer = token['vertices'] = []
        else:
            if token['0'] in {'POINT', 'INSERT', 'VERTEX', 'LINE', 'TEXT'}:
                pointer.append(token)

    return ast


def foreach_words(words, consumer):
    for code, value in words.items():
        consumer(code, value)


def foreach_vertices(vertices, consumer):
    for vertex in vertices:
        consumer(vertex)


def foreach_shapes(shapes, consumer):
    for shape in shapes:
        vertices = shape.pop('vertices', None)
        consumer(shape)
        if vertices:
            foreach_vertices(vertices, consumer)
            consumer({'0':'SEQEND',  '8':shape['8']})


def foreach_entities(shapes, consumer):
    consumer({'0':'SECTION',  '2':'ENTITIES'})
    foreach_shapes(shapes, consumer)
    consumer({'0': 'ENDSEC'})


def foreach_blocks(blocks, consumer):
    consumer({'0':'SECTION',  '2':'BLOCKS'})
    for block in blocks:
        shapes = block.pop('entities')
        consumer(block)
        foreach_shapes(shapes, consumer)
        consumer({'0': 'ENDBLK'})

    consumer({'0': 'ENDSEC'})


def foreach_ast(ast, word_consumer):
    token_consumer = lambda token: foreach_words(token, word_consumer)
    foreach_blocks(ast['blocks'], token_consumer)
    foreach_entities(ast['entities'], token_consumer)
    token_consumer({'0': 'EOF'})