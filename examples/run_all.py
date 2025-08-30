import numpy as np
from oir_core import oir_correlator

"""
Run multiple OIR tests (CHSH and GHZ/Mermin).
"""

def run_chsh():
    # CHSH setup: 4 analyzer directions
    axes = [
        np.array([1,0,0]),
        np.array([0,1,0]),
        np.array([1/np.sqrt(2),1/np.sqrt(2),0]),
        np.array([1/np.sqrt(2),-1/np.sqrt(2),0])
    ]
    value = oir_correlator(axes, eps=0.0, M=100000)
    print("CHSH correlator:", value)

def run_ghz():
    # GHZ setup: 3 analyzer directions
    axes = [
        np.array([1,0,0]), # X
        np.array([0,1,0]), # Y
        np.array([0,0,1]) # Z
    ]
    value = oir_correlator(axes, eps=0.0, M=100000)
    print("GHZ/Mermin correlator:", value)

if __name__ == "__main__":
    print("=== Running OIR tests ===")
    run_chsh()
    run_ghz()
