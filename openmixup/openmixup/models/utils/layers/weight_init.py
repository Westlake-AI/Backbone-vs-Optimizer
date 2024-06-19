# Copyright (c) Open-MMLab. All rights reserved.
# Reference: https://github.com/open-mmlab/mmcv/blob/master/mmcv/cnn/utils/weight_init.py
import math
import warnings
import numpy as np

import torch
import torch.nn as nn
from torch.nn.init import _calculate_fan_in_and_fan_out


def constant_init(module, val, bias=0):
    if getattr(module, 'weight', None) is not None:
        nn.init.constant_(module.weight, val)
    if getattr(module, 'bias', None) is not None:
        nn.init.constant_(module.bias, bias)


def xavier_init(module, gain=1, bias=0, distribution='normal'):
    assert distribution in ['uniform', 'normal']
    if getattr(module, 'weight', None) is not None:
        if distribution == 'uniform':
            nn.init.xavier_uniform_(module.weight, gain=gain)
        else:
            nn.init.xavier_normal_(module.weight, gain=gain)
    if getattr(module, 'bias', None) is not None:
        nn.init.constant_(module.bias, bias)


def normal_init(module, mean=0, std=1, bias=0):
    if getattr(module, 'weight', None) is not None:
        nn.init.normal_(module.weight, mean, std)
    if getattr(module, 'bias', None) is not None:
        nn.init.constant_(module.bias, bias)


def trunc_normal_init(module, mean=0., std=1., bias=0, a=-2., b=2.):
    if getattr(module, 'weight', None) is not None:
        nn.init.trunc_normal_(module.weight, mean, std, a, b)
    if getattr(module, 'bias', None) is not None:
        nn.init.constant_(module.bias, bias)


def uniform_init(module, a=0, b=1, bias=0):
    if getattr(module, 'weight', None) is not None:
        nn.init.uniform_(module.weight, a, b)
    if getattr(module, 'bias', None) is not None:
        nn.init.constant_(module.bias, bias)


def kaiming_init(module,
                 a=0,
                 mode='fan_out',
                 nonlinearity='relu',
                 bias=0,
                 distribution='normal'):
    assert distribution in ['uniform', 'normal']
    if getattr(module, 'weight', None) is not None:
        if distribution == 'uniform':
            nn.init.kaiming_uniform_(
                module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
        else:
            nn.init.kaiming_normal_(
                module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
    if getattr(module, 'bias', None) is not None:
        nn.init.constant_(module.bias, bias)


def caffe2_xavier_init(module, bias=0):
    # `XavierFill` in Caffe2 corresponds to `kaiming_uniform_` in PyTorch
    # Acknowledgment to FAIR's internal code
    kaiming_init(
        module,
        a=1,
        mode='fan_in',
        nonlinearity='leaky_relu',
        distribution='uniform')


def bias_init_with_prob(prior_prob):
    """initialize conv/fc bias value according to giving probablity."""
    bias_init = float(-np.log((1 - prior_prob) / prior_prob))
    return bias_init


def _no_grad_trunc_normal_(tensor, mean, std, a, b):
    # Cut & paste from PyTorch official master until it's in a few official releases - RW
    # Method based on https://people.sc.fsu.edu/~jburkardt/presentations/truncated_normal.pdf
    def norm_cdf(x):
        # Computes standard normal cumulative distribution function
        return (1. + math.erf(x / math.sqrt(2.))) / 2.

    if (mean < a - 2 * std) or (mean > b + 2 * std):
        warnings.warn("mean is more than 2 std from [a, b] in nn.init.trunc_normal_. "
                      "The distribution of values may be incorrect.",
                      stacklevel=2)

    with torch.no_grad():
        # Values are generated by using a truncated uniform distribution and
        # then using the inverse CDF for the normal distribution.
        # Get upper and lower cdf values
        l = norm_cdf((a - mean) / std)
        u = norm_cdf((b - mean) / std)

        # Uniformly fill tensor with values from [l, u], then translate to
        # [2l-1, 2u-1].
        tensor.uniform_(2 * l - 1, 2 * u - 1)

        # Use inverse cdf transform for normal distribution to get truncated
        # standard normal
        tensor.erfinv_()

        # Transform to proper mean, std
        tensor.mul_(std * math.sqrt(2.))
        tensor.add_(mean)

        # Clamp to ensure it's in the proper range
        tensor.clamp_(min=a, max=b)
        return tensor


def variance_scaling_(tensor, scale=1.0, mode='fan_in', distribution='normal'):
    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)
    if mode == 'fan_in':
        denom = fan_in
    elif mode == 'fan_out':
        denom = fan_out
    elif mode == 'fan_avg':
        denom = (fan_in + fan_out) / 2

    variance = scale / denom

    if distribution == "truncated_normal":
        # constant is stddev of standard normal truncated to (-2, 2)
        _no_grad_trunc_normal_(
            tensor, mean=0., std=math.sqrt(variance) / .87962566103423978, a=-2., b=2.)
    elif distribution == "normal":
        tensor.normal_(std=math.sqrt(variance))
    elif distribution == "uniform":
        bound = math.sqrt(3 * variance)
        tensor.uniform_(-bound, bound)
    else:
        raise ValueError(f"invalid distribution {distribution}")


def lecun_normal_init(module, scale=1., mode='fan_in', distribution='truncated_normal'):
    if getattr(module, 'weight', None) is not None:
        variance_scaling_(module.weight, scale=scale, mode=mode, distribution=distribution)
    if getattr(module, 'bias', None) is not None:
        nn.init.zeros_(module.bias)


def lecun_normal_(tensor, scale=1., mode='fan_in', distribution='truncated_normal'):
    """ Reference: pytorch-image-models/timm/models/layers/weight_init.py """
    variance_scaling_(tensor, scale=scale, mode=mode, distribution=distribution)


def trunc_normal_(tensor, mean=0., std=1., bias=0, a=-2., b=2.):
    # type: (Tensor, float, float, float, float, float) -> Tensor
    r"""Fills the input Tensor with values drawn from a truncated
    normal distribution. The values are effectively drawn from the
    normal distribution :math:`\mathcal{N}(\text{mean}, \text{std}^2)`
    with values outside :math:`[a, b]` redrawn until they are within
    the bounds. The method used for generating the random values works
    best when :math:`a \leq \text{mean} \leq b`.
    
    Reference: pytorch-image-models/timm/models/layers/weight_init.py
    
    Args:
        tensor: an n-dimensional `torch.Tensor`
        mean: the mean of the normal distribution
        std: the standard deviation of the normal distribution
        a: the minimum cutoff value
        b: the maximum cutoff value
    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.trunc_normal_(w)
    """
    return _no_grad_trunc_normal_(tensor, mean, std, a, b)
