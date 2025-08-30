import numpy as np
from oir_core import oir_correlator

"""
Example: CHSH correlator using the Orientation Integral Rule (OIR).

This script demonstrates how to compute the CHSH value
with four analyzer directions.
"""

# 4 analyzer directions (unit vectors)
axes = [
    np.array([1,0,0]),
    np.array([0,1,0]),
    np.array([1/np.sqrt(2),1/np.sqrt(2),0]),
    np.array([1/np.sqrt(2),-1/np.sqrt(2),0])
]

# Run OIR correlator
value = oir_correlator(axes, eps=0.0, M=100000)

print("CHSH correlator:", value)
