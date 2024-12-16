from typing import List, Tuple

from .mod_arith import mod_add, mod_mul
from .group import group_add, group_scalar_mul, group_identity


def inner_z(a: List[int], b: List[int]) -> int:
    assert len(a) == len(b)
    result = 0
    for x, y in zip(a, b):
        result = mod_add(result, mod_mul(x, y))
    return result


def inner_g(a: List[int], G: List[int]) -> int:
    assert len(a) == len(G)
    result = group_identity()
    for x, g in zip(a, G):
        result = group_add(result, group_scalar_mul(g, x))
    return result
