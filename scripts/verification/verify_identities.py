"""
Verification of all algebraic identities for the rational-distance
finiteness theorem. Uses SymPy for exact symbolic computation.

Each identity is verified by polynomial division: the remainder
after reduction modulo the relevant curve equation must be exactly 0.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from sympy import *

t, n, w, s, rho, omega = symbols('t n w s rho omega')

print("=" * 60)
print("IDENTITY VERIFICATION SUITE")
print("=" * 60)

# ============================================================
# IDENTITY 1: (dagger) holds on C_T
# ============================================================
print("\n--- Identity 1: (dagger) mod C_T ---")

CT_rel = n**2 - (2*t**4 + 13*t**2 + 16)
R = (3*t**2 + t*n + 4) / (2*(t**2 + 2))
s_nat = (n + t) / (n - t)
dagger = (3 - R)*s_nat**2 + (R**2 - R - 2)*s_nat + R*(1 - R)
dagger_num = expand(numer(cancel(dagger)))
_, rem1 = div(Poly(dagger_num, n), Poly(CT_rel, n), n)
assert expand(rem1.as_expr()) == 0, "IDENTITY 1 FAILED"
print("  VERIFIED: remainder = 0")

# ============================================================
# IDENTITY 2: y_E^2 = P4(w^2) on C_T
# ============================================================
print("\n--- Identity 2: y_E^2 = P4(w^2) mod C_T ---")

y_E = 2*(3 - R)*s_nat + (R**2 - R - 2)
P4_w2 = R**4 - 6*R**3 + 13*R**2 - 8*R + 4
diff2 = cancel(y_E**2 - P4_w2)
num2 = expand(numer(diff2))
_, rem2 = div(Poly(num2, n), Poly(CT_rel, n), n)
assert expand(rem2.as_expr()) == 0, "IDENTITY 2 FAILED"
print("  VERIFIED: remainder = 0")

# ============================================================
# IDENTITY 3: C_T relation = -8*sigma*(dagger) in (w,s)
# ============================================================
print("\n--- Identity 3: C_T <=> (dagger) ---")

t2_ws = (-2*s*w**2 + 2*s + 2*w**2 - 2) / (s*w**2 - 2*s - w**2 + 1)
n_ws = sqrt(t2_ws) * (s + 1) / (s - 1)  # symbolic
n2_ws = t2_ws * (s + 1)**2 / (s - 1)**2
CT_ws_num = cancel(n2_ws - (2*t2_ws**2 + 13*t2_ws + 16))
CT_ws_num_expanded = expand(numer(CT_ws_num))
dagger_ws = (3 - w**2)*s**2 + (w**4 - w**2 - 2)*s + w**2*(1 - w**2)
ratio3 = cancel(CT_ws_num_expanded / dagger_ws)
assert ratio3 == -8*s, f"IDENTITY 3 FAILED: ratio = {ratio3}"
print(f"  VERIFIED: ratio = {ratio3}")

# ============================================================
# IDENTITY 4: Steps 5-7 curve equations on Q_{-1}
# ============================================================
print("\n--- Identity 4: Steps 5-7 on Q_{-1} ---")

Q_rel = omega**2 - (13*rho**2 - 4*rho**4 - 8)

# Step 5: E_x curve
X_ex = -4*rho**2
Y_ex = 4*rho*omega
Ex_check = expand(Y_ex**2 - X_ex*(X_ex**2 + 13*X_ex + 32))
_, rem4a = div(Poly(Ex_check, omega), Poly(Q_rel, omega), omega)
assert expand(rem4a.as_expr()) == 0, "STEP 5 FAILED"
print("  Step 5 (E_x): VERIFIED")

# Step 6: E_B curve
UB = omega**2 / rho**2
VB = 4*omega*(2 - rho**4) / rho**3
EB_check = cancel(VB**2 - UB*(UB**2 - 26*UB + 41))
num6 = expand(numer(EB_check))
_, rem4b = div(Poly(num6, omega), Poly(Q_rel, omega), omega)
assert expand(rem4b.as_expr()) == 0, "STEP 6 FAILED"
print("  Step 6 (E_B): VERIFIED")

# Step 7: C_T curve
tfrak = -2*omega*rho / (rho**4 - 2)
nfrak = -4*(omega**4 - 41*rho**4) / (omega**4 - 26*omega**2*rho**2 + 41*rho**4)
CT_check = cancel(nfrak**2 - (2*tfrak**4 + 13*tfrak**2 + 16))
num7 = expand(numer(CT_check))
_, rem4c = div(Poly(num7, omega), Poly(Q_rel, omega), omega)
assert expand(rem4c.as_expr()) == 0, "STEP 7 FAILED"
print("  Step 7 (C_T): VERIFIED")

# ============================================================
# IDENTITY 5: Distance formulas in (w,s)
# ============================================================
print("\n--- Identity 5: Distance formulas ---")

x_ws = (w + 1) / (w + s)
y_ws = (w - 1) / (w + s)

checks = {
    "a^2": simplify(x_ws**2 + y_ws**2 - 2*(w**2 + 1)/(w + s)**2),
    "b^2": simplify((1-x_ws)**2 + y_ws**2 - ((w-1)**2 + (s-1)**2)/(w+s)**2),
    "c^2": simplify(x_ws**2 + (1-y_ws)**2 - ((w+1)**2 + (s+1)**2)/(w+s)**2),
    "d^2": simplify((1-x_ws)**2 + (1-y_ws)**2 - 2*(s**2+1)/(w+s)**2),
}

for name, val in checks.items():
    assert val == 0, f"{name} FAILED"
    print(f"  {name}: VERIFIED")

# ============================================================
print("\n" + "=" * 60)
print("ALL IDENTITIES VERIFIED SUCCESSFULLY")
print("=" * 60)
