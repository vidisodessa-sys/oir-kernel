import numpy as np
from oir import oir_pair_correlator

def chsh_value(a, ap, b, bp, eps=0.0, M=20000):
    """Compute CHSH value from four directions."""
    Eab = oir_pair_correlator(a, b, eps=eps, M=M)
    Eabp = oir_pair_correlator(a, bp, eps=eps, M=M)
    Eapb = oir_pair_correlator(ap, b, eps=eps, M=M)
    Eapbp = oir_pair_correlator(ap, bp, eps=eps, M=M)

    S_raw = abs(Eab - Eabp + Eapb + Eapbp)
    S_rescaled = 4 * S_raw # map to QM units
    return S_raw, S_rescaled, (Eab, Eabp, Eapb, Eapbp)

if __name__ == "__main__":
    # Standard CHSH settings
    a = np.array([1,0,0])
    ap = np.array([0,1,0])
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])
    bp = np.array([1/np.sqrt(2), -1/np.sqrt(2), 0])

    S_raw, S_rescaled, Evals = chsh_value(a, ap, b, bp, eps=0.0, M=20000)

    print("CHSH test (OIR kernel)")
    print(f"E(a,b) = {Evals[0]:.6f}")
    print(f"E(a,b') = {Evals[1]:.6f}")
    print(f"E(a',b) = {Evals[2]:.6f}")
    print(f"E(a',b') = {Evals[3]:.6f}")
    print("-" * 40)
    print(f"S_raw = {S_raw:.6f}")
    print(f"S_rescaled = {S_rescaled:.6f} (QM units)")
