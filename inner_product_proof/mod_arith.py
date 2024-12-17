import random
from inner_product_proof.group import curve

MODULUS = curve.field.n


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
