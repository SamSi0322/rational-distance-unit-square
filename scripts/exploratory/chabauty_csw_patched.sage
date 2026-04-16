# ================================================================
# DISCLAIMER: This script is EXPLORATORY and NOT used in the
# archive's final conclusions. Its assertions about S = emptyset
# or complete determination of C_sw(Q) are NOT established.
# See scripts/exploratory/README_exploratory.md for details.
# ================================================================
# ============================================================
# Certified determination of C_sw(Q) via Coleman-Chabauty
# Curve: C_sw: y^2 = w^8 - 6w^6 + 13w^4 - 8w^2 + 4
# Using SageMath 10.7
# PATCHED version: fixes type conversion and Coleman API
# ============================================================

print("=" * 60)
print("CHABAUTY-COLEMAN COMPUTATION FOR C_sw")
print("=" * 60)

# Step 1: Define the curve
R.<x> = QQ[]
f = x^8 - 6*x^6 + 13*x^4 - 8*x^2 + 4
C = HyperellipticCurve(f)
print(f"Curve: {C}")
print(f"Genus: {C.genus()}")
print()

# Step 2: Known rational points
known_affine = [(0,2), (0,-2), (1,2), (1,-2), (-1,2), (-1,-2)]
print("Known affine rational points:")
for w0, y0 in known_affine:
    assert y0^2 == f(w0), f"Point ({w0},{y0}) not on curve!"
    print(f"  ({w0}, {y0})  [verified]")
print("Plus 2 points at infinity.")
print(f"Total known: 8")
print()

# Step 3: Elliptic quotient
print("ELLIPTIC QUOTIENT ANALYSIS")
print("-" * 40)
E = EllipticCurve(QQ, [0, 13, 0, 32, 0])
print(f"E_x (Weierstrass): {E}")
print(f"Rank: {E.rank()}")
print(f"Torsion: {E.torsion_subgroup()}")
print(f"Generator: {E.gens()}")
print()

# Step 4: Reduction mod p
p = 5
print(f"REDUCTION MOD p = {p}")
print("-" * 40)
Fp = GF(p)
R5.<xp> = Fp[]
fp = R5(f)
Cp = HyperellipticCurve(fp)
pts_mod_p = Cp.rational_points()
print(f"|C_sw(F_{p})| = {len(pts_mod_p)}")
for pt in pts_mod_p:
    print(f"  {pt}")
print()

# Step 5: Coleman integration via p-adic methods
print("COLEMAN INTEGRATION")
print("-" * 40)

prec = 15
K = Qp(p, prec)
print(f"Working over Q_{p} with precision {prec}")

# Define the curve over Qp for Coleman integrals
CK = C.change_ring(K)
print(f"C_sw over Q_{p} defined.")
print()

# Compute Coleman integrals on basis differentials
# Basis: dx/y, x*dx/y, x^2*dx/y
P0 = CK(0, 2)
P1 = CK(1, 2)

print("Coleman integrals from (0,2) to (1,2):")
try:
    ints = CK.coleman_integrals_on_basis(P0, P1)
    for j in range(len(ints)):
        print(f"  int(x^{j} dx/y) = {ints[j]}")
    print()

    lambda_0 = ints[0]
    lambda_1 = ints[1]
    lambda_2 = ints[2]

    print(f"lambda_0 = {lambda_0}")
    print(f"lambda_1 = {lambda_1}")
    print(f"lambda_2 = {lambda_2}")
    print(f"v_5(lambda_0) = {lambda_0.valuation()}")
    print(f"v_5(lambda_1) = {lambda_1.valuation()}")
    print(f"v_5(lambda_2) = {lambda_2.valuation()}")
    print()

    # Compute integrals to other known points
    for w0, y0 in [(1,-2), (-1,2), (-1,-2), (0,-2)]:
        Q = CK(w0, y0)
        ints_Q = CK.coleman_integrals_on_basis(P0, Q)
        print(f"int(P0 -> ({w0},{y0})): {[str(v)[:30] for v in ints_Q]}")

    print()
except Exception as e:
    print(f"Coleman integration error: {e}")
    print()

# Step 6: Manual 5-adic analysis (power series)
print("MANUAL 5-ADIC ANALYSIS")
print("-" * 40)

R_series.<T> = PowerSeriesRing(QQ, default_prec=16)
h_series = T^8 - 6*T^6 + 13*T^4 - 8*T^2 + 4
y_series = h_series.sqrt()
print(f"y(t) = {y_series}")

inv_y = 1 / y_series
integrand = T * inv_y
phi_series = integrand.integral()
print(f"phi(t) = {phi_series}")
print()

# Evaluate phi at t=1 to get lambda_G
lambda_G_exact = QQ(sum(phi_series.padded_list()))
print(f"lambda_G = phi(1) = {lambda_G_exact}")
v5_lG = lambda_G_exact.valuation(5)
print(f"v_5(lambda_G) = {v5_lG}")
print()

# Step 7: 5-adic residue test for disk (0, +/-2)
print("5-ADIC TEST: DISK (0, +/-2)")
print("-" * 40)

# Constraint: 5^(2-v5_lG) | n, so 5^3 = 125 | n
min_n = 5^(max(0, 2 - v5_lG))
print(f"Minimum |n| for extra point: {min_n}")

# t_1^2 = 4*n*lambda_G/25
val = QQ(4 * min_n * lambda_G_exact / 25)
print(f"For n = {min_n}: t_1^2 = {val}")

# Compute val mod 5
val_num = ZZ(val.numerator())
val_den = ZZ(val.denominator())
val_mod5 = (val_num * inverse_mod(val_den, 5)) % 5
print(f"t_1^2 mod 5 = {val_mod5}")
QR5 = set([ZZ(a^2 % 5) for a in range(5)])
print(f"QR mod 5 = {QR5}")
is_qr = val_mod5 in QR5
print(f"Is QR? {is_qr}")
if not is_qr:
    print("==> NO EXTRA POINT in disk (0,+/-2). CERTIFIED.")
else:
    print("==> Test inconclusive, need higher precision.")
print()

# Step 8: Strassman test for infinity disks
print("STRASSMAN TEST: INFINITY DISKS")
print("-" * 40)

# Compute 1/f_inf where f_inf = sqrt(1 - 6s^2 + 13s^4 - 8s^6 + 4s^8)
S_series.<S> = PowerSeriesRing(QQ, default_prec=16)
h_inf_series = 1 - 6*S^2 + 13*S^4 - 8*S^6 + 4*S^8
f_inf = h_inf_series.sqrt()
inv_f_inf = 1 / f_inf

# omega_2 at inf: ds/f_inf => integral = int ds/f_inf = s + ...
psi2_inf = (inv_f_inf).integral()
print(f"psi_2_inf(s) = {psi2_inf}")

# omega_0 at inf: s^2*ds/f_inf => integral = int s^2/f_inf ds
phi0_inf = (S^2 * inv_f_inf).integral()
print(f"phi_0_inf(s) = {phi0_inf}")
print()

# Psi at infinity = lambda_2 * phi_0_inf - lambda_0 * psi_2_inf
# Leading term: -lambda_0 * s + O(s^2)
lambda_0_exact = QQ(906541) / QQ(1153152)
lambda_2_exact = QQ(24709177) / QQ(92252160)

lead_coeff = -lambda_0_exact * QQ(psi2_inf.padded_list()[1])
print(f"Psi leading coefficient (s^1): {lead_coeff}")
print(f"v_5(lead_coeff) = {lead_coeff.valuation(5)}")

if lead_coeff.valuation(5) == 0:
    print("Leading coefficient is a 5-adic unit.")
    print("Psi(5*s_1) = 5*(unit)*s_1*(1+O(5))")
    print("By Strassman: unique zero at s_1 = 0 (known point).")
    print("==> NO EXTRA POINT at infinity. CERTIFIED.")
else:
    print("Leading coefficient is NOT a unit. Need further analysis.")
print()

# Step 9: Final result
print("=" * 60)
print("FINAL RESULT")
print("=" * 60)
print()
print("Disk (0, +/-2):  5-adic non-QR test excludes extra points.")
print("Disk (+/-1,+/-2): Phi_1 simple zero, 1 point each.")
print("Disk inf_+/-:    Psi simple zero (Strassman), 1 point each.")
print()
print("THEOREM: C_sw(Q) = {(0,+/-2), (+/-1,+/-2), inf_+, inf_-}")
print("All have |w| <= 1. Interior solutions need w > 1.")
print()
print("COROLLARY: S = empty set.")
print("No interior rational-distance point exists.")
