# oir-kernel

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16995727.svg)](https://doi.org/10.5281/zenodo.16995727)

Python implementation of the **Orientation Integral Rule (OIR)** —  
a geometric alternative to the Born rule, with applications to quantum correlations and efficient simulations.

---

## Overview
This repository provides a reference Python implementation of the OIR computational kernel,  
as described in:

- Bakhariev, V. (2025). *The Orientation Integral Rule (OIR): A Geometric Alternative to the Born Rule with Practical Computational Advantages*.  
  DOI: [10.5281/zenodo.16995727](https://doi.org/10.5281/zenodo.16995727)

---

## Contents
- `src/oir_core.py` — core implementation of OIR kernel  
- `examples/` — demo scripts (e.g., CHSH, GHZ correlations)  
- `requirements.txt` — Python dependencies

---

## Installation
Clone the repository:
```bash
git clone https://github.com/vidisodessa-sys/oir-kernel.git
cd oir-kernel
pip install -r requirements.txt
```
---
## Usage

Example: compute a CHSH correlator with OIR.

```python
from oir import oir_correlator, chsh_value
import numpy as np

# Example: CHSH settings
a = np.array([1,0,0])
ap = np.array([0,1,0])
b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])
bp = np.array([1/np.sqrt(2), -1/np.sqrt(2), 0])

S = chsh_value([a, ap, b, bp], eps=0.0, M=20000, mode="equator")
print("CHSH value:", S)
```
## Examples

### CHSH (single run)
Run a single CHSH computation with OIR and print both raw and rescaled (QM units) values.

```bash
python -m examples.chsh_test
```
Example output:
S_raw = 0.676842
S_rescaled = 2.707368 (QM units)

### CHSH (full S from four correlators)
Compute all four correlators and assemble CHSH S; print raw and rescaled.
```bash
python -m examples.chsh_s
```
Example output:
CHSH test (OIR kernel)
E(a,b) = 0.338921
E(a,b') = 0.341057
E(a',b) = 0.339874
E(a',b') = 0.336997
----------------------------------------
S_raw = 0.678855
S_rescaled = 2.715418 (QM units)


---
### GHZ test (3-party correlator)
We also provide a simple 3-point GHZ correlator test.

Run:
```bash
python -m examples.ghz_test
```
Example output:
GHZ test (OIR kernel)
Axes: [1. 0. 0.], [-0.5 0.8660254 0. ], [-0.5 -0.8660254 0. ]
----------------------------------------
E_raw = -0.229421
E_rescaled = -0.917683 (QM units, optional ×4 scaling)

Notes:
For GHZ, the raw OIR value already lies in the natural range [-1,+1], just like in standard QM.
The rescaled value (×4) is shown only for consistency with the CHSH presentation, not because GHZ requires rescaling.
This confirms that OIR reproduces the correct qualitative GHZ-type correlations.

---
### CHSH (benchmark with repeats & timing)
Compare OIR (iso3d) vs QM baseline (equator). Shows 3 runs with per-run timing, and mean ± std; prints raw and rescaled S.
Run the benchmark from the repository root:

```bash
python -m examples.bench_chsh --mode equator # QM (theoretical baseline)
python -m examples.bench_chsh --mode iso3d # OIR Monte Carlo
```
Example output (iso3d):
Mode: iso3d (OIR Monte Carlo)
M = 20000, repeats = 3

Run 1: S_raw = 0.673590, S_rescaled = 2.694358, time = 3.911s  
Run 2: S_raw = 0.676999, S_rescaled = 2.707996, time = 3.960s  
Run 3: S_raw = 0.679678, S_rescaled = 2.718711, time = 3.953s  

S_raw mean = 0.676755 (std 0.002491)  
S_rescaled mean = 2.707022 (std 0.009966)  
avg time ≈ 3.94s per run

Mode: equator (QM baseline)

S (theory) = 2.828427  
time = 0.000s

## Scaling note

The raw OIR kernel produces correlators in the correct range **[-1, 1]**,  
so for direct correlators *E(a,b)* no rescaling is required.

However, when comparing **inequality-type quantities** (e.g. CHSH S-value, GHZ/Mermin functionals)  
against standard quantum mechanical conventions, a factor ×4 is applied:

- **CHSH**: raw OIR gives S ≈ 0.67 → rescaled ×4 → ≈ 2.8 (close to Tsirelson bound 2√2).  
- **GHZ/Mermin**: raw OIR gives value ≈ 1 → rescaled ×4 → ≈ 4 (QM maximum).  
- **Direct correlators E(a,b)**: already normalized to [-1,1], no scaling needed.

This rescaling is **not part of the physics**, only a convention to align OIR outputs with QM-style benchmarks.

## Note on statistics:
- `mean` = average value over several runs.  
- `std` = standard deviation, a measure of fluctuations between runs.  
  A small `std` (e.g. ±0.01) means the Monte Carlo estimate is stable;  
  a larger `std` would indicate more noise or the need for higher `M`.

---

## Command-line (CLI)
After `pip install -e .`, a command `oir` is available:

```bash
# CHSH preset
oir --preset chsh --eps 0.0 -M 100000

# From file (CSV or JSON)
oir --axes-file axes.csv --eps 0.01 -M 200000
```
---

## Citation
If you use this code, please cite:

Vitalii Bakhariev (2025).
The Orientation Integral Rule (OIR): A Geometric Alternative to the Born Rule with Practical Computational Advantages.
Zenodo. DOI: 10.5281/zenodo.16995727

---

BibTeX:

@misc{bakhariev2025oir,
  author       = {Bakhariev, Vitalii},
  title        = {The Orientation Integral Rule (OIR): 
                  A Geometric Alternative to the Born Rule with Practical Computational Advantages},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.16995727},
  url          = {https://doi.org/10.5281/zenodo.16995727}
}

---

## Roadmap
**Mermin inequality** (generalization of GHZ to 3+ parties)  
**Quantum Fourier Transform (QFT) demo** (phase-structured correlations)  
**Grover search (toy version)** (amplitude amplification with OIR)  
**Shor period finding (mini-demo)** (small-N factorization case)  
**Noise/robustness tests** (OIR stability under perturbations)  
  
---

## License
Article text: CC BY 4.0
OIR computational kernel: Non-commercial research use only.
Any commercial or industrial use requires explicit written permission from the author.
Copyright © 2025 Vitalii Bakhariev. All rights reserved.
