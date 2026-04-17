# Rational-Distance Points in the Unit Square: Research Archive (v1.2)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19613981.svg)](https://doi.org/10.5281/zenodo.19613981)

This archive documents a completed exploration of several natural approaches to the unit-square rational distance problem.
No complete solution is claimed; the problem remains open.

## Problem

For the unit square with vertices A=(0,0), B=(1,0), C=(0,1), D=(1,1): does there exist a point P=(x,y) with 0 < y < x < 1 such that all four distances PA, PB, PC, PD are rational?

**This problem remains open.** No claim of solution or non-solution is made.

## What Is Established

| Result | Status | Source |
|---|---|---|
| Genus-3 curve C_sw arises from the problem | CAS-verified | Report 1, verify_identities.py |
| 7 of 8 chain links individually verified | CAS-verified | Report 1, verify_chain.py |
| Stage-2 to Q_{-1} bridge | **Not verified** | Report 1, Section 7 |
| (dagger) not polynomial consequence of (A)-(D) | CAS-verified | Report 1, verify_groebner.py |
| Evidence: no square root in quotient ring | Strong evidence | Report 1, Section 9 |
| Descent discriminant = 4 P_4(w^2) | CAS-verified | Report 1, Section 10 |
| No solution with denominator q <= 100,000 | Exact, exhaustive | Report 2, Run 1 |
| No solution with Pythagorean legs <= 5,000,000 | Exact, exhaustive | Report 2, Run 3 |
| z=14 witness ruled out (mod 193) | Exact | Report 3, Section 6 |
| F_4 is a degree-16 surface in P^6 | Magma-verified | Report 4 |
| F_4 has arithmetic genus 7, Hilbert poly 8n^2-8n+8 | Magma-verified | Report 4 |
| F_4 has 46 singular points (vertex-collision configurations) | Magma-verified | Report 4 |
| Singularity is an A_1 node (verified at one point) | Magma-verified | Report 4 |
| Resolution of F_4 is NOT K3, NOT rational | Inferred from arithmetic genus | Report 4 |
| Resolution is a surface of general type or high-genus elliptic | Deduced | Report 4 |

## What Is NOT Established

- The problem is **not solved** in either direction.
- The algebraic reduction to C_sw is **incomplete** (Stage-2 bridge gap).
- The Jacobian rank bound (Magma) is an exploratory computation, not used in any final conclusion.
- The Chabauty-Coleman analysis has identified errors and is **not used**.
- A_1 nodality at all 46 singular points is inferred by symmetry, not independently verified point by point.

## Contents

```
├── README.md                              This file
├── VERSION                                v1.2 metadata
├── LICENSE                                CC-BY 4.0 + MIT
├── rational_distance_research_archive.pdf Main document (21 pages)
│
├── scripts/
│   ├── search/                            Exact search (Python only)
│   │   ├── direct_search.py              q <= 100,000
│   │   ├── two_triple_search.py          legs <= 2,000,000
│   │   └── search_5M.py                  legs <= 5,000,000
│   │
│   ├── verification/                      CAS verification (SymPy)
│   │   ├── verify_identities.py
│   │   ├── verify_chain.py
│   │   └── verify_groebner.py
│   │
│   ├── geometry/                          Magma geometry scripts
│   │   ├── f4_geometry_fixed.magma       dimension, radical, singular
│   │   ├── f4_singularities.magma        Hilbert poly, boundary
│   │   ├── f4_node_check.magma           Groebner of singular locus
│   │   └── f4_nodality.magma             A_1 verification at one point
│   │
│   └── exploratory/                       Not used in conclusions
│       ├── README_exploratory.md
│       ├── final_certify_Csw.m
│       ├── chabauty_final.py
│       ├── chabauty_csw_patched.sage
│       ├── padic_log2.sage
│       └── mod3_proof.py
│
└── outputs/                               Pre-computed outputs
    ├── magma_output.txt
    ├── sage_padic_log.txt
    └── python/
        ├── identities_output.txt
        ├── chain_output.txt
        └── groebner_output.txt
```

## Quick Start

Run the main exact search (Python >= 3.10, no dependencies):
```bash
cd scripts/search
python search_5M.py
```

Verify the algebraic identities (requires SymPy >= 1.12):
```bash
cd scripts/verification
python verify_identities.py
python verify_chain.py
python verify_groebner.py
```

Geometry scripts (online Magma calculator at `magma.maths.usyd.edu.au/calc`):
```
scripts/geometry/f4_geometry_fixed.magma   # paste entire file
scripts/geometry/f4_singularities.magma
scripts/geometry/f4_node_check.magma
scripts/geometry/f4_nodality.magma
```
Each finishes well under the 120-second online cap.

## License

Text: CC-BY 4.0. Code: MIT.

## Changes

### v1.2 (2026-04-17)
- Added Report 4: geometry of the four-distance surface F_4 (Magma analysis).
- Added `scripts/geometry/` with 4 Magma scripts.
- Updated overview and summary table with F_4 geometric findings.

### v1.1 (2026-04-16)
- Corrected search coverage claims (leg-based, not denominator-based for Runs 2-3).
- Removed unsupported "S = emptyset" assertions from all scripts and outputs.
- Downgraded quotient-ring obstruction from Theorem to Proposition with explicit caveats.
- Moved Chabauty/Magma/mod3 scripts to exploratory/ with explanatory README.
- Added explicit notes on which results depend on unverified phase-file derivations.
- Clarified that the identity in Section 5 is a ratio identity, CAS-verified.
