import numpy as np
from oir import oir_correlator

def ghz_value(axes, eps=0.0, M=20000):
    """Compute GHZ correlator for given analyzer directions."""
    E_raw = oir_correlator(axes, eps=eps, M=M)
    E_rescaled = 4 * E_raw # map to QM units
    return E_raw, E_rescaled

if __name__ == "__main__":
    # GHZ example: 3 analyzers at 120° in xy-plane
    a1 = np.array([1, 0, 0])
    a2 = np.array([-0.5, np.sqrt(3)/2, 0])
    a3 = np.array([-0.5, -np.sqrt(3)/2, 0])

    E_raw, E_rescaled = ghz_value([a1, a2, a3], eps=0.0, M=20000)

    print("GHZ test (OIR kernel)")
    print(f"Axes: {a1}, {a2}, {a3}")
    print("-" * 40)
    print(f"E_raw = {E_raw:.6f}")
    print(f"E_rescaled = {E_rescaled:.6f} (QM units)")
