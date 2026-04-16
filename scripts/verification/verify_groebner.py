"""
Verification that the polynomial elimination ideal is trivial.
This confirms the arithmetic nature of the reduction.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from sympy import *

w, s, p, q, lam, mu = symbols('w s p q lam mu')

print("GROEBNER BASIS COMPUTATION")
print("=" * 60)

# Four polynomial equations encoding the parametrized conditions:
f1 = (s-1)*(1-p**2) - 2*p*(w-1)         # (B) Pythagorean
f2 = (s+1)*(1-q**2) - 2*q*(w+1)         # (C) Pythagorean
f3 = w*(lam**2-2) - (lam**2-4*lam+2)    # (A) Pell
f4 = s*(mu**2-2) - (mu**2-4*mu+2)       # (D) Pell

print("System:")
print(f"  f1 = {f1}")
print(f"  f2 = {f2}")
print(f"  f3 = {f3}")
print(f"  f4 = {f4}")
print()

# Compute Groebner basis with elimination order
print("Computing Groebner basis (lex: p > q > lam > mu > w > s)...")
G = groebner([f1, f2, f3, f4], p, q, lam, mu, w, s, order='lex')
print(f"Basis has {len(G)} elements.")
print()

# Extract elements in Q[w,s] only
elim = [g for g in G if not g.has(p,q,lam,mu)]
print(f"Elements in Q[w,s]: {len(elim)}")

if len(elim) == 0:
    print()
    print("RESULT: Elimination ideal I ∩ Q[w,s] = (0).")
    print()
    print("CONCLUSION: The curve equation (dagger) cannot be obtained")
    print("by polynomial elimination from the parametrized system.")
    print("The reduction is intrinsically ARITHMETIC.")
else:
    for e in elim:
        print(f"  {factor(e)}")

# Also verify that Pell parametrization automatically satisfies (A),(D)
print()
print("Automatic satisfaction of (A) and (D):")
w_lam = (lam**2-4*lam+2)/(lam**2-2)
s_mu = (mu**2-4*mu+2)/(mu**2-2)
FA = cancel(2*(1+w_lam**2))
FD = cancel(2*(1+s_mu**2))
print(f"  2(1+w(lam)^2) = {factor(FA)}")
print(f"  2(1+s(mu)^2)  = {factor(FD)}")
print("  Both are manifestly perfect squares.")
