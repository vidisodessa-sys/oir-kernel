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
- `oir_core.py` — core implementation of OIR kernel  
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

## Usage

Example: compute a CHSH correlator with OIR.

```python
from oir_core import oir_correlator
import numpy as np

# Example: 4 analyzer directions (unit vectors)
axes = [
    np.array([1,0,0]),
    np.array([0,1,0]),
    np.array([1/np.sqrt(2),1/np.sqrt(2),0]),
    np.array([1/np.sqrt(2),-1/np.sqrt(2),0])
]

value = oir_correlator(axes, eps=0.0, M=100000)
print("CHSH correlator:", value)
```
## Citation
If you use this code, please cite:

Vitalii Bakhariev (2025).
The Orientation Integral Rule (OIR): A Geometric Alternative to the Born Rule with Practical Computational Advantages.
Zenodo. DOI: 10.5281/zenodo.16995727

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
## License
Article text: CC BY 4.0
OIR computational kernel: Non-commercial research use only.
Any commercial or industrial use requires explicit written permission from the author.
Copyright © 2025 Vitalii Bakhariev. All rights reserved.
