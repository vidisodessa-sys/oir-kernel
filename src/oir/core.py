import numpy as np

# -----------------------------
# Базовые утилиты (как у тебя)
# -----------------------------
def haar_sample_su2():
    """Generate a random SU(2) unitary (Haar-like demo)."""
    u1, u2, u3 = np.random.normal(size=3)
    norm = np.sqrt(u1**2 + u2**2 + u3**2)
    u1, u2, u3 = u1/norm, u2/norm, u3/norm
    a = u1 + 1j*u2
    b = u3
    return np.array([[a, b], [-b, np.conj(a)]])

def rotate_z_by(u):
    """Apply SU(2) rotation u to z-axis Bloch vector; return 3D unit vector."""
    sigma_x = np.array([[0,1],[1,0]])
    sigma_y = np.array([[0,-1j],[1j,0]])
    sigma_z = np.array([[1,0],[0,-1]])
    rho = (np.eye(2) + sigma_z) / 2 # |0><0|
    rho_rot = u @ rho @ u.conj().T
    x = np.real(np.trace(rho_rot @ sigma_x))
    y = np.real(np.trace(rho_rot @ sigma_y))
    z = np.real(np.trace(rho_rot @ sigma_z))
    v = np.array([x,y,z], dtype=float)
    nrm = np.linalg.norm(v)
    return v/nrm if nrm != 0 else v

def phi(u):
    """Mean-zero anisotropy function over SU(2) (demo)."""
    return np.real(np.trace(u)) - 0.5

# ---------------------------------------
# Многоточечный (GHZ-стиль) коррелятор
# ---------------------------------------
def oir_correlator(axes, eps=0.0, M=10000):
    """
    GHZ-style k-point correlator:
      E = < prod_j K(a_j,u) >, K(a,u)=2 (a·n(u))^2 - 1
    """
    acc = 0.0
    for _ in range(M):
        u = haar_sample_su2()
        n = rotate_z_by(u)
        val = 1.0
        for a in axes:
            c = float(np.dot(a, n))
            val *= (2.0*c*c - 1.0)
        w = 1.0 + (eps**2)*phi(u)
        acc += w * val
    return acc / M

# ---------------------------------------
# Двухточечный коррелятор для CHSH
# + режимы: "iso3d" (по умолчанию) и "equator"
# ---------------------------------------
def oir_pair_correlator(a, b, eps=0.0, M=10000, mode="iso3d"):
    """
    Two-point correlator: E(a,b) = < K(a,u) K(b,u) >.
      mode="iso3d": изотропное 3D усреднение (как у тебя сейчас)
      mode="equator": проектируем n в xy-плоскость (даёт cos(2Δθ) при eps=0)
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    acc = 0.0
    for _ in range(M):
        u = haar_sample_su2()
        n = rotate_z_by(u)

        if mode == "equator":
            n = n.copy()
            n[2] = 0.0
            nn = np.linalg.norm(n)
            if nn == 0:
                continue # крайне редкий случай; пропустим
            n /= nn

        Ka = 2.0*(np.dot(a, n)**2) - 1.0
        Kb = 2.0*(np.dot(b, n)**2) - 1.0
        w = 1.0 + (eps**2)*phi(u)
        acc += w * Ka * Kb
    return acc / M

# ---------------------------------------
# CHSH-комбинация из четырёх E
# ---------------------------------------
def chsh_value(axes, eps=0.0, M=10000, mode="iso3d"):
    """
    S = E(a,b) + E(a,b') + E(a',b) - E(a',b')
    axes = [a, a_prime, b, b_prime]
    """
    a, ap, b, bp = axes
    E = lambda x,y: oir_pair_correlator(x, y, eps=eps, M=M, mode=mode)
    return abs(E(a,b) + E(a,bp) + E(ap,b) - E(ap,bp))

__all__ = [
    "haar_sample_su2",
    "rotate_z_by",
    "phi",
    "oir_correlator",
    "oir_pair_correlator",
    "chsh_value",
]

