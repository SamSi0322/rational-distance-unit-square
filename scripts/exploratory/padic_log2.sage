# Compute the p-adic elliptic logarithm of G = (-8,8) on
# E_x: Y^2 = X^3 + 13X^2 + 32X at p = 5.
#
# Strategy: |E(F_5)| = 8. So 8*G reduces to O mod 5.
# Compute log(8G) via formal group, then divide by 8.

E = EllipticCurve(QQ, [0, 13, 0, 32, 0])
p = 5
prec = 15

# Group order mod p
Ep_Fp = E.change_ring(GF(p))
N = Ep_Fp.order()
print("E(F_5) order:", N)

# N*G should be in the formal group (reduce to O mod p)
G = E(-8, 8)
NG = N * G
print(f"{N}*G =", NG)

# Check it reduces to O mod 5
x_NG, y_NG = NG.xy()
print(f"v_5(x({N}G)) =", QQ(x_NG).valuation(5))
print(f"v_5(y({N}G)) =", QQ(y_NG).valuation(5))
print()

# Now use formal group log on NG
Ep = E.change_ring(Qp(p, prec))
NGp = Ep(x_NG, y_NG)
t_NG = -NGp[0] / NGp[1]
print(f"t({N}G) =", t_NG)
print(f"v_5(t) =", t_NG.valuation())
print()

# Formal log
flog = E.formal_group().log(prec + 5)
log_NG = flog(t_NG)
print(f"log_5({N}G) =", log_NG)
print(f"valuation:", log_NG.valuation())
print()

# log(G) = log(NG) / N
log_G = log_NG / N
print(f"log_5(G) = log({N}G)/{N} =", log_G)
print(f"valuation:", log_G.valuation())
print()

# This is the certified p-adic logarithm.
# For the Chabauty argument: lambda_1 (the Coleman integral of
# w*dw/y from (0,2) to (1,2) on C_sw) is related to log_G
# through the bielliptic map.
print("=" * 50)
print("CERTIFIED p-ADIC LOGARITHM")
print(f"log_5(G) = {log_G}")
print(f"v_5(log_5(G)) = {log_G.valuation()}")
print(f"log_5(G) mod 5 = {log_G / 5^(log_G.valuation()) + O(Qp(5,1)(5))}")
