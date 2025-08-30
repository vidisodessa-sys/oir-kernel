# examples/bench_chsh.py
# Benchmark CHSH for OIR in two regimes: iso3d vs equator
# Usage examples:
# python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3
# python -m examples.bench_chsh --preset standard
# python -m examples.bench_chsh --angles 1,0,0 0,1,0 0.7071,0.7071,0 0.7071,-0.7071,0

import time
import argparse
import numpy as np
from oir import chsh_value

def parse_vec(s: str) -> np.ndarray:
    x, y, z = map(float, s.split(","))
    v = np.array([x, y, z], dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError(f"Zero vector: {s}")
    return v / n

def get_axes(args):
    if args.preset == "standard":
        # Tsirelson-like CHSH set in the xy-plane
        return [
            np.array([1, 0, 0]), # a
            np.array([0, 1, 0]), # a'
            np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]), # b
            np.array([1/np.sqrt(2), -1/np.sqrt(2), 0]), # b'
        ]
    elif args.angles:
        if len(args.angles) != 4:
            raise ValueError("Provide exactly 4 vectors for --angles")
        return [parse_vec(s) for s in args.angles]
    else:
        # default = standard
        return [
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]),
            np.array([1/np.sqrt(2), -1/np.sqrt(2), 0]),
        ]

def run_once(axes, eps, M, mode):
    t0 = time.perf_counter()
    S = chsh_value(axes, eps=eps, M=M, mode=mode)
    dt = time.perf_counter() - t0
    return S, dt

def main():
    p = argparse.ArgumentParser(description="OIR CHSH benchmark")
    p.add_argument("--M", type=int, default=20000, help="Monte Carlo samples")
    p.add_argument("--eps", type=float, default=0.0, help="anisotropy ε")
    p.add_argument("--repeats", type=int, default=3, help="repetitions per mode")
    p.add_argument("--preset", choices=["standard"], default="standard",
                   help="angle preset (standard = typical CHSH optimal set)")
    p.add_argument("--angles", nargs="+",
                   help="override axes with 4 vectors 'x,y,z' ... (exactly 4)")
    args = p.parse_args()

    axes = get_axes(args)

    for mode in ["iso3d", "equator"]:
        Ss, Ts = [], []
        for _ in range(args.repeats):
            S, dt = run_once(axes, args.eps, args.M, mode)
            Ss.append(S); Ts.append(dt)
        print(f"\nMode: {mode}")
        print(f" eps = {args.eps}, M = {args.M}, repeats = {args.repeats}")
        print(f" S mean = {np.mean(Ss):.6f} (std {np.std(Ss):.6f})")
        print(f" time = {np.mean(Ts):.3f}s per run")

if __name__ == "__main__":
    main()

Запуск из корня репозитория:

python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3

Ожидаемо:

Mode: iso3d → S ≈ 0.67

Mode: equator → S ≈ 2.82 при eps=0.0
