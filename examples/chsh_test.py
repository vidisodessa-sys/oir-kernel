import numpy as np
from oir import oir_pair_correlator

def chsh_value(axes, eps=0.0, M=10000):
    a, ap, b, bp = axes
    Eab = oir_pair_correlator(a, b, eps, M)
    Eabp = oir_pair_correlator(a, bp, eps, M)
    Eapb = oir_pair_correlator(ap, b, eps, M)
    Eapbp= oir_pair_correlator(ap, bp, eps, M)
    S_raw = abs(Eab + Eabp + Eapb - Eapbp)
    return S_raw

if __name__ == "__main__":
    # standard CHSH axes
    a = np.array([1,0,0])
    ap = np.array([0,1,0])
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])
    bp = np.array([1/np.sqrt(2),-1/np.sqrt(2), 0])

    S_raw = chsh_value([a, ap, b, bp], eps=0.0, M=20000)
    S_rescaled = 4 * S_raw # QM convention

    print(f"S_raw = {S_raw:.6f}")
    print(f"S_rescaled = {S_rescaled:.6f} (QM units)")
