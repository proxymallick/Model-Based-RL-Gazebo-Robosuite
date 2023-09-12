from XRL_main.spaces.space import Space
from XRL_main.spaces.box import Box
from XRL_main.spaces.discrete import Discrete
from XRL_main.spaces.multi_discrete import MultiDiscrete
from XRL_main.spaces.multi_binary import MultiBinary
from XRL_main.spaces.tuple import Tuple
from XRL_main.spaces.dict import Dict

from XRL_main.spaces.utils import flatdim
from XRL_main.spaces.utils import flatten_space
from XRL_main.spaces.utils import flatten
from XRL_main.spaces.utils import unflatten

__all__ = [
    "Space",
    "Box",
    "Discrete",
    "MultiDiscrete",
    "MultiBinary",
    "Tuple",
    "Dict",
    "flatdim",
    "flatten_space",
    "flatten",
    "unflatten",
]
