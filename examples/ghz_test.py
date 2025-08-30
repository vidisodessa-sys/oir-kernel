import numpy as np
from oir_core import oir_correlator

"""
Example: GHZ/Mermin correlator using the Orientation Integral Rule (OIR).

This script demonstrates how to compute a 3-qubit GHZ-type
correlator with three analyzer directions.
"""

# Analyzer directions (unit vectors) for GHZ test
axes = [
    np.array([1,0,0]), # X direction
    np.array([0,1,0]), # Y direction
    np.array([0,0,1]) # Z direction
]

# Run OIR correlator
value = oir_correlator(axes, eps=0.0, M=100000)

print("GHZ/Mermin correlator:", value)
