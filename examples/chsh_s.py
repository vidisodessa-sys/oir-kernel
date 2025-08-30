import numpy as np
from oir import oir_pair_correlator

def unit(v):
    v = np.array(v, dtype=float)
    return v / np.linalg.norm(v)

# --- Стандартные оси CHSH ---
a = unit([1, 0, 0])
ap = unit([0, 1, 0])
b = unit([1/np.sqrt(2), 1/np.sqrt(2), 0])
bp = unit([1/np.sqrt(2), -1/np.sqrt(2), 0])

eps = 0.0 # параметр модуляции
M = 200_000 # количество выборок Монте-Карло

Ea_b = oir_pair_correlator(a, b, eps=eps, M=M)
Ea_bp = oir_pair_correlator(a, bp, eps=eps, M=M)
Eap_b = oir_pair_correlator(ap, b, eps=eps, M=M)
Eap_bp = oir_pair_correlator(ap, bp, eps=eps, M=M)

S = abs(Ea_b - Ea_bp + Eap_b + Eap_bp)

print(f"E(a,b) = {Ea_b:.6f}")
print(f"E(a,b') = {Ea_bp:.6f}")
print(f"E(a',b) = {Eap_b:.6f}")
print(f"E(a',b') = {Eap_bp:.6f}")
print(f"S_CHSH = {S:.6f}")
