# examples/bench_chsh.py
# Benchmark CHSH for OIR in two regimes: iso3d vs equator
# Usage examples:
# python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3
# python -m examples.bench_chsh --preset standard
# python -m examples.bench_chsh --angles 1,0,0 0,1,0 0.7071,0.7071,0 0.7071,-0.7071,0


import argparse
import numpy as np
from src.oir.core import oir_pair_correlator

def run_chsh(mode="iso3d", M=20000, repeats=3, eps=0.0):
    # Standard CHSH directions
    a = np.array([1, 0, 0])
    a_ = np.array([0, 1, 0])
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])
    b_ = np.array([1/np.sqrt(2), -1/np.sqrt(2), 0])

    results = []
    for _ in range(repeats):
        if mode == "iso3d":
            Eab = oir_pair_correlator(a, b, eps=eps, M=M)
            Eab_ = oir_pair_correlator(a, b_, eps=eps, M=M)
            Ea_b = oir_pair_correlator(a_, b, eps=eps, M=M)
            Ea_b_= oir_pair_correlator(a_, b_,eps=eps, M=M)

            S = abs(Eab + Eab_ + Ea_b - Ea_b_)
        elif mode == "equator":
            # QM baseline (theoretical)
            S = 2*np.sqrt(2)
        else:
            raise ValueError("Mode must be iso3d or equator")
        results.append(S)

    S_raw = np.mean(results)
    S_std = np.std(results)

    # Apply rescaling for comparison
    S_rescaled = 4 * S_raw

    print(f"Mode: {mode}")
    print(f"Raw S = {S_raw:.6f} ± {S_std:.6f}")
    print(f"Rescaled S (QM units) ≈ {S_rescaled:.6f}")
    if mode == "equator":
        print(f"(Tsirelson bound) = {2*np.sqrt(2):.6f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["iso3d", "equator"], default="iso3d")
    parser.add_argument("-M", type=int, default=20000)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--eps", type=float, default=0.0)
    args = parser.parse_args()

    run_chsh(mode=args.mode, M=args.M, repeats=args.repeats, eps=args.eps)



