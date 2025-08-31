# examples/bench_chsh.py
# Benchmark CHSH for OIR in two regimes: iso3d vs equator
# Usage examples:
# python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3
# python -m examples.bench_chsh --preset standard
# python -m examples.bench_chsh --angles 1,0,0 0,1,0 0.7071,0.7071,0 0.7071,-0.7071,0


# examples/bench_chsh.py

import time
import numpy as np
from src.oir.core import oir_pair_correlator

def run_chsh(mode="iso3d", M=20000, repeats=3, eps=0.0):
    """
    Run CHSH benchmark in OIR or QM baseline mode.
    mode = "iso3d" -> OIR Monte Carlo
    mode = "equator" -> QM theoretical baseline
    """
    if mode == "equator":
        print("Mode: equator (QM baseline)")
        print(f"S (theory) = {2*np.sqrt(2):.6f}")
        return

    print(f"Mode: {mode} (OIR Monte Carlo)")
    raw_results = []
    rescaled_results = []
    times = []

    # analyzer directions (standard CHSH)
    a = np.array([1,0,0])
    a_ = np.array([0,1,0])
    b = np.array([1/np.sqrt(2),1/np.sqrt(2),0])
    b_ = np.array([1/np.sqrt(2),-1/np.sqrt(2),0])

    for r in range(repeats):
        t0 = time.time()

        E_ab = oir_pair_correlator(a, b, eps=eps, M=M)
        E_ab_ = oir_pair_correlator(a, b_, eps=eps, M=M)
        E_a_b = oir_pair_correlator(a_, b, eps=eps, M=M)
        E_a_b_= oir_pair_correlator(a_, b_, eps=eps, M=M)

        S_raw = abs(E_ab + E_ab_ + E_a_b - E_a_b_)
        S_rescaled = 4 * S_raw # align with QM metric

        t1 = time.time()
        dt = t1 - t0

        raw_results.append(S_raw)
        rescaled_results.append(S_rescaled)
        times.append(dt)

        print(f"Run {r+1}: S_raw = {S_raw:.6f}, S_rescaled = {S_rescaled:.6f}, time = {dt:.3f}s")

    print()
    print(f"S_raw mean = {np.mean(raw_results):.6f} (std {np.std(raw_results):.6f})")
    print(f"S_rescaled mean = {np.mean(rescaled_results):.6f} (std {np.std(rescaled_results):.6f})")
    print(f"avg time ≈ {np.mean(times):.3f}s per run")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["iso3d","equator"], default="iso3d")
    parser.add_argument("-M", type=int, default=20000)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--eps", type=float, default=0.0)
    args = parser.parse_args()

    run_chsh(mode=args.mode, M=args.M, repeats=args.repeats, eps=args.eps)

