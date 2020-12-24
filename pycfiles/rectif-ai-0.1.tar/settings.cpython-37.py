# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeus/PyTorch-Hackathon-2019/rectifai/settings.py
# Compiled at: 2019-09-17 11:35:34
# Size of source mod 2**32: 451 bytes
import os, logging
from dotenv import load_dotenv
load_dotenv(verbose=True)
logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSENET_PATH = os.path.join(ROOT_DIR, 'data', 'raw', 'posenet.pth')
POSTURENET_PATH = os.path.join(ROOT_DIR, 'data', 'raw', 'posturenet.pth')
import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')