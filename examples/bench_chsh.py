# examples/bench_chsh.py
# Benchmark CHSH for OIR in two regimes: iso3d vs equator
# Usage examples:
# python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3
# python -m examples.bench_chsh --preset standard
# python -m examples.bench_chsh --angles 1,0,0 0,1,0 0.7071,0.7071,0 0.7071,-0.7071,0


import numpy as np
import argparse
import time
from oir import oir_pair_correlator

def chsh_value(a, ap, b, bp, eps=0.0, M=10000):
    """
    Compute CHSH value S = |E(a,b)+E(a,b')+E(a',b)-E(a',b')|
    using OIR pair correlator.
    """
    Eab = oir_pair_correlator(a, b, eps=eps, M=M)
    Eabp = oir_pair_correlator(a, bp, eps=eps, M=M)
    Eapb = oir_pair_correlator(ap, b, eps=eps, M=M)
    Eapbp= oir_pair_correlator(ap, bp,eps=eps, M=M)
    return abs(Eab + Eabp + Eapb - Eapbp), (Eab, Eabp, Eapb, Eapbp)


def run_iso3d(M, eps, repeats, scale):
    print("Mode: iso3d (OIR Monte Carlo)")
    # standard CHSH settings
    a = np.array([1,0,0])
    ap = np.array([0,1,0])
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])
    bp = np.array([1/np.sqrt(2),-1/np.sqrt(2), 0])

    Ss, times = [], []
    for r in range(repeats):
        t0 = time.time()
        S, (Eab,Eabp,Eapb,Eapbp) = chsh_value(a, ap, b, bp, eps=eps, M=M)
        t1 = time.time()
        print(f"\nRun {r+1}:")
        print(f"E(a,b) = {Eab:.6f}")
        print(f"E(a,b') = {Eabp:.6f}")
        print(f"E(a',b) = {Eapb:.6f}")
        print(f"E(a',b') = {Eapbp:.6f}")
        print(f"S = {S:.6f}")
        print(f"time = {t1-t0:.3f}s")
        Ss.append(S); times.append(t1-t0)

    S_mean, S_std = np.mean(Ss), np.std(Ss)
    print(f"\nS mean = {S_mean:.6f} (std {S_std:.6f})")
    if scale != 1.0:
        print(f"S mean × {scale:g} = {S_mean*scale:.6f} (scaled)")
    print(f"time ≈ {np.mean(times):.3f}s per run\n")


def run_equator():
    print("Mode: equator (QM baseline)")
    # Tsirelson bound (theoretical max)
    print("S (theory) = 2.828427\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["iso3d","equator"], default="iso3d")
    p.add_argument("--M", type=int, default=20000, help="number of samples")
    p.add_argument("--eps", type=float, default=0.0, help="anisotropy parameter")
    p.add_argument("--repeats", type=int, default=3, help="number of repetitions")
    p.add_argument("--scale", type=float, default=1.0,
                   help="scale factor for printing S (e.g. 4.0 to match QM scale)")
    args = p.parse_args()

    if args.mode == "iso3d":
        run_iso3d(M=args.M, eps=args.eps, repeats=args.repeats, scale=args.scale)
    elif args.mode == "equator":
        run_equator()



