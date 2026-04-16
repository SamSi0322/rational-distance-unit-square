"""
Direct exact search for rational-distance points in the unit square.
Search model: x = p/q, y = r/q with 0 < r < p < q, gcd(p,r,q)=1.
Test: are p^2+r^2, (q-p)^2+r^2, p^2+(q-r)^2, (q-p)^2+(q-r)^2 all perfect squares?
"""
import sys, math, time
sys.stdout.reconfigure(encoding='utf-8')
from math import gcd, isqrt

def is_perfect_square(n):
    if n < 0:
        return False
    if n == 0:
        return True
    s = isqrt(n)
    return s * s == n

# Precompute quadratic residues mod small moduli for filtering
def qr_set(m):
    return frozenset(pow(i, 2, m) for i in range(m))

# Mod 3 filter: a^2+b^2 must be 0 or 1 mod 3
# a^2+b^2 = 2 mod 3 iff both a,b nonzero mod 3
# For all four sums to be QR mod 3:
# As proven: impossible when gcd(p,r,q) not div by 3 AND q not div by 3.
# But when 3|q, the conditions change.
# So mod 3 filter: with X=p, Y=r, D=q:
# f1 = X^2+Y^2, f2 = (D-X)^2+Y^2, f3 = X^2+(D-Y)^2, f4 = (D-X)^2+(D-Y)^2
# Each must be QR mod 3 (i.e., 0 or 1 mod 3).

QR3 = qr_set(3)  # {0, 1}
QR5 = qr_set(5)  # {0, 1, 4}
QR7 = qr_set(7)  # {0, 1, 2, 4}
QR8 = qr_set(8)  # {0, 1, 4}
QR16 = qr_set(16)  # {0, 1, 4, 9}

def passes_mod_filter(p_val, r_val, q_val):
    """Quick mod-m filter. Returns False if definitely no solution."""
    for m, qr in [(3, QR3), (5, QR5), (7, QR7)]:
        pp = p_val % m
        rr = r_val % m
        qq = q_val % m
        f1 = (pp*pp + rr*rr) % m
        f2 = ((qq-pp)**2 + rr*rr) % m
        f3 = (pp*pp + (qq-rr)**2) % m
        f4 = ((qq-pp)**2 + (qq-rr)**2) % m
        if f1 not in qr or f2 not in qr or f3 not in qr or f4 not in qr:
            return False
    return True

print("=" * 70)
print("DIRECT EXACT SEARCH FOR RATIONAL-DISTANCE POINTS")
print("=" * 70)
print()
print("Model: x = p/q, y = r/q, 0 < r < p < q, gcd(p,r,q)=1")
print("Test: p^2+r^2, (q-p)^2+r^2, p^2+(q-r)^2, (q-p)^2+(q-r)^2 all perfect squares")
print()

# Also use the basic domain symmetry: 0 < y < x < 1
# means 0 < r < p < q. The eightfold symmetry of the square
# means we only need 0 < y < x < 1/2... but let's keep it simple.

Q_MAX = 100000  # Denominator bound for exhaustive search

start_time = time.time()
total_tested = 0
total_passed_mod = 0
total_passed_1sq = 0
solutions_found = []

# Use the mod 3 obstruction insight:
# For q not div by 3: from the proven mod 3 analysis,
# there are NO solutions. So we can skip all q with 3 ∤ q.
# For q div by 3: solutions may exist, need to check.
#
# WAIT: the mod 3 analysis showed no F_3 solutions, but
# Q_3 solutions exist with 3 in denominator. For our
# integer search with common denominator q:
# The four quantities are p^2+r^2 etc. (integers).
# Each must be a perfect square (integer).
# A perfect integer square is 0 or 1 mod 3.
# So we need p^2+r^2 in {0,1} mod 3, etc.
# This IS the F_3 condition (with D=q).
#
# From the F_3 analysis: NO (p,r,q) works when q ≢ 0 mod 3
# (assuming gcd(p,r,q)=1).
# When q ≡ 0 mod 3: the conditions reduce to p^2+r^2 ≡ 0 or 1 mod 3
# for each quantity. Let me re-derive:

# With D=q ≡ 0 mod 3:
# f1 = p^2+r^2, f2 = (-p)^2+r^2 = p^2+r^2, f3 = p^2+(-r)^2 = p^2+r^2,
# f4 = (-p)^2+(-r)^2 = p^2+r^2. All four are THE SAME mod 3!
# So the condition reduces to: p^2+r^2 ≡ 0 or 1 mod 3.
# This holds iff NOT(p ≢ 0 and r ≢ 0 mod 3), i.e., 3|p or 3|r.
# But gcd(p,r,q)=1 and 3|q, so we need gcd(p,r) not div by 3.
# Since 3|q: gcd(p,r,q) coprime means NOT(3|p AND 3|r AND 3|q).
# Since 3|q, we need 3 ∤ gcd(p,r), i.e., NOT(3|p AND 3|r).
# The mod 3 condition requires 3|p OR 3|r.
# Combined: exactly one of p,r is div by 3 (not both, not neither).

# So: for 3|q, we need exactly one of p,r divisible by 3.
# For 3∤q: no solution (as proven by the mod 3 case analysis).

print("Mod 3 filter: q must be divisible by 3.")
print("  When 3|q: exactly one of p,r must be divisible by 3.")
print("  When 3∤q: no solution possible (proven by F_3 analysis).")
print()

# ADDITIONAL: when 3|q and exactly one of p,r div by 3:
# f1 = p^2+r^2. If 3|p, 3∤r: f1 = 0+r^2 = r^2 ≡ 1 mod 3. QR. ✓
# f2 = (q-p)^2+r^2. 3|q, 3|p → 3|(q-p). Same as f1 case: (q-p)^2+r^2 ≡ 1. ✓
# f3 = p^2+(q-r)^2. 3|q, 3∤r → 3∤(q-r). p^2+(q-r)^2 ≡ 0+1 = 1. ✓
# f4 = (q-p)^2+(q-r)^2 ≡ 0+1 = 1. ✓
# All pass. ✓

# So the filter is: 3|q AND exactly one of p,r is divisible by 3.

count_by_q = {}

for q in range(3, Q_MAX + 1):
    if q % 3 != 0:
        continue  # Mod 3 obstruction

    for p in range(1, q):
        # Exactly one of p,r must be div by 3.
        # We'll enforce this in the r-loop.
        p_div3 = (p % 3 == 0)

        for r in range(1, p):
            # Check: exactly one of p,r div by 3
            r_div3 = (r % 3 == 0)
            if p_div3 == r_div3:
                continue  # Both or neither div by 3 -> skip

            # gcd check
            if gcd(gcd(p, r), q) != 1:
                continue

            total_tested += 1

            # Quick mod filter (mod 5, 7)
            if not passes_mod_filter(p, r, q):
                continue

            total_passed_mod += 1

            # Exact square tests (cheapest first)
            s1 = p*p + r*r
            if not is_perfect_square(s1):
                continue
            total_passed_1sq += 1

            s2 = (q-p)**2 + r*r
            if not is_perfect_square(s2):
                continue

            s3 = p*p + (q-r)**2
            if not is_perfect_square(s3):
                continue

            s4 = (q-p)**2 + (q-r)**2
            if not is_perfect_square(s4):
                continue

            # ALL FOUR ARE PERFECT SQUARES!
            a = isqrt(s1)
            b = isqrt(s2)
            c = isqrt(s3)
            d = isqrt(s4)
            solutions_found.append((p, r, q, a, b, c, d))
            print(f"  *** SOLUTION FOUND: x={p}/{q}, y={r}/{q}, "
                  f"a={a}/{q}, b={b}/{q}, c={c}/{q}, d={d}/{q} ***")

    # Progress report every 100 q-values
    if q % 300 == 0:
        elapsed = time.time() - start_time
        print(f"  q <= {q}: tested {total_tested}, "
              f"passed mod filter {total_passed_mod}, "
              f"passed 1st square {total_passed_1sq}, "
              f"solutions {len(solutions_found)}, "
              f"time {elapsed:.1f}s")

elapsed = time.time() - start_time

print()
print("=" * 70)
print("SEARCH RESULTS")
print("=" * 70)
print()
print(f"Search range: q from 3 to {Q_MAX} (only 3|q)")
print(f"Total (p,r,q) tested: {total_tested}")
print(f"Passed mod 5,7 filter: {total_passed_mod}")
print(f"Passed first square test: {total_passed_1sq}")
print(f"Time: {elapsed:.1f}s")
print()

if solutions_found:
    print(f"SOLUTIONS FOUND: {len(solutions_found)}")
    for p, r, q, a, b, c, d in solutions_found:
        print(f"  x = {p}/{q}, y = {r}/{q}")
        print(f"  a = {a}/{q}, b = {b}/{q}, c = {c}/{q}, d = {d}/{q}")
        # Verify
        assert a*a == p*p + r*r
        assert b*b == (q-p)**2 + r*r
        assert c*c == p*p + (q-r)**2
        assert d*d == (q-p)**2 + (q-r)**2
        print(f"  Verified: all four distances exact.")
else:
    print("NO GENUINE RATIONAL-DISTANCE POINT FOUND in searched range.")
