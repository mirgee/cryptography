import random

MODULUS = 2**255 - 19


def mod_add(x: int, y: int) -> int:
    return (x + y) % MODULUS


def mod_sub(x: int, y: int) -> int:
    return (x - y) % MODULUS


def mod_mul(x: int, y: int) -> int:
    return (x * y) % MODULUS


def mod_inv(x: int) -> int:
    return pow(x, MODULUS - 2, MODULUS)


def random_scalar() -> int:
    return random.randint(1, MODULUS - 1)
