"""
Step-by-step verification of the complete formula chain (Steps 1-8).
Each step is verified independently by symbolic computation.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from sympy import *

r, s, t_var, a, b, c = symbols('r s t a b c')
w_sym, sigma = symbols('w sigma')
rho, omega = symbols('rho omega')

print("STEP-BY-STEP CHAIN VERIFICATION")
print("=" * 60)

# ============================================================
# STEP 1: Three-distance parametrization
# ============================================================
print("\nStep 1: Three-distance surface")
N = r**2 + s**2 - 1
Phi = r**3 - r + s**3 - s
C_const = r**4 - 2*r**2 + s**4 - 2*s**2 + 2
target = expand((1-r**2)*(1-s**2)*(2-(r-s)**2))
actual = expand(Phi**2 - N*C_const)
assert expand(actual - target) == 0
print("  Discriminant identity: VERIFIED")

# ============================================================
# STEP 2: Elliptic fibration
# ============================================================
print("\nStep 2: Elliptic fibration")
V = s - r
X = 1/(2*(r-1))
Y_val = t_var/(r-1)**2
curve_RHS = (2-V**2)*(4*X+1)*(2*V*X+1)*(2*(V+2)*X+1)
diff2 = cancel(Y_val**2 - curve_RHS)
num2 = expand(numer(diff2))
t_target = Poly(t_var**2 - target, t_var)
_, rem2 = div(Poly(num2, t_var), t_target, t_var)
assert expand(rem2.as_expr()) == 0
print("  Curve equation mod T_3: VERIFIED")

# ============================================================
# STEP 3: Fourth distance
# ============================================================
print("\nStep 3: Fourth distance equation")
V_s = s - r
X_s = 1/(2*(r-1))
A_val = V_s*X_s + 2*X_s + 1
H_val = 2*V_s**2*X_s**2 + 4*V_s*X_s**2 + 2*V_s*X_s + 2*X_s**2 + 4*X_s + 1
K_val = 4*V_s**2*X_s**2 + 12*V_s*X_s**2 + 6*V_s*X_s + 8*X_s**2 + 12*X_s + 3
Y_s = t_var/(r-1)**2
W2_val = (X_s*Y_s - A_val*K_val)**2 - 8*(2*X_s+1)*(2*(V_s+1)*X_s+1)*H_val**2
d2_P4 = W2_val/(16*X_s**2*H_val**2)
a_sol = (Phi + t_var)/(2*N)
x_sol = (1-r**2+2*a_sol*r)/2
y_sol = (1-s**2+2*a_sol*s)/2
d2_geom = expand((1-x_sol)**2 + (1-y_sol)**2)
diff3 = cancel(d2_geom - d2_P4)
num3 = expand(numer(diff3))
_, rem3 = div(Poly(num3, t_var), t_target, t_var)
assert expand(rem3.as_expr()) == 0
print("  d^2 formula mod T_3: VERIFIED")

# ============================================================
# STEP 4: Self-incidence coordinates
# ============================================================
print("\nStep 4: Distance formulas in (w, sigma)")
x_ws = (w_sym+1)/(w_sym+sigma)
y_ws = (w_sym-1)/(w_sym+sigma)
assert simplify(x_ws**2+y_ws**2 - 2*(w_sym**2+1)/(w_sym+sigma)**2) == 0
assert simplify((1-x_ws)**2+y_ws**2 - ((w_sym-1)**2+(sigma-1)**2)/(w_sym+sigma)**2) == 0
assert simplify(x_ws**2+(1-y_ws)**2 - ((w_sym+1)**2+(sigma+1)**2)/(w_sym+sigma)**2) == 0
assert simplify((1-x_ws)**2+(1-y_ws)**2 - 2*(sigma**2+1)/(w_sym+sigma)**2) == 0
print("  All 4 distance formulas: VERIFIED")
A2B2 = ((w_sym+1)**2+(sigma+1)**2)*((w_sym-1)**2+(sigma-1)**2)
quartic = sigma**4+2*w_sym**2*sigma**2-8*w_sym*sigma+w_sym**4+4
assert expand(A2B2 - quartic) == 0
print("  Quartic U^2 identity: VERIFIED")

# ============================================================
# STEPS 5-7: Q_{-1} -> E_x -> E_B -> C_T
# ============================================================
print("\nSteps 5-7: Curve chain on Q_{-1}")
Q_rel = omega**2 - (13*rho**2 - 4*rho**4 - 8)

# Step 5
Ex_check = expand((4*rho*omega)**2 - (-4*rho**2)*(16*rho**4-52*rho**2+32))
_, r5 = div(Poly(Ex_check, omega), Poly(Q_rel, omega), omega)
assert expand(r5.as_expr()) == 0
print("  Step 5 (E_x): VERIFIED")

# Step 6
UB = omega**2/rho**2
VB = 4*omega*(2-rho**4)/rho**3
n6 = expand(numer(cancel(VB**2 - UB*(UB**2-26*UB+41))))
_, r6 = div(Poly(n6, omega), Poly(Q_rel, omega), omega)
assert expand(r6.as_expr()) == 0
print("  Step 6 (E_B): VERIFIED")

# Step 7
tf = -2*omega*rho/(rho**4-2)
nf = -4*(omega**4-41*rho**4)/(omega**4-26*omega**2*rho**2+41*rho**4)
n7 = expand(numer(cancel(nf**2 - (2*tf**4+13*tf**2+16))))
_, r7 = div(Poly(n7, omega), Poly(Q_rel, omega), omega)
assert expand(r7.as_expr()) == 0
print("  Step 7 (C_T): VERIFIED")

# ============================================================
# STEP 8: C_T -> (dagger)
# ============================================================
print("\nStep 8: C_T implies (dagger)")
t_s, n_s = symbols('t_s n_s')
CT_rel = n_s**2 - (2*t_s**4+13*t_s**2+16)
w2 = (3*t_s**2+t_s*n_s+4)/(2*(t_s**2+2))
s_nat = (n_s+t_s)/(n_s-t_s)
dag = (3-w2)*s_nat**2 + (w2**2-w2-2)*s_nat + w2*(1-w2)
dag_num = expand(numer(cancel(dag)))
_, r8 = div(Poly(dag_num, n_s), Poly(CT_rel, n_s), n_s)
assert expand(r8.as_expr()) == 0
print("  (dagger) mod C_T: VERIFIED")

print("\n" + "=" * 60)
print("ALL 8 STEPS VERIFIED SUCCESSFULLY")
print("=" * 60)
