# examples/bench_chsh.py
# Benchmark CHSH for OIR in two regimes: iso3d vs equator
# Usage examples:
# python -m examples.bench_chsh --M 20000 --eps 0.0 --repeats 3
# python -m examples.bench_chsh --preset standard
# python -m examples.bench_chsh --angles 1,0,0 0,1,0 0.7071,0.7071,0 0.7071,-0.7071,0


import argparse
import time
import numpy as np
from oir import oir_pair_correlator

def rand_n(mode: str) -> np.ndarray:
    """Random hidden direction n on S2."""
    if mode == "iso3d":
        v = np.random.normal(size=3)
        return v / np.linalg.norm(v)
    elif mode == "equator":
        phi = np.random.uniform(0.0, 2*np.pi)
        return np.array([np.cos(phi), np.sin(phi), 0.0])
    else:
        raise ValueError("mode must be iso3d or equator")

def E_pair(a, b, M, eps, mode):
    acc = 0.0
    for _ in range(M):
        n = rand_n(mode)
        Ka = 2.0*(np.dot(a, n)**2) - 1.0
        Kb = 2.0*(np.dot(b, n)**2) - 1.0
        # eps-модуляция: в бенчмарке выключаем (eps=0)
        acc += Ka*Kb
    return acc / M

def chsh_S(M: int, eps: float, mode: str):
    # Оптимальные плоскостные направления (все в XY):
    a = np.array([1.0, 0.0, 0.0]) # 0°
    ap = np.array([0.0, 1.0, 0.0]) # 90°
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0.0]) # +45°
    bp = np.array([1/np.sqrt(2), -1/np.sqrt(2), 0.0]) # -45°

    Eab = E_pair(a, b, M, eps, mode)
    Eabp = E_pair(a, bp, M, eps, mode)
    Eapb = E_pair(ap, b, M, eps, mode)
    Eapbp= E_pair(ap, bp, M, eps, mode)

    S = abs(Eab + Eabp + Eapb - Eapbp)
    return S, (Eab, Eabp, Eapb, Eapbp)

def run(mode: str, M: int, eps: float, repeats: int):
    t0 = time.time()
    Ss = []
    for _ in range(repeats):
        S, _ = chsh_S(M, eps, mode)
        Ss.append(S)
    t1 = time.time()
    Ss = np.array(Ss)
    print(f"\nMode: {mode}")
    print(f"eps = {eps}, M = {M}, repeats = {repeats}")
    print(f"S (mean) = {Ss.mean():.6f} (std {Ss.std(ddof=1):.6f})")
    print(f"S/4 = {Ss.mean()/4:.6f} (для сравнения с прежним “S mean”)")
    print(f"time = {(t1-t0)/repeats:.3f}s per run")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["iso3d","equator"], default="iso3d")
    ap.add_argument("--M", type=int, default=20000)
    ap.add_argument("--eps", type=float, default=0.0)
    ap.add_argument("--repeats", type=int, default=3)
    args = ap.parse_args()
    run(args.mode, args.M, args.eps, args.repeats)

И маленький тестовый скрипт (если хочешь посмотреть сами E-пары), обнови examples/chsh_s.py:

# examples/chsh_s.py
import numpy as np
from oir import oir_pair_correlator # не обязателен здесь
from bench_chsh import E_pair # используем ту же реализацию
from bench_chsh import rand_n # для единообразия

def main():
    M = 20000
    mode = "equator" # или "iso3d"

    a = np.array([1.0, 0.0, 0.0])
    ap = np.array([0.0, 1.0, 0.0])
    b = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0.0])
    bp = np.array([1/np.sqrt(2), -1/np.sqrt(2), 0.0])

    Eab = E_pair(a, b, M, 0.0, mode)
    Eabp = E_pair(a, bp, M, 0.0, mode)
    Eapb = E_pair(ap, b, M, 0.0, mode)
    Eapbp= E_pair(ap, bp, M, 0.0, mode)

    S = abs(Eab + Eabp + Eapb - Eapbp)
    print(f"E(a,b) = {Eab:.6f}")
    print(f"E(a,b') = {Eabp:.6f}")
    print(f"E(a',b) = {Eapb:.6f}")
    print(f"E(a',b') = {Eapbp:.6f}")
    print(f"S_CHSH = {S:.6f}")

if __name__ == "__main__":
    main()


