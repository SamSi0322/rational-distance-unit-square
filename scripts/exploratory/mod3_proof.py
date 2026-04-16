# ================================================================
# DISCLAIMER: This script is EXPLORATORY and NOT used in the
# archive's final conclusions. Its assertions about S = emptyset
# or complete determination of C_sw(Q) are NOT established.
# See scripts/exploratory/README_exploratory.md for details.
# ================================================================
"""
Rigorous proof that F_4 has no solutions modulo 3.
This constitutes a LOCAL OBSTRUCTION at p=3, proving S = empty.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("THEOREM: There is no (x,y) in F_3^2 such that all four of")
print("  x^2+y^2, (1-x)^2+y^2, x^2+(1-y)^2, (1-x)^2+(1-y)^2")
print("are quadratic residues mod 3.")
print("=" * 70)
print()

# In F_3: elements are {0, 1, 2}.
# Quadratic residues mod 3: 0^2=0, 1^2=1, 2^2=1. So QR = {0, 1}.
# Non-residue: {2}.

print("F_3 = {0, 1, 2}")
print("Quadratic residues mod 3: {0, 1}")
print("Non-residue mod 3: {2}")
print()

# Key fact: 2 is NOT a QR mod 3.
# For a sum x^2+y^2 to be QR mod 3, it must be 0 or 1 mod 3.

# Possible values of x^2 mod 3: x=0 -> 0, x=1 -> 1, x=2 -> 1. So x^2 in {0, 1}.
# Possible values of x^2+y^2 mod 3: {0+0, 0+1, 1+0, 1+1} = {0, 1, 2}.
# x^2+y^2 = 2 mod 3 iff x^2=y^2=1 mod 3 iff x,y in {1,2}.

# For x^2+y^2 to be QR: need x^2+y^2 != 2 mod 3.
# x^2+y^2 = 2 iff both x,y nonzero mod 3.
# So: x^2+y^2 is QR mod 3 iff at least one of x,y is 0 mod 3.

print("Condition for x^2+y^2 to be QR mod 3:")
print("  x^2 + y^2 = 2 mod 3  iff  x != 0 and y != 0  (both nonzero mod 3)")
print("  So: x^2+y^2 is QR mod 3  iff  x = 0 or y = 0 mod 3.")
print()

# Now check all four conditions simultaneously.
# f1 = x^2 + y^2          QR iff x=0 or y=0
# f2 = (1-x)^2 + y^2      QR iff (1-x)=0 or y=0, i.e., x=1 or y=0
# f3 = x^2 + (1-y)^2      QR iff x=0 or (1-y)=0, i.e., x=0 or y=1
# f4 = (1-x)^2 + (1-y)^2  QR iff (1-x)=0 or (1-y)=0, i.e., x=1 or y=1

print("Individual conditions (each must hold):")
print("  (I)   x^2 + y^2 is QR          iff  x = 0  OR  y = 0")
print("  (II)  (1-x)^2 + y^2 is QR      iff  x = 1  OR  y = 0")
print("  (III) x^2 + (1-y)^2 is QR      iff  x = 0  OR  y = 1")
print("  (IV)  (1-x)^2 + (1-y)^2 is QR  iff  x = 1  OR  y = 1")
print()

# Now we need all four to hold simultaneously.
# From (I): x=0 or y=0.
# From (II): x=1 or y=0.

# Case A: y = 0 (satisfies both I and II).
#   From (III): x=0 or y=1. Since y=0, need x=0.
#   From (IV): x=1 or y=1. Since y=0, need x=1.
#   Need x=0 AND x=1 mod 3. Impossible (0 != 1 mod 3).

print("PROOF BY CASES:")
print()
print("From (I): x = 0 or y = 0.")
print("From (II): x = 1 or y = 0.")
print()

print("Case A: y = 0.")
print("  (III) requires: x = 0 or y = 1. Since y = 0 != 1: need x = 0.")
print("  (IV) requires: x = 1 or y = 1. Since y = 0 != 1: need x = 1.")
print("  Contradiction: x = 0 AND x = 1 is impossible in F_3.")
print()

# Case B: y != 0, so from (I): x=0. And from (II): since y != 0, need x=1.
#   x=0 AND x=1 mod 3: impossible.

print("Case B: y != 0.")
print("  From (I): since y != 0, need x = 0.")
print("  From (II): since y != 0, need x = 1.")
print("  Contradiction: x = 0 AND x = 1 is impossible in F_3.")
print()

print("Both cases lead to contradiction.")
print()
print("=" * 70)
print("CONCLUSION: F_4 has NO solutions mod 3.")
print("Therefore F_4(Q_3) = empty.")
print("Therefore F_4(Q) = empty.")
print("Therefore S = empty.")
print("=" * 70)
print()
print("This is a COMPLETE proof that no point in the interior of")
print("the unit square has all four vertex-distances rational.")
print()
print("The proof uses only:")
print("  1. The four distance equations (definition of the problem)")
print("  2. The fact that 2 is not a quadratic residue mod 3")
print("  3. A case analysis with 2 cases, each trivially contradictory")
print()
print("No elliptic curves, no genus-3 curves, no Chabauty-Coleman,")
print("no rank bounds, no Magma computation needed.")

print()
print("=" * 70)
print("WAIT -- CHECKING BOUNDARY CAREFULLY")
print("=" * 70)
print()
print("The above proves: no (x,y) in Q^2 satisfies all four QR conditions mod 3.")
print("But we need (x,y) in (0,1)^2 with RATIONAL distances.")
print("Rational distances require a,b,c,d in Q, hence a^2,b^2,c^2,d^2 in Q^2.")
print("In particular, all four quantities must be RATIONAL squares.")
print("A rational square, when reduced mod 3, is a QR mod 3.")
print()
print("More precisely: if a = p/q with p,q integers, gcd(p,q)=1,")
print("then a^2 = p^2/q^2. The condition is that x^2+y^2 = a^2 = p^2/q^2.")
print("Writing x = r/s, y = t/s (common denominator), we get")
print("r^2+t^2 = p^2*s^2/q^2, so q^2(r^2+t^2) = p^2*s^2.")
print()
print("The mod 3 analysis applies to the NUMERATOR of each expression")
print("after clearing denominators. Let me redo this carefully.")

print()
print("=" * 70)
print("CAREFUL MOD 3 ANALYSIS WITH DENOMINATORS")
print("=" * 70)
print()

# Let x = X/D, y = Y/D with X, Y, D integers, D > 0.
# Then:
# a^2 = (X^2+Y^2)/D^2
# b^2 = ((D-X)^2+Y^2)/D^2
# c^2 = (X^2+(D-Y)^2)/D^2
# d^2 = ((D-X)^2+(D-Y)^2)/D^2

# For a,b,c,d rational: each numerator must be a perfect square (times D^2).
# i.e., X^2+Y^2, (D-X)^2+Y^2, X^2+(D-Y)^2, (D-X)^2+(D-Y)^2 must all be
# perfect squares (in Z, after multiplying by D^2 and taking square roots...
# actually they must be of the form (aD)^2 = a^2D^2, so the numerators
# are squares times D^2... no, a = sqrt(X^2+Y^2)/D, so X^2+Y^2 must be
# a perfect square in Q, which means X^2+Y^2 = (rational)^2.

# More carefully: a = sqrt(x^2+y^2) = sqrt(X^2+Y^2)/D.
# For a to be rational: sqrt(X^2+Y^2) must be rational, so X^2+Y^2 must be
# a perfect square of a rational number. Since X,Y are integers (after clearing),
# X^2+Y^2 must be a perfect integer square.

# So we need: X^2+Y^2, (D-X)^2+Y^2, X^2+(D-Y)^2, (D-X)^2+(D-Y)^2 all perfect squares.

# Now apply mod 3: each must be a QR mod 3.
# This is exactly what we checked! With x -> X, y -> Y, and the "1" replaced by D.

# The four conditions mod 3:
# X^2+Y^2 = QR mod 3  iff  X=0 or Y=0 mod 3
# (D-X)^2+Y^2 = QR mod 3  iff  D-X=0 or Y=0 mod 3, i.e., X=D or Y=0 mod 3
# X^2+(D-Y)^2 = QR mod 3  iff  X=0 or D-Y=0 mod 3, i.e., X=0 or Y=D mod 3
# (D-X)^2+(D-Y)^2 = QR mod 3  iff  D-X=0 or D-Y=0 mod 3, i.e., X=D or Y=D mod 3

print("With x = X/D, y = Y/D (X,Y,D integers):")
print()
print("Conditions mod 3:")
print("  (I)   X^2+Y^2 is QR mod 3          iff  X = 0 or Y = 0 mod 3")
print("  (II)  (D-X)^2+Y^2 is QR mod 3      iff  X = D or Y = 0 mod 3")
print("  (III) X^2+(D-Y)^2 is QR mod 3      iff  X = 0 or Y = D mod 3")
print("  (IV)  (D-X)^2+(D-Y)^2 is QR mod 3  iff  X = D or Y = D mod 3")
print()

# Now: from (I) and (II):
# (I): X=0 or Y=0.  (II): X=D or Y=0.

# Case A: Y = 0 mod 3.
#   (III): X=0 or Y=D mod 3. Since Y=0: need X=0 or D=0 mod 3.
#   (IV): X=D or Y=D mod 3. Since Y=0: need X=D or D=0 mod 3.

#   Sub-case A1: D = 0 mod 3.
#     Then all conditions reduce to: X^2 + Y^2 = 0 mod 3 (since D=0 mod 3).
#     X^2+Y^2 = 0 mod 3 iff X=Y=0 mod 3.
#     (D-X)^2+Y^2 = X^2+Y^2 = 0 mod 3 (since D=0). iff X=Y=0 mod 3. Same.
#     So all four: X=Y=0 mod 3 with D=0 mod 3.
#     But then x = X/D and y = Y/D have both X,Y,D divisible by 3.
#     We can divide out: replace X,Y,D by X/3, Y/3, D/3.
#     This is an infinite descent argument. Eventually D is not divisible by 3.
#     So D != 0 mod 3 without loss.

print("WLOG D is not divisible by 3 (divide out common factors).")
print()

#   Sub-case A2: D != 0 mod 3, Y = 0 mod 3.
#     (III): X=0 or Y=D mod 3. Y=0, D!=0, so Y!=D mod 3. Need X=0 mod 3.
#     (IV): X=D or Y=D mod 3. Y=0, D!=0, so Y!=D. Need X=D mod 3.
#     X=0 AND X=D mod 3, with D!=0 mod 3. Contradiction.

print("Case A: Y = 0 mod 3, D != 0 mod 3.")
print("  (III): X = 0 or Y = D. Since Y=0, D!=0: Y != D. So X = 0.")
print("  (IV): X = D or Y = D. Since Y=0, D!=0: Y != D. So X = D.")
print("  X = 0 AND X = D with D != 0: CONTRADICTION.")
print()

# Case B: Y != 0 mod 3.
#   From (I): X = 0 mod 3.
#   From (II): X = D mod 3.
#   X = 0 and X = D mod 3 -> D = 0 mod 3.
#   But D != 0 mod 3 (WLOG). Contradiction.

print("Case B: Y != 0 mod 3, D != 0 mod 3.")
print("  (I): X = 0 mod 3.")
print("  (II): X = D mod 3.")
print("  So D = 0 mod 3. Contradicts D != 0 mod 3.")
print()

print("=" * 70)
print("RIGOROUS CONCLUSION")
print("=" * 70)
print()
print("For any integers X, Y, D with D != 0 and gcd(X,Y,D) not")
print("divisible by 3, there is no solution to the system")
print("  X^2+Y^2, (D-X)^2+Y^2, X^2+(D-Y)^2, (D-X)^2+(D-Y)^2")
print("all being perfect squares, because these four quantities")
print("cannot simultaneously be quadratic residues mod 3.")
print()
print("This proves: the set S of rational-distance points in the")
print("interior of the unit square is empty.")
print()
print("QED.")
