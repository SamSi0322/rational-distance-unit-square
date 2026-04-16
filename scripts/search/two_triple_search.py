"""
Two-Pythagorean-triple intersection search for rational-distance points.

Architecture:
  For a fixed common leg r, find all other legs p with p^2+r^2 = square.
  For each pair (p1, p2) of such partner legs, set q = p1+p2.
  Then conditions 1 and 2 are automatic. Check conditions 3 and 4.

This is vastly more efficient than sweeping over q.
"""
import sys, time
sys.stdout.reconfigure(encoding='utf-8')
from math import gcd, isqrt
from collections import defaultdict

def is_perfect_square(n):
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n

# ===================================================================
# STEP 1: Build index of Pythagorean triples by leg
# ===================================================================
# A Pythagorean triple (a, b, c) with a^2+b^2=c^2 is primitive iff
# gcd(a,b)=1 and a,b have opposite parity.
# Parametrization: a = m^2-n^2, b = 2mn (or swapped), c = m^2+n^2.
# General: k*(a0, b0, c0).

# For our purpose: index by one leg. For each leg value L,
# store all other-leg values that form a Pythagorean triple with L.

LEG_MAX = 2_000_000  # Max leg value to index

print(f"Building Pythagorean triple index up to leg = {LEG_MAX:,}")
start = time.time()

# partners[L] = set of all M such that L^2 + M^2 is a perfect square
# We build this from the parametrization.
partners = defaultdict(set)

m_max = isqrt(LEG_MAX) + 1
prim_count = 0

for m in range(2, m_max + 1):
    for n in range(1, m):
        if (m - n) % 2 == 0:
            continue
        if gcd(m, n) != 1:
            continue

        leg1 = m*m - n*n  # odd leg
        leg2 = 2*m*n       # even leg
        # hyp = m*m + n*n

        prim_count += 1

        # Scale by k
        for k in range(1, LEG_MAX // max(leg1, leg2) + 1):
            L1 = k * leg1
            L2 = k * leg2
            if L1 > LEG_MAX or L2 > LEG_MAX:
                break
            partners[L1].add(L2)
            partners[L2].add(L1)

elapsed_build = time.time() - start
total_entries = sum(len(v) for v in partners.values())
print(f"  Primitive triples generated: {prim_count:,}")
print(f"  Legs indexed: {len(partners):,}")
print(f"  Total (leg, partner) pairs: {total_entries:,}")
print(f"  Build time: {elapsed_build:.1f}s")

# ===================================================================
# STEP 2: For each common leg r, find pairs (p, s) with q = p+s
# ===================================================================
print()
print("=" * 70)
print("SEARCHING FOR RATIONAL-DISTANCE POINTS")
print("=" * 70)
print()

# For conditions 1 and 2:
#   p^2 + r^2 = a^2   =>  p in partners[r]
#   (q-p)^2 + r^2 = b^2  =>  s := q-p in partners[r]
# So: for each r, take all pairs (p, s) from partners[r].
# Set q = p + s.
# Enforce: 0 < r < p, and p < q = p+s (automatic since s > 0).
# Also: r < q (need r < p+s; since r < p and s > 0, this holds).

# For conditions 3 and 4:
#   p^2 + (q-r)^2 must be square
#   s^2 + (q-r)^2 must be square

# Note: q-r = p+s-r. Define t = q-r = p+s-r.
# Condition 3: p^2 + t^2 = square  =>  t in partners[p]  (or p in partners[t])
# Condition 4: s^2 + t^2 = square  =>  t in partners[s]

# So: ALL FOUR conditions become Pythagorean triple conditions:
#   p in partners[r]
#   s in partners[r]
#   t in partners[p]  where t = p+s-r
#   t in partners[s]

# This is a 4-way intersection!

# Algorithm:
# For each r:
#   Let P_r = partners[r] (all legs pairing with r)
#   For each p in P_r with p > r:
#     For each s in P_r with s > 0:
#       t = p + s - r
#       Check: t > 0, t in partners[p], t in partners[s]
#       Also check: gcd(p, r, q) = 1 where q = p+s
#       Mod 3 filter: 3|q and exactly one of p,r div by 3

solutions = []
start_search = time.time()

# Mod 3 filter
def mod3_ok(p_val, r_val, q_val):
    if q_val % 3 != 0:
        return False
    return (p_val % 3 == 0) != (r_val % 3 == 0)

total_r = 0
total_pairs = 0
total_passed_t_check = 0
report_interval = 100000

# Sort legs for deterministic progress reporting
sorted_legs = sorted(partners.keys())

for r in sorted_legs:
    P_r = partners[r]
    # Get all p > r from P_r
    p_list = sorted(v for v in P_r if v > r)

    if not p_list:
        continue

    total_r += 1

    # Convert P_r and partners[p], partners[s] to sets for O(1) lookup
    P_r_set = P_r  # already a set

    for p in p_list:
        # Get partners[p] as a set
        P_p = partners.get(p, set())

        for s in P_r_set:
            if s <= 0:
                continue
            q = p + s
            t = q - r  # = p + s - r

            total_pairs += 1

            # Quick checks before expensive lookups
            if t <= 0:
                continue

            # Mod 3 filter
            if not mod3_ok(p, r, q):
                continue

            # gcd filter
            if gcd(gcd(p, r), q) != 1:
                continue

            # Condition 3: t in partners[p]?
            if t not in P_p:
                continue

            total_passed_t_check += 1

            # Condition 4: t in partners[s]?
            P_s = partners.get(s, set())
            if t not in P_s:
                continue

            # ALL FOUR CONDITIONS MET!
            a = isqrt(p*p + r*r)
            b = isqrt(s*s + r*r)
            c = isqrt(p*p + t*t)
            d = isqrt(s*s + t*t)

            # Verify
            assert a*a == p*p + r*r
            assert b*b == s*s + r*r
            assert c*c == p*p + t*t
            assert d*d == s*s + t*t
            assert t == q - r

            solutions.append((p, r, q, a, b, c, d))
            print(f"*** SOLUTION: x={p}/{q}, y={r}/{q}")
            print(f"    PA={a}/{q}, PB={b}/{q}, PC={c}/{q}, PD={d}/{q}")

    if total_r % 5000 == 0:
        elapsed = time.time() - start_search
        print(f"  [r up to ~{r:,}] legs={total_r:,}, "
              f"pairs={total_pairs:,}, "
              f"t-pass={total_passed_t_check}, "
              f"sols={len(solutions)}, {elapsed:.0f}s")

elapsed_total = time.time() - start_search

print()
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
print(f"Leg index size: {LEG_MAX:,}")
print(f"Common legs processed: {total_r:,}")
print(f"Pair combinations tested: {total_pairs:,}")
print(f"Passed condition 3 (t in partners[p]): {total_passed_t_check}")
print(f"Total search time: {elapsed_total:.1f}s")
print()

if solutions:
    print(f"SOLUTIONS FOUND: {len(solutions)}")
    for p, r, q, a, b, c, d in solutions:
        x_str = f"{p}/{q}"
        y_str = f"{r}/{q}"
        print(f"  x = {x_str}, y = {y_str}")
        print(f"  PA = {a}/{q}, PB = {b}/{q}, PC = {c}/{q}, PD = {d}/{q}")
else:
    max_q_seen = 0
    # The max q = p+s where p,s <= LEG_MAX. So max q ~ 2*LEG_MAX.
    print(f"NO GENUINE RATIONAL-DISTANCE POINT FOUND")
    print(f"  All Pythagorean-compatible (p,r,q) with legs up to {LEG_MAX:,}")
    print(f"  (corresponding to denominators q up to ~{2*LEG_MAX:,})")
    print(f"  have been tested. Zero solutions.")
