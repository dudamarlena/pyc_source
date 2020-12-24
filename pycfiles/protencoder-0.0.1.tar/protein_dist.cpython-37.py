# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/proteinko/protein_dist.py
# Compiled at: 2020-04-25 15:25:37
# Size of source mod 2**32: 1508 bytes
import numpy as np
from proteinko.utils import pdf

def model_distribution(sequence: str, encoding_scheme: dict, overlap_distance: int=2, sigma: float=0.4, sampling_points: int=None):
    scaling_factor = 40
    sequence = sequence.upper()
    dist_vector = np.zeros(scaling_factor * len(sequence) + 2 * overlap_distance * scaling_factor)
    for i, aa in enumerate(sequence):
        try:
            value = encoding_scheme[aa]
        except KeyError:
            raise KeyError(f"Unrecognized amino acid: {aa}")

        x = np.linspace(-2.3263, 2.3263, (2 * overlap_distance + 1) * scaling_factor)
        aa_dist = pdf(x, sigma) * value
        dist_vector[int(i * scaling_factor):int((i + (2 * overlap_distance + 1)) * scaling_factor)] += aa_dist

    dist_vector = dist_vector[overlap_distance * scaling_factor:-overlap_distance * scaling_factor]
    if sampling_points:
        sample_vector, offset = [], 0
        step = int(len(dist_vector) / sampling_points)
        for i in range(sampling_points):
            sample_tick = dist_vector[offset]
            offset += step
            sample_vector.append(sample_tick)

        dist_vector = sample_vector
    return dist_vector


def encode_sequence(sequence: str, encoding_scheme: dict):
    encoded_sequence = []
    for aa in sequence:
        try:
            value = encoding_scheme[aa]
        except KeyError:
            raise KeyError(f"Unrecognized amino acid: {aa}")

        encoded_sequence.append(value)

    return encoded_sequence