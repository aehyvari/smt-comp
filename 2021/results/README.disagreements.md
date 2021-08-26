Disagreements
=============

Single Query
------------

We collected all benchmarks on which at least one solver returned sat and and at least one solver returned unsat

```
cat Single_Query_Track.csv  |csvcut -c 2,12 |cut -d/ -f2- |grep sat$ | sort |uniq | cut -d, -f1 |uniq -c | grep -v '   1 ' | cut -c9- > sq-disagreements.txt
```

In `sq-disagreements-decision.csv` we provide the decision of the
status that we used to evaluate soundness of the solvers.  The
decisions were made, because:

1. For `QF_SLIA`, we manually investigated that the model given by cvc5
   is correct and these benchmarks are indeed sat.  The solver z3str4 was
   buggy.
2. For `QF_LIA`, the authors of opensmt confirmed the bug and fixed it.
3. For `QF_ABVFP`, `QF_BVFP`, `QF_FP`, the authors of COLIBRI confirmed the bug
   and fixed it. The new version agrees with the recorded decision.
4. For `QF_ABVFPLRA`, the last year's COLIBRI solver was unsound.  Again the
   new version of COLIBRI agrees with our decision.
5. For `UF`, the iProver team confirmed a problem with their solver, the
   fixed version of the solver returns unknown for the benchmarks.
6. For `UFDTLIRA`, the last year's Vampire solver disagrees with this years
   Vampire and or cvc4/5.  We therefore assume that Vampire was unsound.
7. For `LIA` and `UFNIA` there were some disagreements with Vampire, that were
   fixed by the Vampire team.
8. `UFNIA` also had other disagreements with Par4. In many cases we went
   with the majority vote.


Incremental
-----------

Two issues were found and resolved as follows:

1. In `QF_ABVFP`, Bitwuzla disaggreed with all other solvers on a few 
   benchmarks. The problem was confirmed by the authors and their fixed
   version agrees with the other solvers.
2. Also in `QF_ABVFP` and in `QF_BVFP`, mathsat disagrees with all other
   solvers on a few benchmarks.  We stick with the majority here.


Cloud
-----

```
cat raw-results-Cloud.csv  |csvcut -c 2,12 |cut -d/ -f2- |grep sat$ | sort |uniq | cut -d, -f1 |uniq -c | grep -v '   1 ' | awk '{print $2}' > Cloud-disagreements.txt
```

1. In `QF_BVFP` Par4 disagreed with all other on two instances with unknown
   status:
    - `QF_BVFP/20170428-Liew-KLEE/imperial_gsl_benchmarks_differentiation_klee.x86_64/query.10.smt2`
    - `QF_BVFP/20170428-Liew-KLEE/imperial_synthetic_interval_klee_bug_symbolic_increment.x86_64/query.18.smt2`
2. In `QF_BVFP` Par4 disagreed with all others on one instance with
   known status:
    - `QF_BVFP/20170428-Liew-KLEE/imperial_gsl_benchmarks_statistics_klee.x86_64/query.14.smt2`
2
3. In `QF_FP` Par4 disagreed with solvers on eight instances with unknown status
    - `QF_FP/griggio/fmcad12/mul_000003_30000_1.smt2`
    - `QF_FP/griggio/fmcad12/test_v5_r10_vr10_c1_s15708.smt2`
    - `QF_FP/griggio/fmcad12/test_v5_r10_vr5_c1_s8690.smt2`
    - `QF_FP/griggio/fmcad12/test_v5_r15_vr1_c1_s26845.smt2`
    - `QF_FP/griggio/fmcad12/test_v7_r12_vr1_c1_s703.smt2`
    - `QF_FP/griggio/fmcad12/test_v5_r10_vr10_c1_s7608.smt2`
    - `QF_FP/griggio/fmcad12/test_v7_r12_vr1_c1_s10576.smt2`
    - `QF_FP/griggio/fmcad12/test_v7_r7_vr1_c1_s24449.smt2`
   In `QF_FP` Par4 disagrees on two instance with known status
    - `QF_FP/griggio/fmcad12/test_v5_r15_vr5_c1_s23844.smt2`
    - `QF_FP/griggio/fmcad12/test_v5_r15_vr5_c1_s26657.smt2`
   In `UFLRA` cvc5-gg disagrees on two instances with known status
    - `UFLRA/misc/set14.smt2`
    - `UFLRA/misc/list2.smt2`


Parallel
--------

```
cat raw-results-Parallel.csv  |csvcut -c 2,12 |cut -d/ -f2- |grep sat$ | sort |uniq | cut -d, -f1 |uniq -c | grep -v '   1 ' | awk '{print $2}' > Parallel-disagreements.txt
```

The disagreements are by the same solvers and in the same instances as
in Cloud, with the addition of

1. In `QF_FP` Par4 disagrees with one instance with known status
    - `QF_FP/griggio/fmcad12/test_v5_r10_vr10_c1_s21502.smt2`

