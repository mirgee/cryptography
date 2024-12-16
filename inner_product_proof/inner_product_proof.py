from dataclasses import dataclass
from typing import List, Tuple

from .mod_arith import mod_add, mod_inv, mod_mul, mod_sub, random_scalar
from .group import group_add, group_identity, group_scalar_mul
from .utils import inner_g, inner_z


@dataclass
class InnerProductProof:
    L: List[int]
    R: List[int]
    a0: int
    b0: int
    G0: int
    H0: int
    u: List[int]


def inner_product_prove(
    a: List[int],
    b: List[int],
    G: List[int],
    H: List[int],
    Q: int,
) -> InnerProductProof:
    n = len(a)
    assert len(b) == n
    assert len(G) == n
    assert len(H) == n
    assert (n & (n - 1)) == 0, "n must be a power of 2"

    L_vals = []
    R_vals = []
    u_ks = []

    a_curr = a[:]
    b_curr = b[:]
    G_curr = G[:]
    H_curr = H[:]

    while len(a_curr) > 1:
        half = len(a_curr) // 2

        a_lo, a_hi = a_curr[:half], a_curr[half:]
        b_lo, b_hi = b_curr[:half], b_curr[half:]
        G_lo, G_hi = G_curr[:half], G_curr[half:]
        H_lo, H_hi = H_curr[:half], H_curr[half:]

        # L_k = <a_lo, G_hi> + <b_hi, H_lo> + <a_lo, b_hi>*Q
        cross1 = inner_g(a_lo, G_hi)
        cross2 = inner_g(b_hi, H_lo)
        cross3 = group_scalar_mul(Q, inner_z(a_lo, b_hi))
        L_k = group_add(group_add(cross1, cross2), cross3)

        # R_k = <a_hi, G_lo> + <b_lo, H_hi> + <a_hi, b_lo>*Q
        cross1 = inner_g(a_hi, G_lo)
        cross2 = inner_g(b_lo, H_hi)
        cross3 = group_scalar_mul(Q, inner_z(a_hi, b_lo))
        R_k = group_add(group_add(cross1, cross2), cross3)

        # TODO: Derive challenge via Fiat-Shamir
        u_k = random_scalar()
        u_k_inv = mod_inv(u_k)

        L_vals.append(L_k)
        R_vals.append(R_k)
        u_ks.append(u_k)

        a_new, b_new, G_new, H_new = [], [], [], []
        for i in range(half):
            a_new.append(mod_add(mod_mul(a_lo[i], u_k), mod_mul(a_hi[i], u_k_inv)))
            b_new.append(mod_add(mod_mul(b_lo[i], u_k_inv), mod_mul(b_hi[i], u_k)))
            G_new.append(
                group_add(
                    group_scalar_mul(G_lo[i], u_k_inv), group_scalar_mul(G_hi[i], u_k)
                )
            )
            H_new.append(
                group_add(
                    group_scalar_mul(H_lo[i], u_k), group_scalar_mul(H_hi[i], u_k_inv)
                )
            )

        a_curr = a_new
        b_curr = b_new
        G_curr = G_new
        H_curr = H_new

    proof = InnerProductProof(
        L=L_vals,
        R=R_vals,
        a0=a_curr[0],
        b0=b_curr[0],
        G0=G_curr[0],
        H0=H_curr[0],
        u=u_ks,
    )
    return proof


def inner_product_verify(
    G: List[int], H: List[int], Q: int, P: int, c: int, proof: InnerProductProof
) -> bool:
    # P + c*Q
    lhs = group_add(P, group_scalar_mul(Q, c))

    # a0*G0 + b0*H0 + (a0*b0)*Q - sum_j(L_j*u_j^2 + u_j^-2 * R_j)
    rhs = group_identity()
    rhs = group_add(rhs, group_scalar_mul(proof.G0, proof.a0))
    rhs = group_add(rhs, group_scalar_mul(proof.H0, proof.b0))
    rhs = group_add(rhs, group_scalar_mul(Q, mod_mul(proof.a0, proof.b0)))

    for L_j, R_j, u_j in zip(proof.L, proof.R, proof.u):
        u_j_sq = mod_mul(u_j, u_j)
        u_j_inv_sq = mod_mul(mod_inv(u_j), mod_inv(u_j))

        cross = group_identity()
        cross = group_add(cross, group_scalar_mul(L_j, u_j_sq))
        cross = group_add(cross, group_scalar_mul(R_j, u_j_inv_sq))

        rhs = mod_sub(rhs, cross)

    return lhs == rhs
