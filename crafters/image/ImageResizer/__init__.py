__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import warnings
from typing import Union, Tuple, Dict, Iterable

import numpy as np

from jina.executors.decorators import single
from jina.executors.crafters import BaseCrafter

from .helper import _load_image, _move_channel_axis, _resize_short


class ImageResizer(BaseCrafter):
    """
    Resize image to the given size.

    :param target_size: Desired output size.
        If size is a sequence like (h, w), the output size will
        be matched to this. If size is an int, the smaller edge
        of the image will be matched to this number maintain
        the aspect ratio.
    :param how: The interpolation method. Valid values include
        `NEAREST`, `BILINEAR`, `BICUBIC`, and `LANCZOS`.
        Default is `BILINEAR`. Please refer to `PIL.Image` for details.
    """

    def __init__(self,
                 target_size: Union[Iterable[int], int] = 224,
                 how: str = 'BILINEAR',
                 channel_axis: int = -1,
                 *args, **kwargs):
        warnings.warn(f'{self!r} will be retired soon, you can add `- !URI2Blob {{}}` to the drivers', DeprecationWarning)
        super().__init__(*args, **kwargs)
        if isinstance(target_size, int):
            self.output_dim = target_size
        elif isinstance(target_size, Iterable):
            self.output_dim = tuple(target_size)
        else:
            raise ValueError(f'output_dim {target_size} should be an integer or tuple/list of 2 integers')
        self.how = how
        self.channel_axis = channel_axis

    @single
    def craft(self, blob: 'np.ndarray', *args, **kwargs) -> Dict:
        """
        Resize the image array to the given size.

        :param blob: The ndarray of the image
        :return: A dict with the cropped image
        """
        raw_img = _load_image(blob, self.channel_axis)
        _img = _resize_short(raw_img, self.output_dim, self.how)
        img = _move_channel_axis(np.asarray(_img), -1, self.channel_axis)
        return dict(offset=0, blob=img.astype('float32'))
