import secrets

from tinyec import registry
from tinyec.ec import Inf, Point

curve = registry.get_curve("secp192r1")


def group_scalar_mul(point: Point, scalar: int) -> Point:
    return scalar * point


def group_add(point1: Point, point2: Point) -> Point:
    return point1 + point2


def group_sub(point1: Point, point2: Point) -> Point:
    return point1 - point2


def group_identity() -> Point:
    return Inf(curve)


def random_group_element() -> Point:
    random_scalar = secrets.randbelow(curve.field.n)
    return group_scalar_mul(curve.g, random_scalar)
