# Rational-Distance Points in the Unit Square

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19613346.svg)](https://doi.org/10.5281/zenodo.19613346)

This archive collects the results of my exploration of the unit-square rational distance problem. I tried several algebraic and computational approaches; none of them resolved the problem, but each produced something useful. The problem is still open.

## The problem

Place a point P = (x, y) strictly inside the unit square (vertices at (0,0), (1,0), (0,1), (1,1)). Can all four distances from P to the vertices be rational simultaneously?

Nobody knows. This archive records what I learned trying to find out.

## What's in here

**The main document** (`rational_distance_research_archive.pdf`, 16 pp.) covers three topics:

1. **Algebraic side.** I found a genus-3 curve C_sw that's naturally connected to the problem through a chain of eight rational maps. Seven of the eight links are verified by SymPy; one key bridge step (Stage-2 to Q_{-1}) I was never able to construct or verify. I also show that the curve equation (dagger) can't be forced by polynomial elimination from the distance conditions, and that a natural 2-descent attempt turns out to be circular.

2. **Search.** I ran an exact (no floating-point) search using a two-Pythagorean-triple intersection method. No solution was found up to denominator q = 100,000 (full sweep) or Pythagorean legs up to 5,000,000 (structured search). The leg-bounded search covers a larger range but isn't the same as a full denominator sweep.

3. **Witness elimination.** Early on I found an arithmetic candidate (z = 14 on a certain elliptic curve progression) that passed a first-layer rationality test. It took a while to figure out why it wasn't a real solution. The answer turned out to be a mod-193 obstruction on a discriminant in the next rationality layer.

**Scripts:**

- `scripts/search/` — the search code. Python >= 3.10, no dependencies. Run `python search_5M.py` for the main search (~3 min).
- `scripts/verification/` — SymPy scripts that verify the algebraic identities and the formula chain. Run all three with `python verify_*.py`.
- `scripts/exploratory/` — things I tried that didn't work out: a Magma rank bound computation, Chabauty-Coleman scripts with errors found later, a mod-3 argument that turned out to be wrong over Q_3. These are kept for the record but aren't part of any conclusion. See the README inside that folder.

**Outputs:**

- `outputs/` — saved output from the Magma and SageMath runs, plus the Python verification transcripts. The Magma output has a disclaimer at the top because the script's final assertions go beyond what's actually proved.

## What I can and can't claim

Things that are solid:
- The algebraic identities (CAS-verified, you can re-run the scripts)
- The search results (exact integer arithmetic, reproducible)
- The z = 14 elimination (finite-field computation, fully specified)
- The Groebner basis showing (dagger) isn't a polynomial consequence

Things that aren't:
- I don't know if the full reduction to C_sw is valid (the bridge gap)
- The quotient-ring obstruction argument is evidence, not a complete proof
- The Chabauty analysis has bugs and I don't use it
- The problem itself is still open — I can't prove solutions exist or don't

## Running the code

```
# Main search (Python only, ~3 min)
cd scripts/search && python search_5M.py

# Verify the algebra (needs SymPy)
cd scripts/verification
python verify_identities.py
python verify_chain.py
python verify_groebner.py
```

## License

Text and reports: CC-BY 4.0. Code: MIT.
