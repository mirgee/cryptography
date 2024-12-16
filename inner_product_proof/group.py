import random
from .mod_arith import MODULUS, mod_add, mod_inv, mod_mul


def group_scalar_mul(generator: int, scalar: int) -> int:
    return mod_mul(generator, scalar)


def group_add(point1: int, point2: int) -> int:
    return mod_add(point1, point2)


def group_identity() -> int:
    return 0


def random_group_element() -> int:
    return random.randint(1, MODULUS - 1)
