# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: qatools/utils.py
# Compiled at: 2018-07-15 09:49:51
# Size of source mod 2**32: 3776 bytes
"""
Small utilities and metric functions for the sample project.
(Copied from our SLAM project)
"""
import numpy as np, pandas as pd
from pandas.api.types import CategoricalDtype

def read_poses(path):
    """Load a monoslam output file into a pandas dataframe describing tracked poses."""
    df = pd.read_csv((str(path)),
      sep='\t',
      header=None,
      names=[
     'a', 'b', 'c', 'x', 'y', 'z', 't', 'confidence', 'is_tracking_good'],
      index_col=6)
    df = df[(~df.index.duplicated(keep='first'))]
    is_tracking_good_type = CategoricalDtype(categories=[1, 3, 2, 0], ordered=True)
    df['is_tracking_good'] = df['is_tracking_good'].astype(is_tracking_good_type)
    return df


def drift_after_loop_metrics(poses):
    r"""Returns the drift accuracy in % of the distance traveled, and the distance traveled.
  We assume the path is a loop, and the distance traveled is computed as:
    $$L = \sum{\sqrt{dx^2+dy^2+dz^2}} $$
  """
    poses_ = poses[['x', 'y', 'z']]
    poses_delta = poses_.shift(1) - poses_
    poses_delta2 = poses_delta ** 2
    poses_dl2 = np.sum(poses_delta2, axis=1)
    poses_dl = np.sqrt(poses_dl2)
    loop_length = np.sum(poses_dl.tail(-1))
    if loop_length < 0.0001:
        return {'loop_drift_pc':0.0, 
         'loop_translation_rmse':0.0,  'dvs_trajectory_length':0}
    start, end = poses_.head(1), poses_.tail(1)
    delta = start.iloc[0] - end.iloc[0]
    error = np.sqrt(np.sum(delta ** 2))
    return {'loop_drift_pc':float(error / loop_length),  'loop_translation_rmse':error,  'dvs_trajectory_length':float(loop_length)}


def trajectory_length(poses):
    poses_ = poses[['x', 'y', 'z']]
    poses_delta = poses_.shift(1) - poses_
    poses_delta2 = poses_delta ** 2
    poses_dl2 = np.sum(poses_delta2, axis=1)
    poses_dl = np.sqrt(poses_dl2)
    return float(np.sum(poses_dl.tail(-1)))


def objective_metrics(poses_est, poses_gt):
    """
  Computes various metrics quantifying the error of a trajectory estimation versus a ground truth.
  parameters:
  - poses_est: pandas dataframe
  - poses_est: pandas dataframe
  """
    metrics = {'trajectory_length': trajectory_length(poses_gt)}
    errors_xyz = poses_est[['x', 'y', 'z']] - poses_gt[['x', 'y', 'z']]
    errors_abc = poses_est[['a', 'b', 'c']] - poses_gt[['a', 'b', 'c']]
    rad_to_degree = 360 / (2 * np.pi)
    metrics['rotation_rmse'] = np.linalg.norm((errors_abc ** 2).mean()) * rad_to_degree
    metrics['translation_aape'] = np.linalg.norm(errors_xyz, axis=1, ord=2).mean()
    metrics['translation_aape_pc'] = metrics['translation_aape'] / metrics['trajectory_length'] if metrics['trajectory_length'] > 0 else 0
    metrics['translation_rmse'] = np.linalg.norm(errors_xyz, ord='fro') / np.sqrt(errors_xyz.shape[0])
    metrics['translation_rmse_pc'] = metrics['translation_rmse'] / metrics['trajectory_length'] if metrics['trajectory_length'] > 0 else 0
    start = errors_xyz.head(1).iloc[0]
    end = errors_xyz.tail(1).iloc[0]
    metrics['translation_drift'] = np.sqrt(np.sum((start - end) ** 2))
    metrics['translation_drift_pc'] = metrics['translation_drift'] / metrics['trajectory_length'] if metrics['trajectory_length'] > 0 else 0
    return metrics