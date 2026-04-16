# Exploratory scripts

These are approaches I tried that didn't pan out. They're here for completeness but I don't rely on any of them in my conclusions.

**final_certify_Csw.m** — Magma script that computes a rank bound on the Jacobian (1 <= rank <= 2, which is correct). But the script goes on to claim S = emptyset based on a Chabauty-Coleman argument that I couldn't get to work properly. The rank bound is the only part I'd stand behind.

**chabauty_final.py, chabauty_csw_patched.sage** — My attempts at Chabauty-Coleman disk analysis. These have real errors: I was using omega_1 as if it were an annihilating differential (it's not, because E_sw has rank 1), and the valuation argument for the (0, ±2) disks has a wrong sign. I kept them because the approach is interesting even if my execution was flawed.

**padic_log2.sage** — Computes a p-adic logarithm. The computation is probably fine on its own but it feeds into the Chabauty scripts above, so it's moot.

**mod3_proof.py** — Tries to prove S = emptyset from the fact that there are no F_3-solutions. The F_3 non-existence is real, but the jump to "no Q_3-solution" is wrong: you can have 3 in the denominator of x or y, which escapes the F_3 analysis entirely. (I do use the correct mod-3 *necessary condition* in my search scripts, but that's derived separately and doesn't claim a local obstruction.)
