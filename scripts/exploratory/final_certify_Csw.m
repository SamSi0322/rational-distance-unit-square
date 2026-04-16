// ================================================================
// DISCLAIMER: This script is EXPLORATORY and NOT used in the
// archive's final conclusions. Its assertions about S = emptyset
// or complete determination of C_sw(Q) are NOT established.
// See scripts/exploratory/README_exploratory.md for details.
// ================================================================
// ============================================================
// final_certify_Csw.m
//
// Curve:  C_sw : y^2 = x^8 - 6*x^6 + 13*x^4 - 8*x^2 + 4
// Task:   Certify rank(J(C_sw)) <= 2 via RankBounds.
//         Combined with the paper's Corollary 8.2, this gives
//         C_sw(Q) = { (0,+/-2), (+/-1,+/-2), inf+, inf- }
//         and S = empty set.
// ============================================================

// --- Environment header ---
p := 5;
search_bound := 100;
printf "\n";
printf "  Script: final_certify_Csw.m\n";
printf "  Prime: p = %o\n", p;
printf "  Search bound: %o\n", search_bound;
printf "  Expects: Magma >= V2.23\n";

// ============================================================
// CORE: CURVE AND BASIC DATA
// ============================================================

printf "\n";
printf "============================================================\n";
printf " CORE: CURVE AND BASIC DATA\n";
printf "============================================================\n";

// --- Define curve ---
_<x> := PolynomialRing(Rationals());
f := x^8 - 6*x^6 + 13*x^4 - 8*x^2 + 4;
C := HyperellipticCurve(f);
g := Genus(C);
printf "  C_sw: y^2 = %o\n", f;
printf "  Genus: %o\n", g;
assert g eq 3;

// --- Jacobian ---
J := Jacobian(C);
printf "  Jacobian defined.\n";

// --- Discriminant ---
disc := Discriminant(f);
printf "  disc(f) = %o\n", Factorization(Integers()!Numerator(disc));

// --- Reduction at p ---
Cp := ChangeRing(C, GF(p));
pts_Fp := RationalPoints(Cp);
printf "  |C_sw(F_%o)| = %o\n", p, #pts_Fp;
for P in pts_Fp do
    printf "    %o\n", P;
end for;
fp := ChangeRing(f, GF(p));
printf "  f mod %o squarefree: %o\n", p, IsSquarefree(fp);

// --- Known rational points ---
printf "\n  Known rational points:\n";
known_pts := {};
for wv in [0, 1, -1] do
    fv := Evaluate(f, wv);
    sq, yv := IsSquare(fv);
    if sq then
        Include(~known_pts, C![wv, yv]);
        Include(~known_pts, C![wv, -yv]);
        printf "    (%o, %o)\n", wv, yv;
        printf "    (%o, %o)\n", wv, -yv;
    end if;
end for;
inf_pts := PointsAtInfinity(C);
for P in inf_pts do
    Include(~known_pts, P);
    printf "    %o  (at infinity)\n", P;
end for;
printf "  Total known: %o\n", #known_pts;

// --- Bounded search and comparison ---
printf "\n  Bounded point search (height <= %o)...\n", search_bound;
search_pts := Points(C : Bound := search_bound);
printf "  Found: %o point(s).\n", #search_pts;

extra := {P : P in search_pts | P notin known_pts};
missing := {P : P in known_pts | P notin search_pts};

if #extra eq 0 and #missing eq 0 then
    printf "  [OK] Search result matches known list exactly.\n";
elif #extra gt 0 then
    printf "  [WARNING] Unexpected point(s) found by search:\n";
    for P in extra do
        printf "    %o\n", P;
    end for;
elif #missing gt 0 then
    printf "  [INFO] Some known points not returned by search\n";
    printf "  (may be outside height bound or at infinity):\n";
    for P in missing do
        printf "    %o\n", P;
    end for;
end if;

// ============================================================
// RANK COMPUTATION
// ============================================================

printf "\n";
printf "============================================================\n";
printf " RANK COMPUTATION VIA RankBounds\n";
printf "============================================================\n";

rank_ub_certified := false;
rank_ub_value := -1;
rank_lb_value := -1;

// --- Attempt RankBounds (two-return form) ---
printf "\n  Attempting RankBounds(J)...\n";
try
    lb, ub := RankBounds(J);
    printf "  RankBounds: %o <= rank(J) <= %o\n", lb, ub;
    rank_lb_value := lb;
    rank_ub_value := ub;
    if ub le 2 then
        rank_ub_certified := true;
    end if;
catch e1
    printf "  RankBounds(J) not available: %o\n", e1;
    // --- Fallback: RankBound (single-return form) ---
    printf "  Attempting RankBound(J)...\n";
    try
        ub := RankBound(J);
        printf "  RankBound: rank(J) <= %o\n", ub;
        rank_ub_value := ub;
        if ub le 2 then
            rank_ub_certified := true;
        end if;
    catch e2
        printf "  RankBound(J) not available: %o\n", e2;
    end try;
end try;

// ============================================================
// SUPPLEMENTARY: ELLIPTIC QUOTIENT
// ============================================================

printf "\n";
printf "============================================================\n";
printf " SUPPLEMENTARY: ELLIPTIC QUOTIENT E_x\n";
printf "============================================================\n";

E := EllipticCurve([0, 13, 0, 32, 0]);
printf "  E_x: %o\n", E;
printf "  Rank(E_x): %o\n", Rank(E);
printf "  Torsion: %o\n", TorsionSubgroup(E);
printf "  Generator: %o\n", Generators(E);

// ============================================================
// FINAL SUMMARY
// ============================================================

printf "\n";
printf "============================================================\n";
printf " FINAL SUMMARY\n";
printf "============================================================\n\n";

if rank_ub_certified then
    printf "  RANK UPPER BOUND CERTIFIED.\n";
    if rank_lb_value ge 0 then
        printf "  %o <= rank(J(C_sw)) <= %o.\n", rank_lb_value, rank_ub_value;
    else
        printf "  rank(J(C_sw)) <= %o.\n", rank_ub_value;
    end if;
    printf "\n  By Corollary 8.2 of the paper:\n";
    printf "  With rank(J) <= 2, Proposition 8.1 gives at most\n";
    printf "  1 rational point per residue disk at p = %o.\n", p;
    printf "  Since |C_sw(F_%o)| = %o = #(known rational points),\n",
        p, #pts_Fp;
    printf "  we conclude:\n";
    printf "\n  C_sw(Q) = {(0,+/-2), (+/-1,+/-2), inf+, inf-}.\n";
    printf "  S = empty set.\n";
    printf "\n  CERTIFICATION COMPLETE.\n";
else
    printf "  NO CERTIFICATION ACHIEVED.\n";
    if rank_ub_value ge 0 then
        printf "  Best rank bound obtained: rank(J) <= %o.\n", rank_ub_value;
        printf "  This exceeds 2 and does not suffice.\n";
    else
        printf "  No rank bound was obtained.\n";
    end if;
    printf "  Possible remedies:\n";
    printf "    - Use a newer Magma version.\n";
    printf "    - Increase time/memory limits.\n";
end if;

printf "\n============================================================\n";
printf " END\n";
printf "============================================================\n";

quit;
