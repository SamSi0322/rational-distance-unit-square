"""
Precomputed-index search at LEG_MAX=5,000,000.
Uses the fast common-leg approach from the 2M run.
Memory optimization: use dict of frozensets (compact for membership testing).
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

LEG_MAX = 5_000_000

print(f"Building index, LEG_MAX = {LEG_MAX:,}")
start = time.time()

partners = defaultdict(list)
m_max = isqrt(LEG_MAX) + 1

for m in range(2, m_max + 1):
    for n in range(1, m):
        if (m - n) % 2 == 0:
            continue
        if gcd(m, n) != 1:
            continue
        leg1 = m*m - n*n
        leg2 = 2*m*n
        for k in range(1, LEG_MAX // max(leg1, leg2) + 1):
            L1 = k * leg1
            L2 = k * leg2
            if L1 > LEG_MAX or L2 > LEG_MAX:
                break
            partners[L1].append(L2)
            partners[L2].append(L1)

# Convert to frozensets for O(1) lookup
for key in partners:
    partners[key] = frozenset(partners[key])

elapsed_build = time.time() - start
total_entries = sum(len(v) for v in partners.values())
print(f"  Legs indexed: {len(partners):,}")
print(f"  Total entries: {total_entries:,}")
print(f"  Build time: {elapsed_build:.1f}s")

# Main search
print()
print("=" * 70)
print("SEARCHING")
print("=" * 70)

solutions = []
start_search = time.time()
total_r = 0
total_pairs = 0
cond3_pass = 0

def mod3_ok(p_val, r_val, q_val):
    return q_val % 3 == 0 and (p_val % 3 == 0) != (r_val % 3 == 0)

sorted_legs = sorted(partners.keys())

for idx, r in enumerate(sorted_legs):
    P_r = partners[r]
    p_list = [v for v in P_r if v > r]
    if not p_list:
        continue
    total_r += 1
    for p in p_list:
        P_p = partners.get(p, frozenset())
        for s in P_r:
            if s <= 0:
                continue
            q = p + s
            t = q - r
            if t <= 0:
                continue
            total_pairs += 1
            if not mod3_ok(p, r, q):
                continue
            if gcd(gcd(p, r), q) != 1:
                continue
            if t not in P_p:
                continue
            cond3_pass += 1
            P_s = partners.get(s, frozenset())
            if t not in P_s:
                continue
            a = isqrt(p*p + r*r)
            b = isqrt(s*s + r*r)
            c = isqrt(p*p + t*t)
            d = isqrt(s*s + t*t)
            solutions.append((p, r, q, a, b, c, d))
            print(f"*** SOLUTION: x={p}/{q}, y={r}/{q}, PA={a}/{q}, PB={b}/{q}, PC={c}/{q}, PD={d}/{q}")

    if idx % 50000 == 0 and idx > 0:
        elapsed = time.time() - start_search
        print(f"  [{idx}/{len(sorted_legs)}] r~{r:,}, pairs={total_pairs:,}, c3={cond3_pass}, {elapsed:.0f}s")

elapsed_total = time.time() - start_search

print()
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
print(f"LEG_MAX = {LEG_MAX:,}")
print(f"Max denominator q: ~{2*LEG_MAX:,}")
print(f"Common legs: {total_r:,}")
print(f"Pairs tested: {total_pairs:,}")
print(f"Condition-3 pass: {cond3_pass}")
print(f"Solutions: {len(solutions)}")
print(f"Search time: {elapsed_total:.1f}s (index build: {elapsed_build:.1f}s)")
print()
if solutions:
    for p, r, q, a, b, c, d in solutions:
        print(f"  x={p}/{q}, y={r}/{q}")
else:
    print("NO GENUINE RATIONAL-DISTANCE POINT FOUND")
    print(f"  Exhaustive: legs up to {LEG_MAX:,}, denominators up to ~{2*LEG_MAX:,}.")
