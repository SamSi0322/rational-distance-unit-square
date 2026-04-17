# Exploratory Scripts (Not Used in Final Conclusions)

The scripts in this directory represent exploratory computations that
were part of the investigation but are **not relied upon** in the
final conclusions of the archive.

## Why these are exploratory

- **final_certify_Csw.m**: Computes a Jacobian rank bound via Magma's
  RankBounds. The rank bound itself is correct, but the script's
  concluding assertions ("S = empty set", "CERTIFICATION COMPLETE")
  depend on a Chabauty-Coleman analysis whose validity was not
  established (see Report 1 for the structural gap).

- **chabauty_final.py**, **chabauty_csw_patched.sage**: Implement
  a Chabauty-Coleman disk analysis. The local arguments contain
  errors identified in audit (use of non-annihilating differentials,
  incorrect valuation claims). Not used in any final result.

- **padic_log2.sage**: Computes a p-adic formal group logarithm.
  The computation itself may be correct, but it feeds into the
  Chabauty analysis above, which is not used.

- **mod3_proof.py**: Contains an argument that no F_3 solutions exist
  for the four-distance system. While the F_3 non-existence is correct,
  the script's conclusion "S = empty" is invalid because Q_3 solutions
  exist with 3 in the denominator (x = u/3 for 3-adic units u).
  The mod 3 filter used in the search scripts (Report 2) is a correct
  necessary condition derived independently; this script is not the
  source of that filter.

## Summary

These scripts document explored approaches. They should not be cited
as establishing any result about the original problem.
