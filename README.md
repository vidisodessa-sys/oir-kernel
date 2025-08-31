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
---
## Benchmarks

We provide a simple CHSH benchmark to compare **OIR** against the **quantum mechanical (QM) baseline**.

Run the benchmark from the repository root:

```bash
python -m examples.bench_chsh --mode equator # QM (theoretical baseline)
python -m examples.bench_chsh --mode iso3d # OIR Monte Carlo

Example results

Mode: iso3d (OIR Monte Carlo)
M = 20000, repeats = 3
S ≈ 0.67 ± 0.01
time ≈ 4s per run

Mode: equator (QM baseline)
S (theory) = 2.828427
time = 0.000s
```
## Scaling note

The raw OIR kernel produces correlators with a natural range different from the QM formalism.

Therefore, its CHSH score is around S ≈ 0.67 by default.

For visual comparison with QM, one may introduce a rescaling factor (×4), giving a value close to the Tsirelson bound (2\sqrt{2} \approx 2.828).

This rescaling is not part of the physics, only a way to align units when comparing with QM conventions.

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
- GHZ examples and benchmarks (equatorial presets, ε-modulation) — planned for v0.2.
  
---

## License
Article text: CC BY 4.0
OIR computational kernel: Non-commercial research use only.
Any commercial or industrial use requires explicit written permission from the author.
Copyright © 2025 Vitalii Bakhariev. All rights reserved.
