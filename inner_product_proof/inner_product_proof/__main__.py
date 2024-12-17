from .group import group_add, group_scalar_mul, random_group_element
from .inner_product_proof import inner_product_prove, inner_product_verify
from .mod_arith import random_scalar
from .utils import inner_g, inner_z

if __name__ == "__main__":
    n = 8

    a = [random_scalar() for _ in range(n)]
    b = [random_scalar() for _ in range(n)]

    G = [random_group_element() for _ in range(n)]
    H = [random_group_element() for _ in range(n)]

    w = random_scalar()
    B = random_group_element()
    Q = group_scalar_mul(B, w)

    P_a = inner_g(a, G)
    P_b = inner_g(b, H)
    P = group_add(P_a, P_b)

    c = inner_z(a, b)

    proof = inner_product_prove(a, b, G, H, Q)

    is_valid = inner_product_verify(G, H, Q, P, c, proof)
    print(f"Proof valid? {is_valid}")
