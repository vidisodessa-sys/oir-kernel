import numpy as np
from oir import oir_correlator

# Single contour on the equator (xy-plane), angle is set in radians
def axis(theta):
    return np.array([np.cos(theta), np.sin(theta), 0.0])

# Optimal angles for CHSH
theta_a = 0.0
theta_ap = np.pi/2
theta_b = np.pi/4
theta_bp = -np.pi/4

a = axis(theta_a)
ap = axis(theta_ap)
b = axis(theta_b)
bp = axis(theta_bp)

M = 200_000
eps = 0.0

# Correlators E(a,b) = ⟨K(a,u)K(b,u)⟩
Eab = oir_correlator([a, b], eps=eps, M=M)
Eabp = oir_correlator([a, bp], eps=eps, M=M)
Eapb = oir_correlator([ap, b], eps=eps, M=M)
Eapbp = oir_correlator([ap, bp], eps=eps, M=M)

# S = E(a,b) + E(a,b') + E(a',b) - E(a',b')
S = Eab + Eabp + Eapb - Eapbp

print(f"E(a,b) = {Eab:.6f}")
print(f"E(a,b') = {Eabp:.6f}")
print(f"E(a',b) = {Eapb:.6f}")
print(f"E(a',b') = {Eapbp:.6f}")
print(f"S ≈ {S:.6f}")
