# MSCS 531 — ILP Techniques: gem5 Simulation Analysis

**Course:** MSCS 531: Computer Architecture and Design
**Author:** Todd Simonson
**Institution:** University of the Cumberlands

## Overview

This repository contains gem5 simulation configurations and results for Assignment 4 Part 2: Practical Exploration of ILP Techniques. Four experiments analyze the impact of pipelining, branch prediction, superscalar issue width, and simultaneous multithreading on processor performance using a matrix multiplication benchmark.

## Requirements

- gem5 version 25.1.0.0 built for X86
- GCC (for compiling the benchmark)
- Python 3 (gem5 dependency)

## Repository Structure

```
mscs531-gem5-ilp-analysis/
├── benchmarks/
│   ├── matrix_multiply.c       # Benchmark source code
│   └── matrix_multiply         # Compiled binary (x86)
├── configs/
│   ├── baseline.py             # TimingSimpleCPU, single issue, no branch prediction
│   ├── branch_tournament.py    # DerivO3CPU with tournament branch predictor
│   ├── branch_local.py         # DerivO3CPU with local branch predictor
│   ├── superscalar.py          # DerivO3CPU, 4-wide issue, tournament predictor
│   └── smt.py                  # DerivO3CPU, 2 hardware threads (SMT)
├── results/
│   ├── baseline/stats.txt
│   ├── branch_tournament/stats.txt
│   ├── branch_local/stats.txt
│   ├── superscalar/stats.txt
│   └── smt/stats.txt
├── .gitignore
└── README.md
```

## Setup

**1. Build gem5 for X86** (if not already built):
```bash
cd ~/gem5
scons build/X86/gem5.opt -j4
```

**2. Clone this repository:**
```bash
git clone git@github.com:tgsimonson/mscs531-gem5-ilp-analysis.git
cd mscs531-gem5-ilp-analysis
```

**3. Compile the benchmark:**
```bash
gcc -O0 benchmarks/matrix_multiply.c -o benchmarks/matrix_multiply
```

**4. Verify the benchmark runs natively:**
```bash
./benchmarks/matrix_multiply
# Expected: Matrix multiplication complete. C[0][0] = 85344
```

## Running Simulations

Run each configuration from the repository root:

```bash
~/gem5/build/X86/gem5.opt --outdir=results/baseline configs/baseline.py
~/gem5/build/X86/gem5.opt --outdir=results/branch_tournament configs/branch_tournament.py
~/gem5/build/X86/gem5.opt --outdir=results/branch_local configs/branch_local.py
~/gem5/build/X86/gem5.opt --outdir=results/superscalar configs/superscalar.py
~/gem5/build/X86/gem5.opt --outdir=results/smt configs/smt.py
```

## Extracting Statistics

Key performance metrics from any results directory:
```bash
grep -E "simInsts|simTicks|ipc|cpi" results/baseline/stats.txt | head -10
```

Branch prediction statistics:
```bash
grep -E "Mispred|mispred" results/branch_tournament/stats.txt | head -10
```

## Configuration Summary

| Config | CPU Model | Issue Width | Branch Predictor | Threads |
|---|---|---|---|---|
| baseline.py | TimingSimpleCPU | 1 | None | 1 |
| branch_tournament.py | DerivO3CPU | 1 | Tournament | 1 |
| branch_local.py | DerivO3CPU | 1 | Local | 1 |
| superscalar.py | DerivO3CPU | 4 | Tournament | 1 |
| smt.py | DerivO3CPU | 1 | Tournament | 2 |

All configurations use: DDR3_1600_8x8 DRAM, 512MB memory range, 1GHz clock, 32kB L1 caches, SE (syscall emulation) mode.

## Troubleshooting Notes

- **TournamentBP instantiation:** In gem5 25.1, branch predictors must be set via a `BranchPredictor` wrapper: `system.cpu.branchPred = BranchPredictor(conditionalBranchPred=TournamentBP(numThreads=1))`
- **SMT multithread assertion:** Set `system.multi_thread = True` before CPU instantiation, and loop interrupt controller port connections across all threads
- **SMT PID conflict:** Assign explicit PIDs to each process: `Process(pid=100)` and `Process(pid=101)`
- **DRAM capacity warning:** Expected behavior in SE mode, does not affect results
EOF
echo "Done"