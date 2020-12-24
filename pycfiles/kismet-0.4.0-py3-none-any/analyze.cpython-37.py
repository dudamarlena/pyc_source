# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/autochthe/kismet-py/kismet/personality/analyze.py
# Compiled at: 2019-01-25 19:12:49
# Size of source mod 2**32: 666 bytes
import regex, torch
from torch.distributions.gamma import Gamma
from torch.distributions.categorical import Categorical
import math
from .responses import responses

def analyze(string: str):
    mentions = len(regex.findall('[Kk]+\\s*[Ii]+\\s*[Ss]+\\s*[Mm]+\\s*[Ee]+\\s*[Tt]+', string))
    attention = math.log(mentions + 0.5) * math.log10(len(string.replace('\\s', '')))
    excitement = int(torch.ceil(Gamma(2.5, 1 / attention).sample()).tolist())
    categorical = Categorical(torch.ones(len(responses)))
    response = []
    for i in range(excitement):
        response.append(responses[categorical.sample()])

    return ' '.join(response)