# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/modeltools.py
# Compiled at: 2018-07-12 08:05:01


def getLayer(model, name):
    for layer in model.layers:
        if layer.name == name:
            return layer


def printLayerInfosAndWeights(model, noweights=False):
    for layer in model.layers:
        g = layer.get_config()
        h = layer.get_weights()
        print g
        if noweights:
            continue
        print h


def fixLayersContaining(m, fixOnlyContaining, invert=False):
    isseq = not hasattr(fixOnlyContaining, 'strip') and hasattr(fixOnlyContaining, '__getitem__') or hasattr(fixOnlyContaining, '__iter__')
    if not isseq:
        fixOnlyContaining = [
         fixOnlyContaining]
    if invert:
        for layidx in range(len(m.layers)):
            m.get_layer(index=layidx).trainable = False

        for layidx in range(len(m.layers)):
            for ident in fixOnlyContaining:
                if len(ident) and ident in m.get_layer(index=layidx).name:
                    m.get_layer(index=layidx).trainable = True

    else:
        for layidx in range(len(m.layers)):
            for ident in fixOnlyContaining:
                if len(ident) and ident in m.get_layer(index=layidx).name:
                    m.get_layer(index=layidx).trainable = False

    return m


def set_trainable(m, patterns, value):
    if isinstance(patterns, basestring):
        patterns = [
         patterns]
    for layidx in range(len(m.layers)):
        name = m.get_layer(index=layidx).name
        if any(i in name for i in patterns):
            m.get_layer(index=layidx).trainable = value

    return m


def loadModelAndFixLayers(filename, fixOnlyContaining):
    from keras.models import load_model
    m = load_model(filename)
    fixLayersContaining(m, fixOnlyContaining)
    return m