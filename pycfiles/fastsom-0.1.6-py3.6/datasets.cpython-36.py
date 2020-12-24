# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/datasets/datasets.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 10171 bytes
"""
This module mimics Fastai dataset utilities for unsupervised data.

"""
import torch, numpy as np, pandas as pd
from torch import Tensor
from torch.utils.data import DataLoader, TensorDataset
from fastai.basic_data import DataBunch
from fastai.tabular import TabularDataBunch, FillMissing, Categorify, Normalize, TabularList
from typing import Union, Optional, List, Callable, Tuple
from .normalizers import get_normalizer
from .samplers import SamplerType, get_sampler, SamplerTypeOrString
from .cat_encoders import CatEncoder, CatEncoderTypeOrString
from ..core import ifnone
__all__ = [
 'UnsupervisedDataBunch',
 'pct_split',
 'build_dataloaders']

def pct_split(x: Tensor, valid_pct: float=0.2):
    """
    Returns a tuple of (train, valid) indices that randomly split `x` with `valid_pct`.

    Parameters
    ----------
    x : Tensor
        The tensor to be split.
    valid_pct : float default=0.2
        The validation data percentage.
    """
    sep = int(len(x) * (1.0 - valid_pct))
    perm = torch.randperm(len(x))
    return (perm[:sep], perm[sep:])


TrainData = Union[(
 Tensor,
 TensorDataset,
 Tuple[(Tensor, Tensor)],
 torch.utils.data.DataLoader)]
ValidData = Union[(TrainData, float)]

def build_dataloaders(train: TrainData, valid: ValidData, sampler: SamplerTypeOrString, bs: int) -> Tuple[(DataLoader, DataLoader, bool)]:
    """
    Transforms `train` and `valid` into `DataLoader` instances.

    Parameters
    ----------
    train: Union[Tensor, TensorDataset, Tuple[Tensor, Tensor], torch.utils.data.DataLoader]
        The training dataset. If a single `Tensor` is provided, it will be replicated as target.
    valid: Union[float, Tensor, TensorDataset, Tuple[Tensor, Tensor], torch.utils.data.DataLoader]
        The validation dataset or split percentage over training data.
    sampler: SamplerTypeOrString
        The sampler to be used to build the `DataLoader`.
    bs: int
        The batch size.
    """
    train_type, valid_type = type(train), type(valid)
    has_labels = not isinstance(train, Tensor) and (not isinstance(train, Tuple) or len(train) > 1)
    train = (train, train) if not has_labels else train
    if isinstance(train, Tuple):
        if isinstance(valid, float):
            train_idxs, valid_idxs = pct_split((train[0]), valid_pct=valid)
            valid = (train[0][valid_idxs], train[1][valid_idxs])
            train = (train[0][train_idxs], train[1][train_idxs])
        else:
            if valid is None:
                valid = (
                 torch.tensor([]), torch.tensor([]))
            else:
                if not has_labels:
                    valid = (
                     valid, valid)
        train = TensorDataset(train[0], train[1])
        valid = TensorDataset(valid[0], valid[1])
    if isinstance(train, TensorDataset):
        train_smp = get_sampler(sampler, train, bs)
        valid_smp = get_sampler(sampler, valid, bs)
        train = DataLoader(train, sampler=train_smp, batch_size=bs)
        valid = DataLoader(valid, sampler=valid_smp, batch_size=bs)
    if isinstance(train, DataLoader):
        if isinstance(valid, DataLoader):
            return (
             train, valid, has_labels)
    raise ValueError(f"Unxpected train / valid data pair of type: {train_type} {valid_type}")


class UnsupervisedDataBunch(DataBunch):
    __doc__ = "\n    `DataBunch` subclass without mandatory labels.\n    If labels are not provided, they will be stubbed.\n\n    All keyword args not listed below will be passed to the parent class.\n\n    Parameters\n    ----------\n    train: Union[Tensor, TensorDataset, Tuple[Tensor, Tensor], torch.utils.data.DataLoader]\n        The training dataset / DataLoader or a Tuple in the form (train, labels). If a single `Tensor` is provided, labels will be stubbed.\n    valid: Union[float, Tensor, TensorDataset, Tuple[Tensor, Tensor], torch.utils.data.DataLoader]\n        The validation dataset / DataLoader or split percentage over training data.\n    bs : int default=64\n        The batch size.\n    sampler : SamplerTypeOrString default=SamplerType.SEQUENTIAL\n        The sampler to be used. Can be `seq`, 'random' or 'shuffle'.\n    normalizer : str default='var'\n    tfms : Optional[List[Callable]] default=None\n        Additional Fastai transforms. These will be forwarded to the DataBunch.\n    cat_enc : Optional[CatEncoder] default=None\n        The categorical encoder to be used, if any.\n    "

    def __init__(self, train, valid=None, bs=64, sampler=SamplerType.SEQUENTIAL, tfms=None, cat_enc=None, normalizer='var', **kwargs):
        self.cat_enc = cat_enc
        self.normalizer = None
        train_dl, valid_dl, has_labels = build_dataloaders(train, valid, sampler, bs)
        self.has_labels = has_labels
        (super().__init__)(
 train_dl,
 valid_dl, device=torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'), 
         dl_tfms=tfms, **kwargs)
        if normalizer is not None:
            self.normalize(normalizer)

    @classmethod
    def from_tabular_databunch(cls, data: TabularDataBunch, bs: Optional[int]=None, normalizer: Optional[str]='var', cat_enc: Union[(CatEncoderTypeOrString, CatEncoder)]='onehot'):
        """
        Creates a new UnsupervisedDataBunch from a DataFrame.

        Parameters
        ----------
        data : TabularDataBunch
            The source TabularDataBunch.
        bs: Optional[int] default=None
            The batch size. Defaults to the source databunch batch size if not provided.
        normalizer: Optional[str] default='var'
            The optional normalization strategy to be used.
        cat_enc : Union[CatEncoderTypeOrString, CatEncoder] default='onehot'
            Categorical encoder.
        """
        return data.to_unsupervised_databunch(bs=bs, cat_enc=cat_enc)

    @classmethod
    def from_df(cls, df: pd.DataFrame, cat_names: List[str], cont_names: List[str], dep_var: str, bs: int=128, valid_pct: float=0.2, normalizer: Optional[str]='var', cat_enc: Union[(CatEncoderTypeOrString, CatEncoder)]='onehot'):
        """
        Creates a new UnsupervisedDataBunch from a DataFrame.

        Parameters
        ----------
        df : pd.Dataframe
            The source DataFrame.
        cat_names : List[str]
            Categorical feature names.
        cont_names : List[str]
            Continuous feature names.
        dep_var : str
            The target variable.
        bs: int default=128
            The batch size.
        valid_pct : float default=0.2
            Validation split percentage.
        normalizer: Optional[str] default='var'
            The optional normalization strategy to be used.
        cat_enc : Union[CatEncoderTypeOrString, CatEncoder] default='onehot'
            Categorical encoder.
        """
        procs = [
         FillMissing, Categorify, Normalize]
        tabular_data = TabularList.from_df(df, path='.', cat_names=cat_names, cont_names=cont_names, procs=procs).split_by_rand_pct(valid_pct).label_from_df(cols=dep_var).databunch(bs=bs,
          num_workers=0)
        return tabular_data.to_unsupervised_databunch(bs=bs, cat_enc=cat_enc)

    def normalize(self, normalizer: str='var') -> None:
        """
        Uses `normalizer` to normalize both train and validation data.

        Parameters
        ----------
        normalizer : str default='var'
            The normalizer to be used. Available values are 'var', 'minmax' or 'minmax-1'.
        """
        save_stats = self.normalizer is None
        self.normalizer = ifnone(self.normalizer, get_normalizer(normalizer))
        train_x, train_y = self.train_ds.tensors
        norm_train_x = self.normalizer.normalize(train_x, save=save_stats)
        self.train_ds.tensors = (norm_train_x, train_y)
        if self.valid_ds is not None:
            if len(self.valid_ds) > 1:
                valid_x, valid_y = self.valid_ds.tensors
                norm_valid_x = self.normalizer.normalize_by(train_x, valid_x)
                self.valid_ds.tensors = (norm_valid_x, valid_y)

    def denormalize(self, data: Tensor) -> Tensor:
        """
        Denormalizes a `Tensor` using the stored normalizer.
        Falls back to simply returning input data if no normalizer is available.
        """
        if self.normalizer is None:
            return data
        else:
            return self.normalizer.denormalize(data)

    def make_categorical(self, t: Tensor) -> np.ndarray:
        """Transforms a Tensor `t` of encoded categorical variables into their original categorical form."""
        return self.cat_enc.make_categorical(t)


def batch_slice(bs: int, maximum: int) -> slice:
    """Generator function. Generates contiguous slices of size `bs`."""
    curr = 0
    while True:
        yield slice(curr, curr + bs)
        curr = 0 if curr + bs > maximum or curr + bs * 2 > maximum else curr + bs


def random_batch_slice(bs: int, maximum: int) -> Tensor:
    """Generator function. Generate uniform random long tensors that can be used to index another tensor."""
    base = torch.zeros(bs)
    while True:
        yield base.uniform_(0, maximum).long()