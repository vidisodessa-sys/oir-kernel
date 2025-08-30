# examples/bench_chsh.py
# Benchmark CHSH for OIR in two regimes: iso3d vs equator
# Usage examples:
# python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3
# python -m examples.bench_chsh --preset standard
# python -m examples.bench_chsh --angles 1,0,0 0,1,0 0.7071,0.7071,0 0.7071,-0.7071,0


import argparse
import time
import numpy as np

def rand_n(mode: str) -> np.ndarray:
    """Сэмпл скрытой оси n на сфере."""
    if mode == "iso3d":
        v = np.random.normal(size=3)
        return v / np.linalg.norm(v)
    elif mode == "equator":
        phi = np.random.uniform(0.0, 2*np.pi)
        return np.array([np.cos(phi), np.sin(phi), 0.0])
    else:
        raise ValueError("mode must be iso3d or equator")

def E_pair(a, b, M, mode):
    """E(a,b) = ⟨K(a,n)K(b,n)⟩, где K=2(a·n)^2-1."""
    acc = 0.0
    for _ in range(M):
        n = rand_n(mode)
        Ka = 2.0*(np.dot(a, n)**2) - 1.0
        Kb = 2.0*(np.dot(b, n)**2) - 1.0
        acc += Ka*Kb
    return acc / M

def chsh_S(M: int, mode: str):
    # Оптимальные направления в плоскости XY
    a = np.array([1.0, 0.0, 0.0]) # 0°
    ap = np.array([0.0, 1.0, 0.0]) # 90°
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0.0]) # +45°
    bp = np.array([1/np.sqrt(2), -1/np.sqrt(2), 0.0]) # -45°

    Eab = E_pair(a, b, M, mode)
    Eabp = E_pair(a, bp, M, mode)
    Eapb = E_pair(ap, b, M, mode)
    Eapbp = E_pair(ap, bp, M, mode)

    S = abs(Eab + Eabp + Eapb - Eapbp)
    return S, (Eab, Eabp, Eapb, Eapbp)

def run(mode: str, M: int, repeats: int):
    t0 = time.time()
    Ss = []
    for _ in range(repeats):
        S, (Eab, Eabp, Eapb, Eapbp) = chsh_S(M, mode)
        print(f"E(a,b) = {Eab:.6f}")
        print(f"E(a,b') = {Eabp:.6f}")
        print(f"E(a',b) = {Eapb:.6f}")
        print(f"E(a',b')= {Eapbp:.6f}")
        print(f"S = {S:.6f}\n")
        Ss.append(S)
    dt = (time.time() - t0)/repeats
    Ss = np.array(Ss)
    print(f"Mode: {mode}")
    print(f"M = {M}, repeats = {repeats}")
    print(f"S mean = {Ss.mean():.6f} (std {Ss.std(ddof=1):.6f})")
    print(f"S/4 = {Ss.mean()/4:.6f} (наследие прежней метрики)")
    print(f"time = {dt:.3f}s per run")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["iso3d","equator"], default="iso3d")
    ap.add_argument("--M", type=int, default=20000)
    ap.add_argument("--repeats", type=int, default=3)
    args = ap.parse_args()
    run(args.mode, args.M, args.repeats)



